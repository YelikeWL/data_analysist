import pandas as pd
surveys_df = pd.read_csv("surveys.csv")

''' Functions below can be used to check data values '''
print (surveys_df)          # all data

# print (surveys_df.dtypes)
# print (type(surveys_df))

# print (surveys_df.head())
# print (surveys_df.tail())
# print ("the dimensionality of DataFrame:", surveys_df.shape)

# print (pd.unique(surveys_df['species_id']))
# print (surveys_df['species_id'].describe())
# print (surveys_df['weight'].describe())
# print (surveys_df['weight'].min())

# grouped_data = surveys_df.groupby('sex') #['sex','month'])
# print (grouped_data['weight'].describe())

# print (surveys_df.columns.values)
# pd.set_option('display.max_columns', 56)

''' Find a proper indexing function in the documentation page to return 
the value of the 3rd row, and the 8th column. Note, the indexing of Python 
starts from 0, thus 3rd row is at index 2 and 8th column at 7. '''

print(surveys_df.iat[2, 7])

# Print the selected few rows and columns
'''What if I want to have the values of the first 3 rows, but only the columns 
from 2nd to 4th, namely, the first 3 rows’ values of month, day and year. '''
# the tree methods shows the same answer
print(surveys_df.iloc[0:3, 1:4])                    # by indexes
print(surveys_df.iloc[:3, [1, 2, 3]])               # :3 is the same as 0:3
print(surveys_df.loc[:2, ["month", "day", "year"]]) # similar to above, except 'loc' uses columns' names directly

'''What if I want to have all the values of the 6th column, namely, the species id. '''
# for all selection (from beginning to the end) use " : "
print(surveys_df.iloc[:, 5])
print(surveys_df.iloc[:, [5]])
print(surveys_df.loc[:, ["species_id"]])

'''What if I want to have all the values of the 6th column, but with the duplicates removed?'''
# Given only the index of the column, we should search the name of the column first
col6_name = surveys_df.columns[5]       # get the name of the column name it as col6_name
print (pd.unique(surveys_df[col6_name]))    # col6_name = 'species_id'
print (surveys_df.species_id.unique())  # can use this only if know the column name