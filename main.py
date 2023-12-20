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

    table = soup.find("table", id = "ContentPlaceHolder1_ProductClassDetail") #extract the table which holds all the chemicals

    #initialize lists to hold relevent data
    CAS = [len(table_rows)]
    productName = [len(table_rows)]
    molecularFormula = [len(table_rows)]

    table_rows = table.find_all("a") #extracts all the rows of the table that use the anchor html tag (all the CAS and product names are wrapped in the anchor tag)


    #extract and append all the CAS numbers and product names into their respective lists
    for chemical in range(len(table_rows)):
        if(chemical%2 == 0):
            CAS.append(table_rows[chemical].text)
            
        else:
            productName.append(table_rows[chemical].text)
            
    table_rows = table.find_all("span") #extracts all the rows of the table that use the span html tag (all the molecular formulas are wrapped in the span tag)
    
    #extract and append all the molecular formulas in its list
    for chemical in range(len(table_rows)):
        molecularFormula.append(table_rows[chemical].text)

    for i in range(len(productName)):
        print(CAS[i], productName[i], molecularFormula[i])