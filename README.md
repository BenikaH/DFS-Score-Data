# DFS-Score-Data
Analyzes the breakdown of player scoring in DFS.
 
## Description
This repository will host tools to analyze the data obtained by the repository DFS-Scraper.  These will help determine
the types of players based on their point distributions.  It uses average score and standard deviation metrics to show 
players who are more consistent and those that are more up side type players.  

## Additional Features
A module to plot individual player point distributions was added. This can be used with player score standard deviations and will give a better visualization of how certain players produce points.  

## Requirements
* MySQLdb
* numpy
* matplotlib 

## To Use: 
1.  Make sure you have database contains data. (See DFS-Scraper to set up)
2.  Run score_data.py with argument -m = csv or print 
3.  To plot point distributions, use -m = plot and -i XXXX XXXX XXXX where 'XXXX' is an arbitrary amount of integers separated by spaces.  
