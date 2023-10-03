# Stopgame analysis

## About
Data analysis of reviews from video game website [stopgame.ru](https://stopgame.ru/).

## Description
Videogames are very popular. People watch reviews on some games to decide whether to buy a game or not, or they just cannot afford the purchase. The purpose of this project is to find out if the genre affects on numbers of reviews. The results can be helpful for advertising placement.

## Note
### Data collection
Data were collected in 18.09.2023. The structure of website can be modified over time ot names of needed tags can be changed. So the dataset was saved info the "stopgame.csv" file to be able to reproduce the analysis without modifications of the "collector" file. The one combines the crawler, which finds links from review web page; the scraper, which gets HTML structure of websites; and the parser, which retrieves information from HTML tags and store it in structured format.

### Data modification
There is no exact value for reviews with more than 10 thousands views, just a number of thousands and letter "K". To make analysis we replace "K" with a random 3-digit number. Save modified data into the new separate file "stopgame_transformed.csv" to avoid the randomization in every analysis run.

## Methods used
* Data Visualization (line charts, histograms, scatter plots, box plots)
* Descriptive statistics (mean, median, standard deviation, count)
* Inferential Statistics (hypothesis testing &mdash; ANOVA, Kruskal-Wallis test)

## Results
The reviews of the games in 'Приключение' genre are the least attractive for stopgame.ru users than of the games in any other genre.
