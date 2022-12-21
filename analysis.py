import pandas as pd
import regex as re
from collections import Counter
from matplotlib import pyplot as plt
import contextily as cx
from PIL import Image


def get_prof_list(entry):
    '''
    converts a profession "tags" entry from string to list

    Parameters
    ---------------
    :entry: string of profession tags of form "['profession1', 'profession2']"

    Returns
    ---------------
    list of strings, containing one string per tag -> ["profession1", "profession2"]
    '''
    entry = str(entry)
    return re.findall("'([a-zA-ZÀ-ÿ]+)'", entry)


def get_prof_str(entry):
    '''
    converts list of profession tags to a string, professions seperated by comma
    e.g. ["profession1", "profession2"] to "profession1, profession2"

    Parameters
    ----------------
    :entry: list of strings, containing one string per tag

    Returns
    -----------------
    string of the form "profession1, profession2"
    '''
    # first get list of tags, then convert them to a string
    return ", ".join(get_prof_list(entry))


def plot_ratio_over_time(df, top_names, col_name="tags", title=""):
    '''
    Computes the ratio top_names/all for each year in the dataframe and each name in top_names
    and plots them.

    Parameters
    ----------------
    :df: dataframe with relevant data
    :top_names: list of the jobs/streets whose frequency should be plotted over the years
    :col_name: name of the column the strings in top_names are contained in
    :title: title of the plot

    Returns
    ----------------
    plot of the frequency of the jobs/streets in top_names over the years
    '''
    #get list of all years in dataframe
    all_years = sorted(df["annee"].unique())
    #instantiate empty dataframe
    df_top_jobs = pd.DataFrame(columns=top_names, index=all_years)
    
    #get the job/street ratio for every year seperately
    for year in all_years:
        year_data = df[df["annee"]==year]
        len_year = len(year_data)
        # get ratio for all jobs
        for top_job in top_names:
            job_ratio = len(year_data[year_data[col_name]==top_job])/len_year
            df_top_jobs.loc[year, top_job] = job_ratio   

    #plot the data
    ax = df_top_jobs.plot.line(figsize=(10,6), title=title)
    ax.legend(bbox_to_anchor=(1.0, 1.0))
    return ax.plot()  

def get_jobs_overtime(df, streetname, int_top_per_decade=10):
    selected = df[df["streetname"]==streetname]
    selected_decades = sorted(selected["annee_bin"].unique())

    selected_jobs = []
    for decade in selected_decades:
        selected_dec_data = selected[selected["annee_bin"]==decade]
        top_dec_jobs = Counter(selected_dec_data["tags"]).most_common(int_top_per_decade)
        top_dec_jobs = [name for name, count in top_dec_jobs]
        selected_jobs += top_dec_jobs
    # delete duplicates
    return list(set(selected_jobs))

def jobs_not_before_after_specific_year(df_in, year, job_col="tags"):
    '''
    Splits dataset in before and after given year, then checks for jobs which are only in one of the
    two sets.
    '''
    df = df_in.groupby(["annee", job_col]).count().reset_index()
    df["afterYearX"] = df.apply(lambda x: x.annee>year, axis=1)
    grouped_df = df.groupby(["afterYearX", job_col]).count().reset_index()    
    
    after = grouped_df[grouped_df["afterYearX"]]
    before = grouped_df[~grouped_df["afterYearX"]]

    jobs_after = set(after[job_col])
    jobs_before = set(before[job_col])

    not_before_yearX = jobs_after.difference(jobs_before)
    not_after_yearX = jobs_before.difference(jobs_after)

    return not_after_yearX, not_before_yearX

def sort_by_number_of_words(set_data):
    '''
    Takes profession strings, checks how many words are contained in them and returns them sorted by
    the number of words (one, two or more words)
    '''
    list_data = list(set_data)
    one_word = []
    two_words = []
    more_words = []
    for entry in list_data:
        entry_list = entry.split(", ")
        if len(entry_list) == 1:
            one_word += entry_list
        elif len(entry_list) == 2:
            two_words.append(", ".join(entry_list))
        else:
            more_words.append(", ".join(entry_list))
    
    return one_word, two_words, more_words

def plot_profession_selection_on_map(df, professions, year, prof_name="name", geo_col="centroid", 
                                    save_fig=False):
    if not geo_col=="geometry":
        df = df.rename(columns={"geometry":"polygons", geo_col:"geometry"})
    fig, ax = plt.subplots(1,1,figsize=(10, 8))
    df_year = df[df["annee"]==year]
    df_year_prof = df_year[df_year["tags"].isin(professions)]
    title = f"Professions in Year {year}"
    _ = df_year_prof.plot(column="tags", legend=True, ax=ax)
    _ = cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
    _ = ax.set_title(title)
    if save_fig:
        plt.savefig(f"figures/{prof_name}{year}.jpg")
    else:
        plt.show()
    plt.close()

def make_gif(years, prof_name="name", gif_name="my_awesome"):
    frames = [Image.open(f"figures/{prof_name}{year}.jpg") for year in years]
    frame_one = frames[0]
    frame_one.save(f"figures/{gif_name}.gif", format="GIF", append_images=frames,
               save_all=True, duration=200, loop=0)