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
* strict_addressing.csv
* vasserot.zip
* voie.zip
* Morphalou3_formatCSV_toutEnUn.zip and Prolex-Unitex_1_2.zip

Intermediary results:
* bottins_prep.pkl
* bottins_tagged_prep.pkl
* FinalDuplicate.pkl
* FinalUnique.pkl
* fuzzy_dictwith80.pkl
* fuzzy_dictwith85.pkl
* not_unique_short_streets.pkl
* unique_short_streets.pkl

Aligned data:
* unique_aligned_tagged.pkl
* unique_aligned.pkl

# Repository organization

    ├── README.md <- The top-level README for this project.
    │
    ├── Enriching-RICH-Data-main <- [Code by Ravinithesh Annapureddy](https://github.com/ravinitheshreddy/Enriching-RICH-Data) to clean professions and create profession tags in Bottin Dataset, slightly modified to fit it to our data
    │
    ├── data <- This subfolder contains all the data needed for this project as well as intermediary results. Some data files were too large and can thus be found on our shared [Google Drive](https://drive.google.com/drive/u/1/folders/1InpxQW7CkIvwWeuQeuzn9GNWZAxDD64g)
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

