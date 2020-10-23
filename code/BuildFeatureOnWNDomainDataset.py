#create feature based on WN Domain dataset
#WordNet Domain dataset; two datafile, one for WN1.6, one for WN2.0
#Snow didn't mention which one they use, but I use WN1.6, since I mapped 2.1 to 1.6
#Snow created two features, but I only created the first one, since I was not sure about
#the second one.
#- "wn-domains-2.0-20050210" contains the mapping between Princeton WordNet 1.6 synsets and their corresponding domains. The format is as above.

df_wn21wn16=pd.read_csv('WN21mapWn16_full.csv')
df_wn_domain=pd.read_csv('/Users/gary/Documents/2020Fall/IntroNLP/project/FeatureSpace/wn-domains-3.2/wn-domains-2.0-20050210',
                         sep='\t',header=None)


df_wn_domain.columns=['offset-pos','domain']
#filter offers that not in domain data
#wn16_offsets_lst = list(set(df_wn21wn16['offset1_wn16'].to_list()+df_wn21wn16['offset2_wn16'].to_list()))

#domain_offsets_lst=list(set(df_wn_domain['offset-pos'].to_list()))

#overlap_offsets_lst = list(set(wn16_offsets_lst)&set(domain_offsets_lst))

for i in range(len(df_wn21wn16)):
    offset1=df_wn21wn16.loc[df_wn21wn16.index[i],'offset1_wn16']
    offset2=df_wn21wn16.loc[df_wn21wn16.index[i],'offset2_wn16']
    dm1=df_wn_domain[df_wn_domain['offset-pos']==offset1]['domain'].to_list()
    dm2=df_wn_domain[df_wn_domain['offset-pos']==offset2]['domain'].to_list()
    if (len(dm1)==1 and len(dm2)==1):
        if dm1[0]==dm2[0]:
            feature=1
    else:
        feature=0
    
    df_wn21wn16.loc[df_wn21wn16.index[i],'wn_domain_feature']=feature

df_wn21wn16.to_csv('WN21mapWn16_WN_Domain_feature.csv',index=False)

