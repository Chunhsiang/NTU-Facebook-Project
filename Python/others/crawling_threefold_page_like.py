import facebook
import pandas as pd
import os
from tqdm import *
token = "EAACEdEose0cBAKTlzFnv6LDEZBIB9r0IZAA8azBEYH8aSpWYblXGmHNQbTxYPwZCAYm89WWWsObLGEnZAigI7Bq3DNt0mY3YMpwlCJCEGK005udRzKZBPwhVCOWyY7azGeUknsm93ZAQGk8AKPerHizuPa96W3dVLgu69T9NYZAIref3K1clZCkq7XM13VI8sHj4JFOQrdqBnwZDZD"
graph = facebook.GraphAPI(access_token= token)
#page_like = graph.get_connections('326683984410', connection_name = "likes", limit = 1000)
#print(page_like)
Russia_pages = {'RT': '326683984410', 
                'RT America': '137767151365', 
                'WikiLeaks Updates': '181961455147909', 
                'WikiLeaksParty': '382548655176036'}


def write_pages_liked(output_file):
	count = 0
	for first_fold_iter in Russia_pages.keys():
		first_fold_id = Russia_pages[first_fold_iter]
		pages_liked_1 = graph.get_connections(first_fold_id,
											 connection_name = "likes", 
											 limit = 1000000
											 )['data']

		pages_liked_1_df = pd.DataFrame(pages_liked_1)
		pages_liked_1_df = pages_liked_1_df.rename( 
												columns = {"id":"page_id",
													    "name":"page_name"})
		output_path = (output_file + first_fold_id + ".csv")
		#output_path = (output_file + first_fold_id + "_" + 
		#				first_fold_iter + ".csv")	

		pages_liked_1_df.to_csv(output_path, index = False)

		for second_fold_iter in tqdm(range(0, len(pages_liked_1_df["page_id"]))):
			output_path = (output_file + 
							pages_liked_1_df["page_id"][second_fold_iter] + 
							".csv")			

			#output_path = (output_file + 
			#				pages_liked_1_df["page_id"][second_fold_iter] + 
			#				"_" + 
			#				pages_liked_1_df["page_name"][second_fold_iter] + 
			#				".csv")
			second_fold_id = pages_liked_1_df["page_id"][second_fold_iter]
			pages_liked_2 = graph.get_connections(second_fold_id,
											 connection_name = "likes", 
											 limit = 1000000
											 )['data']
			if(pages_liked_2!= []):
				pages_liked_2_df = pd.DataFrame(pages_liked_2)
				pages_liked_2_df = pages_liked_2_df.rename( 
													columns = {"id":"page_id",
														    "name":"page_name"})
				if(os.path.isfile(output_path) == False):
					pages_liked_2_df.to_csv(output_path, index = False)

				for third_fold_iter in range(0, len(pages_liked_2_df["page_id"])):
					output_path = (output_file + 
									pages_liked_2_df["page_id"][third_fold_iter] + 
									".csv")
					#output_path = (output_file + 
					#				pages_liked_2_df["page_id"][third_fold_iter] + 
					#				"_" + 
					#				pages_liked_2_df["page_name"][third_fold_iter] + 
					#				".csv")					
					third_fold_id =  pages_liked_2_df["page_id"][third_fold_iter]
					pages_liked_3 = graph.get_connections(third_fold_id,
													 connection_name = "likes", 
													 limit = 1000000
													 )['data']
					if(pages_liked_3!= []):
						pages_liked_3_df = pd.DataFrame(pages_liked_3)
						pages_liked_3_df = pages_liked_3_df.rename( 
															columns = {"id":"page_id",
																    "name":"page_name"})
						if(os.path.isfile(output_path) == False):
							pages_liked_3_df.to_csv(output_path, index = False)		
		count += 1		
		print("done ", count ," over ", len(Russia_pages.keys()), " pages" )

def main():
	write_pages_liked("/home3/ntueconfbra1/Link to fromRA1/Russia/threefold_page_like/")

if __name__ == '__main__':
	main()

	
