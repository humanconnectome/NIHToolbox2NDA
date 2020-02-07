
#program to turn list of unzipped folders of templates etc from the NDA into something that more closely resembles a crosswalk

import os
import pandas as pd
from openpyxl import load_workbook

#specify path to the folder that contains the unzipped folders from the NDA - end path in '/' or
# tell me how I can make this code robust to variations
inout='/yourpath/NIH_toolbox_crosswalk_docs/'

#open one of the folders that the NDA sent and find the file that contains the list of vars in
#your file and the list of vars in the NDA as one-to-one pairs
#for example, we have files with the column headers "NDA Element" and "HCP-D Element"
#we also have files with the column headers "NDA Element" and "HCP-A Element"
#provide the name of local variable:
localvar="HCP-D Element"

# get list of files and folders in the inout directory
# The string containing the name of the new folders from the NDA will be assigned to
# variable called 'Instrument_Short' because after filtering out all the other
# files/folders (list1 and list2 below) thats what you'll have:
# the NDAs shorthand name for the NIH Toolbox Instrument
dirs=pd.DataFrame(os.listdir(inout),columns=['Instrument_Short'])

#initialize an empty crosswalk
crosswalk_meta=pd.DataFrame(columns=['Instrument_Short','key','template','requestfile','varmapfile'])

#create two lists of for file extensions and/or folders in inout that you don't want to be treated
# as something to be added to a crosswalk
list1=['zip','csv','xlsx','pptx'] #file extensions in this folder of folders from Leo that you want to ignore
list2=['HCPD','temp','added_tocrosswalk','dummypass','almost trash','prepped_structures'] #identify folders you want to ignore

# for the items not in list1 or list2, read the folder contents and turn them into something appendable/mergeable
# four possible files:
# Mapping Key has the Full Name of the NDA structure to which this stuff will be mapped, the short name,
# and the name on the Form as we will be uploading it (Inst)
# One file in this folder has an Instrument_short.structure name format
# Occasionally you'll get a formRequest file which will contains NDA verbal instructions that
# ultimately need to be translated into executable python code (more on this later).
# The template file is not used in the crosswalk, but may come in handy for debugging (i.e. if someone
# on either end of this process accidentally assigned the wrong aliases).

for i in dirs.Instrument_Short:
    for j in list1:
        if j in i:
            print('skipping file '+i)
            i='dummypass'
    if i in list2:
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
        df = df.loc[~(df[localvar] == 'PIN')].copy()
        df['Instrument_Short'] = cw.Instrument_Short[0]
        cw2 = pd.merge(cw, df, how='outer', on='Instrument_Short')
        crosswalk_meta = pd.concat([crosswalk_meta, cw2], axis=0,sort=True)

#lastly grab the name of the structure from the varmapfile
crosswalk_meta['structure']=crosswalk_meta.varmapfile.str.split('.').str[-2]

# output this information to a csv in the inout directory so you can easily append it to 
# the full existing/curated Crosswalkfile that you tweaked for your purposes (by renaming localvar, for example)
crosswalk_meta[['template','Instrument_Short','structure','NDA Element',localvar,'requestfile']].to_csv(inout+'crosswalk_part_'+localvar+'.csv',index=False)


