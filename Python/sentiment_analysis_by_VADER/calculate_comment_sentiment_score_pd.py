import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import wordpunct_tokenize
from tqdm import *
import os
import csv
import datetime

def write_file(write_dict, write_path):
	comments_list = ["post_id","comment_id", "comment_message", 
					"sentiment_score", "comment_create_time"]
	for page in write_dict:
		try:
			page_df = pd.DataFrame.from_dict(write_dict[page], orient = 'columns')
		except:
			print(page)
		if(os.path.isfile(write_path)):
			page_df.to_csv(write_path + page + ".csv",
							mode = 'a' ,
							header = False,
							index = False, 
							columns = comments_list )
		else:
			page_df.to_csv(write_path + page + ".csv",
							index = False, 
							columns = comments_list )


def calculating_comment_sentiment_score(comment_folder_path, matched_output_file, 
								unmatched_output_file, event_output_file,
								from_percentage = 0, to_percentage = 1.0):

	sid = SentimentIntensityAnalyzer()
	input_list = os.listdir(comment_folder_path)
	input_list.sort()
	start_file = int( len(input_list) * from_percentage)
	end_file = int( len(input_list) * to_percentage)
	print("dealing from file: ", start_file, " to: ", end_file)

	for file_iter in range(start_file, end_file):
		file_name = comment_folder_path + input_list[file_iter]
		this_file = pd.read_csv(file_name, 
									dtype = {"comment_id": str, 
											"post_id": str, 
											"comment_message": str})
		matched_id_dict = {}
		unmatched_id_dict = {}
		event_dict = {}
		for row_iter in tqdm(range(0 , len(this_file["comment_id"]))):
			this_message = this_file["comment_message"][row_iter]
			if(type(this_message) != str):
				#print(this_file.iloc[row_iter])
				#print("problematic post iter at: ", row_iter)
				continue
			sentiment_score_dict = sid.polarity_scores(this_message)
			try:    
				comment_id_list = this_file["comment_id"][row_iter].split("_")
				post_id_list = this_file["post_id"][row_iter].split("_")
			except:
				print(this_file.iloc[row_iter])
				print("missing id's iter at: ", row_iter)
				continue
			try: 
				see = post_id_list[1]
			except:
				print("skil this post_id: ", post_id_list)
				continue
			page_id = post_id_list[0]
			if(comment_id_list[0] == post_id_list[1]):
				if(page_id not in matched_id_dict):
					matched_id_dict[page_id] ={"post_id":[comment_id_list[0]],
									"comment_id": [comment_id_list[1]], 
									"comment_message": [this_file["comment_message"][row_iter]],
									"sentiment_score": [sentiment_score_dict["compound"]],
									"comment_create_time": [this_file["comment_created_time"][row_iter]]
									}
				else:
					matched_id_dict[page_id]["post_id"].extend([comment_id_list[0]])
					matched_id_dict[page_id]["comment_id"].extend([comment_id_list[1]])
					matched_id_dict[page_id]["comment_message"].extend([this_file["comment_message"][row_iter]])
					matched_id_dict[page_id]["sentiment_score"].extend([sentiment_score_dict["compound"]])
					matched_id_dict[page_id]["comment_create_time"].extend([this_file["comment_created_time"][row_iter]])
			else:
				if(len(comment_id_list) == 1 ):
					if(page_id not in event_dict):
						event_dict[page_id] = {"post_id":[post_id_list[1]],
										"comment_id": comment_id_list, 
										"comment_message": [this_file["comment_message"][row_iter]],
										"sentiment_score": [sentiment_score_dict["compound"]],
										"comment_create_time": [this_file["comment_created_time"][row_iter]]
										}
					else:
						event_dict[page_id]["post_id"].extend([post_id_list[1]])
						event_dict[page_id]["comment_id"].extend(comment_id_list)
						event_dict[page_id]["comment_message"].extend([this_file["comment_message"][row_iter]])
						event_dict[page_id]["sentiment_score"].extend([sentiment_score_dict["compound"]])
						event_dict[page_id]["comment_create_time"].extend([this_file["comment_created_time"][row_iter]])			

				else:
					if(page_id not in unmatched_id_dict):
						unmatched_id_dict[page_id] = {"post_id":[comment_id_list[0]],
										"comment_id": [comment_id_list[1]], 
										"comment_message": [this_file["comment_message"][row_iter]],
										"sentiment_score": [sentiment_score_dict["compound"]],
										"comment_create_time": [this_file["comment_created_time"][row_iter]]
										}
					else:
						unmatched_id_dict[page_id]["post_id"].extend([comment_id_list[0]])
						unmatched_id_dict[page_id]["comment_id"].extend([comment_id_list[1]])
						unmatched_id_dict[page_id]["comment_message"].extend([this_file["comment_message"][row_iter]])
						unmatched_id_dict[page_id]["sentiment_score"].extend([sentiment_score_dict["compound"]])
						unmatched_id_dict[page_id]["comment_create_time"].extend([this_file["comment_created_time"][row_iter]])

		write_file(matched_id_dict, matched_output_file)
		write_file(unmatched_id_dict, unmatched_output_file)
		write_file(event_dict, event_output_file)

		print("done ", file_iter, " at ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def main():
	comment_folder_path = "/home3/ntueconfbra1/Desktop/Link to usfb-data/comment/"
	matched_output_file = "/home3/ntueconfbra1/Link to fromRA1/sentiment_analysis/comments/matched_post_id/"
	unmatched_output_file = "/home3/ntueconfbra1/Link to fromRA1/sentiment_analysis/comments/unmatched_post_id/"
	event_output_file = "/home3/ntueconfbra1/Link to fromRA1/sentiment_analysis/comments/event_post/"
	#row_num = get_num_lines(post_data_path)
	calculating_comment_sentiment_score(comment_folder_path, matched_output_file, 
										unmatched_output_file, event_output_file,
										277/500, 300/500)


if __name__ == '__main__':
	main()

