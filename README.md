# DFS-Score-Data
Analyzes the breakdown of player scoring in DFS.
 
## Description
This repository will host tools to analyze the data obtained by the repository DFS-Scraper.  These will help determine
the types of players based on their point distributions.  It uses average score and standard deviation metrics to show 
players who are more consistent and those that are more up side type players.  

## Requirements
* MySQLdb
* numpy

## To Use: 
1.  Make sure you have database contains data. (See DFS-Scraper to set up)
2.  Run score_data.py with argument -m = csv or print 
