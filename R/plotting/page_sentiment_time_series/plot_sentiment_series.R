#install.packages("tidyquant")
library(tidyquant)
library(readr)

page_sentiment_data = read_csv("/home3/ntueconfbra1/Desktop/Link to fromRA1/sentiment_analysis/plot_sentiment_data.csv")
#lass(page_sentiment_data$post_created_date_CT[1])


#input_id = 5281959998
weekly_average_sentiment_score = function(page_sentiment_data,
                                          input_id, start_date, 
                                          end_date){
  
  info_by_post = page_sentiment_data %>%
    filter(page_id == input_id )%>%
    filter(post_created_date_CT >= as.Date(start_date) &
             post_created_date_CT <= as.Date(end_date)) %>%
    select(page_id, page_name, compound, post_created_date_CT) %>%
    arrange(post_created_date_CT )
  
  info_by_week = info_by_post %>% 
    group_by(week = cut(post_created_date_CT, "week")) %>% 
    summarise(mean_score = mean(compound))
  
  page_name = info_by_post$page_name[1]
  
  return_df = data.frame(rep(page_name, length(info_by_week$week)), info_by_week)
  names(return_df)[1] = "page_name"
  return(return_df)
}


page_list = page_sentiment_data %>%
              group_by(page_id) %>%
              summarise(page_name = first(page_name), post_times = n()) %>% 
              arrange(desc(post_times))
page_list = page_list[!is.na(page_list$page_id),]

setwd("/home3/ntueconfbra1/Link to fromRA1/sentiment_analysis/page_sentiment_time_series_plot/")
i=582
for( i in 914:length(page_list$page_id)){
  plot_data = weekly_average_sentiment_score(page_sentiment_data,
                                             page_list$page_id[i], "2015-01-04", 
                                             "2017-04-08")
  plot(x = as.Date(plot_data$week), y = plot_data$mean_score, type = "l",
       ylab = "sentiment score", xlab = "Date", main =paste("Sentiment score time series","\n",
                                                            plot_data$page_name[1]))
  tryCatch(
    dev.copy(jpeg,filename= as.character(plot_data$page_name[1]) ,width = 1000, height = 732),
    error=function(e){},
    finally = {
      splitted = strsplit(as.character(plot_data$page_name[1]),split = "/")
      new_name = paste(splitted[[1]][1], splitted[[1]][2], sep = "|")
      dev.copy(jpeg,filename= new_name,
                       width = 1000, height = 732)
      #dev.off()
    })
  graphics.off()
  
  if( i %% 100  ==0 )
    print(paste("Done", i))
}

graphics.off()




i=100
start_date = "2015-01-04"
end_date = "2017-04-08"

pp = 913





sentiment_drop_after_election = function(page_sentiment_data,
                                         page_list,
                                         start_date, 
                                         end_date)
{
  page_name_vec = c(NULL)
  sentiment_change_vec = c(NULL)
  
  for( pp in 1:length(page_list$page_id)){
    plot_data = weekly_average_sentiment_score(page_sentiment_data,
                                               page_list$page_id[pp], start_date, 
                                               end_date)

    before_month = c(NULL)
    after_2_weeks = c(NULL)
    for( i in 1:length(plot_data$week)){
      if(as.Date(plot_data$week[i]) > as.Date("2016-10-07")){
        if(as.Date(plot_data$week[i]) < as.Date("2016-11-07")){
          before_month = c(before_month, plot_data$mean_score[i])
        }else if(as.Date(plot_data$week[i]) < as.Date("2016-11-21")){
          after_2_weeks = c(after_2_weeks , plot_data$mean_score[i])
        }
      }
    }
    
    series_std = sd(plot_data$mean_score)    
    if(length(before_month) > 0 && length(after_2_weeks) > 0){
      sentiment_change = mean(after_2_weeks) - mean(before_month) 
      if(abs(sentiment_change) > series_std){
        page_name_vec = c(page_name_vec, as.character(plot_data$page_name[1]))
        sentiment_change_vec = c(sentiment_change_vec, sentiment_change/series_std)
      }
    }
    if( pp %% 100  ==0 )
      print(paste("Done", pp))
  }
  #return_df = data.frame(page_name, sentiment_change)
  return(data.frame(page_name_vec, sentiment_change_vec))
  
}

sentiment_change_df = sentiment_drop_after_election(page_sentiment_data, 
                                                 page_list,
                                                 "2015-01-04", 
                                                 "2017-04-08")
upward_page = sentiment_change_df[sentiment_change_df$sentiment_change_vec > 0, ]
upward_page = upward_page [ order(-upward_page$sentiment_change_vec), ]
write_csv(upward_page, path = "/home3/ntueconfbra1/Link to fromRA1/sentiment_analysis/post_sentiment_comparision_after_election/upward.csv")

downward_page = sentiment_change_df[sentiment_change_df$sentiment_change_vec < 0, ]
downward_page = downward_page [ order(downward_page$sentiment_change_vec), ]
write_csv(downward_page, path = "/home3/ntueconfbra1/Link to fromRA1/sentiment_analysis/post_sentiment_comparision_after_election/downward.csv")



#plot(x = as.Date(plot_data$week), y = plot_data$mean_score, type = "l",
#     ylab = "sentiment score", xlab = "Date", main =paste("Sentiment score time series","\n",
#                                                         plot_data$page_name[1]))
   
