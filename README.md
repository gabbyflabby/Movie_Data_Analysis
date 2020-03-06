# Module 1 Final Project

Gabriela Lopez & Maura Cerow 
Sources: IMDB & Movie DB

## Introduction

For this project, we analyzed movies released between 2010 and 2019. We got our data from IMDB, collecting 10,000 releases for this time period. By scraping IMDB we got the genre(s), MPAA rating, user star rating, title of each film as well as the IMDB Movie ID. With this ID, we then used the Movie DB’s API to get the budget and revenue for these 10k entries. From there, we went on to pose 5 questions we set out to answer:

	1. How much should we expect to spend?
	2. How does what we spend impact our revenue?
	3. What genres gross the most revenue?
	4. What audience should we target to generate the most revenue?
	5. How long should our movie be?

In this project we used the following libraries:

	### Data Collection
	BeauitfulSoup
	Request
	Time
	Config Parser
	Urllib.parse
	HTTPError
	Json
	Pandas

	### Data Cleaning & Visualization
	Pandas
	Numpy
	Matplotlib
	Seaborn

## Data Collection

	See: Data_Collection.ipynb

This file contains the functions we used to gather our data. We built different functions while scraping the first page from our IMDB list and then applied those functions to the remaining pages. We then used Movie DB’s API to return the revenue and budget for each entry we had from IMDB. We were able to access the data from the API by first searching with the IMDB ID in the “Find” search which returned the Movie DB’s ID. From there, we searched with the Movie ID in the “Get Movie” function. From there, we were able to pull out our revenue & budget.

With all metrics collected from our sources, we moved the data into a DataFrame and converted to a CSV to access the data easier when cleaning & dissecting.

In the case that any metric was not listed, we made sure to add a null value which would later clean once loaded into the DataFrame.

## Data Cleaning & Visualization

	See: Visualizations.ipynb

Our first step was to clean our data once loading in the csv file we made after gathering all data.

Once we had our data cleaned, we started to answer our business questions we set out to prove.

	Questions #1 - How much should we expect to spend?
	See Figure 1. Spend per Movie

	Questions #2 - How does what we spend impact our revenue?
	See Figure 2. Budget vs Revenue for Top IMDB Movies

	Questions #3 - What genres gross the most revenue?
	See Figure 3. Revenue by Genre
	See Figure 4. Average Revenue, Budget & Profit by Genre

	Questions #4 - What audience should we target to generate the most revenue?
	See Figure 5. Mean Revenue by MPAA Rating

	Questions #5 - How long should our movie be?
	See Figure 6. User Rating vs Runtime


## Conclusion

### Recommendations
Based on our data set, we can expect to spend ~$14m-$17m per project.

We would expect that as our spend increases, our revenue will also increase.

While top genres all look to return a profit, Musicals and Music movies return a higher profit when compared to their budgets.

The most revenue generating MPAA rating type is G on average. It returns ~$150m more than a film rated PG and $200m more than an PG. An R-rated film on average returns under $70m.

There looks to be a positive trend between user ratings and runtime. As a film increases in runtime, users rated it more favorably.

### Further Analysis
To continue this project, we suggest:
* Find target MPAA rating per genre
* Check which genres are over-saturated
* Find actors, directors, and screenwriters with a high ROI

To view our presentation on this project, please visit the following link.
https://docs.google.com/presentation/d/1zhudJ7S5P-5WI14h1yTlGHQT6qqLznx3e_NopS0y-4E/edit#slide=id.p
