def preprocess(df, column, new_colname=None, map_dict = {"é": "e", "è": "e", "ê":"e", "à":"a", 
                "â":"a", "ô":"o", "î":"i", "û":"u", "ç":"c", "\-":" ", "\_":" ", "' ":"'", "  ":" "}):
    '''
    Takes a column of a dataframe, changes strings to lowercase and replaces map_dict's keys
    with its values.

    Parameters:
    ------------------
    :df: pandas dataframe preprocessing is conducted on 
    :column: name (string) of the column the preprocessing is conducted on
    :new_colname: if not None, assigns this name to the new column which contains the preprocessed data,
                else: assign name {column}_prep to new column
    :map_dict: dictionary containing all the substiutions which should take place

    Returns:
    -------------------
    :data: pandas dataframe with new column containing preprocessed data
    '''
    data = df.copy()
    if not new_colname:
        new_colname = f"{column}_prep"
    data[new_colname] = data[column].str.lower()
    data[new_colname] = data[new_colname].replace(map_dict, regex=True)
    return data

def get_prefix(row, court, long):
    '''
    Takes a row of a dataframe and returns the difference between the entries of the columns
    "long" and "court".

    Parameters:
    ----------------
    :row: row (with column names) of a dataframe
    :court: string
        name of column with shorter entry (has to coincide with end of string of column "long")
    :long: string
        name of column with longer entry

    Returns:
    -----------------
    string of difference between court and long entry of row
    '''
    return row[long].split(row[court])[0]


def substitute_row_by_dict(row, word_dict):
    '''
    helper function for substitute_col_by_dict
    finds and substitutes words in a row, using a dictionary 
    
    Parameters:
    -------------------
    :row: string which might be containing words/characters to substitute
    :word_dict: dictionary of the form {"incorrect/abbreviated word(s):"correct word(s)"}

    Returns:
    --------------------
    :row: string with the substitution
    '''
    for incorrect, correct in word_dict.items():
        if incorrect in row:
            row = row.replace(incorrect, correct)
    return row


def substitute_col_by_dict(column, word_dict):
    '''
    finds and substitutes words in a column, using a dictionary

    Parameters:
    ---------------------
    :column: pandas Series which contains words/characters to substitute
    :word_dict: dictionary of the form {"incorrect/abbreviated word(s):"correct word(s)"}

    Returns:
    ----------------------
    pandas Series which contains substitutions
    '''
    return column.apply(substitute_row_by_dict, args=(word_dict,))

