import csv
import string
import pandas as pd
from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import snowball

f_corpus= open("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/my_corpus_all.csv", "r")
my_corpus= f_corpus.readline()
my_corpus= my_corpus.split(',')

#print(my_corpus[10])

fbPost_tokenize= pd.read_csv("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/fbPost_tokenize_all.csv",
							 usecols= ["post_id", "tokenized_post"], converters= {"post_id": str, "tokenized_post":str})
print("done read fb tokens ", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))

post_id_list= fbPost_tokenize["post_id"].tolist()
tokenized_post_list= fbPost_tokenize["tokenized_post"].tolist()

tokenized_post_list[1]

fact_check_tokenize= pd.read_csv("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/fact_check_tokenize_all.csv",
							 usecols= ["fact_check_id", "tokenized_fact_check"], converters= {"fact_check_id":str, "tokenized_fact_check":str})

print("done read fact check tokens ", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))


fact_check_id_list= fact_check_tokenize["fact_check_id"].tolist()
tokenized_fact_check_list= fact_check_tokenize['tokenized_fact_check'].tolist()

#print(len(post_id_list))

#print(tokenized_fact_check_list[1])

from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn

vectorizer = TfidfVectorizer()
vectorized_train= vectorizer.fit_transform(my_corpus)

vectorized_post= vectorizer.transform(tokenized_post_list )

vectorized_fact= vectorizer.transform(tokenized_fact_check_list )

result= sklearn.metrics.pairwise.cosine_similarity( vectorized_post, vectorized_fact)
print("Done sparse matrixs, having rows:", len(result[:,0]), datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))


fbPost = pd.read_csv(r"/home3/ntueconfbra1/Desktop/Link to usfb-data/1000_page_post/20150101_to_20170408_all.csv", 
							usecols = ['page_id','page_name','post_id','post_name','post_message', 'post_likes', 'post_created_time_CT' ], 
							converters = {'post_name':str, 'post_message': str})

fake_news_data= pd.read_csv(r"/home3/fb/US/KC-CH/fromRA1/fake_news/politifact2_utf8_with_ID.csv", 
							usecols = ['fact_check_id','title','claim', 'rating', 'date'] ,
							converters = {'title': str, 'claim':str, 'rating':str})

print("Done read files ",datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))
#post_date = datetime.strptime(fbPost['post_created_time_CT'][i], '%Y-%m-%d' )

output_file = open("/home3/fb/US/KC-CH/fromRA1/fake_news/fake_news_discussing_posts_byCorpus_try.csv", "w", encoding='utf-8')
headers =["page_id", "post_id", "page_name", "post_name", "post_message", "post_likes",
			 "post_time","tf-idf","fact_check_id", "fact_check_title", "fact_check_claim", "fact_check_time"]
w= csv.DictWriter(output_file, fieldnames= headers)
w.writeheader()

for i in range(0, len(result[:,0])):
	for j in range(0, len(result[0])):
		if(result[i][j] > 0.5):
			if(fake_news_data["rating"][j]== "False" or fake_news_data["rating"][j]== "Pants on Fire!"):
				#post_date = datetime.strptime(fbPost['post_created_time_CT'][i], '%Y-%m-%d %H:%M:%S' )
				post_date = datetime.strptime(fbPost['post_created_time_CT'][i][0:10], '%Y-%m-%d')                
				fact_check_date = fake_news_data['date'][j]
				temp = fact_check_date.split(', ')
				fact_check_date2= datetime.strptime(" ".join([temp[2][0:4], temp[1][0:-2]]), '%Y %B %d')
				date_diff= post_date- fact_check_date2
				if(abs(date_diff.days) <= 30):
                
					w.writerow(
						{
							"page_id": fbPost["page_id"][i], 
							"post_id":fbPost["post_id"][i], 
							"page_name":fbPost["page_name"][i], 
							"post_name":fbPost["post_name"][i], 
							"post_message":fbPost["post_message"][i], 
							"post_likes": fbPost["post_likes"][i], 
							"post_time": fbPost["post_created_time_CT"][i],
							"tf-idf":result[i][j], 
							"fact_check_id": fake_news_data['fact_check_id'][j],
							"fact_check_title": fake_news_data["title"][j], 
							"fact_check_claim":fake_news_data["claim"][j], 
							"fact_check_time":fake_news_data["date"][j]
							}
					)
	print("done ", i ,"rows in total ", len(result[:,0]), "rows")
output_file.close()



