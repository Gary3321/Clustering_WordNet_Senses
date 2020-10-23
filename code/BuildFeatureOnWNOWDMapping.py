#create feature based on mapping between WN and OED, the mapping is based on WN21
#read mapping file
file_map_wnoed=open('/Users/gary/Documents/2020Fall/IntroNLP/project/FeatureSpace/sense_clusters-21.senses','r')

#read sysnset pairs
df_pairs=pd.read_csv('OntoNotes_SensesPairs.csv')


#df_pairs_n=df_pairs[df_pairs['Pos']=='n']
#total_pair=len(df_pairs_n)
total_pair=len(df_pairs)
for i in range(total_pair):
    if (i%1000 ==0):
        print('processing {}/{}'.format(i,total_pair))
    sense1_wn21 = df_pairs.loc[df_pairs.index[i],'Sense1']
    headword=sense1_wn21.split('#')[0]
    sense1_wn21 = sense1_wn21.replace('#','.')
    sense2_wn21 = df_pairs.loc[df_pairs.index[i],'Sense2']
    sense2_wn21 = sense2_wn21.replace('#','.')
    pos = df_pairs.loc[df_pairs.index[i],'Pos']
    
    sense1_keys=''
    sense2_keys=''
    try:
        for lemma1 in wn2.synset(sense1_wn21).lemmas():
            #get sense key for wn21 sense1
            sense1_keys=sense1_keys+lemma1.key()+';'
        for lemma2 in wn2.synset(sense2_wn21).lemmas():
            #get sense key for wn21 sense1
            sense2_keys=sense2_keys+lemma1.key()+';'
    except:
        None

    df_pairs.loc[df_pairs.index[i],'Sense1_keys']=sense1_keys
    df_pairs.loc[df_pairs.index[i],'Sense2_keys']=sense2_keys

#filter sense keys is null
df_pairs = df_pairs[(df_pairs['Sense1_keys'].str.len()>5)&(df_pairs['Sense1_keys'].str.len()>5)]

#get sense clusterings from the mapping between WN and OED
lines = file_map_wnoed.readlines()
count=0
wnoed_lst=[] # a list of sets.
for line in lines:
    count+=1
    line=line.strip('\n')
    if ' ' in line:
        wnoed_lst.append(set(line.split(' ')))

for i in range(len(df_pairs)):
    if i%1000 ==0:
        print('processing {}/{}'.format(i,total_pair))
    sense1_key=df_pairs.loc[df_pairs.index[i],'Sense1_keys']
    sk1_set=set(sense1_key.split(';'))
    
    sense2_key=df_pairs.loc[df_pairs.index[i],'Sense2_keys']
    sk2_set=set(sense2_key.split(';'))
    
    feature=0
    for  w in wnoed_lst:
        sk1_len=len(sk1_set & w)
        sk2_len=len(sk2_set & w)
        if (sk1_len>0 and sk2_len>0):
            feature=1
            break
    
    df_pairs.loc[df_pairs.index[i],'wn_oed_feature']=feature
    
df_pairs.to_csv('WN_OED_Map_Feature_OntoNotes_SensesPairs.csv',index=False)

