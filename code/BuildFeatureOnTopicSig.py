#build topic signature feature for POS=n
#calculate cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np

df_wn21wn16=pd.read_csv('WN21mapWn16.csv')


des_dir='/Users/gary/Documents/2020Fall/IntroNLP/project/FeatureSpace/TopicSingatures_SnowProject/'
filelist = [f for f in listdir(des_dir) if isfile(join(des_dir, f))] #get all files' name

#add corresponding filename to the dataframe
for i in range(len(df_wn21wn16)):
    if i%200==0:
        print('processing {}/{}'.format(i,len(df_wn21wn16)))
    sense1= df_wn21wn16.loc[df_wn21wn16.index[i],'sense1_wn16']
    sense2= df_wn21wn16.loc[df_wn21wn16.index[i],'sense2_wn16']
    for f in filelist:
        if '.'+str(sense1)+'.' in f:
            df_wn21wn16.loc[df_wn21wn16.index[i],'sense1_topic']=f
        if '.'+str(sense2)+'.' in f:
            df_wn21wn16.loc[df_wn21wn16.index[i],'sense2_topic']=f


#calculate the similarity
df_topic=df_wn21wn16[(df_wn21wn16['sense1_topic'].notna())&(df_wn21wn16['sense2_topic'].notna())]

for j in range(len(df_topic)):
    topic1 = df_topic.loc[df_topic.index[j],'sense1_topic']
    topic2 = df_topic.loc[df_topic.index[j],'sense2_topic']
    
    df_tp1=pd.read_csv(des_dir+topic1,header=None,sep=' ')
    df_tp1.columns=['word','tfidf','num']
    tp1=df_tp1['tfidf'].to_list()
    
    df_tp2=pd.read_csv(des_dir+topic2,header=None,sep=' ')
    df_tp2.columns=['word','tfidf','num']
    tp2=df_tp2['tfidf'].to_list()
    
    if len(tp1)>len(tp2):
        tp1 = tp1[:len(tp2)]
    else:
        tp2 = tp2[:len(tp1)]
        
    tp1 = np.array(tp1).reshape(1,len(tp1))
    tp2 = np.array(tp2).reshape(1,len(tp2))
    
    df_topic.loc[df_topic.index[j],'topic_similarity']=cosine_similarity(tp1,tp2)[0,0] 
    

df_topic.to_csv('WN21mapWn16_topic_similarity.csv',index=False) 
