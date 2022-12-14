import pandas as pd
from shapely.ops import linemerge
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from pyproj import Proj, transform
import geopandas as gpd
import matplotlib.pyplot as plt


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
    representative.geometry = Dataframe.iloc[0,:].geometry
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



def assign_gridnumber(Dataframe, gridX, gridY):
    # Assigns Streets to a given grid

    # Translate in right coordinate system
    #gridX = translate_geopoints(gridX)
    #gridY = translate_geopoints(gridY)

    ## Check Y coordinates
    Dataframe["gridY"] = Dataframe.apply(lambda row: compare_point_y(row,gridY), axis=1)
    ## Check X coordinates
    Dataframe["gridX"] = Dataframe.apply(lambda row: compare_point_x(row,gridX), axis=1)
    Dataframe["grid"] = (Dataframe["gridY"]-1) * (len(gridX)-1) + Dataframe["gridX"]
    return 0

def compare_point_x(row, gridX):
    point = float(row["centroid"].x)
    for index in range(1,len(gridX)):
        previous = float(gridX[index-1][1])
        current =  float(gridX[index][1])
        if point > previous and point <= current:
            return(int(index))
            

def compare_point_y(row, gridY):
    point = float(row["centroid"].y)
    for index in range(1,len(gridY)):
        previous = float(gridY[index-1][0])
        current =  float(gridY[index][0])
        if point > previous and point <= current:
            return(int(index))


def translate_geopoints(geopoints):
    inProj = Proj('epsg:4326')
    outProj = Proj('epsg:3857')
    transformed = []
    for index,value in enumerate(geopoints):
        transformed.append(transform(inProj,outProj,value[0],value[1]))
    return transformed


def check_overlap(buffer_list):
    '''
    Checks if all streets in a buffer_list overlap. If they are all connected, return True, else return False.

    Parameters
    ---------------
    :buffer_list: list of geometry objects (in our case: list with buffered streets)

    Returns
    ---------------
    True: all streets/objects are connected (they overlap)
    False: there is at least one pair of streets which are not connected 
                                    (also not through other street(s) in buffer_list)
    '''
    len_buffer = len(buffer_list)
    # instantiate a numpy matrix which will store in entry (i,j) if street i and j overlap
    intersects = np.zeros((len_buffer, len_buffer))

    # go through each pair of streets and check if they overlap
    for i in range(len_buffer):
        for j in range(len_buffer):
            # if street i and j overlap, write 1, otherwise 0
            intersects[i,j] = int(buffer_list[i].intersects(buffer_list[j]))
    
    # treat intersects matrix as adjacency matrix of a graph
    # if the graph is connected (n_components=1), all streets overlap
    n_components = connected_components(csgraph=csr_matrix(intersects), directed=False, return_labels=False)
    if n_components == 1:
        return True
    else:
        return False


def create_grid(y_steps, x_steps, Dataframe):
   # Creates a evenly spaced grid with the given parameters
 
    bounds = Dataframe["centroid"].bounds

    min_y = np.min(bounds.loc[:,"miny"]) - 0.01
    max_y = np.max(bounds.loc[:,"maxy"])

    min_x = np.min(bounds.loc[:,"minx"]) - 0.01
    max_x = np.max(bounds.loc[:,"maxx"]) 

    stepsizeY = (max_y - min_y)/y_steps + 0.01
    gridY = [[min_y + stepsizeY * x, 0] for x in range(0,y_steps+1)]

    stepsizeX = (max_x - min_x)/x_steps + 0.01
    gridX = [[0, min_x + stepsizeX * x] for x in range(0,x_steps+1)]
    
    return gridX, gridY


def get_change_over_years(df, yearcolumn="annee_bin"):
# function that creates dataframe with all jobs for a given bin and assigns jobs to that bin
    pivot = pd.pivot_table(df, values= "rue", index= "tags", columns = yearcolumn, aggfunc="count")
    pivot = pivot.fillna(0)
    pivot = pivot.iloc[1:,1:]
    pivot_rel = pivot.apply(lambda col: col/sum(col))
    change_year = []
    for year in range(1, len(pivot_rel.columns)):
        dif = sum(abs(pivot_rel.iloc[:,year] - pivot_rel.iloc[:,year-1]))/2
        change_year.append(dif)
    return(change_year, pivot.columns[1:])