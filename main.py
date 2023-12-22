import requests
import pandas as pd
from bs4 import BeautifulSoup
import warnings
from airtable import airtable
import time
import random



warnings.simplefilter(action='ignore', category=FutureWarning) #surpress warnings

df = pd.DataFrame(columns=["CAS", "Product Name", "Molecular Formula", "Graph1", "Graph2", "Graph3", "Graph4", "Graph5", "Graph6", "Graph7", "Graph8"])
casFiltered = []
pnFiltered = []
mfFiltered = []

#Note there are 1058 pages of data to scrape
firstPage = int(input("Which page from 1-1058 would you like to begin scraping spectroscopy data")) - 1
lastPage = int(input("What page would you like to go up to (note that this page will not be included)")) - 1

#perliminary error check on page pounds
while firstPage < 1 or firstPage > 1058 or lastPage < 0 or lastPage > 1059 or firstPage > lastPage:
    print("invalid page selection")

for page in range(firstPage, lastPage):
    #download contents of the pages and create BeautifulSoup object
    url = f"https://www.chemicalbook.com/CASDetailList_{page*100}_EN.htm"
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")

    table = soup.find("table", id = "ContentPlaceHolder1_ProductClassDetail") #extract the table which holds all the chemicals

    

    table_rows = table.find_all("a") #extracts all the rows of the table that use the anchor html tag (all the CAS and product names are wrapped in the anchor tag)

    #initialize lists to hold relevent data
    CAS = [len(table_rows)]
    productName = [len(table_rows)]
    molecularFormula = [len(table_rows)]

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

    #remove all chemicals without a spectroscopy webpage
    for cas in range(len(table_rows)):
        r = requests.get(f"https://www.chemicalbook.com/SpectrumEN_{CAS[cas]}_MS.htm")
        print(r.status_code, cas, CAS[cas])
        if(not(r.status_code < 400 and r.status_code >= 200)):
            CAS[cas] = None
            productName[cas] = None
            molecularFormula[cas] = None
            
        time.sleep(random.randint(0, 3))

    while None in CAS:
        # removing None from list using remove method
        CAS.remove(None)
        productName.remove(None)
        molecularFormula.remove(None)
    
    #create list to store the filtered data and remove garbage data in the last entry
    CAS = CAS[0:len(CAS)-1]
    productName = productName[0:len(productName)-1]
    molecularFormula = molecularFormula[0:len(molecularFormula)-1]

    casFiltered.extend(CAS)
    pnFiltered.extend(productName)
    mfFiltered.extend(molecularFormula)

#append the CAS number, product name, and molecular formula to the pandas dataframe
for i in range(len(casFiltered)):
        df = df.append({"CAS":casFiltered[i], "Product Name": pnFiltered[i], "Molecular Formula": mfFiltered[i],
                    }, ignore_index = True)

for page in range(firstPage, lastPage):
    
    #extract spectroscopy data and add it to the dataframe
    row = 0
    for i in range(len(casFiltered)):
        spectroPage = requests.get(f"https://www.chemicalbook.com/SpectrumEN_{casFiltered[i]}_MS.htm").text

        soup = BeautifulSoup(spectroPage, "html.parser")

        images = soup.find_all("img", class_ = "cursorimg")

        for img in range(0,len(images)): 
            print(images[img]['src'])
            df.iat[row, img+3] = images[img]['src']
        row += 1
        time.sleep(random.randint(0, 3))
    
df_cleaned = df.fillna('')  # Replace NaN values with empty string

csv_file_path = 'database.csv'
df.to_csv(csv_file_path, index=False)
