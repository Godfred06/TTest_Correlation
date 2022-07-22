import pandas as pd
import numpy as np
import scipy.stats as stats
import re

#Reading in the files
    
nhl_df=pd.read_csv("/Users/Godfred King/Desktop/Python/Data_science/Course 1/Week 4/Assignment/nhl.csv")
nba_df=pd.read_csv("/Users/Godfred King/Desktop/Python/Data_science/Course 1/Week 4/Assignment/nba.csv")
mlb_df=pd.read_csv("/Users/Godfred King/Desktop/Python/Data_science/Course 1/Week 4/Assignment/mlb.csv")
nfl_df=pd.read_csv("/Users/Godfred King/Desktop/Python/Data_science/Course 1/Week 4/Assignment/nfl.csv")
cities=pd.read_html("/Users/Godfred%20King/Desktop/Python/Data_science/Course%201/Week%204/Assignment/wikipedia_data_files/wikipedia_data.html")[1]


cities=cities.iloc[:-1,[0,3,5,6,7,8]]
#Renaming columns in the cities dataframe
cities= cities.rename(columns={'Metroplitan area':'Metropolitan area', 'Population (2016 est.)[8]':'Population'})
def cleaner(cell):
    '''This function cleans up the metropolitan data by removed the [notes nums at the end of the strings] and the –'''
    if cell== '—' or cell is'None':
        return np.nan
    elif re.findall('\[note\s[0-9]+\]',cell):
        str= re.findall('[a-zA-Z0-9]+',(cell))  
        return list(str)[0]
    else:
        return cell
def remove_star(cell):
    '''Function removes the star at the end of the string'''
    if re.findall('\*$|\+$',cell):
        string= re.findall('\w+',cell)
        return ' '.join(string)
    elif re.findall('\*|\([0-9]+',cell) :
        string=re.findall('[A-Z][a-z]+',cell)
        return ' '.join(string)   
    else:
        return cell   

def str_split(cell):
    '''Function takes a cell and finds a pattern of capital letters followed by a number of small letters. 
        With each capital letter being the start of another string''' 
    if re.findall('\s',str(cell)):
        return cell
    elif re.findall('[A-Z0-9][a-z0-9]+', str(cell)):

        new_word=re.findall('[A-Z0-9][a-z0-9]+',str(cell))
        return new_word
    else:
        return cell    

def mlb_split(cell):
    '''This function splits the MLB columns into respective teams for the Metropolitan areas with multiple teams'''
    if re.findall('\s', str(cell)):
        if re.findall('^[A-Z][a-z]+|[A-Z][a-z]+\s[A-Z][a-z]+', str(cell)):
            x= re.findall('^[A-Z][a-z]+|[A-Z][a-z]+\s[A-Z][a-z]+', str(cell))
            return x      
    elif  re.findall('[A-Z][a-z]+', str(cell)):

        new_word=re.findall('[A-Z][a-z]+',str(cell))
        return new_word  
def remove_note(cell):
    if cell == 'note':
        return np.nan
    else:
        return cell
def remove_none(cell):
    '''Replaces None with np.Nan'''
    if cell is None:
        return np.nan
    else:
        return cell  

        
    #Applying cleaner functions   
cities['NFL']= cities['NFL'].apply(lambda x:cleaner(x))
cities['MLB']= cities['MLB'].apply(lambda x:cleaner(x))
cities['NBA']=cities['NBA'].apply(lambda x:cleaner(x))
cities['NHL']= cities['NHL'].apply(lambda x:cleaner(x))
cities['NHL']=cities['NHL'].apply(lambda x:str_split(x))
cities['NBA']= cities['NBA'].apply(lambda x:str_split(x))
cities['MLB']= cities['MLB'].apply(lambda x:mlb_split(x))
cities['NFL']= cities['NFL'].apply(lambda x:str_split(x))

cities['NFL']= cities['NFL'].apply(lambda x:remove_note(x))
cities['MLB']= cities['MLB'].apply(lambda x:remove_note(x))
cities['NBA']=cities['NBA'].apply(lambda x:remove_note(x))
cities['NHL']= cities['NHL'].apply(lambda x:remove_note(x))

cities['MLB']= cities['MLB'].apply(lambda x:remove_none(x))


nhl_df['team']= nhl_df['team'].apply(lambda x: remove_star(x)) 
nhl_df = nhl_df[nhl_df['year']==2018].drop(index=[0,9,18,26]).set_index('team')
nba_df=nba_df[nba_df['year']== 2018 ]   
nba_df['team']= nba_df['team'].apply(lambda x:remove_star(x))
mlb_df= mlb_df[mlb_df['year']==2018].set_index('team')
nfl_df= nfl_df[nfl_df['year']==2018].drop(index=[0,5,10,15,20,25,30,35]).reset_index().drop('index',axis=1)
nfl_df['team']= nfl_df['team'].apply(lambda x: remove_star(x))
nfl_df=nfl_df.set_index('team')
#Renaming nba team in the nba dataframe
nba_df=nba_df.set_index('team')

nba_df=nba_df.rename(index={'Philadelphia':'Philadelphia 76ers'})

#Calculating the win-loss for the 2018 season for the teams in each sport
nba_df['NBA WL-Ratio']= pd.to_numeric(nba_df['W'])/(pd.to_numeric(nba_df['W'])+pd.to_numeric(nba_df['L']))
nba_df= nba_df['NBA WL-Ratio'].reset_index()
nhl_df['NHL WL-Ratio']= pd.to_numeric(nhl_df['W'])/(pd.to_numeric(nhl_df['W'])+pd.to_numeric(nhl_df['L']))
nhl_df= nhl_df['NHL WL-Ratio'].reset_index()
nfl_df['NFL WL-Ratio']= pd.to_numeric(nfl_df['W'])/(pd.to_numeric(nfl_df['W'])+pd.to_numeric(nfl_df['L']))
nfl_df= nfl_df['NFL WL-Ratio'].reset_index()
mlb_df['MLB WL-Ratio']= pd.to_numeric(mlb_df['W'])/(pd.to_numeric(mlb_df['W'])+pd.to_numeric(mlb_df['L']))
mlb_df= mlb_df['MLB WL-Ratio'].reset_index()






#Keeping on the cities with more than 2 teams in different sports.Like they have one team in the NFL and another in the NBA
cities=cities.dropna(thresh=2)

#Creating a dataframe for the NFL teams
cities_nfl = cities[['Metropolitan area','Population','NFL']]\
    .set_index(['Metropolitan area','Population'])\
    .explode('NFL')\
    .reset_index()
#Creating a dataframe for the nba teams
cities_nba=cities[['Metropolitan area','Population','NBA']]\
    .set_index(['Metropolitan area','Population'])\
    .explode('NBA')\
    .reset_index()
    #Creating a dataframe for the MLB teams
cities_mlb=cities[['Metropolitan area','Population','MLB']]\
    .set_index(['Metropolitan area','Population'])\
    .explode('MLB')\
    .reset_index()
    #Creating a dataframe for the NFL teams
cities_nhl=cities[['Metropolitan area','Population','NHL']]\
    .set_index(['Metropolitan area','Population'])\
    .explode('NHL')\
    .reset_index()
#Creating a new column for the team names
cities_nfl['NFL Team Names']= cities_nfl['Metropolitan area']+' '+ cities_nfl['NFL']
cities_nba['NBA Team Names']= cities_nba['Metropolitan area']+' '+ cities_nba['NBA']
cities_mlb['MLB Team Names']= cities_mlb['Metropolitan area']+' '+ cities_mlb['MLB']
cities_nhl['NHL Team Names']= cities_nhl['Metropolitan area']+' '+ cities_nhl['NHL']

#Renaming the teams to their correct and current team names
cities_nfl= cities_nfl.set_index('NFL Team Names')\
    .rename(index={
        'New York City Giants':'New York Giants',
    'New York City Jets':'New York Jets',
    'San Francisco Bay Area 49ers':'San Francisco 49ers',
    'San Francisco Bay Area Raiders':'Oakland Raiders',
    'Dallas–Fort Worth Cowboys':'Dallas Cowboys',
    'Washington, D.C. Redskins':'Washington Redskins',
    'Boston Patriots':'New England Patriots',
    'Minneapolis–Saint Paul Vikings':'Minnesota Vikings',
    'Miami–Fort Lauderdale Dolphins':'Miami Dolphins',
    'Phoenix Cardinals':'Arizona Cardinals',
    'Tampa Bay Area Buccaneers':'Tampa Bay Buccaneers',
    'Charlotte Panthers':'Carolina Panthers',
    'Nashville Titans':'Tennessee Titans'
}).reset_index()

cities_nba=cities_nba.set_index('NBA Team Names')\
    .rename(index={
    'New York City Knicks': 'New York Knicks',
    'New York City Nets':'Brooklyn Nets',
    'San Francisco Bay Area Warriors':'Golden State Warriors',
    'Dallas–Fort Worth Mavericks':'Dallas Mavericks',
    'Washington, D.C. Wizards':'Washington Wizards',
    'Minneapolis–Saint Paul Timberwolves':'Minnesota Timberwolves',
    'Miami–Fort Lauderdale Heat':'Miami Heat',
    'Indianapolis Pacers':'Indiana Pacers',
    'Salt Lake City Jazz':'Utah Jazz',

}).reset_index()

cities_mlb = cities_mlb.set_index('MLB Team Names')\
    .rename(index={
    'New York City Yankees':'New York Yankees',
    'New York City Mets':'New York Mets',
    'San Francisco Bay Area Giants':'San Francisco Giants',
    'San Francisco Bay Area Athletics':'Oakland Athletics',
    'Dallas–Fort Worth Rangers':'Texas Rangers',
    'Washington, D.C. Nationals':'Washington Nationals',
    'Boston Red':'Boston Red Sox',
    'Minneapolis–Saint Paul Twins':'Minnesota Twins',
    'Miami–Fort Lauderdale Marlins':'Miami Marlins',
    'Phoenix Diamondbacks':'Arizona Diamondbacks',
    'Toronto Blue':'Toronto Blue Jays',
    'Tampa Bay Area Rays':'Tampa Bay Rays',
    'Denver Rockies':'Colorado Rockies'
}).reset_index()

cities_nhl=cities_nhl.set_index('NHL Team Names')\
    .rename(index={
    'New York City Rangers':'New York Rangers',
    'New York City Islanders':'New York Islanders',
    'New York City Devils':'New Jersey Devils',
    'Los Angeles Ducks':'Anaheim Ducks',
    'San Francisco Bay Area Sharks': 'San Jose Sharks',
    'Dallas–Fort Worth Stars':'Dallas Stars',
    'Washington, D.C. Capitals':'Washington Capitals',
    'Minneapolis–Saint Paul Wild':'Minnesota Wild',
    'Denver Avalanche':'Colorado Avalanche',
    'Miami–Fort Lauderdale Panthers':'Florida Panthers',
    'Phoenix Coyotes':'Arizona Coyotes',
    'Tampa Bay Area Lightning':'Tampa Bay Lightning',
    'Las Vegas Golden Knights':'Vegas Golden Knights',
    'Raleigh Hurricanes':'Carolina Hurricanes'
}).reset_index()

#Making the final dataframe with teams, metropolitan area, population and the win-loss ratios
nba_df= pd.merge(cities_nba,nba_df, how='left', left_on='NBA Team Names',right_on='team')
nba_df= nba_df[['Metropolitan area','Population','NBA Team Names','NBA WL-Ratio']]
nfl_df=pd.merge(cities_nfl,nfl_df, how='left', left_on='NFL Team Names',right_on='team')
nfl_df= nfl_df[['Metropolitan area','Population','NFL Team Names','NFL WL-Ratio']]
nhl_df= pd.merge(cities_nhl,nhl_df, how='left', left_on='NHL Team Names',right_on='team')
nhl_df= nhl_df[['Metropolitan area','Population','NHL Team Names','NHL WL-Ratio']]
mlb_df= pd.merge(cities_mlb,mlb_df, how='left', left_on='MLB Team Names',right_on='team')
mlb_df= mlb_df[['Metropolitan area','Population','MLB Team Names','MLB WL-Ratio']]

#Combining the teams, population and win-loss ratios on the Metropolitan area that they are found in 
nba_nfl= pd.merge(nba_df, nfl_df, how='outer', on='Metropolitan area')
nhl_mlb= pd.merge(nhl_df, mlb_df, how='outer', on='Metropolitan area')
fulldata= pd.merge(nba_nfl,nhl_mlb, how='outer', on='Metropolitan area')

#Grouping the WL-Ratio by the Metropolitan areas for each of the sports.Fill the NAs with 0
Ratio= fulldata.groupby(by='Metropolitan area').agg({'NBA WL-Ratio':np.average,'NFL WL-Ratio':np.average,'NHL WL-Ratio':np.average,
                                                        'MLB WL-Ratio':np.average})
Ratio =Ratio.rename(columns={'NHL WL-Ratio':'NHL','MLB WL-Ratio':'MLB','NBA WL-Ratio':'NBA','NFL WL-Ratio':'NFL'})
Ratio['NHL']=pd.to_numeric(Ratio['NHL'])
Ratio['NFL']=pd.to_numeric(Ratio['NFL'])
Ratio['MLB']=pd.to_numeric(Ratio['MLB'])
Ratio['NBA']=pd.to_numeric(Ratio['NBA'])

ratio_main= Ratio



#Putting the p-values for the paired sample t-test into a dataframe
sports = ['NFL', 'NBA', 'NHL', 'MLB']
cols =['NFL','NBA','NHL','MLB']
p_values = pd.DataFrame(index=sports,columns=cols)
for sport in sports:
    for column in cols:
        Ratio=Ratio[[sport,column]].dropna()
        p_values.loc[sport,column]=stats.ttest_rel(Ratio[sport],Ratio[column])[1]
        Ratio=ratio_main
        


p_values.loc['NBA','NBA']= np.nan
p_values.loc['NHL','NHL']= np.nan
p_values.loc['NFL','NFL']= np.nan
p_values.loc['MLB','MLB']= np.nan

p_values=p_values.astype('float')
print(p_values)

#Investigating the correlation between the population in the Metropolitan area and average WL-Ratio
#Correlation between the Population and WL-Ratio for the NBA

nba_correlation= fulldata.groupby(by=['Metropolitan area','Population_x_x']).agg({'NBA WL-Ratio':np.average}).dropna().reset_index()
#Converting the population and the WL Ratio dataframes into numeric data
nba_correlation['Population_x_x']= pd.to_numeric(nba_correlation['Population_x_x'])
nba_correlation['NBA WL-Ratio']= pd.to_numeric(nba_correlation['NBA WL-Ratio'])

print(nba_correlation.columns)
#Correlation betweent the Metropolitan area for areas which have NBA teams and the their average win to loss ratio

print(stats.pearsonr(nba_correlation['Population_x_x'],nba_correlation['NBA WL-Ratio']))







