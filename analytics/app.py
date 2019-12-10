import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import decimal
import warnings
import time

import textwrap

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

times = [6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5]

timeStats = []

for i in times:
    timeStats += [{'val': i, 'w': 0, 'l': 0}]

timeStatsDF = pd.DataFrame(timeStats) 
timeStatsDF = timeStatsDF[['val', 'w', 'l']]
timeStatsBackup = timeStatsDF.copy()


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


##############################################################
################## Time Stats Array Funct ####################
##############################################################
def fill_time_arr(timeStatsDF, df):
    for index, row in df.iterrows():
        if row['Res'] == 'W' and row['Rec'] == True:
            timeStatsDF.at[timeStatsDF[timeStatsDF['val']==row['Time']].index[0], 'w'] += 1
        else:
            timeStatsDF.at[timeStatsDF[timeStatsDF['val']==row['Time']].index[0], 'l'] += 1

    timeStatsDF['t']=0
    timeStatsDF['wp']="..." # We will calculate the wp (win percent) and lp (loss percent) columns
    timeStatsDF['lp']="..."
    decimal.getcontext().prec = 4 # 4 digits of precision (INCLUDING digits before the decimal


    # Calculate and add total, use that to calculate WP and LP and update the dataframe
    for index, row in timeStatsDF.iterrows():
        total = row['w'] + row['l']
        if total != 0:
            timeStatsDF.at[index, 't'] = total
            timeStatsDF.at[index, 'wp'] = decimal.Decimal(row['w']) / decimal.Decimal(total)*100
            timeStatsDF.at[index, 'lp'] = decimal.Decimal(row['l']) / decimal.Decimal(total)*100
        else:
            timeStatsDF.at[index, 't'] = 0
            timeStatsDF.at[index, 'wp'] = 0
            timeStatsDF.at[index, 'lp'] = 0

    # Re-order the columns to our liking
    timeStatsDF = timeStatsDF[['val','w','wp', 'l','lp','t']]
    return timeStatsDF


##############################################################
################### Stats Array Funct ########################
##############################################################
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
    dataStats = dataStats[[ 'name', 'val','checked', 'w','wp', 'l','lp','t']]
    return dataStats


#############################################################
############### Calculate Wins/Total/Win% ###################
#############################################################
# Calculate win percent with current data (/filters)
def calculateWinPTotal(data):
    numWins = 0
    for index, row in data.iterrows():
        if row['Res'] == 'W' and row['Rec'] == True:
            numWins += 1
        
    decimal.getcontext().prec = 4 # 4 digits of precision (INCLUDING digits before the decimal
    return {"numWins": numWins,"wp": round(float (numWins) / float(len(data.index)),3)*100}

#############################################################
###################### Get TP Data ##########################
#############################################################
def getTPData(data):
    tpData = {'ins': 0, 'hl': 0, 'slightpasthl': 0, 'pasthl': 0}
    for index, row in data.iterrows():
        if row['Ins'] == True:
            tpData['ins'] += 1
        elif row['HL'] == True:
            tpData['hl'] += 1
        elif row['Slight Past HL'] == True:
            tpData['slightpasthl'] += 1
        elif row['Past HL'] == True:
            tpData['pasthl'] += 1
    pieData = [
        {
            'values': [tpData['ins'], tpData['hl'], tpData['slightpasthl'], tpData['pasthl']],
            'labels': ['Ins', 'HL', 'SlightPastHL', 'PastHL'],
            'type': 'pie',
            'hoverinfo':'label',
            'textinfo': 'value+percent',
            'marker': dict(colors=['#ff6e6e', '#ffce63', '#fcfc9d', '#dafaa2']),
        },
    ]
    return pieData



############## Call our functions ####################
d = fill_stats_arr(d, df, optionsArr)
timeStatsDF = fill_time_arr(timeStatsDF, df)
wpTotal = calculateWinPTotal(df)
initial_wp = wpTotal["wp"]
numWins = wpTotal["numWins"]
tpData = getTPData(df)

initial_figure_data = dict(
            data=tpData,
            layout=dict(
                title='TP Location',
                showlegend=False,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )


###########################################################
###################### Main Layout ########################
###########################################################

app = dash.Dash(__name__)
app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='filterSelect',
            options=filterValues,
            multi=True,
            value=[]
        )
    ],style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
            id='playSelect',
            options=plays,
            multi=False,
            value=2.2
        ),
    ],style={'width': '10%', 'display': 'inline-block'}),
    html.Div([
        html.Button('Reset Filters', id='reset-button', style={
            "box-shadow":"inset 0px 1px 0px 0px #dcecfb",
            "background":"linear-gradient(to bottom, #bddbfa 5%, #80b5ea 100%)",
            "background-color":"#bddbfa",
            "border-radius":"6px",
            "border":"1px solid #84bbf3",
            "display":"inline-block",
            "cursor":"pointer",
            "color":"#ffffff",
            "font-family":"Arial",
            "font-size":"15px",
            "font-weight":"bold",
            "padding":"6px 24px",
            "text-decoration":"none",
            "text-shadow":"0px 1px 0px #528ecc",
            'position': 'relative',
            'margin-left': '10px',
            'bottom': '13px',
            'height': '35px',
        }),
    ],style={'width': '10%', 'display': 'inline-block'}),
    html.Div(id='text-stats'),
    # html.Div([
    #     html.Div('Loading...')
    # ], id='loading', style={'background-color': 'red'}),
    html.Div([
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
            filter_action="native",
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'width': '10%'
                } for c in d.columns
            ],
            style_data_conditional=[]
        )
    ],id='table-div',style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dash_table.DataTable(
            id='datatable-time',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in timeStatsDF.columns
            ],
            data=timeStatsDF.to_dict('records'),
            column_selectable="multi",
            sort_action='native',
            page_action="native",
            page_current= 0,
            page_size= 100,
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'width': '10%'
                } for c in timeStatsDF.columns
            ],
            style_data_conditional=[]
        ),
        dcc.Graph(
            figure=initial_figure_data,
            style={'height': '300px', 'width': '300px'},
            id='tp-pie-graph'
        ),
    ],id='time-div',style={'width': '48%','position': 'relative', 'left': '3%', 'display': 'inline-block'}),
    html.Div(id='placeholder1'),
])


#############################################################
################### Main App Callbacks ######################
#############################################################
@app.callback(
    [dash.dependencies.Output("datatable-interactivity", "data"),
    dash.dependencies.Output("datatable-time", "data"),
    dash.dependencies.Output("text-stats", 'children'),
    dash.dependencies.Output("tp-pie-graph", "figure")],
    #Output("datatable-interactivity", "style_data_conditional"),
    [dash.dependencies.Input("filterSelect", "value"),
    dash.dependencies.Input("playSelect", "value")]
    #Input("datatable-interactivity", "style_data_conditional")]
)
def update_table(search_value, play_val):
    global df #Data (actual backtest data)
    global d_fresh #Stats
    global optionsArr # Array of options needed to update stats
    global timeStatsBackup # Zeroed out timeStatsDF
    

    #print "style data"
    #print style_data

    # Make a copy of the ORIGINAL data
    d_fresh_copy = d_fresh.copy()
    dataCopy = df.copy()
    timeCopy = timeStatsBackup.copy()


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


    # Now we send this new data to the stats update functions.
    # Stats DF must be fresh copy
    newStats = fill_stats_arr(d_fresh_copy, dataCopy, optionsArr)
    timeStatsNew = fill_time_arr(timeCopy, dataCopy)

    # Calculate WP and totals which we will send to the div
    wpTotal=calculateWinPTotal(dataCopy)
    wp = wpTotal["wp"]
    numWins = wpTotal["numWins"]
    total = len(dataCopy.index)

    #get TP data for pie chart
    tpData = getTPData(dataCopy)
    tpFigure = dict(
            data=tpData,
            layout=dict(
                title='TP Location',
                marker_colors = ['red', 'orange', 'yellow', 'green'],
                showlegend=False,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        )

    return newStats.to_dict('records'), timeStatsNew.to_dict('records'), "Win %: " + str(wp) + " --- NumWins: " + str(numWins) + " --- Total: " + str(total), tpFigure



################# Reset Filters button #################
@app.callback(
    dash.dependencies.Output("filterSelect", 'value'),
    [dash.dependencies.Input('reset-button', 'n_clicks')]
)
def reset_filter(n_clicks):
    return []


#############################################################
############ Main Table Cell Click Callback #################
#############################################################
@app.callback(
    Output("datatable-interactivity", "style_data_conditional"),
    [Input('datatable-interactivity', 'active_cell'),
    Input("datatable-interactivity", "data")])
def highlight_row(active_cell,data):
    wpColors = []
    for row in data:
        wpColors.append('#e5ffcf')
        # if row[u'wp'] > 57.5:
        #     wpColors.append('#a8fc9d')
        # elif row[u'wp'] > 52:
        #     wpColors.append('#eefaa2')
        # else:
        #     wpColors.append('#ffd294')

        
    row_indices = list(range(0,len(data), 1))
    if active_cell is None:
        rowUpdate = []
    else:
        rowUpdate = [{'if': {'row_index': active_cell['row']},'backgroundColor': 'pink'}]
        if active_cell['row'] in row_indices: 
            row_indices.remove(active_cell['row'])


    altColor =[{
        'if': {'row_index': 'odd', 'column_id': c},
        'backgroundColor': 'rgb(245, 245, 245)'
    } for c in ['name','val','checked', 'w', 'l', 'lp', 't']]
    wpColor = [{
        'if': {'row_index': r, 'column_id': 'wp'},
        'backgroundColor': wpColors[r]
    } for r in row_indices] #range(0,len(data), 1)]
    

    fullStyle = altColor + rowUpdate + wpColor
    return fullStyle




############## Time styles ################
@app.callback(
    Output("datatable-time", "style_data_conditional"),
    [Input('datatable-time', 'active_cell'),
    Input("datatable-time", "data")])
def highlight_row(active_cell, data):
    wpColors = []
    for row in data:
        wpColors.append('#e5ffcf')
        # if row[u'wp'] > 57.5:
        #     wpColors.append('#a8fc9d')
        # elif row[u'wp'] > 52:
        #     wpColors.append('#eefaa2')
        # else:
        #     wpColors.append('#ffd294')

        
    row_indices = list(range(0,len(data), 1))
    if active_cell is None:
        rowUpdate = []
    else:
        rowUpdate = [{'if': {'row_index': active_cell['row']},'backgroundColor': 'pink'}]
        if active_cell['row'] in row_indices: 
            row_indices.remove(active_cell['row'])


    altColor =[{
        'if': {'row_index': 'odd', 'column_id': c},
        'backgroundColor': 'rgb(245, 245, 245)'
    } for c in ['name','val','checked', 'w', 'l', 'lp', 't']]
    wpColor = [{
        'if': {'row_index': r, 'column_id': 'wp'},
        'backgroundColor': wpColors[r]
    } for r in row_indices] #range(0,len(data), 1)]
    

    fullStyle = altColor + rowUpdate + wpColor
    return fullStyle






if __name__ == '__main__':
    app.run_server(debug=True)

