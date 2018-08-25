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
time, our program generates a page by page matrix containing shared users among pages (table 1). Then, we normalize a politician's the number of shared like-users with another by dividing the politicians toal like-users(table2). 

![screen shot 2018-08-24 at 10 07 02 pm 2](https://user-images.githubusercontent.com/31845611/44614452-482e9b80-a7ea-11e8-91cf-d1c07785930e.png)



We apply principle component analysis (PCA) to table2 and assigned the first principle component as political ideology score. 
Figure 1 shows the ideology of all US Facebook political users, which seems to be more liberal and lean to the left. 

![figure1](https://user-images.githubusercontent.com/31845611/44614841-2d602500-a7f2-11e8-8814-b19036407ce5.png)


We also compare our computed political ideology score with DW-Nominate Score, which is also a political ideology score measured by senators' behavior on different issues in the congress. 

![figure2](https://user-images.githubusercontent.com/31845611/44614855-b8411f80-a7f2-11e8-9b33-b4827752738b.png)


In addition, we also tried to label where these Facebook users are from by the politicians they like, and come up with the political ideology distribution of all states in the US.

![screen shot 2018-08-24 at 11 13 10 pm 2](https://user-images.githubusercontent.com/31845611/44614905-57fead80-a7f3-11e8-9353-e20f2da804fb.png)



By our calculated political ideology score, we can quantify any politician's popularity by months, by weeks, our even after some important event using all public data on Facebook. Polls or election prediction could be done at any time scale we have in mind. We have also worked on a lot of interesting application like fake-news detection, sentiment analysis, segregation (echo-chamber effect) analysis,full research paper: https://kengchichang.com/paper/thesis-fb-paper.pdf.

In order to derive the political ideology score more efficiently, I have written a Python package by organising all code in the whole process. Which started from connecting the database, building page by page matrix, PCA, and ends with computing the user's score by likes they hit on politician's fan pages. For more detail, please refer to: https://github.com/NTUUSFB/workshop-2017-10/blob/master/4-fbscore/fbscore-demo.ipynb 


## Work I was responsible for in the Facebook project:
Built MySQL database, built package "fb-score", bootstrap of ideology scores for 4-months period, sentiment analysis on post,text comparison for detecting fake news.
