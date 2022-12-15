# Notebooks

The folder `notebooks` contains the notebooks that are used in the pipeline of tags generation for the current project. It contains five files.

## Notebook description

### add_correct_page_numbers

The data outcome of the previous project contains the information about the scanned documents. For each entry, it has the information about the id of the document, the page number in the document, and the row on the page. However, the page number is not aligned to access the document in Gallica. In this notebook, the page number is adjusted and added to a new column titled `gallica_page`.

- The `data/from_previous_project/people_of_paris_1839_1922.csv` file is used as the input to the notebook and the output data with page numbers on Gallica is stored in `data/intermediate_steps/all_paris_jobs_with_gallica_pageno.csv`.

### creating_french_dictionary_words_set

To determine which set of words in the profession string are already having correct spelling and does not require any cleaning a set of correct words is used. Three external data sources are used to create this set of words. The set of words is created in the `cleaning_and_creating_tags.ipynb` notebook. However, in the `creating_french_dictionary_words_set.ipynb` notebook, two of the three external sources are preprocessed and stored as a JSON as pre-processing these files is time-consuming. The notebook reads the two sources of data and stores the words in a JSON file where the keys are the root forms of the words (lemma) and the values are a list of derived words from each lemma (flexions).

- The `data/external_data/Morphalou3_formatCSV_toutEnUn/Morphalou3_CSV.csv` and `data/external_data/Prolex-Unitex_1_2/Prolex-Unitex_1_2.dic` files are used as the input to the notebook and the output data with root forms and derived words are stored in `data/intermediate_steps/words_from_french_language_dictionaries.json`.

### cleaning_special_characters

During the OCRization of the directories, some of the characters and symbols are misinterpreted as special characters. For example, the symbols used to represent medals in the directories were interpreted as _#_ or _*_ or _¥_, in another case the alphabets such as _l_ were interpreted as _!_ or similar misinterpretations. This notebook deals with these cases. There are broadly two categories of cleaning. First, one type of a generic step is that the special characters at the start, in the end, and surrounded by space are removed. The second type of generic step is to replace the same mistake across the dataset. For example, the _d'_ in some cases appears as _ď_ or _f_ appears as _ſ_. The second category of cleaning is for words containing the special characters (not the complete strings). In such cases, the entries were compared manually with the scanned document and the changes were made. 

- The `data/intermediate_steps/all_paris_jobs_with_gallica_pageno.csv` file is used as the input to the notebook and the output data with special characters cleaned professions is stored in `data/intermediate_steps/all_paris_jobs_splchar_cleaned.csv`.

### cleaning_and_creating_tags

This notebook contains key steps of the pipeline to generate tags.

The algorithm is explained in detail at [ALGO DOCUMENT](ADD THE URL TO THE DOCUMENT). In this notebook, the profession for each entry of the dataset is cleaned by providing tags that represent the profession and filling the abbreviations with full forms. This notebook performs the following keys tasks

1. Combining the words in the profession column that are mistakenly broken into multiple words.
2. Removing the connecting and stop words in the profession strings and breaking words at space, apostrophe, and dot to create a list of words for each profession string.
3. The low frequency and not correctly spelled tokens are tried to merge with those in the list of correct words based on the token co-occurrence, frequency, and similarity.
4. The tokens containing a dot are filled with full forms based on co-occurrence, frequency, and similarity.
5. Save the tokens as tags for each entry.

- The `data/intermediate_steps/all_paris_jobs_splchar_cleaned.csv` file is used as the input to the notebook and the output data with tags is stored in `data/outcome_of_current_project/paris_jobs_with_tags_richelieu_project.csv` that has the tags for all address in Paris. In addition `data/from_previous_project/people_of_richelieu_1839_1922.csv` file that contains the geographic coordinates of the address of the Richelieu district is used to create an address wise people list per year and is stored in `data/outcome_of_current_project/street_wise_richelieu_people.json`.

- The notebook also uses `data/intermediate_steps/words_from_french_language_dictionaries.json` and `data/external_data/Street-names/denominations-emprises-voies-actuelles.csv` to create a list of correctly spelled words.