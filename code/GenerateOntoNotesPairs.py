#Generate synset pairs from OntoNotes dataset

import re
import pandas as pd
from os import listdir
from os.path import isfile, join

from xml.dom.minidom import parse
import xml.dom.minidom

def read_xml(path, df_ontonotes,f):
    DOMTree = xml.dom.minidom.parse(path)
    collection = DOMTree.documentElement


    if collection.hasAttribute("lemma"):
        wordpos = collection.getAttribute("lemma")
        #print("Root element : %s" % collection.getAttribute("lemma"))
        #if wordpos is different with filename,use filename
        if f.replace('.xml','')!=wordpos:
            #print('f:',f,'wordpos:',wordpos)
            wordpos=f.replace('.xml','')


    # get all sense
    senses = collection.getElementsByTagName("sense")

    # get the detai info for each sense
    for sense in senses:
        groupsense=''
        group=''
        version=''
        sensenums=''
        if sense.hasAttribute("n"):
            groupsense=sense.getAttribute("n")
            #print ("n: %s" % sense.getAttribute("n"))
        if sense.hasAttribute("group"):
            group = sense.getAttribute("group")
            #print ("group: %s" % sense.getAttribute("group"))
        mapping=sense.getElementsByTagName('mappings')
        for mp in mapping:
            wn=mp.getElementsByTagName('wn')
            try:
                sensenums=wn[0].childNodes[0].data.replace('\n\t','').strip()
            except:
                sensenums=''
            for wnn in wn:
                if wnn.hasAttribute("version"):
                    version=wnn.getAttribute("version")
                    #print('version:',version)


        df_ontonotes = df_ontonotes.append({'Version':version,'WordPos':wordpos,'SenseNums':sensenums,'Group':group,'GroupSense':groupsense},
                                          ignore_index=True)
    return df_ontonotes



def generate_sensepair(df_data,df_pairs):
    """
    Purpos: generate sense pairs
    Auguments:
    df_data: input data
    df_pairs: output data
    """
    #
    wordpos_list=list(set(df_data['WordPos'].to_list()))

    for w in wordpos_list:
        df_word = df_data[df_data['WordPos']==w]
        for i in range(len(df_word)):
            pos =w.split('-')[1]
            wp_i=df_word.loc[df_word.index[i],'WordPos']
            sn_i=df_word.loc[df_word.index[i],'SenseNums']
            gp_i=df_word.loc[df_word.index[i],'GroupSense']
            sense1=wp_i.replace('-','#')+'#'+sn_i

            for j in range(i+1,len(df_word)):
                wp_j=df_word.loc[df_word.index[j],'WordPos']
                sn_j=df_word.loc[df_word.index[j],'SenseNums']
                gp_j=df_word.loc[df_word.index[j],'GroupSense']
                sense2 = wp_j.replace('-','#')+'#'+sn_j

                if gp_i==gp_j:

                    df_pairs=df_pairs.append({'Pos':pos,'Sense1':sense1,'Sense2':sense2,'Merge':'merged'},
                                                      ignore_index=True)
                else:

                    df_pairs=df_pairs.append({'Pos':pos,'Sense1':sense1,'Sense2':sense2,'Merge':'not-merged'},
                                                      ignore_index=True)
    return df_pairs


    


filepath = '/Users/gary/Documents/2020Fall/IntroNLP/project/DataSet/OntoNotes/Ontonotes-sense-groups_wn21/ontonotes-sense-groups/'

filelist = [f for f in listdir(filepath) if isfile(join(filepath, f))] #get all files' name
files_num = len(filelist)
print(files_num)
#print(filelist)
countn=0
countv=1
filesn=[]
filesv=[]
 
df_ontonotes=pd.DataFrame(columns=['Version','WordPos','SenseNums','Group','GroupSense'])

for f in filelist:
    df_ontonotes = read_xml(filepath+f,df_ontonotes,f)
    if '-n' in f:
        countn+=1
        filesn.append(f)
    if '-v' in f:
        countv+=1
        filesv.append(f)
print('n:',countn, 'v:',countv)



df_ontonotes21=df_ontonotes[df_ontonotes['Version']=='2.1']
wordpos_list=list(set(df_ontonotes21['WordPos'].to_list()))
#add pos with duplicate sense number into posduplist
posduplist=[]
for wp in wordpos_list:
    wnsensesnum=','.join(df_ontonotes21[df_ontonotes21['WordPos']==wp]['SenseNums'].to_list())

    wnsensesnumlist=wnsensesnum.split(',')
    #get the same SenseNum in different group
    if len(wnsensesnumlist)>len(set(wnsensesnumlist)):
        posduplist.append(wp)
        #print(wp,' has duplicate sense')

df_ontonotes21.to_csv('OntoNotes_Senses_raw.csv')
#one sense num in one group
df_noteclean21=df_ontonotes21[df_ontonotes21['WordPos'].isin(list(set(wordpos_list)-set(posduplist)))]  


#remove noisy data (bank-n 2&&3; drug-n 1&&2)
#df_note_clean = df_ontonotes[~(df_ontonotes['SenseNum'].str.len()>3)]

df_noteclean21= df_noteclean21[df_noteclean21['SenseNums'].notna()]
df_noteclean21['SenseNums'].replace('wn 1','1',inplace=True)
#remove row with character
df_noteclean21 = df_noteclean21[~(df_noteclean21['SenseNums'].str.contains('[A-Za-z]|&',regex=True))]

df_tmp1=df_noteclean21[df_noteclean21['SenseNums'].str.len()<3]
#df_tmp2 store cluster senses
df_tmp2 = df_noteclean21[~(df_noteclean21['SenseNums'].str.len()<3)]


#split clusters, df_tmp1 stores all the senese and  (GroupSense)
#df_tmp1.drop(columns='Unnamed: 0',inplace=True)
for i in range(len(df_tmp2)):
    Version = df_tmp2.loc[df_tmp2.index[i],'Version']
    WordPos = df_tmp2.loc[df_tmp2.index[i],'WordPos']
    SenseNums = df_tmp2.loc[df_tmp2.index[i],'SenseNums']
    Group = df_tmp2.loc[df_tmp2.index[i],'Group']
    GroupSense = df_tmp2.loc[df_tmp2.index[i],'GroupSense']
    if (',' in SenseNums):
        senses=SenseNums.split(',')
        for s in senses:
            df_tmp1=df_tmp1.append({'Version':Version,'WordPos':WordPos,'SenseNums':s,
                                   'Group':Group,'GroupSense':GroupSense},ignore_index=True)
    elif (' ' in SenseNums):
            senses=SenseNums.split(' ')
            for s in senses:
                df_tmp1=df_tmp1.append({'Version':Version,'WordPos':WordPos,'SenseNums':s,
                                       'Group':Group,'GroupSense':GroupSense},ignore_index=True)
    elif ('.' in SenseNums):
            senses=SenseNums.split('.')
            for s in senses:
                df_tmp1=df_tmp1.append({'Version':Version,'WordPos':WordPos,'SenseNums':s,
                                       'Group':Group,'GroupSense':GroupSense},ignore_index=True)

df_tmp1.to_csv('OntoNotes_Senses_cleaned.csv')


df_pairs=pd.DataFrame(columns=['Pos','Sense1','Sense2','Merge'])

#generate pairs data
df_pairs=generate_sensepair(df_tmp1,df_pairs)
df_pairs.to_csv('OntoNotes_SensesPairs.csv')

