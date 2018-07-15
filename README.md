### NTU Economics Facebook Research Project

## Introduction
Our project research on dynamics of different political actors on Facebook during the 2016 US presidential election. We 
acquired 1000+ media and politician fan pages data along with Facebook user’s activities and reaction to the page's posts
from January 2015 to November 2016. Which was used to quantify political ideology score of the Media, politicians, and 
users interacted with these pages on Facebook on the same spectrum. Interesting applications like election forecasting, 
fake news detection, measuring opinion segregation, etc. were carried out using such measured political ideology score.

## Data and measures for calculating political ideology score.
Facebook "like" data, containing variables: user ID, post ID, page ID, like time, was stored in a local MySQL database.
We created Python scripts to connect the database for the bellow data processing. After deciding our interested period of 
time, our program generates a page by page matrix containing shared users among pages. At which we apply principle component
analysis (PCA) to derive the political ideology score. I was responsible for building the python package for the whole 
process. 
For more detail, please refer to: https://github.com/NTUUSFB/workshop-2017-10/blob/master/4-fbscore/fbscore-demo.ipynb 


## Work I have done:
Built MySQL database, built package "fb-score", bootstrap of ideology scores for 4-months period, sentiment analysis on post,
text comparison for detecting fake news.
