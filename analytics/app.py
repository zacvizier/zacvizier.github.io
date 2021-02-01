# coding=utf-8

import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import decimal
import warnings
import time
import numpy
import textwrap

# Import the Stats dict from the app_stats file
from app_stats import stats

# I was getting an error as a warning that was messing up my app. This suppresses it.
warnings.simplefilter(action='ignore', category=FutureWarning)


#                     dP                                 oo          dP       dP                   
#                     88                                             88       88                   
# .d8888b. .d8888b. d8888P    dP   .dP .d8888b. 88d888b. dP .d8888b. 88d888b. 88 .d8888b. .d8888b. 
# Y8ooooo. 88ooood8   88      88   d8' 88'  `88 88'  `88 88 88'  `88 88'  `88 88 88ooood8 Y8ooooo. 
#       88 88.  ...   88      88 .88'  88.  .88 88       88 88.  .88 88.  .88 88 88.  ...       88 
# `88888P' `88888P'   dP      8888P'   `88888P8 dP       dP `88888P8 88Y8888' dP `88888P' `88888P' 
                                                                                                 
                                                                                                 

# Load data from csv
        # prod
# df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1VYoIhAj2MyZIWr72o-Ix2Rd1mHN_NVC5tTF6oUYNPUU/export?format=csv')
        # dev
# df1 = pd.read_csv("https://docs.google.com/spreadsheets/d/1VYoIhAj2MyZIWr72o-Ix2Rd1mHN_NVC5tTF6oUYNPUU/export?format=csv&id=1VYoIhAj2MyZIWr72o-Ix2Rd1mHN_NVC5tTF6oUYNPUU&gid=542337929")
        # BT Log 3.0 Prod
df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1UXV7iv7_bFgWMktRPich9Z-FcHCq4IXX7HKI5prUNto/export?format=csv')


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
    {'label': '2.6', 'value': 2.6},
    {'label': '3.3', 'value': 3.3},
    ]

# Set up time
times = [6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11.0]
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

#timeValues
timeValues = []
for i in numpy.arange(6.5,11.5,.5):
    timeValues.append({"label": i, "value": i})
  
# Convert the Stats array of objects into a normal array structure with no children objects
for data in stats: 
    data_row = data['data']
    name = data['name'] 
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

filterValues.append({'value': "Env;PB n", "label": "env PB N"})

# Create a dataframe using the rows array we created out of the Stats object array
d = pd.DataFrame(rows) 
d = d[['val','name', 'checked', 'w', 'l']] # Now we can easily re-order the columns to our liking

# We will save a fresh copy of our dataframe in case we need it later
d_fresh = d.copy()


#                   dP                   dP            dP               .8888b                              dP   oo                            
#                   88                   88            88               88   "                              88                                 
# .d8888b. .d8888b. 88 .d8888b. dP    dP 88 .d8888b. d8888P .d8888b.    88aaa  dP    dP 88d888b. .d8888b. d8888P dP .d8888b. 88d888b. .d8888b. 
# 88'  `"" 88'  `88 88 88'  `"" 88    88 88 88'  `88   88   88ooood8    88     88    88 88'  `88 88'  `""   88   88 88'  `88 88'  `88 Y8ooooo. 
# 88.  ... 88.  .88 88 88.  ... 88.  .88 88 88.  .88   88   88.  ...    88     88.  .88 88    88 88.  ...   88   88 88.  .88 88    88       88 
# `88888P' `88888P8 dP `88888P' `88888P' dP `88888P8   dP   `88888P'    dP     `88888P' dP    dP `88888P'   dP   dP `88888P' dP    dP `88888P' 
                                                                                                                                             
                 
                                                                                                   
def fill_time_arr(timeStatsDF, df):
    for index, row in df.iterrows():
        #if row['Res'] == 'W' and row['Rec'] == True:
        if row['Res'] == 'W':
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
    timeStatsDF = timeStatsDF[['val','wp','t']]
    return timeStatsDF
                                                                                                            
def fill_stats_arr(dataStats, df, optionsArr):
    start = time.time()
    for rowStats in optionsArr: # For each item in the BT data, iterate through every possible checkbox
        nameTrueVector = (dataStats['name']==rowStats['name'])
        for i in rowStats['data']: # Iterate through every option per checkbox (T or F, sometimes other stuff like R/PB/T)
            condVector = nameTrueVector & (dataStats['checked']==i['val'])
            position = dataStats[condVector].index[0]
            for index, row in df.iterrows(): # Iterate through every item in the BT Data
                if row[rowStats['val']] == i['dataVal']: # If that option matches the BT data...
                    #if row['Res'] == 'W' and row['Rec'] == True: # Depending on whether it was a Win or Loss, increment
                    if row['Res'] == 'W':
                        dataStats.iat[position, 3] += 1
                    else:
                        dataStats.iat[position, 4] += 1

    pb_no_wins = dataStats.at[0, 'w'] + dataStats.at[1, 'w']
    pb_no_loss = dataStats.at[0, 'l'] + dataStats.at[1, 'l']
    df_pb_n = pd.DataFrame([['Env', 'env', 'PB n', pb_no_wins , pb_no_loss]], columns=['val', 'name', 'checked', 'w', 'l'])
    dataStats = dataStats.append(df_pb_n, ignore_index=True)

    # Set a new column 't' (total) to zero for every row
    dataStats['t']=0
    dataStats['wp']="..." # We will calculate the wp (win percent) and lp (loss percent) columns
    dataStats['lp']="..."
    dataStats['impact'] = '...'
    decimal.getcontext().prec = 4 # 4 digits of precision (INCLUDING digits before the decimal

    wpTotal = calculateWinPTotal(df)

    # Calculate and add total, use that to calculate WP and LP and update the dataframe
    for index, row in dataStats.iterrows():
        total = row['w'] + row['l']
        if total != 0:
            dataStats.at[index, 't'] = total
            dataStats.at[index, 'wp'] = decimal.Decimal(row['w']) / decimal.Decimal(total)*100
            dataStats.at[index, 'lp'] = decimal.Decimal(row['l']) / decimal.Decimal(total)*100
            impact = (decimal.Decimal(row['w']) / decimal.Decimal(total)*100) - decimal.Decimal(wpTotal['wp'])
            if impact < 0.1 and impact > -0.1:
                impact = 0
            dataStats.at[index, 'impact'] = impact
        else:
            dataStats.at[index, 't'] = 0
            dataStats.at[index, 'wp'] = 0
            dataStats.at[index, 'lp'] = 0
            dataStats.at[index, 'impact'] = 0
            
    # Re-order the columns to our liking
    dataStats = dataStats[[ 'name','checked', 'wp', 'w', 't', 'impact']].sort_values(by=['name'], inplace=False, ascending=True)

    return dataStats

def calculateWinPTotal(data):
    numWins = 0
    for index, row in data.iterrows():
        #if row['Res'] == 'W' and row['Rec'] == True:
        if row['Res'] == 'W':
            numWins += 1
        
    decimal.getcontext().prec = 4 # 4 digits of precision (INCLUDING digits before the decimal
    if len(data.index) == 0:
        wp = 0
    else:
        wp = round(float (numWins) / float(len(data.index)),3)*100

    return {"numWins": numWins,"wp": wp}

def getTPData(data):                                                                      
    insWins = 0
    tpData = {'ins': 0, 'hl': 0, 'slightpasthl': 0, 'pasthl': 0, 'imrej': 0}
    for index, row in data.iterrows():
        if row['ImRej'] == True:
            tpData['imrej'] += 1
        elif row['Ins'] == True:
            tpData['ins'] += 1
            if row['Res'] == 'W':
                insWins += 1
        elif row['HL'] == True:
            tpData['hl'] += 1
        elif row['Slight Past HL'] == True:
            tpData['slightpasthl'] += 1
        elif row['Past HL'] == True:
            tpData['pasthl'] += 1


    tpNumbers = {'imrej': tpData['imrej'], 'insL': tpData['ins']-insWins, 'insW': insWins, 'hl': tpData['hl'], 'slightpasthl': tpData['slightpasthl'], 'pasthl': tpData['pasthl'],
                 'total': len(data.index)}


    return tpNumbers       

def getSLData(data):
    #slData = {'rec': 0, 'both': 0, 'closeema': 0, 'farema': 0, 'close_total': 0, 'far_total': 0, 'total': 0}
    slData = {'rec': 0, 'total': 0}
    for index, row in data.iterrows():
        #if row['Rec'] == True:
        if row['Res'] == 'W':
            slData['rec'] += 1
        # if row['Both'] == True:
        #     slData['both'] += 1
        # if row['Close EMA'] == 'W':
        #     slData['closeema'] += 1
        # if row['Close EMA'] != 'N':
        #     slData['close_total'] += 1
        # if row['Far EMA'] == 'W':
        #     slData['farema'] += 1
        # if row['Far EMA'] != 'N':
        #     slData['far_total'] += 1
    slData['total'] = len(data.index)

    if len(data.index) != 0:
        wp_rec = '%.1f' % (float(slData['rec'])/float(len(data.index))*100)
        # wp_both = '%.1f' % (float(slData['both'])/float(len(data.index))*100)
        # wp_close = '%.1f' % (float(slData['closeema'])/float(len(data.index))*100)
        # wp_far = '%.1f' % (float(slData['farema'])/float(len(data.index))*100)
    else:
        wp_rec = 0.0
        # wp_both = 0.0
        # wp_close = 0.0
        # wp_far = 0.0
    
    return slData



# 88d888b. 88d888b. .d8888b.          88 .d8888b. dP    dP .d8888b. dP    dP d8888P 
# 88'  `88 88'  `88 88ooood8 88888888 88 88'  `88 88    88 88'  `88 88    88   88   
# 88.  .88 88       88.  ...          88 88.  .88 88.  .88 88.  .88 88.  .88   88   
# 88Y888P' dP       `88888P'          dP `88888P8 `8888P88 `88888P' `88888P'   dP   
# 88                                                   .88                          
# dP                                               d8888P          

d = fill_stats_arr(d, df, optionsArr)
timeStatsDF = fill_time_arr(timeStatsDF, df)
wpTotal = calculateWinPTotal(df)
initial_wp = wpTotal["wp"]
numWins = wpTotal["numWins"]

checkboxes = [
                {'label': 'Ins/Wk Y', 'value': 'Inside / Wk;y'},
                {'label': 'Ins/Wk N', 'value': 'Inside / Wk;n'},
                {'label': 'Deep Y', 'value': 'Deep;y'},
                {'label': 'Deep N', 'value': 'Deep;n'},
                {'label': 'Long Y', 'value': 'Long;y'},
                {'label': 'Long N', 'value': 'Long;n'},
                {'label': 'Is BOPB Y', 'value': 'Is BOPB;y'},
                {'label': 'Is BOPB N', 'value': 'Is BOPB;n'},
                {'label': 'Alr BOPB Y', 'value': 'Alr BOPB;y'},
                {'label': 'Alr BOPB N', 'value': 'Alr BOPB;n'},
                {'label': 'NoRm Y', 'value': 'NoRm 2 HL;y'},
                {'label': 'NoRm N', 'value': 'NoRm 2 HL;n'},
                {'label': 'Mjr SR Y', 'value': 'Mjr SR;y'},
                {'label': 'Mjr SR N', 'value': 'Mjr SR;n'},
                {'label': '2PB Wkr Y', 'value': '2nd PB Wkr;y'},
                {'label': '2PB Wkr N', 'value': '2nd PB Wkr;n'},
                {'label': 'Mjr DP Y', 'value': 'Mjr DP;y'},
                {'label': 'Mjr DP N', 'value': 'Mjr DP;n'},
                {'label': 'DP Y', 'value': 'DP;y'},
                {'label': 'DP N', 'value': 'DP;n'},
                {'label': 'Btwn Y', 'value': 'Btwn EMAs;y'},
                {'label': 'Btwn N', 'value': 'Btwn EMAs;n'},
                {'label': 'Touched Y', 'value': 'Touched EMA;y'},
                {'label': 'Touched N', 'value': 'Touched EMA;n'},
            ]


#                     oo             dP                                       dP   
#                                    88                                       88   
# 88d8b.d8b. .d8888b. dP 88d888b.    88 .d8888b. dP    dP .d8888b. dP    dP d8888P 
# 88'`88'`88 88'  `88 88 88'  `88    88 88'  `88 88    88 88'  `88 88    88   88   
# 88  88  88 88.  .88 88 88    88    88 88.  .88 88.  .88 88.  .88 88.  .88   88   
# dP  dP  dP `88888P8 dP dP    dP    dP `88888P8 `8888P88 `88888P' `88888P'   dP   
#                                                     .88                          
#                                                 d8888P                           

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Store(id='memory'),
    dcc.Store(id='info'),
    html.Div([ # top
        html.Div([ # selections/btns
            html.Div([ # selections
                html.Div([ 
                    dcc.Dropdown(
                    id='playSelect',
                    options=plays,
                    multi=False,
                    value=2.2 )], style={'width':'10%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Dropdown(
                        id='filterSelect',
                        options=filterValues,
                        multi=True,
                        value=[])], style={'width':'50%', 'display': 'inline-block', 'margin-left': '0.5%'}),
                html.Div([
                    dcc.Input(
                        id="numEntries", 
                        type="number", 
                        placeholder="# Entries", 
                        debounce=True,
                        style={
                            'display': 'inline-block',
                            'height': '28px',
                            'width': '15%',
                            'border-radius': '8%',
                            'margin-left': '0.5%',
                            'position': 'relative',
                        }),
                    dcc.Input(
                        id="ticker", 
                        type="text", 
                        placeholder="Stock", 
                        debounce=True,
                        style={
                            'display': 'inline-block',
                            'height': '28px',
                            'width': '15%',
                            'border-radius': '8%',
                            'margin-left': '0.5%',
                            'position': 'relative',
                        }),
                    dcc.Input(
                        id="id-start", 
                        type="number", 
                        placeholder="Start", 
                        debounce=True,
                        style={
                            'display': 'inline-block',
                            'height': '28px',
                            'width': '15%',
                            'border-radius': '8%',
                            'margin-left': '0.5%',
                            'position': 'relative',
                        }),
                    dcc.Input(
                        id="id-end", 
                        type="number", 
                        placeholder="End", 
                        debounce=True,
                        style={
                            'display': 'inline-block',
                            'height': '28px',
                            'width': '15%',
                            'border-radius': '8%',
                            'margin-left': '0.5%',
                            'position': 'relative',
                        }),
                        ], style={'position': 'absolute','display': 'inline-block'})
                ],style={'width': '90%', 'display': 'inline-block'}), 
            html.Div([ #btns
                html.Button('Submit', id='submit-button', style={
                    "box-shadow":"inset 0px 1px 0px 0px #a6e7ff",
                    "background":"linear-gradient(to bottom, #a6e7ff 5%, #6db6d1 100%)",
                    "border-radius":"6px",
                    "border":"1px solid #a6e7ff",
                    "color":"#ffffff",
                    "padding":"6px 24px",
                    'font-size': '20px',
                    'height': '35px',
                    'width': '32%'
                    }),
                html.Button('Screenshots', id='screenshot-button', style={
                    "box-shadow":"inset 0px 1px 0px 0px #9caaff",
                    "background":"linear-gradient(to bottom, #9caaff 5%, #3c488f 100%)",
                    "border-radius":"6px",
                    "border":"1px solid #9caaff",
                    "color":"#ffffff",
                    'margin-left': '2%',
                    'font-size': '20px',
                    'height': '35px',
                    'width': '32%',
                    }),
                html.Button('Clear', id='checkbox-button', style={
                    "box-shadow":"inset 0px 1px 0px 0px #fc77d7",
                    "background":"linear-gradient(to bottom, #fc77d7 5%, #7a175e 100%)",
                    "border-radius":"6px",
                    "border":"1px solid #fc77d7",
                    "color":"#ffffff",
                    'margin-left': '2%',
                    'font-size': '20px',
                    'height': '35px',
                    'width': '12%',
                    }),
                html.Button('Set Time', id='time-button', style={
                    "box-shadow":"inset 0px 1px 0px 0px #fc77d7",
                    "background":"linear-gradient(to bottom, #fc77d7 5%, #7a175e 100%)",
                    "border-radius":"6px",
                    "border":"1px solid #fc77d7",
                    "color":"#ffffff",
                    'margin-left': '2%',
                    'font-size': '20px',
                    'height': '35px',
                    'width': '12%',
                    })
                ],style={'width': '90%', 'display': 'inline-block', 'margin-bottom': '1%'}),
            ], style={'width': '53%', 'display': 'inline-block', 'float': 'left'}),
        html.Br(),
        html.Div([ # checklist
                dcc.Checklist(
                    id='checklist',
                    options=checkboxes,
                    value=[],
                    labelStyle={'display': 'block', 'font-size': '12px'},
                    style={'column-count': '7', 'column-gap': '0px'}
                )
            ], style={'width': '45%', 'float': 'right', 'height': '80px', 'position': 'relative', 'margin-top': '-20px', 'right': '50px'})
        ], style={'display': 'inline-block', 'width': '100%'}),
    html.Div([ # bottom
        html.Div([ # main table / first column
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in d.columns
                ],
                data=d.to_dict('records'),
                column_selectable="multi",
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
            )],id='table-div',style={'width': '24%', 'display': 'inline-block', 'float': 'left'}),
        html.Div([ # 2nd column
            html.Div([ # sl table
                dash_table.DataTable(id='sl_table',
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": False} for i in ['SL', 'wp', 'wins', 'total']
                    ],
                    data=[],
                    column_selectable="multi",
                    sort_action='native',
                    page_action="native",
                    page_current= 0,
                    page_size= 5,
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'width': '10%'
                        } for c in ['SL', 'wp', 'wins', 'total']
                    ],
                    style_data_conditional=[]
                )], style={'width': '49%','position': 'relative', 'display': 'inline-block'}),
            html.Div([ # tp table
                dash_table.DataTable(id='tp_table',
                    columns=[
                        {"name": i, "id": i, "deletable": False, "selectable": False} for i in ['TP', '%', 'total']
                    ],
                    data=[],
                    column_selectable="multi",
                    sort_action='native',
                    page_action="native",
                    page_current= 0,
                    page_size= 5,
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'width': '10%'
                        } for c in ['TP', '%', 'total']
                    ],
                    style_data_conditional=[]
                )], style={'width': '49%','position': 'relative', 'left': '2%', 'display': 'inline-block'}),
            html.Div(style={'height': '20px'}),
            dash_table.DataTable(id='datatable-env', # env table
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": False} for i in d.columns
                ],
                data=[],
                column_selectable="multi",
                sort_action='native',
                page_action="native",
                page_current= 0,
                page_size= 5,
                style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'width': '10%'
                    } for c in d.columns
                ],
                style_data_conditional=[]),
            html.Div([dcc.Dropdown(id='timeSelect', # time select
                    options=timeValues,
                    multi=True,
                    value=[7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0, 10.5, 11]
                )],style={'width': '100%', 'display': 'inline-block', 'margin-top': '20px'}),
            dash_table.DataTable(id='datatable-time', # time table
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
                ],style_data_conditional=[]),
            ],id='time-div',style={'width': '26%','position': 'relative', 'margin-left': '1%', 'display': 'inline-block', 'overflow': 'hidden', 'top': '-14px'}),
        html.Div(id='imgs', style={'width': '48%','position': 'relative', 'display': 'inline-block', 'float': 'right', 'height': '850px', 'overflow': 'scroll'}),
        ]),
    html.Div(id='placeholder')
])


#                         dP            dP                           dP            dP       dP          
#                         88            88                           88            88       88          
# dP    dP 88d888b. .d888b88 .d8888b. d8888P .d8888b.              d8888P .d8888b. 88d888b. 88 .d8888b. 
# 88    88 88'  `88 88'  `88 88'  `88   88   88ooood8                88   88'  `88 88'  `88 88 88ooood8 
# 88.  .88 88.  .88 88.  .88 88.  .88   88   88.  ...                88   88.  .88 88.  .88 88 88.  ... 
# `88888P' 88Y888P' `88888P8 `88888P8   dP   `88888P'                dP   `88888P8 88Y8888' dP `88888P' 
#          88                                         oooooooooooo                                      
#          dP                                                                                           
@app.callback(
    [dash.dependencies.Output("datatable-interactivity", "data"),
    dash.dependencies.Output("datatable-time", "data"),
    dash.dependencies.Output("datatable-env", "data"),
    dash.dependencies.Output("sl_table", "data"),
    dash.dependencies.Output("tp_table", "data"),
    dash.dependencies.Output("memory", "data"),
    dash.dependencies.Output("info", "data"),
    ],
    [dash.dependencies.Input('submit-button', 'n_clicks')],
    [State("filterSelect", "value"),
    State("playSelect", "value"),
    State("timeSelect", "value"),
    State("checklist", "value"),
    State("numEntries", "value"),
    State("ticker", "value"),
    State("id-start", "value"),
    State("id-end", "value")])

def update_table(submit_click, search_value, play_val, time_value, checklist, numEntries, ticker, idstart, idend): 
    global df #Data (actual backtest data)
    global d_fresh #Stats
    global optionsArr # Array of options needed to update stats
    global timeStatsBackup # Zeroed out timeStatsDF



    # Make a copy of the ORIGINAL data
    d_fresh_copy = d_fresh.copy()
    dataCopy = df.copy()
    timeCopy = timeStatsBackup.copy()

    if idstart is not None:
        dataCopy = dataCopy[dataCopy['Id'] >= idstart]
    if idend is not None:
        dataCopy = dataCopy[dataCopy['Id'] <= idend]

    if numEntries is None and numEntries != "":
        numEntries = len(dataCopy.index)
    
    dataCopy = dataCopy.tail(numEntries)

    if ticker is not None and ticker != "":
        dataCopy = dataCopy[dataCopy['Stock'] == ticker.upper()]


    if play_val is not None:
        if play_val == 2.6:
            data22 = dataCopy[(dataCopy['Play'] == 2.2) & (dataCopy['StrMv'] == True)]
            data36 = dataCopy[dataCopy['Play'] == 3.6]
            dataCopy = pd.concat([data22, data36], ignore_index=True).drop_duplicates()
        elif play_val == 3.3:
            data31 = dataCopy[dataCopy['Play'] == 3.1]
            data36 = dataCopy[dataCopy['Play'] == 3.6]
            dataCopy = pd.concat([data31, data36], ignore_index=True).drop_duplicates()
        else:
            dataCopy = dataCopy[dataCopy['Play'] == play_val]

    # Store the values from the multi-dropdown in a variable. No reason.
    valArr = search_value

    if (valArr is None):
        newStats = d

    # We got values in our multi-select, now we have to filter the data and return the updated data to the app
    else:
        values = []
        valuesCheckbox = []
        for val in valArr:
            values.append({"val": val[:val.find(';')], "checked": val[val.find(';')+1:]})
        for val in checklist:
            valuesCheckbox.append({"val": val[:val.find(';')], "checked": val[val.find(';')+1:]})

        
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

        for i in valuesCheckbox:
            if i['checked'] == 'y':
                dataCopy = dataCopy[dataCopy[i['val']]==True]
            elif i['checked'] == 'n':
                dataCopy = dataCopy[dataCopy[i['val']]==False]


    # Before sending the new data to the stats update function, we want to further filter it to only include the times which we selected
    if len(time_value) !=0:
        for index, row in dataCopy.iterrows():
            if row['Time'] not in time_value:
                dataCopy.drop(index, inplace=True)


    # Now we send this new data to the stats update functions.
    # Stats DF must be fresh copy
    newStats = fill_stats_arr(d_fresh_copy, dataCopy, optionsArr)
    timeStatsNew = fill_time_arr(timeCopy, dataCopy)


    # Calculate WP and totals which we will send to the div
    wpTotal=calculateWinPTotal(dataCopy)
    wp = wpTotal["wp"]
    numWins = wpTotal["numWins"]
    total = len(dataCopy.index)

    envStats = newStats[newStats['name']=='env']

    # store DF in storage
    data_screenshots = dataCopy[[ 'Id', 'Scrn', 'Rec', 'Res', 'Dates']]
    mem = data_screenshots.to_dict('records')

    info = str(play_val)
    for i in search_value:
        info = info + " + " + i


    ##### Get SL data #####
    slData = getSLData(dataCopy)
    #print slData

    if slData['total'] != 0:
        wp_rec = '%.1f' % (float(slData['rec'])/float(slData['total'])*100)
        # wp_both = '%.1f' % (float(slData['both'])/float(slData['total'])*100) 
        # if slData['close_total'] != 0:
        #     wp_close = '%.1f' % (float(slData['closeema'])/float(slData['close_total'])*100)
        # else:
        #     wp_close = 0.0
        # if slData['far_total'] != 0:
        #     wp_far = '%.1f' % (float(slData['farema'])/float(slData['far_total'])*100)
        # else:
        #     wp_far = 0.0
    else:
        wp_rec = 0.0
        # wp_both = 0.0
        # wp_close = 0.0
        # wp_far = 0.0


    # sl_d = {
    #     'SL': ["Rec","Both", "Close", "Far"], 'wp': [wp_rec,wp_both, wp_close, wp_far], 
    #     'wins':[int(slData['rec']), int(slData['both']), int(slData['closeema']), int(slData['farema'])],
    #     'total': [int(slData['total']), int(slData['total']), int(slData['close_total']), int(slData['far_total'])]
    # } 
    sl_d = {
        'SL': ["Rec"], 'wp': [wp_rec], 
        'wins':[int(slData['rec'])],
        'total': [int(slData['total'])]
    } 
    sl_df = pd.DataFrame(data=sl_d)

    slrec = "Win %: " + str(wp) + "% --- NumWins: " + str(numWins) + " --- Total: " + str(total)
    sltest = "..."

    
    ### Get TP values ####
    tpValues = getTPData(dataCopy)

    hl_plus = tpValues['hl'] + tpValues['slightpasthl'] + tpValues['pasthl']
    insw_plus = tpValues['insW'] + tpValues['hl'] + tpValues['slightpasthl'] + tpValues['pasthl']
    imrej = tpValues['imrej']
    sphl_plus = tpValues['slightpasthl'] + tpValues['pasthl']


    if tpValues['total'] != 0:
        wp_hl_plus = '%.1f' % (float(hl_plus)/float(tpValues['total'])*100)
        wp_insw_plus = '%.1f' % (float(insw_plus)/float(tpValues['total'])*100)
        wp_imrej = '%.1f' % (float(imrej)/float(tpValues['total'])*100)
        wp_sphl_plus = '%.1f' % (float(sphl_plus)/float(tpValues['total'])*100)
    else:
        wp_hl_plus = 0.0
        wp_insw_plus = 0.0
        wp_imrej = 0.0
        wp_sphl_plus = 0.0

    tp_d = {
        'TP': ["HL+", "InsW+", "SPHL+","ImRej"], '%': [wp_hl_plus, wp_insw_plus, wp_sphl_plus, wp_imrej],
        'total': [int(tpValues['total']), int(tpValues['total']), int(tpValues['total']), int(tpValues['total'])]
    } 
    tp_df = pd.DataFrame(data=tp_d)

    


    return newStats.to_dict('records'), timeStatsNew.to_dict('records'),envStats.to_dict('records'), sl_df.to_dict('records'), tp_df.to_dict('records'), mem, info


#            dP   dP                                              dP dP dP                         dP                
#            88   88                                              88 88 88                         88                
# .d8888b. d8888P 88d888b. .d8888b. 88d888b.    .d8888b. .d8888b. 88 88 88d888b. .d8888b. .d8888b. 88  .dP  .d8888b. 
# 88'  `88   88   88'  `88 88ooood8 88'  `88    88'  `"" 88'  `88 88 88 88'  `88 88'  `88 88'  `"" 88888"   Y8ooooo. 
# 88.  .88   88   88    88 88.  ... 88          88.  ... 88.  .88 88 88 88.  .88 88.  .88 88.  ... 88  `8b.       88 
# `88888P'   dP   dP    dP `88888P' dP          `88888P' `88888P8 dP dP 88Y8888' `88888P8 `88888P' dP   `YP `88888P' 


@app.callback(
    [dash.dependencies.Output("imgs", "children")],
    [dash.dependencies.Input('screenshot-button', 'n_clicks')],
    [State("memory", "data"), State("info", "data")])
def reset_filter(scrn_btn, mem, info):
    scrn_list = pd.DataFrame.from_dict(mem)

    imgList = []
    imgList.append(html.Div(info, style={ 'color': 'black', 'font-size': '26px', 'font-weight': 'bold'}))
    for index, row in scrn_list.iterrows():
        #if row['Rec'] == True:
        if row['Res'] == 'W':
            winStr = "Win"
        else:
            winStr = "Loss"
        span = str(row['Id']) + "--" + str(winStr) + "--" + str(row['Dates']) + "--" + str(row['Scrn'])
        imgList.append(html.A(href=row['Scrn'],target='_blank', children=(html.Img(src=row['Scrn'], style={'width':'98%'}))))
        imgList.append(html.Span(span, style={'position': 'absolute', 'color': 'cyan', 'font-size': '26px', 'font-weight': 'bold', 'left': '0px', 'margin-top': '30px', 'margin-left': '5px'}))

    return [imgList]


# ################# Clear Num Entries #################
# @app.callback(
#     dash.dependencies.Output("numEntries", "value"),
#     [Input('clear-numEntries', 'n_clicks')])
# def reset_filter(n_clicks):
#     return None

################# Reset Checkboxes button #################
@app.callback(
    dash.dependencies.Output("checklist", "value"),
    [dash.dependencies.Input('checkbox-button', 'n_clicks')])
def reset_filter(n_clicks):
    return []


################# Reset Time button #################
@app.callback(
    dash.dependencies.Output("timeSelect", "value"),
    [dash.dependencies.Input('time-button', 'n_clicks')])
def reset_filter(n_clicks):
    return [7,7.5,8,8.5,9,9.5,10,10.5,11]


#############################################################
############ Main Table Cell Click Callback #################
#############################################################
@app.callback(
    Output("datatable-interactivity", "style_data_conditional"),
    [Input('datatable-interactivity', 'active_cell'),
    Input("datatable-interactivity", "data"),
    Input('datatable-interactivity', "filter_query")])
def highlight_row(active_cell,data, filter_query):
    wpColors = []
    altColor=[]
    rowUpdate = []

        
    if filter_query == None or filter_query == '': #or myQuery == '':
        for row in data:
            if row[u'wp'] > 57.5:
                wpColors.append('#a8fc9d')
            elif row[u'wp'] > 52:
                wpColors.append('#eefaa2')
            else:
                wpColors.append('#ffd294')

            
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
        } for c in ['name','val','checked', 'w', 'l', 'lp', 't', 'impact']]
        wpColor = [{
            'if': {'row_index': r, 'column_id': 'wp'},
            'backgroundColor': wpColors[r]
        } for r in row_indices] #range(0,len(data), 1)]
    

        fullStyle = altColor + rowUpdate + wpColor
        return fullStyle
    
    else: 
        data2 = pd.DataFrame(data)
        
        myQuery = filter_query.split('contains ')[1]
        data3 = data2[data2['name'].str.contains(myQuery)].to_dict('records')


        for row in data3:
            if row[u'wp'] > 57.5:
                wpColors.append('#a8fc9d')
            elif row[u'wp'] > 52:
                wpColors.append('#eefaa2')
            else:
                wpColors.append('#ffd294')
            
            
        row_indices = list(range(0,len(data3), 1))
        if active_cell is None:
            rowUpdate = []
        else:
            rowUpdate = [{'if': {'row_index': active_cell['row']},'backgroundColor': 'pink'}]
            if active_cell['row'] in row_indices: 
                row_indices.remove(active_cell['row'])


        altColor =[{
            'if': {'row_index': 'odd', 'column_id': c},
            'backgroundColor': 'rgb(245, 245, 245)'
        } for c in ['name','val','checked', 'w', 'l', 'lp', 't', 'impact']]
        wpColor = [{
            'if': {'row_index': r, 'column_id': 'wp'},
            'backgroundColor': wpColors[r]
        } for r in row_indices]
    

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
        wpColors.append('#dfeef5')

        
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
    } for c in ['name','val','checked', 'w', 'l', 'lp', 't', 'impact']]
    wpColor = [{
        'if': {'row_index': r, 'column_id': 'wp'},
        'backgroundColor': wpColors[r]
    } for r in row_indices]
    

    fullStyle = altColor + rowUpdate + wpColor
    return fullStyle


if __name__ == '__main__':
    app.run_server(debug=True)

