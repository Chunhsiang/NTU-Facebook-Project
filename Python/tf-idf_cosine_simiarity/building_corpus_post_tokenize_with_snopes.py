import csv
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from nltk.stem import snowball
from datetime import datetime


snopes= pd.read_csv(r"/home3/ntueconfbra1/Link to fromRA1/fake_news/corpuses_and_tokens/snopes/snopes_all_used.csv", 
							usecols = ['snopes_id','title','claim'] ,
							converters = {'title': str, 'claim':str})


print("Done reading file")

stop_words = set(stopwords.words('english'))

stop_words.update(['.', ',', '"', "'",'\u2018','\u2019', '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','#','--->','$','&','-','/','http','/#','://'])

punctuations = str.maketrans(dict.fromkeys(string.punctuation))

stem_En= snowball.EnglishStemmer()

corpus_dict= {}
fbPost_list=[]
snopes_list=[]
iter_count= 0


import nltk
En_words = set(nltk.corpus.words.words())


for iter_snopes in range(0, len(snopes['snopes_id'] ) ):
	snopes_string=""
	temp = snopes['title'][iter_snopes]+ snopes['claim'][iter_snopes]
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
			in_string= " "+word
			snopes_string+= in_string
			if(stemmed_word not in corpus_dict):
				corpus_dict[word] = True
    
	
	snopes_list.append(snopes_string)
	print("Fact check! done row: ", iter_snopes, " in total ",  len(snopes['snopes_id'] ), "rows")



fbPost_tokenize= pd.read_csv("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/fbPost_tokenize_all.csv",
							 usecols= ["tokenized_post"], converters= {"tokenized_post":str})

post_tokenized_list= fbPost_tokenize["tokenized_post"].tolist()
for i in range(0, len(post_tokenized_list)):
	temp_list= post_tokenized_list[i].split(" ")
	for j in temp_list:
		if(j not in corpus_dict):
			corpus_dict[j]= True
	print("Include Post tokens! done row: ", i, " in total ",  len(post_tokenized_list), "rows")

print("Done include fb tokens ", datetime.now().strftime("%Y-%m-%d %H:%M:%S" ))


f = open("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/snopes/my_corpus_all.csv", "w")
w_corpus = csv.writer(f)

w_corpus.writerow(corpus_dict.keys())


f_fact= open("/home3/fb/US/KC-CH/fromRA1/fake_news/corpuses_and_tokens/snopes/snopes_tokenize_all.csv", "w")
fact_headers =["snopes_id", "tokenized_snopes"]
w_fact = csv.DictWriter(f_fact, fieldnames=fact_headers)
w_fact.writeheader()


for_write_iter=0
for i in snopes["snopes_id"]:
	w_fact.writerow({"snopes_id":i, "tokenized_snopes": snopes_list[for_write_iter]})
	for_write_iter+=1