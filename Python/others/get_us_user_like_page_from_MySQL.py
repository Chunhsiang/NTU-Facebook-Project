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




def sql_table(cursor, start_date,  end_date, current_month):
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
	,        "' )"
	,   "UNION ALL( "
	,     "SELECT user_id, post_id " 
	,     "FROM `1000_page_" , current_month
	,     "`WHERE post_created_date_CT >= '" , start_date 
	,     "' AND post_created_date_CT <= '" , end_date
	,        "' )"
	,    ") AS temp "
	,    "GROUP BY  user_id,  page_id  ) as temp2 "
	,  "GROUP BY user_id"] 

	sql_command_list = ''.join(str(word) for word in sql_command_list)
	cursor.execute(sql_command_list)
	four_week = cursor.fetchall()
	four_week_df = pd.DataFrame(list(four_week))
	four_week_df.columns = ["user_id", "like_pages", "like_times"]
	return(four_week_df)



def sql_table_2months(cursor, start_date,  end_date, current_month, next_month):
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
	,           "' ) "
	,       " UNION ALL"
	,           " (SELECT user_id, post_id"
	,           " FROM `politician_",next_month
	,			"` WHERE post_created_date_CT <= '", end_date
	,           "' )"
	,       ") AS union_t1"
	,   " UNION ALL("
	,       " SELECT *"
	,       " FROM("
	,           "(SELECT user_id, post_id"
	,           " FROM `1000_page_",current_month
	,			"` WHERE post_created_date_CT >= '", start_date
	,           "' )"
	,       " UNION ALL"
	,           "(SELECT user_id, post_id "
	,           "FROM `1000_page_",next_month
	,			"` WHERE post_created_date_CT <= '", end_date
	,           "' )"
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
	return(four_week_df)



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
				saving_path):

	cursor.execute("set group_concat_max_len = 1000000000;")
	start_date =  datetime.strptime(start_date, "%Y-%m-%d")
	end_date =  start_date + timedelta(days = duration)
	final_day = datetime.strptime(final_day, "%Y-%m-%d")
	current_month =  date_char(start_date, "m")

	while(end_date <= final_day):
		print("start:",start_date,"to",end_date, "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
		current_month_firstday =  current_month + "-01"
		current_month_firstday = datetime.strptime(current_month_firstday, "%Y-%m-%d")
		write_path = saving_path + "us_user_like_page" + date_char(start_date, "d") + "_to_" + date_char(end_date, "d")
		if( end_date.strftime("%Y-%m") > start_date.strftime("%Y-%m") ):
			if( start_date.strftime("%Y-%m") > current_month_firstday.strftime("%Y-%m") ):
				current_month =  datetime.strftime(start_date, "%Y-%m")
				print("new month", current_month)
				week_table = sql_table(cursor, date_char(start_date, "d"),  date_char(end_date, "d"), current_month)
				week_table.to_csv(write_path, index = False)
				print("done:",date_char(start_date, "d"),"to",date_char(end_date, "d"), "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
			
			else:
				print("front month", current_month)
				next_month =  end_date.strftime("%Y-%m")
				week_table =  sql_table_2months(cursor, date_char(start_date, "d"),  date_char(end_date, "d"), current_month, next_month)
				week_table.to_csv(write_path, index = False)
				print("done:",date_char(start_date, "d"),"to",date_char(end_date, "d"),  "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))				  
				print("back month", next_month)
		else:
			week_table = sql_table(cursor, date_char(start_date, "d"),  date_char(end_date, "d"), current_month)
			week_table.to_csv(write_path, index = False)
			print("done:",date_char(start_date, "d"),"to",date_char(end_date, "d"), "at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
		  
		start_date = start_date + timedelta(days = forward_days)
		end_date = end_date + timedelta(days = forward_days)



def main():
	db = pymysql.connect(host = 'localhost', user ='root',
					   passwd = '********', db = '1000_page_us_user_like_post')
	cursor = db.cursor()
	start_date = "2015-09-06"
	final_day = "2015-10-04"
	duration = 27
	forward_days = 7
	saving_path = "/home3/usfb/analysis/analysis-prediction/temp/us_user_like/try_python/"
	extract_table(cursor,
				start_date, 
				final_day, 
				duration, 
				forward_days, 
				saving_path)



if __name__ == '__main__':
	main()
