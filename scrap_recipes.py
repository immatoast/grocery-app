# import necessary libraries
import requests
from bs4 import BeautifulSoup 
from collections import defaultdict
import json
import re

# creates dictionary of dictionaries --> nested dictionaries
dataDict = defaultdict(dict) 

## Websites I unsuccessfully tried to webscrap
# website = "https://www.myrecipes.com/favorites#/collection/53424894"
# website = "https://www.foodnetwork.com/recipes/dinner"

links = []
website = f"https://www.nutrition.gov/recipes/search"
webpage = requests.get(website) # API call to website
soup = BeautifulSoup(webpage.content, 'lxml')

li = soup.find_all('li', class_="usa-pagination__item usa-pagination__arrow usa-pagination__page-no")
pages = [l.a.get('href') for l in li]

# Collects recipe urls from all pages on www.nutrition/gov
for p in pages:
    website = "https://www.nutrition.gov/recipes/search" + p
    webpage = requests.get(website) # API call to website
    soup = BeautifulSoup(webpage.content, 'lxml')
    links = links + soup.find_all('a', rel="bookmark")

# Webscraps all recipe urls for recipe name and ingredients
for i in range(len(links)): # rel="bookmark" helps filter out the recipe links
    recipe_link = "https://www.nutrition.gov" + links[i].get('href')
    recipe_page = requests.get(recipe_link) # API call to recipe website
    recipe_soup = BeautifulSoup(recipe_page.content, 'lxml')
    recipe_name = recipe_soup.h1.span.string # Would "get_text" work???
    span = recipe_soup.find_all('span', class_ = "ingredient-name")
    ingr_list = [re.sub(r"(\(.+\))", "",ingr.string) for ingr in span] # list of ingredients for each recipe
    ingr_csv = ", ".join(ingr_list) # convert list to comma-separated values (CSV)
    
    # store data into separate dictionaries
    dataDict['name'][i] = recipe_name 
    dataDict['url'][i] = recipe_link 
    dataDict['ingredients'][i] = ingr_csv
    
print("Total number of recipes:", len(dataDict['name']))

'''Created a json file that holds the recipes data.'''
filename = "recipes.json"
with open(filename, 'w') as f:
    json.dump(dataDict, f) # writes data into a json file
    print("JSON file created.")