import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import decimal
import warnings
#import numpy as np
warnings.simplefilter(action='ignore', category=FutureWarning)

# Load data from csv
df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1VYoIhAj2MyZIWr72o-Ix2Rd1mHN_NVC5tTF6oUYNPUU/export?format=csv')
# Filter only rows with a valid Id
df = df1[(df1['Id'] > 0)]

# Store a copy of this for when we reset the filters
df_og = df

# Create empty Stats array
# -- Stats includes details for every column in the BT Log
stats = [
    {
        "name": "env",
        "val": "Env",
        "checkedOptions": [{'dataVal': 'R', 'val': 'R'}, {'dataVal': 'T', 'val': 'T'}, {'dataVal': 'PB', 'val': 'PB'}],
        "data": [
            {"checked": 'R', "w": 0, "l": 0},
            {"checked": 'T', "w": 0, "l": 0},
            {"checked": 'PB', "w": 0, "l": 0}]
    },
    {
        "name": "strmv",
        "val": "StrMv",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "imp sr",
        "val": "Imp SR",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "tr sr",
        "val": "Tr SR",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "mjr sr",
        "val": "Mjr SR",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "hllh",
        "val": "HLLH",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    }
    
]

# Create a copy of the Stats *empty* array, in case we need it in the future
baseStats = stats

# Create array of possible play numbers, primed for the Dropdown field
plays = [
    {'label': '2.1', 'value': 2.1},
    {'label': '2.2', 'value': 2.2},
    {'label': '3.1', 'value': 3.1},
    {'label': '3.6', 'value': 3.6},
    {'label': '4.8', 'value': 4.8},
    {'label': '5.8', 'value': 5.8},
    {'label': '7.2', 'value': 7.2},
    {'label': '7.3', 'value': 7.3},
    ]

# Initialize rows, which will be the array that will eventually
#    become the table that we will be looking at
rows = []
optionsArr = []
# filterValues will be the values that will be populated in the multi-select field
#    which is used to filter
filterValues = []
  

# Convert the Stats array of objects into a normal array structure with no children objects
#    We cannot create a table with an array that contains children, pandas doesn't know what to
#     do with them.
for data in stats: 
    data_row = data['data'] # First, we need to get the 'data' child object
    name = data['name'] # We will also need the name and append it, so we know which column it is
    val = data['val']
    checkedOptions = data['checkedOptions']
    #optionsElement
    optionsArr.append({"data":data['checkedOptions'], "name": name, "val": val})
    #optionsArr.append({'naname)
    #optionsArr.append(val)
      
    for row in data_row: # Iterate through the data_rows (child object) we just got
        row['name'] = name  # Add the 'name' variable we just got to a new 'name' key value in 
        row['val'] = val
        rows.append(row) # Append the row, now with the "name" value, to the rows array we created earlier

#print optionsArr

# Iterate through our new rows array and fill out our filterValues array
for data in rows:
    label = data['name'] + ' ' + data['checked'] # The label of the value in the multi-select field will be the name SPACE y or n
    value = data['val'] + ';' + data['checked'] # The actual value (behind the scenes) will have a semicolon delimiter
    filterValues.append({"label": label, "value": value}) # Now just append these two values as an object in the filterValues array

  
# Create a dataframe using the rows array we created out of the Stats object array
d = pd.DataFrame(rows) 
d = d[['val','name', 'checked', 'w', 'l']] # Now we can easily re-order the columns to our liking

#print d

# We will save a fresh copy of our dataframe in case we need it later
d_fresh = d.copy()


# This is where we fill out the array of stats based on whether the cell is checked or not.
# This is a function to do said task.
def fill_stats_arr(dataStats, df, optionsArr):
    for index, row in df.iterrows(): # Iterate through every item in the BT Data
        for rowStats in optionsArr: # For each item in the BT data, iterate through every possible checkbox
            for i in rowStats['data']: # Iterate through every option per checkbox (T or F, sometimes other stuff like R/PB/T)
                if row[rowStats['val']] == i['dataVal']: # If that option matches the BT data...
                    if row['Res'] == 'W' and row['Rec'] == True: # Depending on whether it was a Win or Loss, increment
                        dataStats.at[dataStats[(dataStats['name']==rowStats['name']) & (dataStats['checked']==i['val'])].index[0], 'w'] += 1
                    else:
                        dataStats.at[dataStats[(dataStats['name']==rowStats['name']) & (dataStats['checked']==i['val'])].index[0], 'l'] += 1

        
    # Set a new column 't' (total) to zero for every row
    dataStats['t']=0
    dataStats['wp']="..." # We will calculate the wp (win percent) and lp (loss percent) columns
    dataStats['lp']="..."
    decimal.getcontext().prec = 4 # 4 digits of precision (INCLUDING digits before the decimal


    # Calculate and add total, use that to calculate WP and LP and update the dataframe
    for index, row in dataStats.iterrows():
        total = row['w'] + row['l']
        if total != 0:
            dataStats.at[index, 't'] = total
            dataStats.at[index, 'wp'] = decimal.Decimal(row['w']) / decimal.Decimal(total)*100
            dataStats.at[index, 'lp'] = decimal.Decimal(row['l']) / decimal.Decimal(total)*100
        else:
            dataStats.at[index, 't'] = 0
            dataStats.at[index, 'wp'] = 0
            dataStats.at[index, 'lp'] = 0
    # Re-order the columns to our liking
    dataStats = dataStats[['val', 'name', 'checked', 'w','wp', 'l','lp','t']]
    return dataStats
    #print(dataStats)

# Call our function
d = fill_stats_arr(d, df, optionsArr)

def calculateWinPTotal(data):
    numWins = 0
    for index, row in data.iterrows():
        if row['Res'] == 'W' and row['Rec'] == True:
            numWins += 1
        
    decimal.getcontext().prec = 4 # 4 digits of precision (INCLUDING digits before the decimal


    return round(float (numWins) / float(len(data.index)),3)*100

initial_wp = calculateWinPTotal(df)




app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='filterSelect',
            options=filterValues,
            multi=True
        )
    ],style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
            id='playSelect',
            options=plays,
            multi=False
        )
    ],style={'width': '10%', 'display': 'inline-block'}),
    html.Div(id='text-stats'),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False} for i in d.columns
        ],
        data=d.to_dict('records'),
        column_selectable="multi",
        #selected_columns=[],
        #selected_rows=[],
        sort_action='native',
        page_action="native",
        page_current= 0,
        page_size= 100,
        #filter_action="native"
        style_cell_conditional=[
            {
            'if': {'column_id': c},
            'display': 'none'
            } for c in ['val']
            ],
    )
])


@app.callback(
    [dash.dependencies.Output("datatable-interactivity", "data"),
    dash.dependencies.Output("text-stats", 'children')],
    [dash.dependencies.Input("filterSelect", "value"),
    dash.dependencies.Input("playSelect", "value")]
)
def update_table(search_value, play_val):
    global df #Data (actual backtest data)
    global d_fresh #Stats
    global optionsArr # Array of options needed to update stats

    # Make a copy of the ORIGINAL data
    d_fresh_copy = d_fresh.copy()
    dataCopy = df.copy()

    if play_val is not None:
        dataCopy = dataCopy[dataCopy['Play'] == play_val]


    # Store the values from the multi-dropdown in a variable. No reason.
    valArr = search_value

    if (valArr is None):
        newStats = d

    # We got values in our multi-select, now we have to filter the data and return the updated data to the app
    else:
        values = []
        for val in valArr:
            values.append({"val": val[:val.find(';')], "checked": val[val.find(';')+1:]})
        #print values

        
        
        # Iterate through every multi-select value, get the value for "Checked" and filter the list based on it
        for i in values:
            if i['checked'] == 'y':
                dataCopy = dataCopy[dataCopy[i['val']]==True]
            elif i['checked'] == 'n':
                dataCopy = dataCopy[dataCopy[i['val']]==False]
            elif i['checked'] == 'R':
                dataCopy = dataCopy[dataCopy[i['val']]=="R"]
            elif i['checked'] == 'PB':
                dataCopy = dataCopy[dataCopy[i['val']]=="PB"]
            elif i['checked'] == 'T':
                dataCopy = dataCopy[dataCopy[i['val']]=="T"]


    newStats = fill_stats_arr(d_fresh_copy, dataCopy, optionsArr)

    print newStats
    wp = calculateWinPTotal(dataCopy)    

    return newStats.to_dict('records'), "Win %: " + str(wp)

    ## TODO - left off here
    # add more columns

    # also, the opposite row in the dataframe is all 0's. that's fine, technically that's correct behavior, 
    # but maybe i should highlight it so i know to ignore it? 
    #    as if all 0's isn't obvious enough
    # one thing is for sure, i should highlight what i AM filtering
    # also, i might have an issue with stuff that don't have a 'y' or 'n' "checked" value. such as Env. anything that isn't true or false needs
    #   to be handled separately.
    # another potential tricky thing will be handling the play #

    # last question - how fast will this be with more columns? Will it be faster than power bi and can i improve the performance/efficiency.

    #maybe filter the rows with all 0's to the bottom if possible, so they don't take up screen space

    # wins should not be based on Res='W', it should be based on Rec = TRUE
    # or maybe i should update my stats objects to include the other various options






if __name__ == '__main__':
    app.run_server(debug=True)