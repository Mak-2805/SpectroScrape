import requests
import pandas as pd
from bs4 import BeautifulSoup
import warnings
from airtable import airtable
import time
import random


df = pd.DataFrame(columns=["CAS", "Product Name", "Molecular Formula", "Graph1", "Graph2", "Graph3", "Graph4", "Graph5", "Graph 6", "Graph 7", "Graph 8"])

#Note there are 1058 pages of data to scrape
for page in range(2):
    #download contents of the pages and create BeautifulSoup object
    url = f"https://www.chemicalbook.com/CASDetailList_{page*100}_EN.htm"
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")

