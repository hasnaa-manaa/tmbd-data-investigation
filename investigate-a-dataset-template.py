#!/usr/bin/env python
# coding: utf-8

# > **Movies Report**:
# 
# # Project: Investigate a Dataset (tmbd)
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# > **Movies**: This report is based on tmbd data describing features of movies including genres,budger, revenue, directors and average vote.  
# We will try to answer some questions using this dataset like  
# Q1 which genres was prefered among years?  
# Q2 Which companies produced the highest revenue movies ?  
# Q3 Which movies had the highest budget ?   and Did they return highest revenue?   

# In[1]:


# Use this cell to set up import statements for all of the packages that you
import pandas as pd
import numpy as np
import matplotlib as plt
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
get_ipython().run_line_magic('matplotlib', 'inline')
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# 
# 
# ### General Properties

# In[2]:


# Load your data and print out a few lines. Perform operations to inspect data
movies=pd.read_csv('tmdb-movies.csv')
#   types and look for instances of missing or possibly errant data.
movies.head()


# In[16]:


movies.info()


# In[3]:



#investigate null values
movies.isna().sum()


# In[21]:


#fill null and zero values of budget by mean
def replace_zeros_nulls_byMean(col):
    mean=movies[movies[col]>0][col].mean()
    movies[col].fillna(mean,inplace=True)
    movies[col].replace({0:mean}, inplace=True)
    movies[col]= movies[col].astype(int)


# In[22]:


#cleaning revenue,budget
replace_zeros_nulls_byMean('revenue')
replace_zeros_nulls_byMean('budget')


# In[73]:


movies['revenue']


# In[74]:


movies['budget']


# In[ ]:



#drop unused columns
movies=movies.drop(['keywords','tagline','homepage','cast'],axis=1)


# In[ ]:


movies=movies.drop('overview',axis=1)
movies.head()


# In[6]:



#convert to date
movies['release_date']=pd.to_datetime(movies['release_date'])
movies.info()


# In[58]:


#detect duplicates
movies.duplicated()


# In[23]:


df=movies.copy()


# In[7]:


#remove"|" from genres
movies['genres']=movies['genres'].str.split("|",n=1,expand=True)


# In[16]:


movies.head()


# In[8]:


##remove"|" from production_companies
movies['production_companies']=movies['production_companies'].str.split("|",n=1,expand=True)


# In[64]:


movies.head()


# In[18]:


movies['release_year'].value_counts()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# 
# 

# In[36]:


#Starting with exploring data distribution of vote_average
ax=movies[['vote_average']].hist()
plt.pyplot.title("vote_average histogram")
plt.pyplot.show()


# Most films are rated in the range(5,7)

# <a id='eda'></a>
# ## Q1 which genres was prefered over last 2 decades?
# 

# In[9]:


#limit genres to most common
movies['genres'].value_counts()


# we can notice that most movies are Comedy, Action, Drama

# In[10]:


#limiting genres
genres_to_consider = ['Drama', 'Comedy','Action']
new_df=movies[movies['genres'].isin(genres_to_consider)]


# In[11]:


#limiting years
new_df=new_df[new_df['release_year']>=2000]


# In[32]:


#line plot is used to plot avg_vote over time, units here indicate for chosen genres
import seaborn as sns
ax=sns.relplot(x='release_year', y='vote_average', hue='genres',units='genres',estimator=None,kind='line', data=new_df)
ax.set(xlabel='release_year', ylabel='vote_average')
plt.pyplot.title("vote_average of different genres over 20 years")
plt.pyplot.show()


# We can notice that there is slight even distribution exccept some exremes like the drop of avg_vote of action movies in 2007 or the rise of Drama movies average vote in 2014.

# ### Research Question 2   Which  companies  produced the highest revenue  movies ?

# In[13]:


#based on revenue we select top 10 companies 
movies.sort_values(by=['revenue'],ascending=False).head(10)['production_companies']
top=movies.sort_values(by=['revenue'],ascending=False).head(10)


# In[30]:


plt.rc('figure', figsize=(20, 5))
ax=sns.barplot(x='production_companies',y='revenue', data=top)
ax.set(xlabel='production companies', ylabel='revenue')
plt.pyplot.title("companies revenue from single  top movie")
plt.pyplot.show()


# This chart shows us the top 10 revenues get from single movie and the production company.

# ### Q3 Which movies had the highest budget ? and Did they return highest revenue

# In[15]:


#to answer the question we start to invstigate movies with highest budget
movies.sort_values(by=['budget'],ascending=False).head(10)[['original_title','budget','revenue']]


# In[16]:


#investigate movies with highest revenue 
movies.sort_values(by=['revenue'],ascending=False).head(10)[['original_title','budget','revenue']]


# In[17]:


#check which movie is in both groups?
movies.sort_values(by=['revenue'],ascending=False).head(10)[['original_title','budget','revenue']].isin(movies.sort_values(by=['budget'],ascending=False).head(10)[['original_title','budget','revenue']])


# It's clear that only one movie "Avengers: Age of Ultron" exists in both lists!

# ## Limitation
#     There have some limitations working with dataset:
#     Budget and revenue had some missing or unreasonable values.
#     If we had that data we might change some insights if they were among the highest revenue movies
#     Regarding votes calculated, if you run the code below  they vary from very few to much larger. This can affect the      vote_average and increase bias expectancy.
#     

# In[26]:


movies['vote_count'].value_counts()


# <a id='conclusions'></a>
# ## Conclusions
# 
#      At the end of this report, we investigated top rated genres over the last two decades.
#      We have known the companies that produces the highest rated movies 
#      we found that high budget of movie doesn't mean high revenue at all
# 
# 
