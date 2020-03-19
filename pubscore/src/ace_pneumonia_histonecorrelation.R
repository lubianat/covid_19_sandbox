library("data.table")
library("PubScore")


genes <- fread("data/list.txt", header = F)


genes <- genes$V1

pubscore_object <- pubscore(terms_of_interest = c("ACE2", "histone", "pneumonia"), genes = genes)
p <- heatmapViz(pubscore_object)
library(plotly)
py <- ggplotly(p)
p
htmlwidgets::saveWidget(py, "ace2_histone_pneumonia.html")

counts <- pubscore_object@counts

write.table(counts, file = "ace2_histone_pneumonia.tsv", sep = "\t")


