
# function to deal with whitespace and caps:
def trimandlower(dframe):
    dframe.columns = dframe.columns.str.lower()\
            .str.replace('  ',' ')\
            .str.replace(' ','_')
    for i in dframe.columns:
    # checking datatype of each columns
        if dframe[i].dtype == 'object':
    # applying strip function on column
            dframe[i] = dframe[i].str.replace('  ',' ')\
                .str.replace(' ','_')\
                .str.lower()
        else: pass
    return(dframe)