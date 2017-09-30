library("Rfacebook")
library("dbConnect")
library("RMySQL")
library("dplyr")
library("data.table")
library("lubridate")


#input_file_path = "/home3/ntueconfbra1/Link to fromRA1/Extract_FB_data/output_files/like_post_data/"
#output_file_path = "/home3/ntueconfbra1/Link to fromRA1/Extract_FB_data/output_files/others/"
#MySQL_user = "root"
#MySQL_password = ******
#dbname = "try_Facebook_API"



build_tables_in_MySQL = function(input_file_path, output_file_path, 
                                 MySQL_user, MySQL_password, dbname){
  
  file_dir = input_file_path
  file_list_name = list.files(file_dir)
  file_list = as.Date(list.files(file_dir))
  year_month_vec = format(file_list, format = "%Y-%m")
  
  con = dbConnect(MySQL(), user = MySQL_user, password = MySQL_password, dbname = dbname, host='localhost')
  exist_tables = dbGetQuery(con, "show tables;")
  if(is.na(exist_tables[1,1])){
    print("Your database is currently empty")
  }else{
    print(paste("Tables in your database:", exist_tables))
  }
  
  loop_month_index = 1
  
  for(i in 1:length(file_list)){
    if(i==1){
      year_month= paste("`",year_month_vec[loop_month_index], "`", sep="")
      dbGetQuery(con, paste("create table", year_month, "(user_id varchar(20), post_id varchar(41), post_created_date_CT varchar(10));"))
    }else if(year(file_list[i]) > year(file_list[i-1]) | month(file_list[i]) > month(file_list[i-1])){
      loop_month_index= loop_month_index+1
      year_month= paste("`",year_month_vec[loop_month_index], "`", sep="")
      dbGetQuery(con, paste("create table", year_month, "(user_id varchar(20), post_id varchar(41), post_created_date_CT varchar(10));"))
  
    }
  
    
    like_date<- fread(paste(file_dir, file_list_name[i], sep =""), select =c("user_id", "post_id"), sep=",", header = T, colClasses = c("user_id" = "character", "post_id"="character"))
    names(like_date)<- c("user_id", "post_id")
    like_date<- like_date %>% group_by(user_id, post_id)%>%summarize()
    
    like_date<- as.data.frame(like_date, row.names = NULL)
    like_date<- cbind(like_date, rep(as.character(file_list[i]), length(like_date[,1])))
    names(like_date)<- c("user_id", "post_id", "post_created_date_CT")
    fwrite(like_date, paste(output_file_path, "temp", sep=""), sep=",", eol="\n", row.names=F)
    like_date_table<- paste("'", output_file_path, "/temp'", sep="")
    
    dbGetQuery(con, paste("load data local infile", like_date_table, "ignore into table", year_month, "fields terminated by ',' lines terminated by '\n' ignore 1 lines ;"))
  
    print(paste("done:", file_list[i]))
  }
}
