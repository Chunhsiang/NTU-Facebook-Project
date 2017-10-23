import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import wordpunct_tokenize
from tqdm import *
import os

def calculating_sentiment_score(post_data_path, output_file, 
                                from_percentage = 0, to_percentage = 1.0):

    sid = SentimentIntensityAnalyzer()
    fbPost = pd.read_csv(post_data_path , 
    					usecols = ['post_id','post_name','post_message'], 
                        dtype = {'post_id':str, 'post_name':str, 
                                'post_message': str})
    file_total_lines = len(fbPost['post_id'])
    if(from_percentage == 0):
        start_row = 0    
    else:
        start_row = int(from_percentage * file_total_lines)
    if(to_percentage == 1.0):
        end_row = file_total_lines
    else:
        end_row  = int(to_percentage * file_total_lines)

    fbPost_sentiment = pd.DataFrame(columns = 
                                    ['post_id','compound', 'neg', 'neu', 'pos'])
    print("Sentiment score calculation start from row: ", start_row, 
        " to ", end_row)
    post_score_dict ={}
    for iter_post in tqdm(range(start_row, end_row)):
        analyzed_string = ""
        if ( fbPost['post_name'][iter_post] != "Timeline Photos" 
            and type(fbPost['post_name'][iter_post]) != float):
            analyzed_string += fbPost['post_name'][iter_post]
        if (type(fbPost['post_message'][iter_post]) != float ):
            analyzed_string += fbPost['post_message'][iter_post]
        sentiment_score_dict = sid.polarity_scores(analyzed_string)
        this_id = fbPost['post_id'][iter_post]
        post_score_dict[this_id] = sentiment_score_dict

        #sentiment_score_dict['post_id'] = fbPost['post_id'][iter_post]
        #fbPost_sentiment['post_id'].loc[iter_post] = fbPost['post_id'][iter_post]
        #fbPost_sentiment['compound'].loc[iter_post] = sentiment_score_dict['compound']
        #fbPost_sentiment['neg'].loc[iter_post] = sentiment_score_dict['neg']
        #fbPost_sentiment['neu'].loc[iter_post] = sentiment_score_dict['neu']
        #fbPost_sentiment['pos'].loc[iter_post] = sentiment_score_dict['pos']
    post_score_df = pd.DataFrame.from_dict(post_score_dict, orient = 'index')
    post_score_df['post_id'] = post_score_df.index
    post_score_df = pd.merge(post_score_df, fbPost, on = "post_id", how = "inner")

    if(from_percentage != 0):
        post_score_df.to_csv(output_file, mode = 'a', header = False,
                            index = False,  columns = ["post_id", "neg",
                                                    "neu","pos", 
                                                    "compound","post_name",
                                                    "post_message"])
    else:
        post_score_df.to_csv(output_file, mode = 'w', header = True, 
                            index = False,  columns = ["post_id", "neg",
                                                    "neu","pos", 
                                                    "compound","post_name",
                                                    "post_message"])


def main():
    post_data_path = "/home3/ntueconfbra1/Desktop/Link to usfb-data/1000_page_post/20150101_to_20170408_all.csv"
    output_file = "/home3/ntueconfbra1/Desktop/Link to fromRA1/sentiment_analysis/20150101_to_20170408_1000_post_sentiment.csv"
    #row_num = get_num_lines(post_data_path)
    calculating_sentiment_score(post_data_path, output_file, from_percentage = 5/6, to_percentage = 6/6 )



if __name__ == '__main__':
    main()
