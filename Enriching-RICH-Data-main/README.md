# Projet Richelieu 
 Normalization and alignment of data extracted from the annuaires

## RICH.DATA

This project is built on the [Projet Richelieu](https://github.com/adescombes/Richelieu) that has OCRised and created a dataset of the entries of people obtained from the 19th-century city directories of Paris. The dataset contains information about people including their profession. The key contributions of the project are the normalization and alignment of the profession produced by the _Projet Richelieu_. The normalization of the profession is made by adding single words called tags that are used to compose the profession string. In short, the project added tags after cleaning the words to each profession that will enrich the data to be accessible through text-based search. 

This repository contains the algorithm and code for the normalization and alignment process.

## Background

One of the outcomes of the _Projet Richelieu_ is two datasets. The first is a dataset about the activities of people in Paris between the years 1839 and 1922. It contained the details such as name, profession, address (street name and number), the year of the entry, and details about the direction in which the entry was present. From the first dataset, a subset of lines was extracted that were present in the streets of the Richelieu district in Paris. Along with the details of the first dataset, the latitude and longitude for the address were also added.

## Summary

This project (that is contained in this repository) enriches the dataset created by the previous project. It normalized and aligns the professional information across the years making it possible to access and search the dataset. The enriched profession is represented by single words called tags. 

The document detaling the alogorithm and the results can be [seen here](./documents/Report/Enriching_RICH_data_INHA_Internship_Report.pdf).

### Data

For the data outcome of the previous project, see the `data/from_previous_project` folder.
- The file `people_of_paris_1839_1922.csv` contains the data extracted from directories for complete Paris.
- The file `people_of_richelieu_1839_1922.csv` contains the data extracted from `people_of_paris_1839_1922.csv` with the addresses belonging to the Richelieu district.

For the data outcome of the current project, see the `data/outcome_of_current_project` folder.
- The file `people_of_paris_with_profession_tags_1839_1922.csv` contains the data with an additional column of tags for complete Paris.
- The file `street_wise_people_of_richelieu_with_profession_tags_1839_1922.json` contains the data of people belonging to the Richelieu district grouped based on the street name and number.

The structure of the files is detailed in the respective folders.

### Process

The pipeline is detailed at [report](./documents/Report/Enriching_RICH_data_INHA_Internship_Report.pdf) and coded through the Jupyter notebooks. Five notebooks are used for this project. The notebooks must be viewed/processed in the same order as mentioned here.
- `add_correct_page_numbers.ipynb`: The dataset obtained from the previous project contained the page number that did not correspond to the pages numbers of the scanned documents on Gallica. This notebook adds the page number to all the entries that help in accessing the scanned directories.
- `creating_french_dictionary_words_set.ipynb`: The notebook is used to read the language dictionaries provided by ortolang and Prolex-Unitex and create a JSON file of correctly spelled words with the root word (lemma) as the key and the list of derived words (flexions) as the values.
- `cleaning_special_characters.ipynb`: During the OCR process, some symbols and alphabets were misinterpreted as special characters. This notebook is used to rectify and remove the non-alphanumeric characters present in the professions.
- `cleaning_and_creating_tags.ipynb`: The professions are broken down and added as tags to the data point. This is the most important notebook that contains the steps and commentary on how the profession strings are converted into tags.
- `plots_for_results_generator.ipynb`: The notebook is used to produce the plots required to analyze the result.

## Repository organization

    ├── README.md <- The top-level README for using this project.
    │
    ├── data <- The canonical data sets are used in the notebooks are placed in the subdirectories.
        ├──from_previous_project <- The folder contains the data outcome of the previous project.
        ├──outcome_of_current_project <- The folder contains the outcome of the current project
        ├──external_data <- The folder contains the additional datasets used in the project. For this project, the external datasets used were the language dictionaries and street names.
        ├──intermediate_steps <- The folder will contain any data produced during the process of the project.
    │
    ├── notebooks <- Jupyter notebooks used in the project.
    |
    └── documents: The directory contains the report describing the algorithm and the results.