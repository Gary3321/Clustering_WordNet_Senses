#concatnate all the features together.

#'note_pairs_wnsimilarity.csv' # wordnet::similarity package
features_path='/Users/gary/Documents/2020Fall/IntroNLP/project/'
feature_files=['OntoNotes_SensesPairs.csv','note_pairs_wnsimilarity.csv','OntoNotes_SensesPairs_WNFeatures.csv',
              'WN21mapWn16_topic_similarity.csv','WN21mapWn16_WN_Domain_feature.csv','WN_OED_Map_Feature_OntoNotes_SensesPairs.csv']

df_sensepari=pd.read_csv(features_path+feature_files[0])
df_sensepari= df_sensepari[['Pos', 'Sense1', 'Sense2', 'Merge']]
df_sensepari=df_sensepari.drop_duplicates()

print('df_sensepari',len(df_sensepari))
df_wnpackage=pd.read_csv(features_path+feature_files[1])
print('df_wnpackage',len(df_wnpackage))

df_features_tmp = df_sensepari.merge(df_wnpackage,left_on=['Sense1', 'Sense2','Merge'], 
                              right_on=['sense1', 'sense2','merge'], how='left')


df_features_tmp=df_features_tmp[['Pos', 'Sense1', 'Sense2', 'Merge', 
       'lch', 'hso', 'jcn', 'leskvalue', 'linvalue', 'resvalue', 'vecvalue',
       'wupvalue']]
df_features_tmp=df_features_tmp.drop_duplicates()
print('df_features_tmp',len(df_features_tmp))

df_wncorpus=pd.read_csv(features_path+feature_files[2])

print('df_wncorpus',len(df_wncorpus))

df_features_tmp1 = df_features_tmp.merge(df_wncorpus,left_on=['Pos', 'Sense1', 'Sense2', 'Merge'], 
                              right_on=['Pos', 'Sense1', 'Sense2', 'Merge'], how='left')

df_features_tmp1.columns
print('df_features_tmp1',len(df_features_tmp1))


df_features_tmp1=df_features_tmp1[['Pos', 'Sense1', 'Sense2', 'Merge', 'lch', 'hso', 'jcn', 'leskvalue',
       'linvalue', 'resvalue', 'vecvalue', 'wupvalue', 
        'pertainyms', 'antonyms', 'deriv', 'lemmas',
       'verbgroup', 'verbframe', 'hyper_min', 'hyper_max']]

df_features_tmp1=df_features_tmp1.drop_duplicates() 

#topic feature
df_topfea=pd.read_csv(features_path+feature_files[3])
#replace '.' with '#'
df_topfea['sense1_wn21']=df_topfea['sense1_wn21'].str.replace('.','#')
df_topfea['sense2_wn21']=df_topfea['sense2_wn21'].str.replace('.','#')

df_topfea
print('df_topfea',len(df_topfea))

df_features_tmp2 = df_features_tmp1.merge(df_topfea[['pos','sense1_wn21','sense2_wn21','topic_similarity']],left_on=['Pos', 'Sense1', 'Sense2'], 
                              right_on=['pos', 'sense1_wn21','sense2_wn21'], how='left')


print('df_features_tmp2',len(df_features_tmp2))

df_features_tmp2=df_features_tmp2[['Pos', 'Sense1', 'Sense2', 'Merge', 'lch', 'hso', 'jcn', 'leskvalue',
       'linvalue', 'resvalue', 'vecvalue', 'wupvalue', 'pertainyms',
       'antonyms', 'deriv', 'lemmas', 'verbgroup', 'verbframe', 'hyper_min',
       'hyper_max', 'topic_similarity']]

df_features_tmp2=df_features_tmp2.drop_duplicates()
#domain feature
df_domainfea=pd.read_csv(features_path+feature_files[4])

df_domainfea['sense1_wn21']=df_domainfea['sense1_wn21'].str.replace('.','#')
df_domainfea['sense2_wn21']=df_domainfea['sense2_wn21'].str.replace('.','#')
print('df_domainfea',len(df_domainfea))

df_features_tmp3 = df_features_tmp2.merge(df_domainfea[['pos','sense1_wn21','sense2_wn21','wn_domain_feature']],left_on=['Pos', 'Sense1', 'Sense2'], 
                              right_on=['pos', 'sense1_wn21','sense2_wn21'], how='left')

df_features_tmp3.columns
print('df_features_tmp3',len(df_features_tmp3))

df_features_tmp3=df_features_tmp3[['Pos', 'Sense1', 'Sense2', 'Merge', 'lch', 'hso', 'jcn', 'leskvalue',
       'linvalue', 'resvalue', 'vecvalue', 'wupvalue', 'pertainyms',
       'antonyms', 'deriv', 'lemmas', 'verbgroup', 'verbframe', 'hyper_min',
       'hyper_max', 'topic_similarity', 'wn_domain_feature']]

df_features_tmp3=df_features_tmp3.drop_duplicates()
#wn-oed mapping feature
df_wnoedfea=pd.read_csv(features_path+feature_files[5])
df_wnoedfea
print('df_wnoedfea',len(df_wnoedfea))
df_features = df_features_tmp3.merge(df_wnoedfea[['Pos', 'Sense1', 'Sense2', 'Merge','wn_oed_feature']],left_on=['Pos', 'Sense1', 'Sense2','Merge'], 
                              right_on=['Pos', 'Sense1', 'Sense2', 'Merge'], how='left')

df_features=df_features[['Pos', 'Sense1', 'Sense2', 'Merge', 'lch', 'hso', 'jcn', 'leskvalue',
       'linvalue', 'resvalue', 'vecvalue', 'wupvalue', 'pertainyms',
       'antonyms', 'deriv', 'lemmas', 'verbgroup', 'verbframe', 'hyper_min',
       'hyper_max', 'topic_similarity', 'wn_domain_feature', 'wn_oed_feature']]

df_features=df_features.drop_duplicates()
df_features
print('df_features',len(df_features))

#since NaN, there are still duplicated rows in df_features. drop duplicates after replacing
#Nan with other values


#update verb group using results from perl
#use perl to get the following features: antonyms, deriv, pertainyms, verbgroups
file_path='/Users/gary/Documents/2020Fall/IntroNLP/project/note_pairs_wncourpus_similarity.csv'
df_perl=pd.read_csv(file_path)

df_perl_vg=df_perl[df_perl[' vgrp1']==df_perl[' vgrp2']]
for i in range(len(df_perl_vg)):
    sense1=df_perl_vg.loc[df_perl_vg.index[i],'sense1']
    sense2=df_perl_vg.loc[df_perl_vg.index[i],' sense2']
    df_features.loc[((df_features['Sense1']==sense1)&(df_features['Sense2']==sense2)),'verbgroup']=1


df_features.to_csv('feature_space.csv',index=False)

