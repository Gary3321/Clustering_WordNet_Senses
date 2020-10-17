'''
Build feature space:
1, twin: the number of shared synonyms between two synsets
2, antonym: whether two synsets share an antonym
3, pertainym: whether two synsets share an pertainym
4, deriv: whether two synsets share derivationally related forms
5, verbgrp: whether two verb synsets are linked in a VERBGROUP (indicating semantic similarity)
6, verbfrm: whether two verb synsets share a VERBFRAM (indicating syntactic similarity) 

'''
#wordnet 2.1

#df_pairs
for i in range(len(df_pairs)):
    pertainyms1=[]
    antonyms1=[]
    deriv1=[]
    lemmas1=[]
    verbgroup1=[]
    verbframe1=[]
    pertainyms2=[]
    antonyms2=[]
    deriv2=[]
    lemmas2=[]
    verbgroup2=[]
    verbframe2=[]
    pertainymsflag=''
    antonymsflag=''
    derivflag=''
    lemmasflag=''
    verbgroupflag=''
    verbframeflag=''
    hyper_min=''
    hyper_max=''

    sense1 = df_pairs.loc[df_pairs.index[i],'Sense1']
    sense1 = sense1.replace('#','.')
    sense2 = df_pairs.loc[df_pairs.index[i],'Sense2']
    sense2 = sense2.replace('#','.')
    pos = df_pairs.loc[df_pairs.index[i],'Pos']
    
    # sense1's twin, pertainyms, antonyms, derivationally_related_forms,
    # verb group, frame id, hyper_min, hyper_max
    try:
        
        #WN, WNMax feature
        #calculate hyper distance
        sense1_hyper = wn2.synset(sense1)
        sense1_hypers = lambda s: s.hypernyms()
        hyper1= list(sense1_hyper.closure(sense1_hypers))
        
        sense2_hyper = wn2.synset(sense2)
        sense2_hypers = lambda s: s.hypernyms()
        hyper2 = list(sense2_hyper.closure(sense2_hypers))
           
        #find the nearest hyper, and average the distance as the least distance
        for h1 in hyper1:
            if h1 in hyper2:
                hyper_min = (hyper1.index(h1)+hyper2.index(h1))/2
                break
        


        #find the farest hyper, and average the distance as the largest distance
        for h1 in reversed(hyper1):
            if h1 in hyper2:
                hyper_max = (hyper1.index(h1)+hyper2.index(h1))/2
                break
                
        
        for lemma in wn2.synset(sense1).lemmas():
            
            pertainyms1=pertainyms1+lemma.pertainyms()
            antonyms1=antonyms1+lemma.antonyms()
            deriv1=deriv1+lemma.derivationally_related_forms()
            lemmas1.append(lemma.name())
            
            if pos=='v':
                verbgroup1=verbgroup1+lemma.verb_groups()
                verbframe1=verbframe1+lemma.frame_ids()

                
        # sense2's pertainyms, antonyms, derivationally_related_forms
        for lemma in wn2.synset(sense2).lemmas():
            
            pertainyms2=pertainyms2+lemma.pertainyms()
            antonyms2=antonyms2+lemma.antonyms()
            deriv2=deriv2+lemma.derivationally_related_forms()
            lemmas2.append(lemma.name())
             
            #verb group, verb frame
            if pos=='v':
                verbgroup2=verbgroup2+lemma.verb_groups()
                verbframe2=verbframe2+lemma.frame_ids()
                
      
        if (len(set(pertainyms1)&set(pertainyms2))>0):
            pertainymsflag=1
        else:
            pertainymsflag=0

        if (len(set(antonyms1)&set(antonyms2))>0):
            antonymsflag=1
        else:
            antonymsflag=0 

        if (len(set(deriv1)&set(deriv2))>0):
            derivflag=1
        else:
            derivflag=0 
        
        #verb group, verb frame
        if pos=='v':
            if (len(set(verbgroup1)&set(verbgroup2))>0):
                verbgroupflag=1
            else:
                verbgroupflag=0
                
            if (len(set(verbframe1)&set(verbframe2))>0):
                verbframeflag=1
            else:
                verbframeflag=0
            

        
        lemmasflag=len(set(lemmas1)&set(lemmas2))
       
        
        df_pairs.loc[df_pairs.index[i],'pertainyms']=pertainymsflag
        df_pairs.loc[df_pairs.index[i],'antonyms']=antonymsflag
        df_pairs.loc[df_pairs.index[i],'deriv']=derivflag
        df_pairs.loc[df_pairs.index[i],'lemmas']=lemmasflag
        
        df_pairs.loc[df_pairs.index[i],'verbgroup']=verbgroupflag
        df_pairs.loc[df_pairs.index[i],'verbframe']=verbframeflag
         
        df_pairs.loc[df_pairs.index[i],'hyper_min']=hyper_min
        df_pairs.loc[df_pairs.index[i],'hyper_max']=hyper_max

        
    except:
        None
    
df_pairs.to_csv('OntoNotes_SensesPairs_WNFeatures.csv')    
 
