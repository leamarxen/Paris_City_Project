# Repopulating Paris

# Summary

This project works with around 4.4 million datapoints which have been extracted from address books in Paris (Bottin Data). The address books date from the period 1839-1922 and contain the name, profession and place of residence of Parisian citizens. In a first step, we align this data with geodata of Paris’s city network, in order to be able to conduct a geospatial analysis on the resulting data in a second step. 

More information can be found on the wiki page: [Paris: address book of the past](http://fdh.epfl.ch/index.php/Paris:_address_book_of_the_past)

# Notebooks

There are several jupyter notebooks which were used for the alignment and analysis of the data. They should be executed in the order they are presented hereunder. For the sake of clarity and reusability, we collected the function of each notebook in seperate python files. The files used for a notebook will be given in brackets.

* Preprocessing.ipnyb (preprocessing.py): Preprocessing of the street names in the Bottin Data, including substitution of abbreviations.
* street_processing.ipnyb (preprocessing.py, paris_methods.py): Aligning the two street network datasets "Open Data" (2022) and "Vasserot" (1836), solving conflicts for non-unique entries
* Alignment.ipnyb (preprocessing.py, alignment.py): Aligning bottin streets with the streets of the street data computed in street_processing.ipnyb
* analysis.ipynb (): Analysis on the aligned data

# Data
The following data has been used:
* strict_addressing.csv (to find in [Google Drive](https://drive.google.com/drive/u/1/folders/1InpxQW7CkIvwWeuQeuzn9GNWZAxDD64g)): OCRized Bottin Data, more information at the [wiki](http://fdh.epfl.ch/index.php/Paris:_address_book_of_the_past#Bottin_Dataset)
* paris_jobs_with_tags_richelieu_project.csv (to find in [Google Drive](https://drive.google.com/drive/u/1/folders/1InpxQW7CkIvwWeuQeuzn9GNWZAxDD64g)): Bottin Data, but with additional column "tags" containing tags for the professions, result of pipeline used from [Enriching-RICH-Data](https://github.com/ravinitheshreddy/Enriching-RICH-Data) by Ravinithesh Annapureddy  
* vasserot.zip: Street network of Paris in 1836, data from [Vasserot](https://alpage.huma-num.fr/donnees-vasserot-version-1-2010-a-l-bethe/)
* voie.zip: Street network of Paris today, data from [Open Paris](https://opendata.paris.fr/explore/dataset/voie/information/)
* Morphalou3_formatCSV_toutEnUn.zip and Prolex-Unitex_1_2.zip (to find in data folder of "Enriching-RICH-Data-main"): used during the Pipeline for the Enriching-RICH-Data to get the file "paris_jobs_with_tags_richelieu_project.csv"

Intermediary results:
* bottins_prep.pkl (to find in [Google Drive](https://drive.google.com/drive/u/1/folders/1InpxQW7CkIvwWeuQeuzn9GNWZAxDD64g)): pickled Bottin Data with additional column "rue_processed", containing the preprocessed streets after having executed Preprocessing.ipnyb
* bottins_tagged_prep.pkl (to find in [Google Drive](https://drive.google.com/drive/u/1/folders/1InpxQW7CkIvwWeuQeuzn9GNWZAxDD64g)): same as bottins_prep.pkl, but with additional column "tags" providing profession tags from the Enriching-RICH-Data Pipeline; is obtained when setting USE_TAGGED_DATASET = True in the file Preprocessing.ipnyb
* FinalDuplicate.pkl: pickled street dataframe from joined vasserot and openparis street data,  where multiple streets had same street name and did not lie close to each other -> after running street_processing.ipnyb
* FinalUnique.pkl: same as FinalDuplicate.pkl, but for unique (full) street names -> after running street_processing.ipnyb
* not_unique_short_streets.pkl: pickled street dataframe grouped on the short street names, where short street name was not unique and streets with same short street name did not overlap on the map -> after running street_processing.ipnyb
* unique_short_streets.pkl: same as not_unique_short_streets.pkl, but for streets with unique short street name and those where streets with same short street names overlapped on the map -> after running street_processing.ipnyb
* fuzzy_dictwith80.pkl: Dictionary containing streets from the Bottin dataset as keys and a corresponding street from street data as values, provided their similarity is greater than 80 -> after running Alignment.ipynb
* fuzzy_dictwith85.pkl: same as fuzzy_dictwith80.pkl, but with threshold 85 -> after running Alignment.ipynb

Aligned data:
* unique_aligned_tagged.pkl (to find in [Google Drive](https://drive.google.com/drive/u/1/folders/1InpxQW7CkIvwWeuQeuzn9GNWZAxDD64g)): Tagged Bottin data (bottins_tagged_prep.pkl) aligned on geolocated streets (FinalUnique.pkl and unique_short_streets.pkl) -> after running Alignment.ipynb with USE_TAGGED_DATASET=True
* unique_aligned.pkl (to find in [Google Drive](https://drive.google.com/drive/u/1/folders/1InpxQW7CkIvwWeuQeuzn9GNWZAxDD64g)): same as unique_aligned_tagged.pkl, but without column containing tagged professions -> after running Alignment.ipynb with USE_TAGGED_DATASET=False

# Repository organization

    ├── README.md <- The top-level README for this project.
    │
    ├── Enriching-RICH-Data-main <- Code by Ravinithesh Annapureddy 
        (https://github.com/ravinitheshreddy/Enriching-RICH-Data) 
        to clean professions and create profession tags in Bottin Dataset, 
        slightly modified to fit it to our data
    │
    ├── data <- This subfolder contains all the data needed for this project 
                as well as intermediary results. Some data files were too large 
                and can thus be found on our shared Google Drive (see section "Data").
    |
    └── Jupyter Notebooks and Python files (see section "Notebooks" for closer description)
        - Alignment.ipynb
        - alignment.py
        - analysis.ipynb
        - paris_methods.py
        - Preprocessing.ipynb
        - preprocessing.py
        - street_processing.ipynb

# Team

Ben: ben.kriesel@epfl.ch
Lea: lea.marxen@epfl.ch

