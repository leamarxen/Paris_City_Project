import pandas as pd
import re
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
    ax = df_top_jobs.plot.line(figsize=(10,6), title=title, colormap="hsv")
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

def plot_profession_selection_on_map(df, professions, year, prof_name="name", geo_col="geometry", 
                                    save_fig=False, comparable=True, color=None):
    '''
    plot the distributions of professions on a map for a given year

    Parameters
    --------------
    :df: dataframe with one datapoint per row
    :professions: list of profession strings that should be displayed on the map
    :year: year which should be looked at
    :prof_name: name if figure should be saved
    :geo_col: the column with the geodata
    :save_fig: if True, save the plot; if False, display it
    :comparable: if True, give predefined limits for x and y axis
    :color: specify color if all data should be plotted in the same color
    '''
    #change column for geodata if necessary
    if not geo_col=="geometry":
        df = df.rename(columns={"geometry":"polygons", geo_col:"geometry"})

    df_year = df[df["annee"]==year]
    df_year_prof = df_year[df_year["tags"].isin(professions)]

    #begin plotting
    fig, ax = plt.subplots(1,1,figsize=(10, 8))
    title = f"Professions in Year {year}"
    # same color for all professions
    if color:
        _ = df_year_prof.plot(column="tags", legend=True, ax=ax, alpha=0.5, color=color)
    # different color for each profession
    else:
        _ = df_year_prof.plot(column="tags", legend=True, ax=ax, alpha=0.5, cmap="Spectral")
    if comparable:
        plt.xlim(250000, 270000)
        plt.ylim(6244000, 6258000)
    _ = cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
    _ = ax.set_title(title)

    # save or display figure
    if save_fig:
        plt.savefig(f"figures/{prof_name}{year}.jpg")
    else:
        plt.show()
    plt.close()


def make_gif(years, prof_name="name"):
    '''
    makes gif out of already saved images in subfolder "figures"

    Parameters
    --------------
    :years: list of years which should be used
    :prof_name: part of the name of the path the data is stored at (-> {prof_name}{year}.jpg)
    '''
    # open each image, store them in a list and convert to a gif
    frames = [Image.open(f"figures/{prof_name}{year}.jpg") for year in years]
    frame_one = frames[0]
    frame_one.save(f"figures/{prof_name}.gif", format="GIF", append_images=frames,
               save_all=True, duration=600, loop=0)


def gif_for_professions(rich_data, professions, prof_name, geo_col="geometry", color=None):
    '''
    takes a dataframe and a list of professions; first saves data plot for each year in the data
    which shows the distribution of the professions over Paris, then makes a gif out of it
    (all stored in subfolder "figures")

    Parameters:
    :rich_data: dataframe with datapoints
    :professions: list of profession strings that should be displayed on the map
    :prof_name: part of the name of the path the data is stored at (-> {prof_name}{year}.jpg)
    :geo_col: the column with the geodata
    :color: specify color if all data should be plotted in the same color
    '''
    subset = rich_data[rich_data["tags"].isin(professions)]
    years = sorted(subset["annee"].unique())
    # save image with profession distribution for each year
    for year in years:
        plot_profession_selection_on_map(rich_data, professions=professions, year=year, 
                geo_col=geo_col, prof_name=prof_name, save_fig=True, color=color)
    # make gif out of saved images and save it in "figures" folder
    make_gif(years = years, prof_name=prof_name)