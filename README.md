# Challenge Collecting Data
---
* Developer Name: Sijal Kumar Joshi
* Level : Junior Developer
* Started: 26/01/2020 H:9h00
* Duration: 3 days
* Deadline: 29/01/2021 16:00
* Team challenge : Solo
* Type of Challenge: Consolidation
* Promotion: AI Theano 2
* Coding Bootcamp: Becode Artificial Intelligence (AI) Bootcamp

# Goal Objective
---
Use a python library to collect as much data as possible.

1. To scrape a website
2. To build a dataset from scratch
3. To Implement a strategy to collect as much data as possible.

What ?
This group consists of making predictions on real estate prices using Web scraping.

Why ?
The real estate company "ImmoEliza" wants to create a machine learning model to make price predictions on real estate sales in Belgium.

When ?
This is a 3 days project. The dead line is on 29/01/21 at 4 PM.

How ?
This program scrap data from website depending solely on Scrapy including the delay process.

# The Mission
---
The real estate company "ImmoEliza" wants to create a machine learning model to make price predictions on real estate sales in Belgium. You must therefore create a dataset that holds the following columns :

* Locality
* Type of property (House/apartment)
* Subtype of property (Bungalow, Chalet, Mansion, ...)
* Price
* Type of sale (Exclusion of life sales)
* Number of rooms
* Area
* Fully equipped kitchen (Yes/No)
* Furnished (Yes/No)
* Open fire (Yes/No)
* Terrace (Yes/No)
	* If yes: Area
* Garden (Yes/No)
	* If yes: Area
* Surface of the land
* Surface area of the plot of land
* Number of facades
* Swimming pool (Yes/No)
* State of the building (New, to be renovated, ...)
* Must save everything in a csv file.

# Features
---
* Grab data from the website. (currently viw website without javascript)
* Empty row and missing infomation set to value None.
* 

# About the Repository
---
There are only 2 branches Main and Dev because of its simplicity.

# Code Style
* Each class have a __str__() method
* Each function or class is typed
* Each function or class contains a docstring
* The code is formatted with black
* The code has been commented.
* The code is cleaned of any commented unused code.

### README.md
---
* Detail infomation and briefs.

### main.py
---
This is where the game starts.
It imports everything you need to start the game here,
If you want an interactive version, the number of players and the names of players will also be requested here.

### utils folder
---
In other words, it has 3 files: 

i. card.py
	* This is where the 52 cards for the card game are developed and generated. 
	
	* This is also where the card deck is packed, shuffled and distributed to the players. 

ii. player.py
	* This is where the player would select the card randomly during it's turn 
	
	* The player can choose which card to play if you choose the interactive version. 
	
iii. game.py
	* This is where the actual codes for the game are. 
	
	* Here you can see a board class which shows the game's mechanics and how the game works.

# Pending...
---
* Scraping data from Java script website. 
* Encountring the captcha issue automatically.

# Thank you for reading