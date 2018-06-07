library(data.table)
library(dplyr)
library(plyr)
library(ggplot2)
library(fiftystater)
library(Cairo)
#library(extrafont)
library(maps)
library(ggthemr)
ggthemr(palette="pale", layout="clear", spacing=0.6) # load ggthemr to use

base_theme = theme(
  title        = element_text(size=13, face="plain"),
  axis.title   = element_text(size=12, face="plain"),
  axis.text.y  = element_text(size=10, face="plain"),
  axis.text.x  = element_text(size=10, face="plain"),
  legend.text  = element_text(size=10, face="plain"),
  legend.title = element_text(size=10, face="plain"),
  axis.title.y = element_text(margin=margin(r=2), face="plain"),
  axis.title.x = element_text(margin=margin(t=2), face="plain"),
  plot.caption = element_text(size=11, margin=margin(t=4), hjust = 0.5,
                              face="plain")
)




user_like_state <- fread("/home3/usfb/analysis/analysis-ideology-change/temp/user-state/us_user_like_state_max_unique.csv")
states <- user_like_state$like_state_max
state_total_users_df <- data.table(table(states)[state.name])

user_like_fakepage <- fread("/home3/usfb/analysis/analysis-ideology-change/temp/fake-news-user/all_user_like_fake_post_page_time.csv")
user_like_fakepage$state <- user_like_state$like_state_max[match(user_like_fakepage$user_id, user_like_state$user_id)]
overall = data.frame(tolower(state.name))
colnames(overall) <- "state"
row.names(overall) <- state.name

overall$state_times <- as.numeric(table(user_like_fakepage$state)[state.name])
overall$share_user_like_fake_posts <- overall$state_times/(state_total_users_df$N[match(row.names(overall), state_total_users_df$states)])
overall$share_user_like_fake_posts <- round(overall$share_user_like_fake_posts, digits = 4)

# Plot Share of User Like Fake Post

p_map <- ggplot(overall, aes(map_id = state)) + 
  # map points to the fifty_states shape data
  geom_map(aes(fill = share_user_like_fake_posts), map = fifty_states) + 
  ggtitle("Share of User Like Fake Post")+
  expand_limits(x = fifty_states$long, y = fifty_states$lat) +
  coord_map() +
  scale_x_continuous(breaks = NULL) + 
  scale_y_continuous(breaks = NULL) +
  labs(x = "", y = "") +
  scale_fill_gradient(low = "blue", high = "red", name = "") +
  theme(plot.title = element_text(hjust=0.5), legend.position = "bottom",
        panel.background = element_blank())  +
  base_theme

setwd("/home3/usfb/analysis/analysis-ideology-change/output/chunhsiang")
cairo_pdf("share_of_user_like_fake_post.pdf",
          width=6, height=4.5, family="Source Sans Pro")
print(p_map)
dev.off()



#Plot scatter plot
state_path = "~/usfbdata/state_level/"
election = read_csv(paste0(state_path, "presidential_general_election_2016.csv"))
election = election[election$name=="H. Clinton", ]
overall$state_m = rownames(overall)
#median = read_csv(paste0(state_path, "state_median_ideology_from_1000_page_20161001_to_20161107.csv"))
# median = read_csv(paste0(state_path, "state_share_from_1000_page_20161001_to_20161107_state_20161001_to_20161107_exclude_gov.csv"))
state = read_csv(paste0(state_path, "state-level-variables.csv"))
abbre = read_csv(paste0(state_path, "state_abbreviation.csv"))
colnames(abbre) = c("state", "state_abbre")
merge = merge(overall, election, by.x= "state_m", by.y="state")
merge = merge(merge, state, by.x="state_m", by.y="state")
merge = merge(merge, abbre, by.x="state_m", by.y="state")
merge$state_type = ifelse(merge$is_winner == "True", "Dem", "Rep")
swing_states = c("FL", "OH", "WI", "MI", "PA", "IA")
merge[merge$state_abbre %in% swing_states, ]$state_type = "Swing"
merge$state_type = as.factor(merge$state_type)
merge$state_type = factor(merge$state_type,
                          levels=c("Rep", "Swing", "Dem"))
merge$vote_pct = 1 - merge$vote_pct

library(ggrepel)
library(RColorBrewer)
red = brewer.pal(4, "Set1")[1]
blue = brewer.pal(4, "Set1")[2]
purple = brewer.pal(4, "Set1")[4]

## State voter share closer to Clinton
fake_post_VS_trump_share_scatter_plot = function(merge , title){
  p = ggplot(merge, aes(share_user_like_fake_posts, vote_pct , label=state_abbre)) 
  p_scatter = p + 
    stat_smooth(
      method="lm", 
      colour="gray50", 
      se=TRUE,
      fill="grey") +
    geom_point(aes(shape=state_type, color=state_type, fill=state_type)) +
    scale_color_manual(
      labels=c("Rep wins 2016 & 2012", "Swings from Obama to Trump", "Dem wins 2016 & 2012"), 
      values=c(red, purple, blue)) +
    scale_fill_manual(
      labels=c("Rep wins 2016 & 2012", "Swings from Obama to Trump", "Dem wins 2016 & 2012"), 
      values=c(red, purple, blue)) +
    scale_shape_manual(
      labels=c("Rep wins 2016 & 2012", "Swings from Obama to Trump", "Dem wins 2016 & 2012"), 
      values=c(23, 21, 22)) + 
    geom_text_repel(point.padding = unit(0.15, "lines"), 
                    box.padding = unit(0.15, "lines"),
                    nudge_y = 0.1,
                    size = 3
    ) +
    theme_classic(base_size = 16) +
    scale_x_continuous("Share of Facebook User liked fake post") +
    scale_y_continuous("2016 Trump Vote Share") +
    #  labs(caption = "Using 2016-10-28 to 2016-11-07 likes to guess user's state") + 
    theme(legend.position=c(0.21, 0.95),  legend.title=element_blank()) +
    base_theme
  setwd("/home3/usfb/analysis/analysis-ideology-change/output/chunhsiang")
  cairo_pdf(title,
            width=6, height=4.5, family="Source Sans Pro")
  print(p_scatter)
  dev.off()
  
  return(p_scatter)
}
p_scatter = fake_post_VS_trump_share_scatter_plot(merge, 
                                                  "fake_post_vs_trump_share_scatter_plot")
#p_scatter

outlier_states = c("GA", "ID", "TX", "AZ")
merge_adjusted = merge[!(merge$state_abbre %in% outlier_states),]
p_scatter_adjusted = fake_post_VS_trump_share_scatter_plot(merge_adjusted,
                                                           "fake_post_vs_trump_share_scatter_plot_adjusted")


#p_scatter_adjusted
