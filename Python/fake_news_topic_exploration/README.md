# 2016 Presidential Election Fake News Analysis

Slides:
https://docs.google.com/presentation/d/1V4vxpBDHxyCNS7dTn8kcWQjpkNU-HRqXB1O3rQeflnQ/edit?usp=sharing 

## Introduction
Fake News has been considered a serious problem as it forms false belief and threaten the integrity of a democracy. The problem could be even more damaging on Facebook, which provides not only a platform for spreading fake news, but also an algorithm to people that tend to "like" the article feeded to them. Before trying to answer the spread of fake news and their influences on Facebook, we started with exploring their discussion topics and the words that are brought up together with certain politicians and issues.

## Data
* Post data from 1000 popular political Facebook pages having url that links to fake news website. 
* 6-months monthly analysis from 2016.03 - 2016.08
* Uses “post_name” text data of the each post

## Fake News Discussion Topics
Done by K-means clustering. 
Example of Findings:

<img width="1020" alt="screen shot 2019-01-16 at 6 45 35 pm" src="https://user-images.githubusercontent.com/31845611/51287954-a89fbe80-19bf-11e9-835a-7ba4b0a0e5cb.png"> 



## Surrounding Discussion of Certain Politicians/Issue
Done by Word2Vec.
Example of Findings:
(Each box is a two month window)

<img width="1021" alt="screen shot 2019-01-16 at 6 48 44 pm" src="https://user-images.githubusercontent.com/31845611/51287998-d4bb3f80-19bf-11e9-8a2a-8ffe079a1772.png">


<img width="1018" alt="screen shot 2019-01-16 at 6 48 50 pm" src="https://user-images.githubusercontent.com/31845611/51288016-e3095b80-19bf-11e9-8eee-e8abbd1564ce.png">
