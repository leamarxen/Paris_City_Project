import pandas as pd
from shapely.ops import linemerge

def add_overlap_indices(Dataframe, current_row, comparing_row):
    # Checks if two streets overlap, if they do a "match identifier" is added to the street 
    intersect_check = current_row.buffer.intersects(Dataframe["buffer"].iloc[comparing_row])
    if intersect_check:
        current_row.matching.append(Dataframe.iloc[comparing_row]["IDENTIFI"])
        
def add_overlap_final(Dataframe, current_row, comparing_row):
    # Checks if two streets overlap, if they do a "match identifier" is added to the street 
    intersect_check = current_row.buffer.intersects(Dataframe["buffer"].iloc[comparing_row])
    if intersect_check:
        current_row.matching.append(Dataframe.iloc[comparing_row]["rowid"])

def same_identifier(row, identifier):
    # Checks if two streets have the same "match identifier"
    row_matches_identifier = identifier in row["matching"]
    return row_matches_identifier

def merge_streets(Dataframe):
    # Creates one representative containing combined all matching streets and all "match identifiers"
    new_geometry = Dataframe.iloc[0].geometry
    new_identifiers = []
    new_year = []
    Dataframe.apply(lambda row: linemerge([new_geometry, row.geometry]),axis=1)
    Dataframe.apply(lambda row: new_identifiers.extend(row.matching), axis=1)
    Dataframe.apply(lambda row: new_year.extend(row.year), axis=1)

    # Define representative
    representative = Dataframe.iloc[0]
    representative.geometry = new_geometry
    representative.matching = new_identifiers
    representative.year = new_year
    return(representative)

def merge_streets_final(Dataframe):
    # Creates one representative containing combined all matching streets and all "match identifiers"
    new_identifiers = []
    new_year = []
    Dataframe.apply(lambda row: new_identifiers.extend(row.matching), axis=1)
    Dataframe.apply(lambda row: new_year.extend(row.year), axis=1)

    # Define representative
    representative = Dataframe.iloc[0]
    representative.geometry = Dataframe.iloc[0,14]
    representative.matching = new_identifiers
    representative.year = new_year
    return(representative)

def duplicate_processing(Dataframe, streetcolumn):

    # Initialisation
    streetnames = Dataframe[streetcolumn].unique()
    Dataframe["matching"] = pd.np.empty((len(Dataframe), 0)).tolist()

    # For each street name
    for streetname in streetnames:
        ## Filter DF for street name and create new temporary Dataframe
        filter = Dataframe[streetcolumn] == streetname
        MatchingStreetname = Dataframe[filter]
        # remove values from main dataframe
        Dataframe = Dataframe[~filter]
        
        # Add indices of streets that overlap
        for comparing_row in range(0,len(MatchingStreetname)):
            MatchingStreetname.apply(lambda current_row: add_overlap_indices(MatchingStreetname, current_row, comparing_row), axis=1)

        ## Merge all streets with overlapping segments
        for identifier in MatchingStreetname.IDENTIFI:
            # Create temporary dataframe with all streets that intersect that index
            MatchingStreetname["filter"] = MatchingStreetname.apply(lambda current_row: same_identifier(current_row, identifier), axis=1)
            MatchingIndex = MatchingStreetname[MatchingStreetname["filter"]]
            # Only work with dataframes having more than one street
            if len(MatchingIndex) == 1:
                pass
            else:
                # remove all streets with index from MatchingStreet DF
                MatchingStreetname = MatchingStreetname[~MatchingStreetname["filter"]]

                # Create one representative containing all values of streets with same index
                representative = merge_streets(MatchingIndex)

                # Add one representative back to MatchingStreet DF
                representative = pd.Series.to_frame(representative).T
                MatchingStreetname = pd.concat([MatchingStreetname,representative])
        # Add all representatives back to Main Dataframe

        Dataframe = pd.concat([Dataframe, MatchingStreetname])

    return Dataframe


def duplicate_final(Dataframe, streetcolumn):

    # Initialisation
    streetnames = Dataframe[streetcolumn].unique()
    Dataframe["matching"] = pd.np.empty((len(Dataframe), 0)).tolist()

    # For each street name
    for streetname in streetnames:
        ## Filter DF for street name and create new temporary Dataframe
        filter = Dataframe[streetcolumn] == streetname
        MatchingStreetname = Dataframe[filter]
        # remove values from main dataframe
        Dataframe = Dataframe[~filter]
        
        # Add indices of streets that overlap
        for comparing_row in range(0,len(MatchingStreetname)):
            MatchingStreetname.apply(lambda current_row: add_overlap_final(MatchingStreetname, current_row, comparing_row), axis=1)

        ## Merge all streets with overlapping segments
        for identifier in MatchingStreetname.rowid:
            # Create temporary dataframe with all streets that intersect that index
            MatchingStreetname["filter"] = MatchingStreetname.apply(lambda current_row: same_identifier(current_row, identifier), axis=1)
            MatchingIndex = MatchingStreetname[MatchingStreetname["filter"]]
            # Only work with dataframes having more than one street
            if len(MatchingIndex) == 1:
                pass
            else:
                # remove all streets with index from MatchingStreet DF
                MatchingStreetname = MatchingStreetname[~MatchingStreetname["filter"]]

                # Create one representative containing all values of streets with same index
                representative = merge_streets_final(MatchingIndex)

                # Add one representative back to MatchingStreet DF
                representative = pd.Series.to_frame(representative).T
                MatchingStreetname = pd.concat([MatchingStreetname,representative])
        # Add all representatives back to Main Dataframe

        Dataframe = pd.concat([Dataframe, MatchingStreetname])

    return Dataframe