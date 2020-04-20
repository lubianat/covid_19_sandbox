library(PubScore)

df = fread("~/Downloads/query (7).csv")
compounds = df$interactorinhibitorLabel

terms_of_interest = c("SARS-CoV")



pub <- pubscore(terms_of_interest = terms_of_interest, genes = compounds )
p <- heatmapViz(pub)
library(plotly)
ggplotly(p)

plot(p)