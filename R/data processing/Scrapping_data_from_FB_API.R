library("Rfacebook")
library("dbConnect")
library("RMySQL")
library("dplyr")
library("data.table")
library("lubridate")

#page_list = c(889307941125736, 153080620724, 6815841748)
#starting_date = "2016-09-01"
#ending_date = "2016-10-08"
#token = "EAASdh1QTPOkBAK1DctVIGO0nFJm3ikMO5zFJEP3jxF8ZB46lbSVajAmm4ZB1xWuqiwc6HR9kklBd0jLc1vji2f8t"
#output_file_path = "/home3/ntueconfbra1/Link to fromRA1/Extract_FB_data/output_files/like_post_data/"

write_user_page_data = function(page_list, starting_date, ending_date, token, output_file_path){
  write_list = list()
  for( page_iter in 1:length(page_list)){
    page_info = getPage(page_list[page_iter], token, n= 10^20, since = starting_date, until = ending_date, reactions = F)
    
    for( post_iter in length(page_info[,1]):1){
      post_id = page_info$id[post_iter]
      post_time = as.character(as.Date(page_info$created_time[post_iter], "%Y-%m-%d"))
      write_list[[post_time]][[post_id]] =  getPost(post_id, token, n = 10^20 , comments = F)[["likes"]]$from_id
      print(paste("done",(length(page_info[,1]) - post_iter), "in total posts of", length(page_info[,1])))
    }
  }
  
  for( date_iter in 1:length(write_list)){
    date = names(write_list)[date_iter]
    for( post_iter in 1:length(write_list[[date_iter]])){
      post_id = names(write_list[[date_iter]])[[post_iter]]
      output_name = paste(output_file_path, date, ".csv", sep="")
      row_num = length(write_list[[date_iter]][[post_iter]])
      fwrite(data.table("user_id" = write_list[[date_iter]][[post_iter]], 
                        "post_id" =  rep(post_id, row_num), 
                        "post_created_date" = rep(date), row_num),
             output_name,
             append = T)
    }
  }
