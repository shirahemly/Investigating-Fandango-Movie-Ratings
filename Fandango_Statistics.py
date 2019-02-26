#!/usr/bin/env python
# coding: utf-8

# # Investigating Fandango Movie Ratings

# In October 2015, a data journalist named Walt Hickey analyzed movie ratings data and found strong evidence to suggest that Fandango's rating system was biased and dishonest. 
# Hickey found that there's a significant discrepancy between the number of stars displayed to users and the actual rating, which he was able to find in the HTML of the page.
# 
# Fandango's officials replied that the biased rounding off was caused by a bug in their system rather than being intentional, and they promised to fix the bug as soon as possible. 
# 
# In this project, I'll analyze more recent movie ratings data to determine whether there has been any change in Fandango's rating system after Hickey's analysis.

# In[46]:


import pandas as pd
pd.options.display.max_columns = 100
from pandas import DataFrame
from numpy import arange
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[2]:


fandango_score_comparison = pd.read_csv('fandango_score_comparison.csv')
movie_ratings_16_17 = pd.read_csv('movie_ratings_16_17.csv')


# In[3]:


fandango_score_comparison.head(2)


# In[4]:


movie_ratings_16_17.head(2)


# In[5]:


# Isolating relevant data for this project into new dfs

hickeys_fandango_scores = fandango_score_comparison[['FILM', 'Fandango_Stars', 'Fandango_Ratingvalue', 'Fandango_votes', 'Fandango_Difference']]
new_fandango_scores = movie_ratings_16_17[['movie', 'year', 'fandango']]


# In[6]:


hickeys_fandango_scores.head(2)


# In[7]:


new_fandango_scores.head(2)


# The goal of this project is to determine whether there has been any change in Fandango's rating system after Hickey's analysis.
# 
# The population - All the movie ratings stored on Fandango's website.
# 
# I'm interested in sampling the population at two different periods in time - Prior to Hickey's analysis and post.
# 
# 'hickeys_fandango_scores' is a representation of the data collected by Hickey for his analysis, therefore it includes movie ratings previous to his analysis. (The data from Fandango was pulled on Aug. 24, 2015)
# 
# 'new_fandango_scores' is a representation of data collected between the years 2016 and 2017, after Hickey's analysis.
# 
# 
# #sampling#
# 
# According to Hickey's README.md file of the data set's repository, the sampling was not random, and had the following criteria:
# - The movie had tickets on sale in 2015.
# - The movie must have at least 30 user votes.
# 
# Second sample's conditions:
# - The movie released in 2016 or later.
# - The movie have received a significant number of votes (README.md did not specify how many)
# 
# Both samples are subject to trends and it's unlikely to be representative of our population of interest.
# It seems that both samples were collected as purposive sampling, and served their collectors' needs for their projects.
# Unfortunately, the two samples are not useful for this project's objectives.

# # Changing the Goal of our Analysis

# Since the collected data is not useful for the original project's goal, the two options that I have is to either collect new data or change the goal of the project. 
# 
# New goal - Determine whether there's any difference between Fandango's rating for popular movies in 2015 and Fandango's rating for popular movies in 2016.
# 
# Populations - 
# - All ratings for popular movies in 2015
# - All ratings for popular movies in 2016
# 
# A popular movie (for the sake of this project), is one with over 30 user ratings. Since the second dataset does not include number of user ratings, I would manually check a small sample of movies over at Fandango's website to see if it matches the criteria.
# 
# 

# In[8]:


new_fandango_scores.sample(10, random_state=1)


# In[9]:


manual_rating_check = DataFrame({'Movie': ['Mechanic: Resurrection', 'Warcraft', 'Max Steel', 'Me Before You', 'Fantastic Beasts and Where to Find Them', 'Cell', 'Genius', 'Sully', 'A Hologram for the King', 'Captain America: Civil War'],
                                'No. of ratings': [2251, 7280, 494, 5270, 13486, 18, 127, 11890, 501, 35144]})

sum(manual_rating_check['No. of ratings'] > 30)/10*100


# 90% of the movies I've sampled have over 30 user's ratings on Fandango's website.

# In[10]:


# Isolating movies from 2015 and 2016 to new dfs

hickeys_fandango_scores['Year'] = hickeys_fandango_scores['FILM'].str[-5:-1]


# In[11]:


hickeys_fandango_scores.head(2)


# In[13]:


movies_2015 = hickeys_fandango_scores[hickeys_fandango_scores['Year'] == '2015'].copy()


# In[15]:


movies_2015['Year'].value_counts()


# In[19]:


movies_2016 = movie_ratings_16_17[movie_ratings_16_17['year'] == 2016].copy()


# In[21]:


movies_2016['year'].value_counts()


# In[22]:


movies_2015.head(2)


# In[24]:



movies_2016.head(2)


# In[58]:


plt.style.use('fivethirtyeight')

movies_2015['Fandango_Stars'].plot.kde(label='2015', legend=True, figsize=(8,6.5))
movies_2016['fandango'].plot.kde(label='2016', legend=True)

plt.title("Comparing distribution shapes for Fandango's ratings\n(2015 vs 2016)", y=1.05, fontsize=20)
plt.xlabel("Stars", fontsize=18)
plt.xlim(0,5)
plt.xticks(arange(0,5,.5))
plt.ylabel("Density", fontsize=18)
plt.show()


# - Both distributions are left skewed.
# - 2016 distribution comparing to 2015 distribution is slightly shifted to the left - Movie ratings in 2016 are lower than in 2015.
# 
# 
# According to the chart above, Fandango's scores are mostely high. Since Fandango also sell tickets, it is possible that the ratings are bias.

# In[81]:


print("2015")
movies_2015['Fandango_Stars'].value_counts(normalize=True).sort_index()*100


# In[82]:


print("2016")
movies_2016['fandango'].value_counts(normalize=True).sort_index()*100


# In 2016, the minimum rating is lower than in 2015 (2.5  instead of 3 stars).
# In 2016, very high ratings had lower percentage compare to 2015 (4.5 and 5 stars).
# 

# In[83]:


mean_2015 = movies_2015['Fandango_Stars'].mean()
mean_2016 = movies_2016['fandango'].mean()

median_2015 = movies_2015['Fandango_Stars'].median()
median_2016 = movies_2016['fandango'].median()

#most repeated value
mode_2015 = movies_2015['Fandango_Stars'].mode()[0] 
mode_2016 = movies_2016['fandango'].mode()[0] 

summary = pd.DataFrame()
summary['2015'] = [mean_2015, median_2015, mode_2015]
summary['2016'] = [mean_2016, median_2016, mode_2016]
summary.index = ['mean', 'median', 'mode']
summary


# In[89]:


plt.style.use('fivethirtyeight')

summary['2015'].plot.bar(color = '#0066FF', align = 'center', label = '2015', width = .30, figsize=(8,6.5))
summary['2016'].plot.bar(color = '#CC0000', align = 'edge', label = '2016', width = .30)


plt.title("Comparing distribution shapes for Fandango's ratings\n(2015 vs 2016)", y=1.05, fontsize=20)
plt.ylim(0,5)
plt.yticks(arange(0,5.1,.5))
plt.ylabel("Stars", fontsize=18)
plt.legend(framealpha = 0, loc = 'upper center')

plt.show()


# In[90]:


(summary.loc['mean'][0] - summary.loc['mean'][1]) / summary.loc['mean'][0]


# # Conclusion

# Our analysis shows that there is a difference between Fandango's ratings for movies in 2015 and Fandango's ratings for movies in 2016.
# Popular movies that released in 2016 got lower ratings than Popular movies that released in 2015.
# 
# It looks like Fandango fixed the bias rating system after Hickey's analysis.

# In[ ]:




