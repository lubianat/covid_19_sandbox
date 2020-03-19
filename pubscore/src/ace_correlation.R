library("data.table")
library("PubScore")


genes <- fread("pubscore/data/correlated genes.txt", header = F)

genes <- genes$V1

pubscore_object <- pubscore(terms_of_interest = "ACE2", genes = genes)
p <- heatmapViz(pubscore_object)
library(plotly)
py <- ggplotly(p)
p
htmlwidgets::saveWidget(py, "index.html")

