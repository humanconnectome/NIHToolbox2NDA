
#program to turn list of unzipped folders from Leo into something that more closely resembles a crosswalk

import os
import pandas as pd
from openpyxl import load_workbook

inout='/home/petra/UbWinSharedSpace1/redcap2nda_Lifespan2019/NIH_toolbox_crosswalk_docs/'
dirs=pd.DataFrame(os.listdir(inout),columns=['Instrument_Short'])
crosswalk_meta=pd.DataFrame(columns=['Instrument_Short','key','template','requestfile','varmapfile'])
lsit2=['zip','csv']
listst=['HCPD','temp','added','dummypass']
for i in dirs.Instrument_Short:
    for j in lsit2:
        if j in i:
            print('skipping file '+i)
            i='dummypass'
    if i in listst:
        if i not in 'dummypass':
            print('skipping folder '+i)
    else:
        requestfile=''  #need to initialize this particular var becaus some folders dont have requests
        cw = pd.DataFrame(columns=['Instrument_Short', 'key', 'template', 'requestfile', 'varmapfile'])
        haystack=os.listdir(inout+i)
        for j, element in enumerate(haystack):
            if "Key" in element:
                key=element
            elif "template" in element:
                template=element
            elif "01.xlsx" in element:
                varmapfile=element
            elif 'equest' in element:
                requestfile=element
        cw.loc[0, ['Instrument_Short', 'key','template','varmapfile','requestfile']] = [i, key,template,varmapfile,requestfile]
        wb = load_workbook(inout + cw.Instrument_Short[0] + '/' + cw.varmapfile[0])
        ws = wb.active
        df = pd.DataFrame(ws.values)
        df.columns = [df.iloc[0, 0], df.iloc[0, 1]]
        df = df.loc[~(df['NDA Element'] == 'NDA Element')].copy()
        df = df.loc[~(df['HCP-A Element'] == 'PIN')].copy()
        df['Instrument_Short'] = cw.Instrument_Short[0]
        cw2 = pd.merge(cw, df, how='outer', on='Instrument_Short')
        crosswalk_meta = pd.concat([crosswalk_meta, cw2], axis=0,sort=True)
crosswalk_meta['structure']=crosswalk_meta.varmapfile.str.split('.').str[-2]
crosswalk_meta[['template','Instrument_Short','structure','NDA Element','HCP-A Element','requestfile']].to_csv(inout+'crosswalk_HCPA.csv',index=False)


