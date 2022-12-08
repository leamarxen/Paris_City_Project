import pandas as pd

def align_on_column(df_not_aligned, df_streets, df_aligned=pd.DataFrame(), 
                    mergeOnLeft="street", mergeOnRight="street", align_method=""):
    # make copies to avoid alteration of source dataframes
    not_aligned = df_not_aligned.copy()
    streets = df_streets.copy()
    if not df_aligned.empty:
        aligned = df_aligned.copy()
    else:
        aligned = df_aligned
        
    # merge
    merged = not_aligned.merge(streets, how="left", left_on=mergeOnLeft, right_on=mergeOnRight, suffixes=(False, False))
    # append newly aligned cases to aligned dataframe
    newly_aligned = merged[merged[mergeOnRight].notna()]
    # add column to know what alignment was on
    newly_aligned["align_method"] = align_method
    aligned = pd.concat([aligned, newly_aligned])
        
    # update not aligned rows
    not_aligned = merged[merged[mergeOnRight].isna()]
    not_aligned = not_aligned.drop(list(streets.columns), axis=1)
    print(f"Joining on {mergeOnLeft} and {mergeOnRight}, method:{align_method}\n" +\
        f"#total aligned: {len(aligned)}, newly aligned: {len(newly_aligned)}, not aligned: {len(not_aligned)}")
    
    return aligned, not_aligned