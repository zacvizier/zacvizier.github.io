# coding=utf-8

import pandas as pd
import decimal
import warnings
import time
import numpy

df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/19phzMaZtwMfkPH69ISJRhdqF9TbCi8TwAuPo_K84HU4/export?format=csv')

df = df1[(df1['Play'] > 0)]

print df


#for index, row in df.iterrows():