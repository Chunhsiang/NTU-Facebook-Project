library(readr)
library(sqldf)
library(data.table)
#library(tidyverse)
#library(xts)
#library(RColorBrewer)
user_state<- fread("~/usfbdata/us_user_info/us_user_info_us_user_like_state_max_unique.csv", drop="like_time_max", colClasses=c( rep("character",3)))


find_support_rate <- function( time ){
  user_path<- paste("/home3/ntueconfbra1/Link to fromRA1/ideology_scores_by_4_weeks/us_user_data/us_user_user_like_page_4_weeks",time,".csv", sep="")
  pol_path<- paste("/home3/ntueconfbra1/Link to fromRA1/ideology_scores_by_4_weeks/page_ideology_score/page_ideology_score_4_weeks",time,".csv", sep="")
  us_user_ideology <- fread( user_path,select = c("user_id","user_PC1_mean"), colClasses=c("character",rep("numeric",4)))
  us_user_ideology<- as.data.frame(us_user_ideology)
  politician_ideology <- read_csv(pol_path, col_types = cols(page_id = col_character()))
  temp<- politician_ideology
  hillary_ideology<- temp[temp[,2]== "Hillary Clinton", 4]
  trump_ideology<- temp[temp[,2]== "Donald J. Trump", 4]
  middle<- (hillary_ideology+trump_ideology)/2
  
  
  whole_data<- merge(us_user_ideology, user_state, by= "user_id")
  
  state_observation<- sqldf(paste("SELECT like_state_max as state, count(*) as total_user FROM whole_data GROUP BY state"))
  hillary_state<- sqldf(paste("SELECT like_state_max as state, count(*) as supporters FROM whole_data WHERE user_PC1_mean <", middle, "GROUP BY state"))
  
  
  support_rate = hillary_state$supporters / state_observation$total_user
  
  print(paste(time," done at:", Sys.time()))
  return(support_rate)
}

classify_list<- function(support_dataframe, threshold){
  far_right<- c()
  middle_right<- c()
  far_left<- c()
  middle_left<- c()
  swing<- c()
  for(i in 1:50){
    if(mean(support_dataframe[,i]) < threshold[1])
      far_right<- c(far_right, names(support_dataframe)[i])
    else if(threshold[1] <= mean(support_dataframe[,i]) && mean(support_dataframe[,i]) < threshold[2])
      middle_right<- c(middle_right, names(support_dataframe)[i])
    else if (threshold[2] <= mean(support_dataframe[,i]) && mean(support_dataframe[,i]) < threshold[3])
      swing<- c(swing, names(support_dataframe[i]))
    else if (threshold[3] <= mean(support_dataframe[,i]) && mean(support_dataframe[,i]) < threshold[4])
      middle_left<- c(middle_left, names(support_dataframe)[i])
    else if(mean(support_dataframe[,i]) >= threshold[4])
      far_left<- c(far_left, names(support_dataframe)[i])
  }
  classified_list<- list(far_right, middle_right, swing, middle_left, far_left)
  return(classified_list)
}





time_vec_4weeks<- c(rep("", 79))
time_start= as.Date("2015-05-03")
for(i in 1:length(time_vec_4weeks)){
  time_end= time_start+27
  time_vec_4weeks[i]= paste(time_start, "to", time_end, sep = "_")
  time_start= time_start+7
}



print(paste("starting time of building panel:",Sys.time()))

for(i in 1:length(time_vec_4weeks)){
  if(i==1){
    hillary_state_support_pannel<- find_support_rate(time_vec_4weeks[i])
  }else{
    hillary_state_support_pannel <- rbind(hillary_state_support_pannel,find_support_rate(time_vec_4weeks[i]))
  }
}

hillary_state_support_pannel_used= data.frame(hillary_state_support_pannel[,c(-1, -34)], row.names = time_vec_4weeks)#picking out unfounded and non-voting delegates:
names(hillary_state_support_pannel_used)<- state.name
write.csv(hillary_state_support_pannel_used, "/home3/ntueconfbra1/Desktop/Link to fromRA1/support_rate_surveillance/by_four_weeks/hillary_support_rate_pannel.csv")

plot_data<- read.csv( "/home3/ntueconfbra1/Desktop/Link to fromRA1/support_rate_surveillance/by_four_weeks/hillary_support_rate_pannel.csv")

temp_split= strsplit(time_vec_4weeks, split = "_")
time_x_axis= c(as.Date(temp_split[[1]][3]))
for(i in 2:length(time_vec_4weeks)){
  time_x_axis= c(time_x_axis, as.Date(temp_split[[i]][3], "%Y-%m-%d"))
}

sparse_time_x_axis= time_x_axis[c(seq(1,length(time_x_axis), by=2))]

setwd("/home3/ntueconfbra1/Desktop/Link to fromRA1/support_rate_surveillance/by_four_weeks/50_states_Clinton_support_rate/")
#plot_x_lim=c(as.Date(time_x_axis[1]), as.Date(time_x_axis[length(time_x_axis)]))

for( i in 2:length(plot_data[1, ])){
  plot(x= time_x_axis, y= plot_data[,i], type="l", xaxt="n", ylim = c(0,1),
       main=paste(names(plot_data)[i], "2015-05-30 to 2016-11-26"), xlab = "Month-Date", ylab = "Clinton Support Rate")
  axis.Date(1, at=time_x_axis, format="%m-%d")
  dev.copy(jpeg,filename= paste( names(plot_data)[i],"support rate time series") ,width = 1000, height = 732)
  dev.off()
}
