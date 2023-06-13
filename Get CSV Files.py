from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

###
#Scrape through NBA draft data until the most recent season

#Columns for final dataset
draft_columns=['Pk', 'Tm', 'Player', 'College', 'Yrs', 'G', 'MP', 'PTS', 'TRB', 'AST', 'FG%', '3P%', 'FT%', 'MP', 'PTS', 'TRB', 'AST', 'WS', 'WS/48', 'BPM', 'VORP']

def scrape_draft_data(years=[2017,2018]):
    final_df=pd.DataFrame(columns=draft_columns)

    for y in years:
        #Draft year to scrape
        year = y
       #Placing string url string with year being iterable
        url = f"https://www.basketball-reference.com/draft/NBA_{year}.html"
        html = urlopen(url)
        soup= BeautifulSoup(html, features = 'lxml')
        # get rows from table (tr denotes table rows, td is table data)
        rows = soup.findAll('tr')[0:] # Removes Rk
        rows_data = [[td.getText() for td in rows[i].findAll('td')]
                     for i in range(len(rows))]
        #placing data in a DataFrame
        df_1 = pd.DataFrame(rows_data,columns=draft_columns)
        print(df_1)
        # merge data frames
        final_df=pd.concat([final_df,df_1])
        print(final_df)
#Export data to csv file
    final_df.to_csv("nba_draft_data.csv", index=False)

###Calling function with the draft years I want data from
scrape_draft_data(years=[2000,2001,2002,2003,2004,2005,2006,2007,
                         2008,2009,2010,2011,2012,2013,2014,2015,
                         2016,2017,2018,2019, 2020, 2021])