# Data outcome of Projet Richelieu

The folder `from_previous_project` contains the data produced by the previous project. It contains three files.

## Files description

### people_of_paris_1839_1922

This is a CSV file that contains all extracted addresses from the OCRization of the directories. The CSV file contains 8 columns and their description is 

1. unnamed: The ark identifier of the document on Gallica.
2. `page`: The page in which the entry is present in the document.
3. `row`: The row of the entry on the page.
4. `Nom`: The name of the person.
5. `Métier`: The profession of the person (extracted through OCR).
6. `Rue`: The name of the street in the address of the person.
7. `Numéro`: The number in the street in the address of the person.
8. `annee`: The year in which the entry is published.

### people_of_richelieu_1839_1922

This is a CSV file that contains data extracted from the `people_of_paris_1839_1922.csv` with the addresses belonging to the Richelieu district. In addition to the columns present in the `people_of_paris_1839_1922.csv`, this file has the clean Rue and Numéro columns along with the geographical coordinates of the address. The CSV file contains 11 columns and their description is 

1. unnamed: The index of the row (does not provide any information)
2. `document`: The ark identifier of the document on Gallica.
3. `annee`: The year in which the entry is published.
4. `page`: The page in which the entry is present in the document.
5. `row`: The row of the entry on the page.
6. `Nom`: The name of the person.
7. `Métier`: The profession of the person (extracted through OCR).
8. `Rue`: The name of the street in the address of the person.
9. `Numéro`: The number in the street in the address of the person.
10. `X`: The latitude of the address (Rue + Numéro)
11. `Y`: The longitude of the address (Rue + Numéro)


### repertoires

This is an XLSX file containing the information about the scanned data on the Gallica. It has 3 sheets. The first sheet `répertoires triés` has the link to the scanned document, the start page, and the end page per year. The `listes` sheet contains the list of directories available on the Gallica. Lastly, `Paris Adresses` contains the links to scanned data on Gallica that provides data about the addresses of Paris.

- The current phase of the project uses `répertoires triés` to obtain the correct page number for each entry in the `people_of_paris_1839_1922.csv` dataset.