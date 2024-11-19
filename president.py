import os
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({'font.size': 6})
plt.rcParams['figure.figsize'] = [6, 6]

def create_df():
    path = os.path.join("C:\\", "Users", "Amith", "Documents", "projects", "president", "data.csv")
    df = pd.read_csv(path)
    return df
    
def process_df(df):
    #Drop useless columes, rename mode -> vote_type, remove non-partisan parties
    df = df.drop(columns=['state_po', 'county_fips', 'office', 'version'])
    df = df.rename(columns={"mode" : "vote_type"})
    df.drop(df[df.party == 'GREEN'].index, inplace=True)
    df.drop(df[df.party == 'LIBERTARIAN'].index, inplace=True)
    df.drop(df[df.party == 'OTHER'].index, inplace=True)
    df = df.dropna(axis=1, how='all')

    #Define types
    df = df.astype({'year' :  str, 'state' : str, 'county_name' : str, 'candidate' : str, 'party' : str, 'candidatevotes' : int, 'totalvotes' : int, 'vote_type' : str})

    #Combine votes if vote_type is not total
    df = df.groupby(['year', 'state', 'county_name', 'candidate', 'party', 'totalvotes'], as_index=False)['candidatevotes'].sum()

    #Calculate candidates/parties vote percentage
    df['percentage'] = (df['candidatevotes']/df['totalvotes'])
    df['percentage'] = df['percentage'].round(2)
    
    return df

def group_by_states(df):
    #Get unqiue list of states and years
    years = df['year'].unique()
    states = df['state'].unique()

    #Create list (each element will be dict, see vote_dist.json)
    vote_dist = []
    
    #Loop through years
    for year in years:
        for state in states:
            #For each state get total number of votes
            total_votes_in_state = int(df.loc[(df['state'] == state) & (df['year'] == year) & (df['party'] == 'DEMOCRAT'), 'totalvotes'].sum())
            #For each state get total number of Democrat votes
            total_dem_votes_in_state = int((df.loc[(df['state'] == state) & (df['year'] == year) & (df['party'] == 'DEMOCRAT'), 'candidatevotes'].sum()))
            #For each state get total number of republican votes
            total_rep_votes_in_state = int((df.loc[(df['state'] == state) & (df['year'] == year) & (df['party'] == 'REPUBLICAN'), 'candidatevotes'].sum()))
            #Add entry for each state for each years with total votes and percentage of votes of each party
            vote_dist.append({
                'state' : state, 'year' : str(year),  
                'democrat_percent' : round(total_dem_votes_in_state/total_votes_in_state, 2),
                'republican_percent' : round(total_rep_votes_in_state/total_votes_in_state, 2),
                'total_votes' : total_votes_in_state
            })
        
        #Output to JSON
        if (os.path.isfile('vote_dist.json')): os.remove('vote_dist.json')
        with open('vote_dist.json', 'w') as fp:
            json.dump(vote_dist, fp)
            
    return vote_dist

def get_state_votes_by_year_and_state(year, state, state_votes):
    #Small function for pulling vote distribution between dems and reps for a given year and state
    state_votes_filtered_by_state = [item for item in state_votes if item["state"] == state]
    for entry in state_votes_filtered_by_state:
        if entry['year'] == year:
            #Returns dict containing year, total votes that year, Democrat percentage, Replublican percentage
            return entry

def compare_county_to_state_by_year(df, state_votes):
    state_name = 'ARIZONA'
    
    #Get list of years to loop through
    years = df['year'].unique()
    
    #Co-ordinates for subplots
    x, y = 0, 0
    
    #Setup figure + sublpots
    figure, axis = plt.subplots(3, 2)
    figure.suptitle('Vote Distribution Between Democrat and Republican of a state and its counties', fontsize=16)
    
    #Loop though years
    for year in years:
        #Separate Democrat and Republican stats for easier processing
        df_dem = df.loc[(df['party'] == 'DEMOCRAT') & (df['year'] == year) & (df['state'] == state_name)]
        df_rep = df.loc[(df['party'] == 'REPUBLICAN') & (df['year'] == year) & (df['state'] == state_name)]
        
        ##Returns dict containing year, total votes that year, Democrat percentage, Replublican percentage
        state_votes_individual = get_state_votes_by_year_and_state(year, state_name, state_votes)
        
        #Get list of county names and add _DEM to it
        plot_x_dem = df_dem['county_name'].tolist()
        plot_x_dem = [x + '_DEM' for x in plot_x_dem]
        #Get list of percentage values
        plot_y_dem = df_dem['percentage'].tolist()
        
        #Get list of county names and add _DEM to it
        plot_x_rep = df_rep['county_name'].tolist()
        plot_x_rep = [x + '_REP' for x in plot_x_rep]
        #Get list of percentage values
        plot_y_rep = df_rep['percentage'].tolist()
        
        #Create another series of 2 data points - vote distribution of parties on state level
        plot_x_state = ['ARIZONA_DEM', 'ARIZONA_REP']
        plot_y_state = [float(state_votes_individual['democrat_percent']), float(state_votes_individual['republican_percent'])]
        
        #Plot series for state data
        axis[x, y].barh(plot_x_state, plot_y_state, color = 'Black')
        
        #Plot series for Democrat data
        axis[x, y].barh(plot_x_dem, plot_y_dem, color ='Blue')
        
        #Plot series for Republican data
        axis[x, y].barh(plot_x_rep, plot_y_rep, color = 'Red')
        
        #Plot appearance
        axis[x, y].grid(color = 'green', linestyle = '--', linewidth = 0.5)
        axis[x, y].set_title(state_name + ' ' + year)
        xticks = np.arange(0.0, 1.1, 0.1)
        xlabels = [str(round(x, 1)) for x in xticks]
        axis[x,y].set_xticks(xticks, labels=xlabels)
        axis[x,y].set_facecolor('xkcd:light grey')
        
        #Logic for incrementing co-ordinates of next subplot (0,0 - 0,1 - 1,0 - 1,1 etc.)
        if y == 0:
            y = y + 1
        elif y == 1:
            x = x + 1
            y = 0
    
    #Plot appearance
    plt.legend(prop={'size': 6})
    plt.xlabel("State/County")
    plt.show(block=False)
        
def compare_county_to_state_difference(df, state_votes):
    state_name = 'ARIZONA'
    
    #Get list of years to loop through
    years = df['year'].unique()
    
    #Co-ordinates for subplots
    x, y = 0, 0
    
    #Setup figure + sublpots
    figure, axis = plt.subplots(3, 2)
    figure.suptitle('Difference between What Percentage of Votes Were for a Party Compared to the Overall State', fontsize=16)
    
    #Loop though years
    for year in years:
        #Separate Democrat and Republican stats for easier processing
        df_dem = df.loc[(df['party'] == 'DEMOCRAT') & (df['year'] == year) & (df['state'] == state_name)]
        df_rep = df.loc[(df['party'] == 'REPUBLICAN') & (df['year'] == year) & (df['state'] == state_name)]
        
        #Returns dict containing year, total votes that year, Democrat percentage, Replublican percentage
        state_votes_for_year = get_state_votes_by_year_and_state(year, state_name, state_votes)
        
        #Get list of county names and add _DEM to it
        plot_x_dem = df_dem['county_name'].tolist()
        plot_x_dem = [x + '_DEM' for x in plot_x_dem]
        
        #Get list of county names and add _REP to it
        plot_x_rep = df_rep['county_name'].tolist()
        plot_x_rep = [x + '_REP' for x in plot_x_rep]
        
        #Gets percentage of votes for Democrats and Replicans at state level
        total_dem_votes = float(state_votes_for_year['democrat_percent'])
        total_rep_votes = float(state_votes_for_year['republican_percent'])
        
        #Gets list of percentage of votes for each party (one entry for each county), hen subtracts it from what the party achieved at state level
        plot_y_dem = df_dem['percentage'].tolist()
        plot_y_dem = [(total_dem_votes - x)*100 for x in plot_y_dem]
        plot_y_rep = df_rep['percentage'].tolist()
        plot_y_rep = [(total_rep_votes - x)*100 for x in plot_y_rep]

        #Plot Democrat and Replican stats
        axis[x, y].barh(plot_x_dem, plot_y_dem, color ='Blue')
        axis[x, y].barh(plot_x_rep, plot_y_rep, color = 'Red')
        
        #Plot appearance
        axis[x, y].grid(color = 'green', linestyle = '--', linewidth = 0.5)
        axis[x, y].set_title(state_name + ' ' + year)
        min_value = min(plot_y_dem + plot_y_rep)
        max_value = max(plot_y_dem + plot_y_rep)
        xticks = np.arange(int(min_value), int(max_value), 1)
        xlabels = [str(x) for x in xticks]
        axis[x,y].set_xticks(xticks, labels=xlabels)
        axis[x,y].set_facecolor('xkcd:light grey')

        #Logic for incrementing co-ordinates of next subplot (0,0 - 0,1 - 1,0 - 1,1 etc.)
        if y == 0:
            y = y + 1
        elif y == 1:
            x = x + 1
            y = 0
            
    #Plot appearance
    plt.legend(prop={'size': 6})
    plt.show(block=False)
        
        
        
    

def main():
    #Create DF from CSV
    df = create_df()
    
    #Process/satinize df
    df = process_df(df)
    
    #Sumarize votes by year and county for each state - see vote_dist.json
    state_votes = group_by_states(df)
    
    #Compare vote distribution between between a given county compared to its state for a given year
    compare_county_to_state_by_year(df, state_votes)
    
    #Difference Between What Percentage of Votes Were for a Party Compared to the Overall State
    compare_county_to_state_difference(df, state_votes)
    
    pause = input("Press Enter to exit")


if __name__ == '__main__':
    main()