
import pandas as pd
import plotnine as p9

surveys_complete = pd.read_csv("surveys.csv")
surveys_complete = surveys_complete.dropna()

"""
p = (p9.ggplot(surveys_complete,
               p9.aes(x='weight', y='hindfoot_length'))#,color = 'year' ,color = 'species_id'
     + p9.geom_point())

print (p)
"""

"""
p =(p9.ggplot(surveys_complete,
              p9.aes('weight', 'hindfoot_length',  color = 'species_id'))
    + p9.geom_point()
    + p9.facet_wrap("sex"))#year
print (p)
"""

"""
survey_year = surveys_complete[surveys_complete
                ["year"].isin([1998,2000,2001,1977])]

p =(p9.ggplot(data=survey_year,
           mapping=p9.aes(x='weight',
                          y='hindfoot_length',
                          color='species_id'))
    + p9.geom_point()
    + p9.facet_wrap("year"))#facet_grid("year ~ sex"))
print (p)
"""


"""
p =(p9.ggplot(surveys_complete,
              p9.aes('species_id', fill='weight', color = 'sex'))
    + p9.geom_bar(stat = 'identity'))
print (p)
"""

"""
p =(p9.ggplot(surveys_complete,
              p9.aes('species_id', 'weight'))#, color = 'sex'
    + p9.geom_boxplot())
"""

"""
p =(p9.ggplot(data=surveys_complete,
           mapping=p9.aes(x='species_id',
                          y='weight',
                          color='year'))
    + p9.geom_jitter(alpha=0.4)
    + p9.geom_violin(alpha=0.2, color="0.7")
    + p9.scale_y_log10())
"""

"""
yearly_counts = surveys_complete.groupby(
    ['year', 'species_id'])['species_id'].count()
yearly_counts = yearly_counts.reset_index(name='counts')
p =((p9.ggplot(data=yearly_counts,
           mapping=p9.aes(x='year',
                          y='counts',
                          color='species_id'))
    + p9.geom_line()))
"""

"""
yearly_weight = surveys_complete.groupby(['year', 'species_id'])['weight'].mean().reset_index()

p =(p9.ggplot(data=yearly_weight,
           mapping=p9.aes(x='year',
                          y='weight'))
    + p9.geom_line()
    + p9.facet_wrap("species_id"))
"""


#print ('after dropNa: \n',surveys_complete)
#p = (p9.ggplot(surveys_complete, aes(x='weight', y='hindfoot_length')) + geom_point())
#(p9.ggplot(data=surveys_complete, mapping=p9.aes(x='species_id')) + p9.geom_bar())



# Below are the functions used in Task 3 Tutorial 3

# Question b
'''
p = (p9.ggplot(surveys_complete,
               p9.aes(x='weight', y='hindfoot_length',
                      color = 'sex'))
     + p9.geom_point())
print(p)
'''

# Question c
'''
p = (p9.ggplot(surveys_complete,
               p9.aes(x='species_id', y='weight',
                      color = 'sex'))
     + p9.geom_bar(stat = 'identity')
     + p9.facet_wrap("sex")    # for dividing by sex
)
print(p)
'''

# Question d
'''
survey_year = surveys_complete[surveys_complete
                ["year"].isin([1979,1993,1999,1977])]

p = (p9.ggplot(survey_year,
               p9.aes(x='species_id', y='hindfoot_length',
                      color = 'sex'))
     + p9.geom_point())
print(p)
'''