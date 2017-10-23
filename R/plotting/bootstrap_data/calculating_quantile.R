library(magrittr)
whole_folder_dir = "/home3/ntueconfbra1/Desktop/Link to fromRA1/ideology_scores_by_4_weeks/bootstrap/page_score_1%_200times_raw"
date_folder_list= list.files(whole_folder_dir, full.names = TRUE)
for( i in 1:length(date_folder_list)){
  #date_folder = paste(whole_folder_dir, date_file_list[i], sep="/")
  bootstrap_file_list = list.files(date_folder_list[i], full.names = TRUE)
  #bootstrap_path_list = 
  df = read_csv(bootstrap_file_list[1],
                col_types  = cols(page_id = col_character(), PC1_std = col_double()))
  for( j in 2:length(bootstrap_file_list)){
    temp = read_csv(bootstrap_file_list[j],
                    col_types  = cols(page_id = col_character(), PC1_std = col_double()))
    df = merge(df, temp, by="page_id", all =T, suffixes = c(j-1,j))
  }
  date_list = list.files(whole_folder_dir, full.names = FALSE)
  write_csv(df, paste("/home3/ntueconfbra1/Desktop/Link to fromRA1/ideology_scores_by_4_weeks/bootstrap/page_score_1%_200times_combined/all/",
                      date_list[i], ".csv", sep="") )
  percentile_97.5 = c(rep(0, length(df[,1])))
  percentile_2.5 = c(rep(0, length(df[,1])))
  for( k in 1:length(df[,1])){
    sorted_row = sort(df[k,-1])
    percentile_97.5[k] = sorted_row[1, round(0.975*length(sorted_row))]
    percentile_2.5[k] = sorted_row[1, round(0.025*length(sorted_row))+1]
  }
  
  df_percentile = data.frame(df$page_id, percentile_2.5, percentile_97.5)
  write_csv(df_percentile, paste("/home3/ntueconfbra1/Desktop/Link to fromRA1/ideology_scores_by_4_weeks/bootstrap/page_score_1%_200times_combined/percentile/",
                      date_list[i], ".csv", sep="") )
  print(paste("done", date_list[i]))
}









#for (i in length(files)) {
#  temp = read_csv()
#  df = merge(df, temp, by="page_id")
#}
#summary = df %>% 
#  group_by(page_id) #%>% 
  #summarise(df, quantile_2.5=quantile(prob = 0.025),
  #          quantile_97.5=quantile(prob =  0.975))

#see = summarise(baseball,
 #         duration = max(year) - min(year),
  #        nteams = length(unique(team)))

