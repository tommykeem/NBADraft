## needed libraries
from urllib.request import urlopen, urlcleanup
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode
import requests
import time

### error checking package
import sys

### In order for this code to run as designed there needs to be a column in the dataset
# That is title FNAME which contains the text string needed to be entered for there
# College statistics url defined in the function. The string is formatted as
# "[First name]-[last name]-1" for a majority of players.
#I created this column using Google Sheets and then loaded this data below

draftdf = pd.read_csv('/Users/pauly/Desktop/Github/NBADraft/jarrett_batch.csv')
player_names = []
for player in draftdf['FNAME']:
    name = ''
    if isinstance(player, str):
        temp = player
        name = str(player.replace("Jr.", "")) # Remove name suffix and spaces between multiple words last names. #
        name = str(player.replace("Sr.", ""))
        player_names.append([unidecode(name.replace(" ", "").lower()), temp])
    else:
        player_names.append([None, None])
print(player_names)

# Create function to collect data from basketball-reference URL
def scrape_college_data(names=[]):
    stats = []
    for name in names:
        try:
            name[0] += '-1'
            player_name = name[0]
            urlcleanup()
            url = f"http://www.sports-reference.com/cbb/players/{player_name}.html"
            html = urlopen(url)
            soup= BeautifulSoup(html, features = 'lxml')
            soup_table = soup.find(name = 'table', attrs = {'id' : 'players_per_game'})


            # get rows from table
            for row in soup_table.find_all('tr')[-1:]: # Excluding the first 'tr', since that's the table's title head
                player = {}
                player['Player']= (draftdf['Player'].loc[draftdf['FNAME'] == name[1]]).item()
                player['College_Season'] = row.find('th', {'data-stat' : 'season'}).text
                player['College'] = row.find('td', {'data-stat' : 'school_name'}).text
                player['College_Games_Played'] = row.find('td', {'data-stat' : 'games'}).text
                player['College_Games_Started'] = row.find('td', {'data-stat' : 'games_started'}).text
                player['College_Field_Goals_Made_Per_Game'] = row.find('td', {'data-stat' : 'fg_per_g'}).text
                player['College_Field_Goals_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fga_per_g'}).text
                player['College_FG%'] = row.find('td', {'data-stat' : 'fg_pct'}).text
                player['College_2PT_Field_Goals_Made_Per_Game'] = row.find('td', {'data-stat' : 'fg2_per_g'}).text
                player['College_2PT_Field_Goals_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fg2a_per_g'}).text
                player['College_2PT_FG%'] = row.find('td', {'data-stat' : 'fg2_pct'}).text
                player['College_3PT_Field_Goals_Made_Per_Game'] = row.find('td', {'data-stat' : 'fg3_per_g'}).text
                player['College_3PT_Field_Goals_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fg3a_per_g'}).text
                player['College_3PT_FG%'] = row.find('td', {'data-stat' : 'fg3_pct'}).text
                player['College_Free_Throws_Made_Per_Game'] = row.find('td', {'data-stat' : 'ft_per_g'}).text
                player['College_Free_Throws_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fta_per_g'}).text
                player['College_FT%'] = row.find('td', {'data-stat' : 'ft_pct'}).text
                player['Offensive_Rebounds_pergame'] = row.find('td', {'data-stat' : 'orb_per_g'}).text
                player['Defensive_Rebounds_pergame'] = row.find('td', {'data-stat' : 'drb_per_g'}).text
                player['Total_Rebounds_pergame'] = row.find('td', {'data-stat' : 'trb_per_g'}).text
                player['Assists_pergame'] = row.find('td', {'data-stat' : 'ast_per_g'}).text
                player['Steals_pergame'] = row.find('td', {'data-stat' : 'stl_per_g'}).text
                player['Blocks_pergame'] = row.find('td', {'data-stat' : 'blk_per_g'}).text
                player['Turnovers_pergame'] = row.find('td', {'data-stat' : 'tov_per_g'}).text
                player['Fouls_pergame'] = row.find('td', {'data-stat' : 'pf_per_g'}).text
                player['Points_pergame'] = row.find('td', {'data-stat' : 'pts_per_g'}).text
                player['Team_strength_of_schedule'] = row.find('td', {'data-stat' : 'sos'}).text
                stats.append(player)
            time.sleep(10)


#Adding an exception to view any errors when collecting data for each player
        except:
            print('For player: ',name[0], sys.exc_info())
#Collecting data into dataframe then placing into a csv file
    df=pd.DataFrame(stats)
    print(df)
    df.to_csv('college_statistics_kendall.csv')

scrape_college_data(player_names)