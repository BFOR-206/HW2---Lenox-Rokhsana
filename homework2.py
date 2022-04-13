#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 17:10:02 2022

@author: lenox grayson & rokhsana ahmadi
"""

#%% Imports

import pandas as pd

#%% Read in data

aiml_data = pd.read_csv('reddit_database.csv')

aiml_data.head()

#%% Basic information about the data

aiml_data.info()
aiml_data.describe()

#%% Convert date columns to a proper date/time format

aiml_data['author_created_date'] = pd.to_datetime(aiml_data['author_created_utc'], unit='s')

aiml_data['created_date'] = pd.to_datetime(aiml_data['created_date'])

aiml_data = aiml_data.sample(10000)

aiml_data.info()


# aiml_data.describe(include='all')
# hide the warning message

aiml_data.describe(include='all', datetime_is_numeric=True)


#%% Get the day of the week

aiml_data['dow'] = aiml_data['created_date'].dt.day_name()

# this prints the plot directly, minimal formatting:
aiml_data.groupby('dow')['created_date'].count().plot(kind='bar')
 

#%% Format the plot to be ordered by natural day of the week

aiml_data['dow'] = pd.Categorical(aiml_data['dow'], categories=
    ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'],
    ordered=True)

#%% Which subreddit has the most posts (top 5)?  (1.1)

top_sub= aiml_data['subreddit'].str.split(expand=True).stack().value_counts()

(top_sub.head(5))

#%% Which user has the most posts (top 5)?  (1.2)

top_user = aiml_data['author'].str.split(expand=True).stack().value_counts()

(top_user.head(5))


#%% Which subreddit has the most distinct post authors?  (1.3)

distinct_author = aiml_data.groupby('subreddit')['author'].count()


#%% Which subreddit contains the greatest percentage of posts with a post body 
# (i.e. contains a value in the post column)? (1.4) 

percent_post = aiml_data.groupby('subreddit')['post'].count() 
percent_postTotal = aiml_data.groupby('subreddit')['created_date'].count()

percent=(percent_post/percent_postTotal * 100)

print(percent.idxmax())


#%% Plot the total number of posts across all subreddits over time (line plot) (2.1)

alltimeSub = aiml_data.groupby(aiml_data['created_date'].dt.year)['created_date'].count().plot(kind='line')



#%% Plot a histogram showing the distribution of post scores. (2.2)

aiml_data['score'].plot.hist()


#%% Plot the number of posts per day of the week.  (2.3)  


PPDOW = aiml_data.groupby('dow')['post'].count().plot(kind='bar')


#%% Plot the number of posts per hour of the day. (2.4)


aiml_data['dow'] = aiml_data['created_date'].dt.hour

postPerHour = aiml_data.groupby('dow')['post'].count().plot(kind='bar')


#%% Which subreddits had the most new posts in the latest 30 days of data (top 5)? (3.1)

latest30Days = aiml_data.subreddit[aiml_data['created_date']>=  aiml_data['created_date'].max() - pd.Timedelta(days=30)]

print(latest30Days.head(5))


#%% Does the length of a post title correlate with score of the post? (3.2)

aiml_data['post_length'] =aiml_data['title'].str.len()

correlation=aiml_data.corr()


#%% Show the top 20 words from post titles (3.3) 

top20_words = aiml_data['post'].str.split(expand=True).stack().value_counts()

print(top20_words.head(20))


#%% What are the top 10 most linked website domains? (3.4) 

top10_link = aiml_data['full_link'].str.split(expand=True).stack().value_counts()

print(top10_link.head(10))

