import csv
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import snowball


#fbPost = pd.read_csv(r"/home3/ntueconfbra1/Desktop/Link to usfb-data/politician_post/201501-201611.csv", 
#						usecols = ['post_id','post_name','post_message'], converters = {'post_name':str, 'post_message': str})
fbPost = pd.read_csv(r"/home3/ntueconfbra1/Desktop/Link to usfb-data/1000_page_post/20150101_to_20170408_all.csv", 
						usecols = ['post_id','post_name','post_message'], converters = {'post_name':str, 'post_message': str})

fact_check= pd.read_csv(r"/home3/fb/US/KC-CH/fromRA1/fake_news/politifact2_utf8_with_ID.csv", 
							usecols = ['fact_check_id','title','claim'] ,
							converters = {'title': str, 'claim':str})

print("Done reading file")

stop_words = set(stopwords.words('english'))

stop_words.update(['.', ',', '"', "'",'\u2018','\u2019', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','#','--->','$','&','-','/','http','/#','://'])

punctuations = str.maketrans(dict.fromkeys(string.punctuation))

stem_En= snowball.EnglishStemmer()

corpus_dict= {}
#fbPost_token_dict={}
#fact_check_token_dict={}
fbPost_list=[]
fact_check_list=[]
iter_count= 0

import nltk
En_words = set(nltk.corpus.words.words())

for iter_post in range(0, len(fbPost ['post_id'] ) ):
	#post_tokenized_list=[]
	post_tokenize_string=""
	temp = fbPost['post_name'][iter_post]+ fbPost['post_message'][iter_post]
	lowers= temp.lower()
	no_punctuation= lowers.translate(punctuations)
	tokens= wordpunct_tokenize(no_punctuation)
	for word in tokens:        
		if(word.startswith("http")):
			continue
		if(word not in En_words):
			continue
		if(word not in stop_words):
			stemmed_word = stem_En.stem(word)
			#post_tokenized_list.append(word)
			in_string= " "+word
			post_tokenize_string+= in_string
			if(stemmed_word not in corpus_dict):
				corpus_dict[word] = True
    
	#fbPost_token_dict[fbPost['post_id'][iter_post]] = post_tokenized_list
	fbPost_list.append(post_tokenize_string)
	print("Posts done row: ", iter_post, " in total ",  len(fbPost['post_name'] ), "rows")

for iter_fact_check in range(0, len(fact_check['fact_check_id'] ) ):
	#fact_check_tokenized_list=[]
	fact_check_string=""
	temp = fact_check['title'][iter_fact_check]+ fact_check['claim'][iter_fact_check]
	lowers= temp.lower()
	no_punctuation= lowers.translate(punctuations)
	tokens= wordpunct_tokenize(no_punctuation)
	for word in tokens:        
		if(word.startswith("http")):
			continue
		if(word not in En_words):
			continue
		if(word not in stop_words):
			stemmed_word = stem_En.stem(word)
			#fact_check_tokenized_list.append(word)
			in_string= " "+word
			fact_check_string+= in_string
			if(stemmed_word not in corpus_dict):
				corpus_dict[word] = True
    
	
	#fact_check_token_dict[fact_check['fact_check_id'][iter_fact_check]] = fact_check_tokenized_list
	fact_check_list.append(fact_check_string)
	print("Fact check! done row: ", iter_fact_check, " in total ",  len(fact_check['fact_check_id'] ), "rows")

f = open("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/my_corpus_all.csv", "w")
w_corpus = csv.writer(f)

len(corpus_dict.keys())

w_corpus.writerow(corpus_dict.keys())

f_fb= open("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/fbPost_tokenize_all.csv", "w")
fb_headers =["post_id", "tokenized_post"]
w_fb = csv.DictWriter(f_fb, fieldnames=fb_headers)
w_fb.writeheader()
#for i in fbPost_token_dict.keys():
#    w_fb.writerow({"post_id": i, "tokenized_post": fbPost_token_dict[i]})
for_write_iter=0
for i in fbPost["post_id"]:
	w_fb.writerow({"post_id": i, "tokenized_post": fbPost_list[for_write_iter] })
	for_write_iter+=1

f_fact= open("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/fact_check_tokenize_all.csv", "w")
fact_headers =["fact_check_id", "tokenized_fact_check"]
w_fact = csv.DictWriter(f_fact, fieldnames=fact_headers)
w_fact.writeheader()

#for i in fact_check_token_dict.keys():
#    w_fact.writerow({"fact_check_id":i, "tokenized_fact_check": fact_check_token_dict[i]})
for_write_iter=0
for i in fact_check["fact_check_id"]:
	w_fact.writerow({"fact_check_id":i, "tokenized_fact_check": fact_check_list[for_write_iter]})
	for_write_iter+=1