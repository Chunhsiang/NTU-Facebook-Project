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
#page_data= temp_file$user_PC1_mean
#plot_name= "Ideology distribution after sampling"
#bandwidth= 150

page_plot <- function(page_data, bandwidth){
  page_data<- sort(page_data)
  box_point <- seq(from= min(page_data), to= max(page_data), length.out = bandwidth)
  box_value <- rep(0, bandwidth)
  box_value<- GetBoxValue(page_data, box_point, box_value)
  plot_data<- cbind(box_point, box_value)
  return(plot_data)
}

library("ggplot2")

six_files<- list.files("/home3/ntueconfbra1/Link to fromRA1/user_ideology_4months/")
six_box_value<- list()

for(i in 1:length(six_files)){
  temp_file<- fread(paste("/home3/ntueconfbra1/Link to fromRA1/user_ideology_4months/",six_files[i], sep=""))
  temp_plot_value<- page_plot(temp_file$user_PC1_mean, 150)
  six_box_value[[i]]<-  temp_plot_value
  }
#six_box_value[[3]]<- temp_plot_value

for(i in 1: 6){
  six_box_value[[i]][,2]= six_box_value[[i]][,2]/ sum(six_box_value[[i]][,2])
}

#plot_name= "US Facebook user ideology distribution 4-month evolution from 2015 to 2016"
patt<- c("red", "orange", "yellow", "green", "blue", "purple")
patt2<- c("plum3", "hotpink3","indianred" , "red2", "red3", "red4")
plot(as.data.frame(six_box_value[[1]]), xlim= c(-1.5, 1.5), ylim= c(0,0.1),xlab="ideology score",
                  ylab="percentage", col= patt[1], type= "l", main=plot_name)

#plot(as.data.frame(six_box_value[[2]]), xlim= c(-3.22, 3), ylim= c(0,0.5), col= patt[2], type= "l")
#lines(six_box_value[[2]][,1], six_box_value[[2]][,2], col= patt[2] )
for( i in 2:6){
  lines(x= six_box_value[[i]][,1], y= six_box_value[[i]][,2], col= patt2[i])
}

par(xpd =F)
plot(as.data.frame(six_box_value[[1]]), xlim= c(-1.3, 1.3), ylim= c(0,0.1),xlab="ideology score",
     ylab="percentage", col= "blue", type= "l", main=plot_name)

lines(x= six_box_value[[3]][,1], y= six_box_value[[3]][,2], col= "purple")
lines(x= six_box_value[[5]][,1], y= six_box_value[[5]][,2], col= "red")
legend( "topright", legend = c("2015-01 to 2015-04","2015-09 to 2015-12" ,"2016-05 to 2016-08" ), 
      cex=0.5,  xpd = TRUE,  lty = 1, lwd = 1.5,  bty = "n",col = c("blue","purple","red"))



df<- data.frame(six_box_value[[1]])
pp<-ggplot(data=df)

pp+geom_curve(aes(x= six_box_value[[1]][1,1], y= six_box_value[[1]][1,2], xend=six_box_value[[1]][150,1], yend=six_box_value[[1]][150,2]))
