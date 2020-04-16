#!/usr/bin/env python
# coding: utf-8

# # HTML Parser for IMDB
# ---
# **Author Github:** [Giray Coskun](https://github.com/giraycoskun)
# 
# **Valid Links:**
# 
# https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&view=simple
# 
# https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count=10&start=5&ref_=adv_nxt
# 
# ---
# **Legal issues on Web Scraping:**
# 
# https://www.lawinsociety.org/legal-perspectives-on-scraping-data-from-the-modern-web
# 
# ---
# 
# #### Tutorial: https://realpython.com/beautiful-soup-web-scraper-python/
class Movie:
    def __init__(self, title, year, rank, rating=None):
        self.title = title
        self.rank = rank
        self.year = year
        self.rating = rating
    
    def print_(self):
        if(self.rating == None):
            func = print( str(self.rank) + ". " + self.title + ", " + str(self.year))
        else:
            func = print( str(self.rank) + ". " + self.title + ", " + str(self.year) + ", " + str(self.rating))
        return func


from bs4 import BeautifulSoup
import requests
import urllib.request, urllib.parse

COUNT = 250
START =1
output_filename = "film_list_"+str(COUNT)+".csv"

URL = "https://www.imdb.com/search/title/?groups=top_1000&view=simple&sort=user_rating,desc&count="+str(COUNT)+"&start="+str(START)+"&ref_=adv_nxt"
print(URL)

def getMovies(URL):

	page = requests.get(URL)
	print("Status Code:",page.status_code)

	soup = BeautifulSoup(page.content, 'html.parser')

	contents = soup.find_all(class_="lister-item-content")
	movie_list = []
	for element in contents:

	    title = element.find('a').text
	    #print(title)
	    year = element.find(class_="lister-item-year text-muted unbold").text.strip('()')
	    #print(year)
	    rank = int(element.find(class_="lister-item-index unbold text-primary").text.strip('.'))
	    #print(rank)
	    rating = element.find(class_="col-imdb-rating").text.strip()
	    #print(rating)
	    
	    temp = Movie(title, year, rank, rating)
	    temp.print_()
	    movie_list.append(temp)

	return movie_list


movie_list = getMovies(URL)

with open(output_filename, 'w') as file:
    file.write("Rank, Title, Year, Rank")
    for movie in movie_list:
        line = '\n' + str(movie.rank) + ', ' + movie.title + ', ' + str(movie.year) + ', ' + str(movie.rating)
        file.write(line)