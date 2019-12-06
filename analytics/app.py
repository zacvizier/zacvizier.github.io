import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import decimal
import warnings
import time

# I was getting an error as a warning that was messing up my app. This suppresses it.
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import the Stats dict from the app_stats file
from app_stats import stats


# Load data from csv
df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1VYoIhAj2MyZIWr72o-Ix2Rd1mHN_NVC5tTF6oUYNPUU/export?format=csv')
# Filter only rows with a valid Id
df = df1[(df1['Id'] > 0)]

# Store a copy of this for when we reset the filters
df_og = df







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
    optionsArr.append({"data":data['checkedOptions'], "name": name, "val": val})

      
    for row in data_row: # Iterate through the data_rows (child object) we just got
        row['name'] = name  # Add the 'name' variable we just got to a new 'name' key value in 
        row['val'] = val
        rows.append(row) # Append the row, now with the "name" value, to the rows array we created earlier

# Iterate through our new rows array and fill out our filterValues array
for data in rows:
    label = data['name'] + ' ' + data['checked'] # The label of the value in the multi-select field will be the name SPACE y or n
    value = data['val'] + ';' + data['checked'] # The actual value (behind the scenes) will have a semicolon delimiter
    filterValues.append({"label": label, "value": value}) # Now just append these two values as an object in the filterValues array

  
# Create a dataframe using the rows array we created out of the Stats object array
d = pd.DataFrame(rows) 
d = d[['val','name', 'checked', 'w', 'l']] # Now we can easily re-order the columns to our liking



# We will save a fresh copy of our dataframe in case we need it later
d_fresh = d.copy()


'''
    Description
    Purpose: Fill out the Stats dataframe, which is the main data displayed to the user
    Inputs: dataStats - fresh stats series, all zeroed out. Use d_fresh.copy() to obtain a fresh copy
            df - BT data set. Does not have to be entire data, can be filtered set
            optionsArr - the function iterates through every item in the BT list, and cycles through every option for each checkbox
                this input is a dictionary containing the name of each column and a list of all possible values.
                use optionsArr by default
    Output: Filtered dataframe, columns ordered properly, with totans and win % and loss %
'''
def fill_stats_arr(dataStats, df, optionsArr):
    start = time.time()
    for rowStats in optionsArr: # For each item in the BT data, iterate through every possible checkbox
        nameTrueVector = (dataStats['name']==rowStats['name'])
        for i in rowStats['data']: # Iterate through every option per checkbox (T or F, sometimes other stuff like R/PB/T)
            condVector = nameTrueVector & (dataStats['checked']==i['val'])
            position = dataStats[condVector].index[0]
            for index, row in df.iterrows(): # Iterate through every item in the BT Data
                if row[rowStats['val']] == i['dataVal']: # If that option matches the BT data...
                    if row['Res'] == 'W' and row['Rec'] == True: # Depending on whether it was a Win or Loss, increment
                        dataStats.iat[position, 3] += 1
                    else:
                        dataStats.iat[position, 4] += 1

                    # if row['Res'] == 'W' and row['Rec'] == True: # Depending on whether it was a Win or Loss, increment
                    #     dataStats.at[dataStats[(dataStats['name']==rowStats['name']) & (dataStats['checked']==i['val'])].index[0], 'w'] += 1
                    # else:
                    #     dataStats.at[dataStats[(dataStats['name']==rowStats['name']) & (dataStats['checked']==i['val'])].index[0], 'l'] += 1
    end = time.time()
    print "total time"
    print (end-start)
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

# Call our function
d = fill_stats_arr(d, df, optionsArr)

# Calculate win percent with current data (/filters)
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
            multi=False,
            value=2.2
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
    
    # if play_val is not None:
    #     for index, row in dataCopy.iterrows():
    #         if row['Play'] == play_val:
    #           meow = 0

    # Store the values from the multi-dropdown in a variable. No reason.
    valArr = search_value

    if (valArr is None):
        newStats = d

    # We got values in our multi-select, now we have to filter the data and return the updated data to the app
    else:
        values = []
        for val in valArr:
            values.append({"val": val[:val.find(';')], "checked": val[val.find(';')+1:]})
        
        
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


    # Now we send this new data to the fill_stats_arr function to give us a new dataframe which we will pass to the output
    newStats = fill_stats_arr(d_fresh_copy, dataCopy, optionsArr)

    #print newStats
    wp = calculateWinPTotal(dataCopy)

    return newStats.to_dict('records'), "Win %: " + str(wp)




if __name__ == '__main__':
    app.run_server(debug=True)