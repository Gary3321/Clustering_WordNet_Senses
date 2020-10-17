'''
Topic signature data:
Each file is named according to the following pattern:
measure.BNCfilt.target_word.PoS.sense.txt.bz2
for instance: tf_idf.BNCfilt.church.n.1.txt.bz2, which corresponds to the
topic signature of the first sense of church built using the tf.idf
measure.
- Each file is compresed with bzip2 (http://sources.redhat.com/bzip2/)

1) read df_wn21wn16 and copy the corresponding files into another folder
2) unzip these files
3) calculate the cosine similarity of each pair 
'''
import os
import os.path

df_wn21wn16=pd.read_csv('WN21mapWn16.csv')
directory='/Users/gary/Documents/2020Fall/IntroNLP/project/FeatureSpace/TopicSignatures/signatures_lem/'
des_dir='/Users/gary/Documents/2020Fall/IntroNLP/project/FeatureSpace/TopicSingatures_SnowProject/'

total_pair = len(df_wn21wn16)
senses=[]
for i in range(total_pair):
    sense1=df_wn21wn16.loc[df_wn21wn16.index[i],'sense1_wn16']
    sense2=df_wn21wn16.loc[df_wn21wn16.index[i],'sense2_wn16']
    senses.append(sense1)
    senses.append(sense2)

for s in senses:
    if s!=s:
        senses.remove(s)
#copy corresponding files to des_dir
j=0
for s in set(senses):
    try:
        if (j%500==0):
            print('processing {}/{}'.format(j,len(set(senses))))
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in [f for f in filenames if "BNC_filt."+s in f]:
                cp='cp '+os.path.join(dirpath, filename)+' '+des_dir+filename
                #copy files 
                os.system(cp)
                #unzip='bzip2 -d '+
                #print(filename)
        j+=1
    except:
        None


