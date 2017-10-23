import pandas as pd


sentiment = pd.read_csv("/home3/ntueconfbra1/Desktop/Link to fromRA1/sentiment_analysis/20150101_to_20170408_1000_post_sentiment.csv",
						usecols =  ["post_id", "compound", "neg", "neu", "pos"])
fbPost = pd.read_csv("/home3/ntueconfbra1/Desktop/Link to usfb-data/1000_page_post/20150101_to_20170408_all.csv",
    					usecols = ['post_id', 'page_id','page_name', 'post_created_date_CT'])
merged_data = pd.merge(fbPost, sentiment, on = "post_id", how = "inner")
merged_data.to_csv("/home3/ntueconfbra1/Desktop/Link to fromRA1/sentiment_analysis/plot_sentiment_data.csv",
					index = False)
