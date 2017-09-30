library("Rfacebook")
library("dbConnect")
library("RMySQL")
library("dplyr")
library("data.table")
library("lubridate")

last_date_of_the_month<- function(in_date){
  in_month<- month(in_date)
  run_date<- in_date
  while(month(run_date) == in_month){
    run_date= run_date+1
  }
  return(run_date-1)
}

sql_table<- function(con, current_month, start_date, end_date){
  testweek_union<- dbGetQuery(con, 
                              paste("SELECT  user_id,  GROUP_CONCAT(page_id) as like_pages, GROUP_CONCAT(like_time) AS like_times
                                      FROM (
                                        SELECT user_id, SUBSTRING_INDEX(post_id,'_',1) as page_id, count(*) AS like_time
                                          FROM ( 
                                            SELECT user_id, post_id 
                                              FROM `",current_month,"`
                                              WHERE post_created_date_CT >= '", start_date, "' 
                                                    AND post_created_date_CT <= '", end_date, "' 
                                          )as temp1
                                          GROUP BY  user_id,  page_id  ) as temp2
                                      GROUP BY user_id" 
                                    , sep=""))
  return(testweek_union)
}

sql_table_two_month<- function(con, current_month, next_month, start_date, end_date){
  testweek_union<- dbGetQuery(con, 
                              paste("SELECT  user_id,  GROUP_CONCAT(page_id) as like_pages, GROUP_CONCAT(like_time) AS like_times
                                      FROM (
                                        SELECT user_id, SUBSTRING_INDEX(post_id,'_',1) as page_id, count(*) AS like_time
                                          FROM ( 
                                            SELECT *
                                              FROM(
                                                  SELECT user_id, post_id 
                                                    FROM `",current_month,"`
                                                    WHERE post_created_date_CT >= '", start_date, "'
                                              ) AS union_t1
                                            UNION ALL(
                                            SELECT * 
                                              FROM(
                                                (SELECT user_id, post_id 
                                                   FROM `",next_month,"`
                                                      WHERE post_created_date_CT >= '", end_date, "')
  
                                              ) AS union_t2
                                          )
                                        )AS temp
                                      GROUP BY  user_id,  page_id  ) as temp2
                                    GROUP BY user_id" 
                                    , sep=""))
  return(testweek_union)
}



get_user_like_page_table = function(start_date, terminate_date,
                                    daysOf_startDate_minus_endDate, 
                                    daysOf_startDate_minus_startDate_across_files,
                                    output_file_path, MySQL_user, 
                                    MySQL_password, dbname){
  
  con = dbConnect(MySQL(), user = MySQL_user, password = MySQL_password, dbname = dbname, host='localhost')  
  dbGetQuery(con, "set group_concat_max_len = 1000000;")
  start_date = as.Date(start_date)
  terminate_date = as.Date(terminate_date)
  end_date = start_date + daysOf_startDate_minus_endDate
  current_month<- format(start_date, "%Y-%m")
  setwd(output_file_path)
  
  
  while(end_date <= terminate_date){
    print(paste("start:",start_date,"to",end_date, "at:", Sys.time()))
    current_month_firstday<- paste(current_month, "-01", sep="")
    if(year(end_date)*12+month(end_date) > year(current_month_firstday)*12+ month(current_month_firstday) ){
      if(year(start_date)*12+month(start_date) > year(current_month_firstday )*12 +month( current_month_firstday ) ){
        current_month= format(start_date, "%Y-%m")
        print(paste("new month", current_month))
        week_table<- sql_table(con, current_month, start_date, end_date)
        
      }else{
        print(paste("front month", current_month))
        next_month<- format(end_date, "%Y-%m")
        week_table<- sql_table_two_month(con, current_month,next_month, start_date, end_date)
        #current_month<- format(end_date, "%Y-%m")
        print(paste("back month", next_month))
      }
    }else{
      week_table<- sql_table(con, current_month, start_date, end_date)
    }
    
    fwrite(week_table, paste("us_user_like_page_",start_date,"_to_", end_date, sep=""))
    print(paste("done:",start_date,"to",end_date, "at:", Sys.time()))
    
    start_date<- start_date+daysOf_startDate_minus_startDate_across_files
    end_date<- end_date+daysOf_startDate_minus_startDate_across_files
  }
  
}
#get_user_like_page_table("2016-09-01", "2016-09-14", 6,7, 
#                         output_file_path, MySQL_user, 
#                         MySQL_password, dbname)
