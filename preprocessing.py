def preprocess(df, column, new_colname=None, map_dict = {"é": "e", "è": "e", "ê":"e", "à":"a", 
                "â":"a", "ô":"o", "î":"i", "û":"u", "ç":"c", "\-":" ", "\_":" ", "' ":"'", "  ":" "}):
    '''
    Takes a column of a dataframe, changes strings to lowercase and replaces map_dict's keys
    with its values.
    '''
    data = df.copy()
    if not new_colname:
        new_colname = f"{column}_prep"
    data[new_colname] = data[column].str.lower()
    data[new_colname] = data[new_colname].replace(map_dict, regex=True)
    return data


def substitute_row_by_dict(row, word_dict):
    '''
    helper function for substitute_col_by_dict
    finds and substitutes words in a row, using a dictionary 
    
    :row: string which might be containing words/characters to substitute
    :word_dict: dictionary of the form {"incorrect/abbreviated word(s):"correct word(s)"}
    '''
    for incorrect, correct in word_dict.items():
        if incorrect in row:
            row = row.replace(incorrect, correct)
    return row


def substitute_col_by_dict(column, word_dict):
    '''
    finds and substitutes words in a column, using a dictionary

    :column: pandas Series which contains words/characters to substitute
    :word_dict: dictionary of the form {"incorrect/abbreviated word(s):"correct word(s)"}
    '''
    return column.apply(substitute_row_by_dict, args=(word_dict,))

'''
    #two different replacement methods to reduce computation time 
    # abbreviations without spaces (" ")   
    words_no_space = [entry for entry in word_dict.keys() if " " not in entry]
    dict_no_space = {key:word_dict[key] for key in words_no_space}
    # replacement
    result = column.str.split().apply(lambda x: ' '.join([dict_no_space.get(e, e) for e in x]))
    
    # abbreviations with spaces (-> for loop, takes longer)
    words_with_space = [entry for entry in word_dict.keys() if " " in entry]
    if words_with_space:
        dict_with_space = {key:word_dict[key] for key in words_with_space}
        # replacement
        result = result.apply(substitute_row_by_dict, args=(dict_with_space,))

    return result


'''

