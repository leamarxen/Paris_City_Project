# External Data

In the process of creating tags for each profession three external data sources are used. These three data sources correspond to language dictionaries that will help in distinguishing the tokens that already have a correct spelling. Out of the three data sources, two are french language dictionaries including proper nouns and one is dataset about the street names in Paris.

## File description

### Morphalou3_CSV

The `Morphalou3_CSV.csv` file in the `Morphalou3_formatCSV_toutEnUn` folder has the data of the lexicons of the French language. The set of words is provided by ortolang as [Morphalou3](https://repository.ortolang.fr/api/content/morphalou/2/LISEZ_MOI.html#idp37913792) that has 159,271 lemmas and 954,690 inflected forms of modern French. The CSV file provided by Morphalou3 in [Morphalou3_formatCSV_toutEnUn](https://repository.ortolang.fr/api/content/morphalou/2/), whose format is described [here](https://repository.ortolang.fr/api/content/morphalou/2/LISEZ_MOI.html#idp37944688).


### Prolex-Unitex_1_2

The `Prolex-Unitex_1_2.dic` file in the `Prolex-Unitex_1_2` folder has the data of common proper nouns used in French. The data which is in `DIC` format is provided [here](https://tln.lifat.univ-tours.fr/medias/fichier/prolex-unitex-1-2_1562935068094-zip?ID_FICHE=321994&INLINE=FALSE). Each row in the file has the word and its details in a single word (such as the context it is used and whether is masculine/feminine and singular or plural) separated by a comma.

### denominations-emprises-voies-actuelles

The `denominations-emprises-voies-actuelles.csv` file in the `Street-names` folder is the table of streets of Paris which is obtained from [Open Paris Data](https://opendata.paris.fr/explore/dataset/denominations-emprises-voies-actuelles/table/?disjunctive.siecle&disjunctive.statut&disjunctive.typvoie&disjunctive.arrdt&disjunctive.quartier&disjunctive.feuille&sort=typo_min). The `denominations-emprises-voies-actuelles.csv` file contains details of the streets of Paris in 28 columns. The `Dénomination complète minuscule` columns is used.