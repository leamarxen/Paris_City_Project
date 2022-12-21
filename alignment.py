import pandas as pd
from fuzzywuzzy import process, fuzz
import multiprocessing
from multiprocessing.dummy import Pool
from functools import partial


def align_on_column(df_not_aligned, df_streets, df_aligned=pd.DataFrame(), 
                    mergeOnLeft="street", mergeOnRight="street", align_method=""):
    '''
    Takes two dataframes and makes a left join on the relevant columns.

    Parameters
    -------------------
    :df_not_aligned: pandas dataframe with entries that have to be aligned
    :df_streets: pandas dataframe with the geolocated street data
    :df_aligned: if existing, pandas dataframe with already aligned data that the newly aligned
                data should be appended to
    :mergeOnLeft: name of the column of the non-aligned data the join should be executed on
    :mergeOnRight: name of the column of the street data the join should be executed on
    :align_method: name of the alignment method used (will be saved in column "align_method")

    Returns
    --------------------
    :aligned: pandas dataframe with already + newly aligned data
    :not_aligned: pandas dataframe with data which could not be aligned
    '''
    # make copies to avoid alteration of source dataframes
    not_aligned = df_not_aligned.copy()
    streets = df_streets.copy()
    if not df_aligned.empty:
        aligned = df_aligned.copy()
    else:
        aligned = df_aligned
        
    # the left join
    merged = not_aligned.merge(streets, how="left", left_on=mergeOnLeft, right_on=mergeOnRight, suffixes=(False, False))
    # append newly aligned cases to aligned dataframe
    newly_aligned = merged[merged[mergeOnRight].notna()]
    # add column to know what alignment was on
    newly_aligned["align_method"] = align_method
    aligned = pd.concat([aligned, newly_aligned])
        
    # update not aligned dataframe
    not_aligned = merged[merged[mergeOnRight].isna()]
    not_aligned = not_aligned.drop(list(streets.columns), axis=1)

    # print statistics
    print(f"Joining on {mergeOnLeft} and {mergeOnRight}, method:{align_method}\n" +\
        f"#total aligned: {len(aligned)}, newly aligned: {len(newly_aligned)}, not aligned: {len(not_aligned)}")
    
    return aligned, not_aligned


#methods for fuzzy matching

#ravis code (see Enriching rich data project)
def simple_processor(token: str) -> str:
    """A string processor to return the same string as input.
        This dummy processor is used to avoid the default processor of the Rapidfuzz module to calculate string similarity.

    Parameters
    ----------
    token : str
        The input string to process.

    
    Returns
    -------
    str
        The output string same as the input string.
    """
    return token


def get_closest_street_w_cutoff(additional_args, bottin_data):
    '''
    takes a street from the bottin data and the list of clean streets and returns a tuple with the
    street and its most similar counterpart 
    (for similarity use fuzz.ratio which is based on Levenshtein distance)

    Parameters
    -------------------------
    :bottin_data: one string of a street from the bottin data
    :additional_args:
        [0]: list of clean streets (strings) where a similar street should be chosen from
        [1]: integer between 0 and 100 defining the threshold which similarity has to surpass 
            (otherwise extractOne returns None)

    Returns
    -------------------------
    if above the defined threshold, return tuple with bottin street and most similar matching street
    from clean streetlist
    '''
    streets, score_cutoff = additional_args
    best_one = process.extractOne(bottin_data, streets, processor=simple_processor, scorer=fuzz.ratio,
                                score_cutoff=score_cutoff)
    # if a matching street has been found
    if best_one:
        # best_one[0] because it returns the similarity value on second position and we only want street name
        return (bottin_data, best_one[0])


def get_fuzzy_dict(streets, bottin_streets, score_cutoff):
    '''
    takes the list of bottin streets and gets the most similar street from list of streets,
    pair is saved in a dictionary if the similarity surpasses the specified threshold

    Parameters
    -------------
    :streets: list of streets (strings) with the clean street data
    :bottin_streets: list of streets which have to be aligned
    :score_cutoff: threshold value for similarity (int between 0 and 100)

    Returns
    ---------------
    :fuzzy_dict: dictionary of the form {bottin street: clean street}
    '''
    # use multiprocessing to speed up computation
    pool = Pool(multiprocessing.cpu_count())

    # compute the pairs of similar streets -> results of form [(bottin street, clean street)]
    results = pool.map(partial(get_closest_street_w_cutoff, (streets, score_cutoff)), bottin_streets)

    pool.close()
    pool.join()

    # remove None values from the results
    results_set = set(results)
    results_set.remove(None)

    # convert to dictionary
    fuzzy_dict = dict(results_set)

    return fuzzy_dict


def print_sample(df, align_methods, sample_size, random_state=42):
    '''
    This function takes a certain amount of samples from the given (aligned) data with specified alignment
    methods and prints the street (Bottin Data), the matched street and the specific alignment method for 
    each sample.

    Parameters
    ----------------
    :df: dataframe with aligned data
    :align_methods: all alignment methods that samples should be chosen from
    :sample_size: the number of samples to print
    :random_state: random state to make result reproducible
    '''
    df = df[df["align_method"].isin(align_methods)].sample(n=sample_size, random_state=random_state)
    data = zip(df["rue"], df["streetname"], df["align_method"])
    for i, entry in enumerate(data):
        print(f"{i+1}. bottin: {entry[0]}  -  matched: {entry[1]}   ({entry[2]})") 