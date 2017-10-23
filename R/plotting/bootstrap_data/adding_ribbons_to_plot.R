library(tidyverse)
library(data.table)
library(directlabels)
library(RColorBrewer)
library(ggthemr)


ggthemr(palette="pale", layout="clear", spacing=0.6)
base_theme = theme(
  title        = element_text(size=13, face="plain"),
  axis.title   = element_text(size=12, face="plain"),
  axis.text.y  = element_text(size=10, face="plain"),
  axis.text.x  = element_text(size=10, face="plain"),
  legend.text  = element_text(size=10, face="plain"),
  legend.title = element_text(size=10, face="plain"),
  axis.title.y = element_text(margin=margin(r=2), face="plain"),
  axis.title.x = element_text(margin=margin(t=2), face="plain"),
  plot.caption = element_text(
    size=11, margin=margin(t=4), hjust=0.5, face="plain")
)

setwd(paste0("/home3/ntueconfbra1/Desktop/Link to fromRA1/",
             "ideology_scores_by_4_weeks/page_ideology_score/"))
files = list.files(pattern="*.csv")

ReadFile = function(file) {
  df_date = substr(file, nchar(file) - 13, nchar(file) - 4)
  df = read_csv(file)
  df$date = as.Date(df_date)
  df
}

page_ideology_4_weeks = list()
page_ideology_4_weeks = lapply(files, ReadFile)
page_ideology_4_weeks = rbindlist(page_ideology_4_weeks)
#setwd("~/usfbcode/")

files_b = list.files(paste0("/home3/ntueconfbra1/Desktop/",
                     "Link to fromRA1/ideology_scores_by_4_weeks/bootstrap/",
                     "page_score_1%_400times_combined/percentile/"),
                     pattern="*.csv", full.names = T)
page_ideology_4_weeks_b = list()
page_ideology_4_weeks_b = lapply(files_b, ReadFile)
page_ideology_4_weeks_b = rbindlist(page_ideology_4_weeks_b)
names(page_ideology_4_weeks_b)[1] = "page_id"

#boot_try = ReadFile("/home3/ntueconfbra1/Desktop/Link to fromRA1/ideology_scores_by_4_weeks/bootstrap/page_score_1%_200times_combined/percentile/2015-05-03_to_2015-05-30.csv")

# Politicians

page_select_name = c("Donald J. Trump", "Hillary Clinton", "Ted Cruz", 
                     "Bernie Sanders", "Marco Rubio", "Gary Johnson", "Elizabeth Warren", 
                     "Paul Ryan")
page_select_label = c("Trump", "Clinton", "Cruz", "Sanders", "Rubio", 
                      "Johnson", "Warren", "Ryan")
#page_select_name = c("Donald J. Trump", "Hillary Clinton", "Gary Johnson")

#page_select_label = c("Trump", "Clinton","Johnson")
page_plot_info = page_ideology_4_weeks %>%
  filter(page_name %in% page_select_name) %>%
  filter(date==min(page_ideology_4_weeks$date)) %>%
  mutate(level=as.factor(rank(-PC1_std))) %>%
  merge(data.frame(
    "page_name" = page_select_name, 
    "label" = page_select_label), by="page_name") %>%
  select(page_id, page_name, label, level)

df_plot = page_ideology_4_weeks %>%
  select(page_id, PC1_std, date) %>%
  merge(page_plot_info, by="page_id")

df_plot_b = page_ideology_4_weeks_b %>%
  select(page_id, percentile_2.5, percentile_97.5, date) %>%
  merge(page_plot_info, by="page_id")

df_plot = merge(df_plot, page_ideology_4_weeks_b, by = c("page_id", "date"))

eb = aes(ymax = percentile_97.5, ymin = percentile_2.5, alpha = 0.2, fill = level, colour=NA)

pdf("politician-1percent-400times.pdf")
p = ggplot(df_plot, aes(date, PC1_std, group=page_name, color=level)) + 
  geom_line()+
  geom_ribbon(eb)+
  scale_colour_manual(
    values = colorRampPalette(
      c("#e41a1c", "#377eb8"))(length(page_select_name)),
    guide = "none") + 
  scale_fill_manual(
    values = colorRampPalette(
      c("#e41a1c", "#377eb8"))(length(page_select_name)),
    guide = "none") + 

  scale_x_date(
    date_labels = "%m-%d\n%Y", 
    date_breaks = "2 month", 
    expand=c(0.15, 0)
  ) + 
  geom_dl(aes(label=label), method=list(dl.trans(x=x+.3), "last.bumpup")) +
  geom_dl(aes(label=label), method=list(dl.trans(x=x-.3), "first.bumpup")) + 
  xlab("") + 
  ylab("Estimated Facebook Ideology Score")+
  ggtitle("4 weeks politician ideology")


setwd("/home3/ntueconfbra1/Desktop/Link to fromRA1/ideology_scores_by_4_weeks/bootstrap/plots")
#cairo_pdf("politician-1%-400times.pdf",
#          width=8, height=5, family="Source Sans Pro")
print(p)
dev.off()

