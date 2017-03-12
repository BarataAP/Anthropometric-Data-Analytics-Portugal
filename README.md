# Anthropometric-Data-Analytics-Portugal
Implementation code for my MSc in Bioinformatics thesis project.

The goal was to create a set of scripts which enable the creation of: a database to harbour information (in this case, regarding measurements of anthorpometric distances and weights), a prompt-assisted data insertion tool, and a convenient way to manipulate data.

createDB.py: python code to produce a database. File edition is advised in order to accomodate specific data structure needs.

insertValues.py: when run, a user-friendly windows opens, prompting variable values to insert (related to the properties and attributes defined for the database in createDB.py).

analysis.py: module containing data manipulation functions.

CHLO.db: database containing all collected data within this thesis project.

CHLO.csv: csv file representing CHLO.db
