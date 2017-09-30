GetBoxValue<- function(page_data, group_bound, group_proportion){
  n <- length(page_data)
  iter <-1
  for(i in 1:length(group_bound)){
    while(iter< n){
      if(page_data[iter] <= group_bound[i] ){
        group_proportion[i] = group_proportion[i]+ 1 
        iter = iter+1
      }else{
        break
      }
    }
  }
  return(group_proportion)
}

#page_plot(all_users, "Ideology distribution after sampling", 150)
#page_data= all_users
#plot_name= "Ideology distribution after sampling"
#bandwidth= 150

page_plot <- function(page_data, plot_name, bandwidth){
  
  group_bound <- c(-1.2, -0.4, 0.4, 1.2, 2) #enter boundary for groups
  
  group_proportion<- rep(0, 5)
  group_proportion<- GetBoxValue(page_data, group_bound, group_proportion)
  
  box_point <- seq(from= min(page_data), to= max(page_data), length.out = bandwidth)
  box_value <- rep(0, bandwidth)
  box_value<- GetBoxValue(page_data, box_point, box_value)
  
  plot(x= box_point, y= round(box_value/sum(box_value), digits = 4), type= "l", xlab = "ideology", ylab = "density" , main=plot_name)
  
  abline(v=group_bound[1:4], col=c("blue", "blue","red", "red"))
  text(c(min(-1.5, page_data[1]),  group_bound[1:4])+0.1, rep(max(round(box_value/sum(box_value), digits = 4)),4), as.character(round(group_proportion/sum(group_proportion),digits= 2)))
  blue2red<- colorRampPalette(c("blue","red"))
  segments(x0 =box_point, y0=rep(0, length(box_point)), x1 =box_point, y1= round(box_value/sum(box_value), digits = 4) , col= blue2red(length(box_value)), lwd = 10 )
  #return(quantile(page_data, probs = seq(0, 1, by= 0.01)))
}



library(readr)
library(dplyr)
us_user_ideology_all <- read_csv("~/usfbdata/us_user_info/us_user_ideology_from_1000_page_and_politician_20150101_to_20161107_all.csv", 
                                 col_types = cols(user_PC1_mean_weighted = col_skip(), user_PC1_median = col_skip(), user_PC1_median_weighted = col_skip(), user_id = col_character()))

us_user_state <- read_csv("~/usfbdata/us_user_info/us_user_info_us_user_like_state_max_unique.csv", col_types = cols(like_time_max = col_skip(),user_id = col_character()))

state_population_census_2016 <- read_csv("~/usfbdata/state_level/state_population_census_bureau_2016.csv")

combined_data<- inner_join(us_user_ideology_all, us_user_state, by= "user_id")
combined_data<- combined_data[is.na(combined_data$like_state_max) == 0, ]
state_fb_user<- as.data.frame(combined_data %>% group_by( like_state_max) %>% summarise(n=n()) )
#remove "Non-voting delegates
state_fb_user<- state_fb_user[-33, ]
#remove District of Columbia
state_population_census_2016<- state_population_census_2016[-9, ]

#state_fb_user[,1]== state_population_census_2016[,1]
proportion_comparision<- cbind(state_fb_user[,1], state_fb_user[,2]/sum(state_fb_user[,2]),  state_population_census_2016[,1], state_population_census_2016[,2]/sum(state_population_census_2016[,2]))
names(proportion_comparision)<- c("state_FB", "FB_proportion", "state_Census", "Census_proportion")
#View( cbind(state_fb_user[,1], state_fb_user[,2]/sum(state_fb_user[,1]),  state_population_census_2016[,1]))

proportion_comparision[(proportion_comparision[,2]>proportion_comparision[,4]), ]
active_states_temp<- proportion_comparision[(proportion_comparision[,2]>proportion_comparision[,4]), c(1,2,4)]
active_states_with_weight<- cbind.data.frame(as.character(active_states_temp[,1]), as.numeric(active_states_temp[,3]/active_states_temp[,2]))
less_active_states <- as.character(proportion_comparision[(proportion_comparision[,2]<proportion_comparision[,4]), 1])
less_active_states_users<- filter( combined_data , like_state_max %in%  less_active_states)
all_users<- less_active_states_users


for(i in 1: length(active_states_with_weight[,1]) ){
  temp<- filter( combined_data , like_state_max %in%  as.character(active_states_with_weight[i,1]))
  temp<- sample_frac(temp,  as.numeric(active_states_with_weight[i,2]))
  all_users<-  rbind(all_users, temp)
}

all_users<- all_users %>% arrange(user_PC1_mean)
all_users<- as.data.frame(all_users)
all_users_ideology<- as.numeric(all_users[,2])
head(all_users_ideology)
page_plot(all_users_ideology, "Ideology distribution after sampling", 150)

us_user_ideology_all_plot<- us_user_ideology_all %>% arrange(user_PC1_mean)
us_user_ideology_all_plot<- as.data.frame(us_user_ideology_all_plot)
us_user_ideology_all_plot_plot<- as.numeric(us_user_ideology_all_plot[,2])
page_plot(us_user_ideology_all_plot_plot , "All user Ideology distribution", 150)



us_user_state_exclude_sanders <- read_csv("~/Desktop/us_user_info_us_user_info.us_user_state_201501_to_201611_all_exclude_sanders.csv", col_types = cols(user_id = col_character()))
combined_data_2<- inner_join(us_user_ideology_all, us_user_state_exclude_sanders, by= "user_id")
combined_data_2<- combined_data_2[is.na(combined_data_2$user_state) == 0, ]
state_fb_user_2<- as.data.frame(combined_data_2 %>% group_by(user_state) %>% summarise(n=n()) )
#remove "Non-voting delegates
state_fb_user_2<- state_fb_user_2[-33, ]


proportion_comparision_2<- cbind(state_fb_user_2[,1], state_fb_user_2[,2]/sum(state_fb_user_2[,2]),  state_population_census_2016[,1], state_population_census_2016[,2]/sum(state_population_census_2016[,2]))
names(proportion_comparision_2)<- c("state_FB", "FB_proportion", "state_Census", "Census_proportion")
proportion_comparision_2[(proportion_comparision_2[,2]>proportion_comparision_2[,4]), ]

active_states_temp_2<- proportion_comparision_2[(proportion_comparision_2[,2]>proportion_comparision_2[,4]), c(1,2,4)]
active_states_with_weight_2<- cbind.data.frame(as.character(active_states_temp_2[,1]), as.numeric(active_states_temp_2[,3]/active_states_temp_2[,2]))
less_active_states_2 <- as.character(proportion_comparision_2[(proportion_comparision_2[,2]<proportion_comparision_2[,4]), 1])
names(combined_data_2)
less_active_states_users_2<- filter( combined_data_2 , user_state %in%  less_active_states_2)
all_users_2<- less_active_states_users_2

for(i in 1: length(active_states_with_weight_2[,1]) ){
  temp<- filter( combined_data_2 , user_state %in%  as.character(active_states_with_weight_2[i,1]))
  temp<- sample_frac(temp,  as.numeric(active_states_with_weight_2[i,2]))
  all_users_2<-  rbind(all_users_2, temp)
}

all_users_2<- all_users_2 %>% arrange(user_PC1_mean)

all_users_2_ideology<- as.numeric(all_users_2[,2])

page_plot(all_users_2_ideology, "Exclude Sander Ideology distribution after sampling", 150)


conservative_states<-  c("Texas","Alabama" ,"Oklahoma")
liberal_states<- c("California", "New York", "Massachusetts")
swing_states<- c("Wisconsin", "Pennsylvania", "Michigan", "Virginia")

state_name= "New York"
draw_state<- function(state_name){
  temp<- filter( combined_data ,like_state_max %in%  state_name)
  temp1<- temp %>% arrange(user_PC1_mean)
  temp1<- as.data.frame(temp1)
  temp_plot<- as.numeric(temp1[,2])
  page_plot(temp_plot, paste("Ideology distibution of", state_name), 150)
}
all_states<- c(conservative_states, liberal_states, swing_states)
old.par <- par(mfrow=c(3, 3))

dev.off()
par(old.par)
plot(all_users_ideology)
for(i in 1: 9){
 draw_state(all_states[i])
  
}
