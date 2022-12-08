# Paris City project
FDH Paris City Project

# Ziele:
- Timeline/Change Berufe & Stassen
- Raster, wie arbeiten mit 
    - Centroids / Adressen?
- Strassen
    - Visualisierung
    
# Fundament
- 1836 Datensatz:
    -  dup. strassen gemerged und 1 shapefile
- Bottin Daten:
    - Preprocessing voies 
        - shortstreet alignment
        - fuzzy matching
        (Describe quality)
    - Berufe bereinigt
    - Funktion, d. eine Strasse einem Bottin Eintrag zuordnet


# Street analysis from bottin dataset
This analysis wants to find new streets coming up in the bottin dataset and
streets disapearing in the bottin dataset.
## Preprocess streets from the bottin dataset
### Make Dictionary with all streets in bottin dataset
## Streets appearing
### Copy Dictionary remove 1836 Data (they already exist)
### Find out when they are first appearing 
### Add creation year to dataset
## Streets disapearing 
### Copy Dictionary
### Count number of entries for each street from 1922 backwards
### Determine last year where there were still entries
### Add destructed year to dataset

