from fbscore import base
from fbscore import write
from fbscore import read
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA
from datetime import datetime
from datetime import timedelta
from tqdm import *
import logging
import json
import sys,os
import time
import argparse
import csv
import pandas as pd
import mmap
import os.path
import numpy as np
import pymysql


from scipy import linalg
import statistics as st




def sql_table(cursor, start_date,  end_date, current_month, bootstrap_p, b_seed):
	sql_command_list = ["SELECT  user_id, "
	," GROUP_CONCAT(page_id) as like_pages,"
	," CAST(GROUP_CONCAT(like_time) AS CHAR CHARACTER SET utf8)AS like_times "
	," FROM ("
	,   "SELECT user_id, SUBSTRING_INDEX(post_id,'_',1) as page_id, count(*) AS like_time "
	,    "FROM ( ("
	,     "SELECT user_id, post_id "
	,     "FROM `politician_" , current_month
	,     "` WHERE post_created_date_CT >= '" , start_date 
	,       "' AND post_created_date_CT <= '" , end_date
	,        "' AND RAND(",b_seed, ")< " , bootstrap_p
	,        ")"
	,   "UNION ALL( "
	,     "SELECT user_id, post_id " 
	,     "FROM `1000_page_" , current_month
	,     "`WHERE post_created_date_CT >= '" , start_date 
	,     "' AND post_created_date_CT <= '" , end_date
	,      "' AND RAND(",b_seed,")< " , bootstrap_p
	,        ")"
	,    ") AS temp "
	,    "GROUP BY  user_id,  page_id  ) as temp2 "
	,  "GROUP BY user_id"] 

	sql_command_list = ''.join(str(word) for word in sql_command_list)
	cursor.execute(sql_command_list)
	four_week = cursor.fetchall()
	four_week_df = pd.DataFrame(list(four_week))
	four_week_df.columns = ["user_id", "like_pages", "like_times"]
	return(four_week_df["like_pages"])



def sql_table_2months(cursor, start_date,  end_date, current_month, next_month, bootstrap_p, b_seed):
	sql_command_list = ["SELECT  user_id, "
	," GROUP_CONCAT(page_id) as like_pages,"
	," CAST(GROUP_CONCAT(like_time) AS CHAR CHARACTER SET utf8)AS like_times "
	," FROM ("
	,   "SELECT user_id, SUBSTRING_INDEX(post_id,'_',1) as page_id, count(*) AS like_time "
	,   " FROM ( "
	,       " SELECT *"
	,       " FROM("
	,       " ( "
	,       	" SELECT user_id, post_id"
	,           " FROM `politician_",current_month
	,			"` WHERE post_created_date_CT >= '", start_date
	,            "' AND RAND(", b_seed, ")<= " ,bootstrap_p
	,           ") "
	,       " UNION ALL"
	,           " (SELECT user_id, post_id"
	,           " FROM `politician_",next_month
	,			"` WHERE post_created_date_CT <= '", end_date
	,            "' AND RAND(",b_seed ,")<= " ,bootstrap_p
	,           " )"
	,       ") AS union_t1"
	,   " UNION ALL("
	,       " SELECT *"
	,       " FROM("
	,           "(SELECT user_id, post_id"
	,           " FROM `1000_page_",current_month
	,			"` WHERE post_created_date_CT >= '", start_date
	,           "' AND RAND(", b_seed,")<= " ,bootstrap_p
	,           ")"
	,       " UNION ALL"
	,           "(SELECT user_id, post_id "
	,           "FROM `1000_page_",next_month
	,			"` WHERE post_created_date_CT <= '", end_date
	,            "' AND RAND(", b_seed, ")<= " ,bootstrap_p
	,           ")"
	,        ") AS union_t2"
	,   ")"
	,   ") AS temp"
	,   " GROUP BY  user_id,  page_id  ) as temp2"
	," GROUP BY user_id" ] 

	sql_command_list = ''.join(str(word) for word in sql_command_list)
	cursor.execute(sql_command_list)
	four_week = cursor.fetchall()
	four_week_df = pd.DataFrame(list(four_week))
	four_week_df.columns = ["user_id", "like_pages", "like_times"]
	return(four_week_df["like_pages"])

def user_like_page_to_page_page_matrix(like_pages_pd_column):
	page_page_dict = {}
	for row in like_pages_pd_column :
		pageid_list = row.split(',')
		for j, p in enumerate(pageid_list):
			if p not in page_page_dict:
				page_page_dict[p] = {}
			for k, p1 in enumerate(pageid_list):
				if k < j:
					continue
				elif k == j:
					page_page_dict[p][p] = page_page_dict[p].get(p,0) + 1
				else:
					if p1 not in page_page_dict:
						page_page_dict[p1] = {}
					page_page_dict[p][p1] = page_page_dict[p].get(p1,0) + 1
					page_page_dict[p1][p] = page_page_dict[p1].get(p,0) + 1
	
	sorted_dict_keys = sorted(page_page_dict.keys())
	page_page_df = pd.DataFrame(index = sorted_dict_keys, columns = sorted_dict_keys)

	for i in sorted(page_page_dict.keys()):    
		for j in sorted(page_page_dict[i].keys()):
			page_page_df[i][j] = page_page_dict[i][j]

	page_page_df= page_page_df.fillna(0) 

	return(page_page_df)



def page_page_matrix_to_page_score(page_page_dataframe,
								  clinton_on_the_left = False ):
	df = page_page_dataframe
	A = df.values
	id_used = list(map(int , df.columns.values))
	matrix_size = len(df.columns)
	G = np.zeros((matrix_size, matrix_size)) 
	for i in range(0, matrix_size):
		for j in range(0, matrix_size):
			G[i,j] = A[i,j] / A[i,i]

	G_std = StandardScaler().fit_transform(G)
	pca = sklearnPCA(n_components = 2)
	P_PCA = pca.fit_transform(G_std)
	P_PCA_std = StandardScaler().fit_transform(P_PCA)
	SVD_df = pd.DataFrame({"page_id": id_used,
						 "PC1": P_PCA[:, 0], 
						 #"PC2": P_PCA[:, 1],
						 "PC1_std": P_PCA_std[:, 0]})
						 #"PC2_std": P_PCA_std[:, 1]})
	# Ensure the liberal's have negative ideology score by checking Clinton's.
	if(clinton_on_the_left == True ):
		clinton_index = SVD_df.index[SVD_df["page_id"] 
										== 889307941125736].tolist()[0]
		if(SVD_df["PC1"][clinton_index] > 0):
			SVD_df["PC1"] = -SVD_df["PC1"]
			SVD_df["PC1_std"] = -SVD_df["PC1_std"]
	return(SVD_df)

def compute_and_write_page_score(like_pages_pd_column, write_path, iteration):
	page_page_df = user_like_page_to_page_page_matrix(like_pages_pd_column)
	page_score_df = page_page_matrix_to_page_score(page_page_df, True)
	page_score_df.to_csv(write_path + "bootstrap_" + str(iteration) + ".csv" ,
						columns = ["page_id", "PC1_std"],
						index = False )



def date_char(date, tt):
	if tt == "d":
		return(str(datetime.strftime(date, "%Y-%m-%d")))
	elif tt == "m":
		return(str(datetime.strftime(date, "%Y-%m")))



def extract_table(cursor,
				start_date, 
				final_day,
				duration, 
				forward_days, 
				saving_path,
				b_times,
				bootstrap_p):

	cursor.execute("set group_concat_max_len = 1000000000;")
	start_date =  datetime.strptime(start_date, "%Y-%m-%d")
	end_date =  start_date + timedelta(days = duration)
	final_day = datetime.strptime(final_day, "%Y-%m-%d")
	current_month =  date_char(start_date, "m")

	while(end_date <= final_day):
		print("start:",start_date,"to",end_date, "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
		current_month_firstday =  current_month + "-01"
		current_month_firstday = datetime.strptime(current_month_firstday, "%Y-%m-%d")
		saving_path = saving_path + date_char(start_date, "d") +"_to_" +  date_char(end_date, "d") + "/"
		if not os.path.exists(saving_path):
			os.makedirs(saving_path)
		if( end_date.strftime("%Y-%m") > start_date.strftime("%Y-%m") ):
			if( start_date.strftime("%Y-%m") > current_month_firstday.strftime("%Y-%m") ):
				current_month =  datetime.strftime(start_date, "%Y-%m")
				print("new month", current_month)
				for i in range(4, b_times):
					week_table = sql_table(cursor, date_char(start_date, "d"),  date_char(end_date, "d"), current_month, bootstrap_p, i)
					compute_and_write_page_score(week_table, saving_path, i)
					print("done:",date_char(start_date, "d"),"to",date_char(end_date, "d"), i, "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
			
			else:
				print("front month", current_month)
				next_month =  end_date.strftime("%Y-%m")
				for i in range(4, b_times):
				  week_table =  sql_table_2months(cursor, date_char(start_date, "d"),  date_char(end_date, "d"), current_month, next_month, bootstrap_p, i)
				  compute_and_write_page_score(week_table, saving_path, i)
				  print("done:",date_char(start_date, "d"),"to",date_char(end_date, "d"), i, "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))				  
				print("back month", next_month)
		else:
			for i in range(4, b_times):
				week_table = sql_table(cursor, date_char(start_date, "d"),  date_char(end_date, "d"), current_month, bootstrap_p, i)
				compute_and_write_page_score(week_table, saving_path, i)
				print("done:",date_char(start_date, "d"),"to",date_char(end_date, "d"), i, "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
		  
		start_date = start_date + timedelta(days = forward_days)
		end_date = end_date + timedelta(days = forward_days)



def main():
	db = pymysql.connect(host = 'localhost', user ='root',
					   passwd = 'ntueconfb', db = '1000_page_us_user_like_post')
	cursor = db.cursor()
	start_date = "2015-09-06"
	final_day = "2015-10-04"
	duration = 27
	forward_days = 7
	saving_path = "/home3/usfb/analysis/analysis-prediction/temp/bootstrap_by_like/page_score_1%_200times_raw/"
	b_times = 200
	bootstrap_p = 0.05
	extract_table(cursor,
				start_date, 
				final_day, 
				duration, 
				forward_days, 
				saving_path,
				b_times,
				bootstrap_p)



if __name__ == '__main__':
	main()
