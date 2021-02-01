
import datetime
import csv

import pandas as pd
from ta.utils import dropna
from ta.trend import EMAIndicator, SMAIndicator

from polygon import RESTClient


def ts_to_datetime(ts) -> str:
    return datetime.datetime.fromtimestamp(ts / 1000.0).strftime('%Y-%m-%d %H:%M')


def main():

    # VARIABLES
    START_TIME_HOUR = 6
    START_TIME_MINUTE = 40
    END_TIME_HOUR = 12
    END_TIME_MINUTE = 50

    
    df = pd.read_csv('COSTtest1.csv', sep=',')


    # Clean NaN values
    df = dropna(df)

    # Get EMA values
    indicator_ema15 = EMAIndicator(close=df["close"], n=15)
    indicator_ema50 = EMAIndicator(close=df["close"], n=50)
    indicator_ema100 = EMAIndicator(close=df["close"], n=100)
    indicator_ema200 = EMAIndicator(close=df["close"], n=200)
    indicator_sma300 = SMAIndicator(close=df["close"], n=300)

    # Insert EMA values into dataframe
    df['ema15'] = indicator_ema15.ema_indicator()
    df['ema50'] = indicator_ema50.ema_indicator()
    df['ema100'] = indicator_ema100.ema_indicator()
    df['ema200'] = indicator_ema200.ema_indicator()
    df['sma300'] = indicator_sma300.sma_indicator()


    # Determine uptrend or downtrend
    df['ema_trend'] = 'na'

    # uptrend. 15 > 100, 50 > 200, 100 > 200
    df.loc[((df['ema15'] > df['ema100']) & (df['ema50'] > df['ema200'])
        & (df['ema100'] > df['ema200']) & (df['ema100'] > df['sma300'])),'ema_trend'] = 'up'

    # downtrend. 15 < 100, 50 < 200, 100 < 200
    df.loc[((df['ema15'] < df['ema100']) & (df['ema50'] < df['ema200']) 
        & (df['ema100'] < df['ema200']) & (df['ema100'] < df['sma300'])),'ema_trend'] = 'down'       




    # determine whether price is touching 15 ema
    df['touching15'] = "no"

    # if real body is teaching 15, set touching15 to yes
    # green candle touching 15
    df.loc[((df['ema15'] > df['open']) & (df['ema15'] < df['close'])),'touching15'] = 'yes'

    # red candle touching 15
    df.loc[((df['ema15'] > df['close']) & (df['ema15'] < df['open'])),'touching15'] = 'yes'





    # determine whether price is touching 200 ema
    df['touching200'] = "no"

    # if real body is teaching 200, set touching200 to yes
    # green candle touching 200
    df.loc[((df['ema200'] > df['low']) & (df['ema200'] < df['high'])),'touching200'] = 'yes'

    # red candle touching 200
    df.loc[((df['ema200'] > df['high']) & (df['ema200'] < df['low'])),'touching200'] = 'yes'


    # Signal for when price crosses up or down. Can combine with trend variable
    #green candle cross up
    df['entry_cross15_bull'] = "unk"
    df.loc[((df['open'] < df['close']) & (df['touching15'] == 'yes') & (df['close'] > df['ema15'])),'entry_cross15_bull'] = 'yes'

    # (if red candle & touching 15 & close is below the 15)
    df['entry_cross15_bear'] = "unk"
    df.loc[((df['open'] > df['close']) & (df['touching15'] == 'yes') & (df['close'] < df['ema15'])),'entry_cross15_bear'] = 'yes'

    # df['close_under_15'] = 'no'
    # df.loc[ ((df['ema_trend'] == 'up') & ) ,close_under_15 ] = 'yes'
    






    # set entry pos 1 if price goes past 15
    df['entryPos1'] = -1
    df['entryPos2'] = -1
    df['entryPos1_time'] = ""
    df['valleybull'] = -1
    df['valleybear'] = -1
    df['inEntry'] = -1
    df['entrySL'] = -1
    df['entryTP'] = -1
    df['entryType'] = ""

    df['inPB'] = 'no' # will need to check if its a range (when I figure out how to) and ignore this if so
    df['hl'] = -1

    countW = 0
    countL = 0

    #for i, row in df.iterrows():
    for i, row in df.iloc[1:].iterrows():


        dt = str(df.loc[i, 'time'])
        dt_hour = dt.split(":")[0][-2:]
        dt_minute = dt.split(":")[1][:2]


        # inPB + HL: bullish first
        # if prev not in pb, and if trend is up, and if (current high is less than previous high or current close is 
        #       less than previous close) - set inPB to yes and HL to prev high
        if(df.loc[i, 'ema_trend'] == 'up'):
            if(df.loc[i-1, 'inPB'] == 'no'):
                if((df.loc[i, 'ema_trend'] == 'up') & ((df.loc[i, 'high'] < df.loc[i-1, 'high']) or (df.loc[i, 'close'] < df.loc[i-1, 'close']))): # & (df.loc[i, 'close'] < df.loc[i-1, 'close'])
                    df.loc[i, 'inPB'] = 'yes'
                    df.loc[i, 'hl'] = df.loc[i-1, 'high']

            # else if prev IS in pb
            else:
                #if(i==1286): print("in here 1 - " + str(df.loc[i, 'high']) + " --- " + str(df.loc[i-1, 'hl']))
                #if current high is less than previous HL value OR current close is less than previous close
                if((df.loc[i, 'high'] < df.loc[i-1, 'hl']) or (df.loc[i, 'close'] < df.loc[i-1, 'close'])):
                    # set inPB to yes and hl to either yesterday's hl or today's high, whichever is higher
                    df.loc[i, 'inPB'] = 'yes'
                    df.loc[i, 'hl'] = (df.loc[i-1, 'hl']) if (df.loc[i-1, 'hl'] > df.loc[i, 'high']) else (df.loc[i, 'high'])

                ## if current high is greater than previous hl and previous close is greater than current open, we're no longer in a PB
                if((df.loc[i, 'high'] > df.loc[i-1, 'hl']) and (df.loc[i, 'close'] > df.loc[i-1, 'open'])):
                    df.loc[i, 'inPB'] = 'no'

            if((df.loc[i, 'hl'] == -1) & (df.loc[i, 'inPB'] == 'no')):
                df.loc[i, 'hl'] = df.loc[i, 'high']
        elif(df.loc[i, 'ema_trend'] == 'down'):
            if(df.loc[i-1, 'inPB'] == 'no'):
                if((df.loc[i, 'ema_trend'] == 'down') & ((df.loc[i, 'low'] > df.loc[i-1, 'low']) or (df.loc[i, 'close'] > df.loc[i-1, 'close']))): # & (df.loc[i, 'close'] < df.loc[i-1, 'close'])
                    df.loc[i, 'inPB'] = 'yes'
                    df.loc[i, 'hl'] = df.loc[i-1, 'low']

            # else if prev IS in pb
            else:
                #if(i==1286): print("in here 1 - " + str(df.loc[i, 'high']) + " --- " + str(df.loc[i-1, 'hl']))
                #if current high is less than previous HL value OR current close is less than previous close
                if((df.loc[i, 'low'] > df.loc[i-1, 'hl']) or (df.loc[i, 'close'] > df.loc[i-1, 'close'])):
                    # set inPB to yes and hl to either yesterday's hl or today's high, whichever is higher
                    df.loc[i, 'inPB'] = 'yes'
                    df.loc[i, 'hl'] = (df.loc[i-1, 'hl']) if (df.loc[i-1, 'hl'] < df.loc[i, 'low']) else (df.loc[i, 'low'])

                ## if current high is greater than previous hl and previous close is greater than current open, we're no longer in a PB
                if((df.loc[i, 'low'] < df.loc[i-1, 'hl']) and (df.loc[i, 'close'] < df.loc[i-1, 'open'])):
                    df.loc[i, 'inPB'] = 'no'

            if((df.loc[i, 'hl'] == -1) & (df.loc[i, 'inPB'] == 'no')):
                df.loc[i, 'hl'] = df.loc[i, 'low']
        

        # if price touching 200, set entry pos to -1 (reset)
        if((df.loc[i, 'touching200'] == 'yes')):
            df.loc[i, 'entryPos1'] = -1
            df.loc[i, 'entryPos2'] = -1
            #df.loc[i, 'valleybear'] = -1
            df.loc[i, 'entryPos1_time'] = ""
            df.loc[i, 'inPB'] = "no"
            df.loc[i, 'hl'] = -1
        
        # old if (added this to places where "inEntry" is set): elif((int(dt_hour)  12) or (int(dt_hour) == 12 and int(dt_minute) < 45)):
        # if it's after end time, reset entryPos1/2, posTime, and valleybear
        elif(int(dt_hour) == END_TIME_HOUR and int(dt_minute) >= END_TIME_MINUTE):
            df.loc[i, 'entryPos1'] = -1
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'entryPos1_time'] = ""
            df.loc[i, 'valleybear'] = -1
        
        elif(int(dt_hour) == START_TIME_HOUR and int(dt_minute) <= START_TIME_MINUTE):
            df.loc[i, 'entryPos1'] = -1
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'entryPos1_time'] = ""
            df.loc[i, 'valleybear'] = -1


        # if prev does not have valid number and this one is, set to current index - Bullish
        elif((df.loc[i, 'touching15'] == 'yes') & (df.loc[i, 'ema_trend'] == 'up') & (df.loc[i, 'entry_cross15_bull'] != 'yes')):
            df.loc[i, 'entryPos1'] = i
            df.loc[i, 'entryPos1_time'] = df.loc[i, 'time']

        # if prev does not have valid number and this one is, set to current index - Bearish
        elif((df.loc[i, 'touching15'] == 'yes') & (df.loc[i, 'ema_trend'] == 'down') & (df.loc[i, 'entry_cross15_bear'] != 'yes')):
            df.loc[i, 'entryPos1'] = i
            df.loc[i, 'entryPos1_time'] = df.loc[i, 'time']

        # if prev had a valid  number (> 0), set to same value as prev
        elif((df.loc[(i-1),'entryPos1'] > -1)):
            df.loc[i, 'entryPos1'] = df.loc[i-1, 'entryPos1']
            df.loc[i, 'entryPos1_time'] = df.loc[i-1, 'entryPos1_time']


        # get the valley - Bullish
        if((df.loc[(i), 'entryPos1'] > -1) & (df.loc[i, 'ema_trend'] == 'up') & ((df.loc[i, 'low'] < df.loc[(i-1), 'valleybear']) or (df.loc[(i-1), 'valleybear'] == -1))):
            #print("vb1 " + str(df.loc[i, 'time']))
            df.loc[i, 'valleybear'] = df.loc[i, 'low']
        elif((df.loc[(i), 'entryPos1'] > -1) & (df.loc[i, 'ema_trend'] == 'up') & (df.loc[i, 'low'] >= df.loc[(i-1), 'valleybear'])):
            #print("vb2 " + str(df.loc[i, 'time']))
            df.loc[i, 'valleybear'] = df.loc[i-1, 'valleybear']

        # get the valley - Bearish
        if((df.loc[(i), 'entryPos1'] > -1) & (df.loc[i, 'ema_trend'] == 'down') & (df.loc[i, 'high'] > df.loc[(i-1), 'valleybear'])):
            df.loc[i, 'valleybear'] = df.loc[i, 'high']
        elif((df.loc[(i), 'entryPos1'] > -1) & (df.loc[i, 'ema_trend'] == 'down') & (df.loc[i, 'high'] <= df.loc[(i-1), 'valleybear'])):
            df.loc[i, 'valleybear'] = df.loc[i-1, 'valleybear']


        # entryPos2 - if entryPos1 is true and price crosses in direction of trend, set entry pos 2
        # if prev had a valid  number (> 0), set to same value as prev
        if((df.loc[(i-1),'entryPos2'] > -1) & (df.loc[(i-1),'entryPos1'] > -1)):
            df.loc[i, 'entryPos2'] = df.loc[i-1, 'entryPos2']
            df.loc[i, 'entryPos2_time'] = df.loc[i-1, 'entryPos2_time'] 

        # if pulled past 15, trend is bullish, and crossed 15 bullish
        #if((df.loc[i, 'entryPos1'] > -1) & (df.loc[i, 'ema_trend'] == 'up') & (df.loc[i, 'entry_cross15_bull'] == 'yes')):
        if((df.loc[i, 'entryPos1'] > -1) & (df.loc[i, 'entryPos2'] == -1) & (df.loc[i, 'ema_trend'] == 'up') & (df.loc[i, 'close'] > df.loc[i, 'ema15']) & (df.loc[i, 'close'] > df.loc[i, 'open'])):
            df.loc[i, 'entryPos2'] = i
            df.loc[i, 'entryPos2_time'] = df.loc[i, 'time']

        # if pulled past 15, trend is bearish, and crossed 15 bearish
        #elif((df.loc[i, 'entryPos1'] > -1) & (df.loc[i, 'ema_trend'] == 'down') & (df.loc[i, 'entry_cross15_bear'] == 'yes')):
        elif((df.loc[i, 'entryPos1'] > -1) & (df.loc[i, 'entryPos2'] == -1) & (df.loc[i, 'ema_trend'] == 'down') & (df.loc[i, 'close'] < df.loc[i, 'ema15']) & (df.loc[i, 'open'] > df.loc[i, 'close'])):
            df.loc[i, 'entryPos2'] = i
            df.loc[i, 'entryPos2_time'] = df.loc[i, 'time']

        # 1 - if price goes back past the 15 but is not inEntry, reset entryPos2 BUT keep entryPos1
        #   NOTE - not working for situations where the bar doesn't cross, but jumps under the 15
        #elif((df.loc[i, 'entryPos2'] > -1) & (df.loc[i, 'touching15'] == 'yes') & (df.loc[i, 'inEntry'] == -1)):

        #bullish
        elif((df.loc[i, 'ema_trend'] == 'up') & (df.loc[i, 'entryPos2'] > -1) & (df.loc[i, 'close'] < df.loc[i, 'ema15']) & (df.loc[i, 'inEntry'] == -1)):
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'entryPos2_time'] = ""
        #bearish
        elif((df.loc[i, 'ema_trend'] == 'down') & (df.loc[i, 'entryPos2'] > -1) & (df.loc[i, 'close'] > df.loc[i, 'ema15']) & (df.loc[i, 'inEntry'] == -1)):
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'entryPos2_time'] = ""

        

        # if previous inEntry is true, set current inEntry - this will reset with later conditions if necessary
        if((df.loc[i-1, 'inEntry'] > -1)):
            df.loc[i, 'inEntry'] = df.loc[i-1, 'inEntry']
            df.loc[i, 'entrySL'] = df.loc[i-1, 'entrySL']
            df.loc[i, 'entryTP'] = df.loc[i-1, 'entryTP']
            df.loc[i, 'entryType'] = df.loc[i-1, 'entryType']

        # If entryPos2 and another green real body, set inEntry, SL, and TP - Bullish
        elif( (df.loc[i-1, 'entryPos2'] > -1) & (df.loc[i, 'open'] <= df.loc[i, 'close']) & (df.loc[i, 'ema_trend'] == 'up')#):
                & (df.loc[i, 'inPB'] == 'yes')):
            print("In Bull Entry: " + (str)(df.loc[i, 'time']))
            df.loc[i, 'inEntry'] = df.loc[i, 'close']
            df.loc[i, 'entrySL'] = df.loc[i, 'valleybear'] - 0.02
            df.loc[i, 'entryTP'] = df.loc[i, 'inEntry'] + (df.loc[i, 'inEntry'] - df.loc[i, 'entrySL'])
            df.loc[i, 'entryType'] = "bull"

        # If entryPos2 and another red real body, set inEntry, SL, and TP - Bearish
        elif( (df.loc[i-1, 'entryPos2'] > -1) & (df.loc[i, 'open'] >= df.loc[i, 'close']) & (df.loc[i, 'ema_trend'] == 'down')#):
                & (df.loc[i, 'inPB'] == 'yes')):
            print("In Bear Entry: " + (str)(df.loc[i, 'time']))
            df.loc[i, 'inEntry'] = df.loc[i, 'close']
            df.loc[i, 'entrySL'] = df.loc[i, 'valleybear'] + 0.02
            df.loc[i, 'entryTP'] = df.loc[i, 'inEntry'] - (df.loc[i, 'entrySL']-df.loc[i, 'inEntry'])
            df.loc[i, 'entryType'] = "bear"

        

        # if inEntry, entrySL is hit, reset inEntry and print that SL was hit (will record this later) - Bullish
        if((df.loc[i, 'inEntry'] > -1) & (df.loc[i, 'entrySL'] <= df.loc[i, 'high']) & (df.loc[i, 'entrySL'] >= df.loc[i, 'low'])): # & (df.loc[i, 'ema_trend'] == 'up')
        #if((df.loc[i, 'inEntry'] > -1) & (df.loc[i, 'entrySL'] >= df.loc[i, 'low'])):
            print('SL hit1 ' + (str)(df.loc[i, 'time']))
            countL += 1
            df.loc[i, 'inEntry'] = -1
            df.loc[i, 'entrySL'] = -1
            df.loc[i, 'entryTP'] = -1
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'entryType'] = ""

        # if inEntry, entrySL is hit, reset inEntry and print that SL was hit (will record this later) - Bearish
        if((df.loc[i, 'inEntry'] > -1) & (df.loc[i, 'entrySL'] >= df.loc[i, 'low']) & (df.loc[i, 'entrySL'] <= df.loc[i, 'high'])):
        #if((df.loc[i, 'inEntry'] > -1) & ((df.loc[i, 'high'] <= df.loc[i, 'entrySL']) & (df.loc[i-1, 'high'] >= df.loc[i, 'entrySL']))):
            print('SL hit2 ' + (str)(df.loc[i, 'time']))
            countL += 1
            df.loc[i, 'inEntry'] = -1
            df.loc[i, 'entrySL'] = -1
            df.loc[i, 'entryTP'] = -1
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'entryType'] = ""
        
        #if inEntry and price hit TP, print that TP was hit (will record this later) - Bullish
        if((df.loc[i, 'inEntry'] > -1) & (df.loc[i, 'entryTP'] <= df.loc[i, 'high']) & (df.loc[i, 'entryTP'] >= df.loc[i, 'low'])): #potential problem with gaps
            print('TP hit1 ' + (str)(df.loc[i, 'time']))
            countW += 1
            df.loc[i, 'inEntry'] = -1
            df.loc[i, 'entrySL'] = -1
            df.loc[i, 'entryTP'] = -1
            df.loc[i, 'entryPos1'] = -1
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'valleybear'] = -1
            df.loc[i, 'entryType'] = ""

        #if inEntry and price hit TP, print that TP was hit (will record this later) - Bearish
        if((df.loc[i, 'inEntry'] > -1) & (df.loc[i, 'entryTP'] >= df.loc[i, 'low']) & (df.loc[i, 'entryTP'] <= df.loc[i, 'high'])):
            print('TP hit2 ' + (str)(df.loc[i, 'time']))
            countW += 1
            df.loc[i, 'inEntry'] = -1
            df.loc[i, 'entrySL'] = -1
            df.loc[i, 'entryTP'] = -1
            df.loc[i, 'entryPos1'] = -1
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'valleybear'] = -1
            df.loc[i, 'entryType'] = ""

            # if inentry and time is 12:59, and neither TP nor SL were hit, get out
        if((int(dt_hour) == 12) and (int(dt_minute) == 59)):
            if(df.loc[i, 'inEntry'] > -1):
                print('Session ended - 12:59')
            df.loc[i, 'inEntry'] = -1
            df.loc[i, 'entrySL'] = -1
            df.loc[i, 'entryTP'] = -1
            df.loc[i, 'entryPos1'] = -1
            df.loc[i, 'entryPos2'] = -1
            df.loc[i, 'valleybear'] = -1
            df.loc[i, 'entryType'] = ""

        
        


    # 10/6 8:14 - the SL is set to the low of the first candle after it pb's past the 15, clearly some logic is messed up but i'm not able to figure out why
    #       tried changing the logic operators but now it's giving me a bigger error






    df.to_csv('baba_results.csv', index = False)
    print("countW: " + str(countW))
    print("countL: " + str(countL))
    pd.set_option('display.max_rows', None)
    print(df.loc[2050:2150,['time', 'hl', 'inPB']])
    #print(df.index)


if __name__ == '__main__':
    main()



     # Further improvements

     # there are times where the wick is impulsive, but it ends up breaking in the data. Ex: https://www.tradingview.com/x/eKjrfDjo/
            # the data had this as 364.00, when it's clearly 361.60. so that messed everything up

    # find HL
    # TGT Oct-8 - incorrectly says in PB with incorrect value for hl - likely because of 15 https://www.tradingview.com/x/xOoRFDQW/ 
    # add check for if 2nd candle went past HL (need to find HL first)

    # BEFORE ANYTHING ELSE, GET RID OF THE LOW-HANGING FRUITS. UGLY RANGES, PRICE STILL IN PB/RANGE, ETC.

    # don't enter trades until 6:40 - DONE

    # Can't have HLLH like https://www.tradingview.com/x/G4rfOUs6/
    # in this case, need a way to determine HL, and if price goes past it, reset to new HL and flag something as "reset"
    # maybe not idk. basically don't want HLLH (unless...?)

    # CRM 10-14: this should be an entry: https://www.tradingview.com/x/601X5EYr/

    # OHLC may have anomoly data - need to detect those. at least print it out with a warning so i can correct it

    #CRM 10/07 - 9:07AM - entry and TP same candle - wrong

    #CRM 10/13 had 8 entries despite being a range with zero actual entries
    
    #CRM 10/21 7:46 entered and never exited - check values
    #  if it's an errant wick, I might have to check for that in helper.py and fix it

    # add check for doji candles - should be okay within a certain range, which is a flag that should be toggled

    # speaking of flags, add flags wherever possible, put variables at the top. 

    # entry at the doji which is under the 15, should be only if it's above the 15 https://www.tradingview.com/x/K2TpsUwI/ (10/06)
    #    same issue https://www.tradingview.com/x/dwlNbBzt/ (10/06)

    # this one should have been an entry (10/08) https://www.tradingview.com/x/ZTo8K97z/ 
    
    # 300 SMA is causing this not to enter: https://www.tradingview.com/x/9fbB59Xd/ (10/26)

    # Even though it's a loss, this one should enter: (FB 10/19) https://www.tradingview.com/x/5Ya2L9fn/

    # TGT has little gaps that mess up the application. best to deal with it now, as stocks will get more gappy
 
    # this one was an entry, but it touched 200. should not be entry https://www.tradingview.com/x/v5fA3xg3/ 

    # trade should close at end of day regardless of where it was. 12:59 to be exact

    # this should enter on the doji https://www.tradingview.com/x/abUo1ZlO/

    # this shouldn't be an entry https://www.tradingview.com/x/v5wtm1sU/

    # this should enter on the 2nd red candle since it's a minor pb (it's entering on the one after) https://www.tradingview.com/x/uh2AUHZP/
    # note that this actually hurts me here (it would enter, doesn't currently), but that's ok. best to stay consistent. i can try different variations out to see which works best https://www.tradingview.com/x/cG8Wiw72/ 

    # if it broke out then pulled back then broke out again, should be the same entry

    # had about 5 losses here (oct 9 - FB) - need a way to find if it's a range https://www.tradingview.com/x/PBEcWXbO/ 

    # need a way to determine SRs
    # possible sr calculation: lookback? last x bars (100, 300, 600)

    # need a way to determine which EMA it hit

    # might not be able to, but could i avoid these kinds of entries? https://www.tradingview.com/x/Dgu2UaQT/ 

    #thinking about whether i should allow simultaneous entries. that's not how i trade, sure, but i'm missing out on important data. i think for this purpose, i should set a flag to allow it
    # flags in general - think of how i can implement them. but for now, it's fine.

    
############# DONE ####################

        # DONE --- anything after 12:45 shouldn't enter https://www.tradingview.com/x/A0WvkO7C/