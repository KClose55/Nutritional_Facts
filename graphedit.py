import numpy as np
import pandas as pd
import openpyxl as op

df = pd.read_excel('bakingMAIN.xlsx', index_col='Unnamed: 0')
#df2 = pd.read_excel('bakingTRANSPOSE.xlsx', index_col='Unnamed: 0')
#df3 = pd.read_excel('dailyvalue.xlsx', index_col='nutrient')
#df4 = op.load_workbook('nftemplate3.xlsx')




#excel_file='Miscellaneous\\baking.xlsx'
#df3 = pd.read_excel(excel_file, index_col='Unnamed: 0')
df2=df.transpose()
df2.to_excel('bakingTRANSPOSE.xlsx')

#for i in df.index:
#    if df['gmwt desc1'][i] == 'cup':
#        df['gmwt desc3'][i]='cups'
#        df['gmwt 3'][i]=df['gmwt 1'][i]
#    elif df['gmwt desc1'][i] == 'oz':
#        df['gmwt desc3'][i]='ounce'
#        df['gmwt 3'][i]=df['gmwt 1'][i]
#        df['gmwt desc4'][i]='ounces'
#        df['gmwt 4'][i]=df['gmwt 1'][i]
#    elif df['gmwt desc1'][i] == 'tsp':
#        df['gmwt desc3'][i]='teaspoon'
#        df['gmwt 3'][i]=df['gmwt 1'][i]
#        df['gmwt desc4'][i]='teaspoons'
#        df['gmwt 4'][i]=df['gmwt 1'][i]
#    elif df['gmwt desc1'][i] == 'tbsp':
#        df['gmwt desc3'][i]='tablespoon'
#        df['gmwt 3'][i]=df['gmwt 1'][i]
#        df['gmwt desc4'][i]='tablespoons'
#        df['gmwt 4'][i]=df['gmwt 1'][i]
#
#    if df['gmwt desc2'][i] == 'cup':
#        df['gmwt desc5'][i]='cups'
#        df['gmwt 5'][i]=df['gmwt 2'][i]
#    elif df['gmwt desc2'][i] == 'oz':
#        df['gmwt desc5'][i]='ounce'
#        df['gmwt 5'][i]=df['gmwt 2'][i]
#        df['gmwt desc6'][i]='ounces'
#        df['gmwt 6'][i]=df['gmwt 2'][i]
#    elif df['gmwt desc2'][i] == 'tsp':
#        df['gmwt desc5'][i]='teaspoon'
#        df['gmwt 5'][i]=df['gmwt 2'][i]
#        df['gmwt desc6'][i]='teaspoons'
#        df['gmwt 6'][i]=df['gmwt 2'][i]
#    elif df['gmwt desc2'][i] == 'tbsp':
#        df['gmwt desc5'][i]='tablespoon'
#        df['gmwt 5'][i]=df['gmwt 2'][i]
#        df['gmwt desc6'][i]='tablespoons'
#        df['gmwt 6'][i]=df['gmwt 2'][i]







