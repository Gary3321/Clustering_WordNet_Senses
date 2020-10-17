#map WN2.1 to WN1.6 for topic signuature
#this mapping only for nouns is based on sensekey, headword, and pos
#
'''
The basic idea is that if two synsets from different WN versions share the same ‘word’+’pos’+’sense key’, 
then they are identical. This algorithm is tested on WN2.x and WN3.0, and achieved 97% accuracy.
'''

df_pairs=pd.read_csv('OntoNotes_SensesPairs.csv')

df_wn21wn16=pd.DataFrame(columns=['pos','sense1_wn21','sense2_wn21','sense1_wn16','sense2_wn16','sense1_wn21_def','sense1_wn16_def','sense2_wn21_def','sense2_wn16_def'])

df_pairs_n=df_pairs[df_pairs['Pos']=='n']
total_pair=len(df_pairs_n)
for i in range(total_pair):
    if (i%1000 ==0):
        print('processing {}/{}'.format(i,total_pair))
    sense1_wn21 = df_pairs_n.loc[df_pairs_n.index[i],'Sense1']
    headword=sense1_wn21.split('#')[0]
    sense1_wn21 = sense1_wn21.replace('#','.')
    sense2_wn21 = df_pairs_n.loc[df_pairs_n.index[i],'Sense2']
    sense2_wn21 = sense2_wn21.replace('#','.')
    pos = df_pairs_n.loc[df_pairs_n.index[i],'Pos']
    
    try:
        for lemma1 in wn2.synset(sense1_wn21).lemmas():
            sense1_wn21_def = wn2.synset(sense1_wn21).definition()
            #get sense key for wn21 sense1
            wn2_sense1_key=lemma1.key()
            sense1_wn16=''
            #enumerate all wn synsests for headword#pos,find the same sense key
            for synset1 in wn16.synsets(headword, pos):
                lemmas = synset1.lemmas()
                for l1 in lemmas:
                    #if sense key equal, keep the wn16 synset name
                    if l1.key() == wn2_sense1_key:
                        sense1_wn16=synset1.name()
                        sense1_wn16_def= synset1.definition()


        for lemma2 in wn2.synset(sense2_wn21).lemmas():
            sense2_wn21_def = wn2.synset(sense2_wn21).definition()
            wn2_sense2_key=lemma2.key()
            sense2_wn16=''
            for synset2 in wn16.synsets(headword, pos):
                lemmas = synset2.lemmas()
                for l2 in lemmas:
                    if l2.key() == wn2_sense2_key:
                        sense2_wn16=synset2.name()
                        sense2_wn16_def= synset2.definition()
    
        df_wn21wn16=df_wn21wn16.append({'pos':pos,'sense1_wn21':sense1_wn21,'sense2_wn21':sense2_wn21,'sense1_wn16':sense1_wn16.replace('.0','.'),'sense2_wn16':sense2_wn16.replace('.0','.'),'sense1_wn21_def':sense1_wn21_def,'sense1_wn16_def':sense1_wn16_def,'sense2_wn21_def':sense2_wn21_def,'sense2_wn16_def':sense2_wn16_def},
                                   ignore_index=True)
    except:
        None
    
df_wn21wn16.to_csv('WN21mapWn16.csv',index=False)
