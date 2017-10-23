import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import wordpunct_tokenize
from tqdm import *
import os
import csv
import datetime

def find_candidate_related_posts(post_path, output_path):
	post_data = pd.read_csv(post_path, 
							usecols = ['post_id','post_name','post_message'],
	 						converters = {'post_id':str, 'post_name':str, 'post_message': str})
	trump_relatives = ["melania", "ivanka", "eric", "tiffany", "barron"]
	trump_jr = [".jr", "jr"]
	clinton_relatives = ["bill", "chelsea"]
	trump_post_indexs = []
	clinton_post_indexs = []



	for i in tqdm(range(0, len(post_data["post_id"]))):
		trump_flag = 0
		clinton_flag = 0
		post_flag = 0
		post_content = post_data["post_name"][i] + post_data["post_message"][i] 
		post_token = wordpunct_tokenize(post_content.lower())
		if (len(post_token) == 0) :
			continue
		if(post_token[0] == "trump"):
			trump_flag = 1
			trump_post_indexs.extend([i])
		elif(post_token[0] == "clinton"):
			clinton_flag = 1
			clinton_post_indexs.extend([i])
		if (len(post_token) == 1):
			continue
		for word_index in range(1, len(post_token)-1):
			if(post_token[word_index] == "trump" and trump_flag == 0):
				if(post_token[word_index - 1] in trump_relatives or post_token[word_index + 1] not in trump_jr):
					trump_flag = 1
					trump_post_indexs.extend([i])
					if(clinton_flag == 1 ):
						post_flag = 1
						break
			elif(post_token[word_index] == "clinton" and clinton_flag == 0):
				if(post_token[word_index - 1] not in clinton_relatives):
					clinton_flag = 1
					clinton_post_indexs.extend([i])
					if(trump_flag == 1):
						post_flag = 1
						break
		
			if(post_flag == 1):
				break


		if(post_flag == 0):
			last_iter = len(post_token) -1
			if(post_token[last_iter] == "trump" and post_token[last_iter - 1] not in trump_relatives):
				trump_flag = 1
				trump_post_indexs.extend([i])
			elif(post_token[last_iter] == "clinton" and post_token[last_iter - 1] not in clinton_relatives):
				clinton_flag = 1
				clinton_post_indexs.extend([i])	

	trump_related_posts = post_data.iloc[trump_post_indexs]	
	trump_related_posts.index.name = "index"
	trump_related_posts.to_csv(output_path + "posts_about_trump.csv")

	clinton_related_posts = post_data.iloc[clinton_post_indexs]
	clinton_related_posts.index.name = "index"
	clinton_related_posts.to_csv(output_path + "posts_about_clinton.csv")

def main():
	output_path = "/home3/ntueconfbra1/Desktop/Link to fromRA1/candidate_related_posts/"
	post_path = "/home3/usfb/analysis-fake-news/input/post/1000-page/2015-01-01-to-2017-04-08.csv"
	find_candidate_related_posts(post_path, output_path)


if __name__ == '__main__':
	main()

