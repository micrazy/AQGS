# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 09:47:45 2017

@author: user
"""

import gensim, logging
import  os,re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




###stopwords
stopwords=[]
with open('./data/stopwords.txt',encoding='utf-8') as fpsw:
    for l in fpsw.readlines():
        stopwords.append(l.strip())
#print(stopwords)
### import data 
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname),encoding='utf-8'):
                l=re.split('[,.?;:!\'\"\t\n ]',line.lower())
                ll=[w for w in l if w not in stopwords and  len(w)>1] 
                yield ll

                
                
sentences = MySentences('./data/tatoeba') # a memory-friendly iterator
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#load model
model = gensim.models.Word2Vec.load_word2vec_format('./data/model_vec',binary=True) 

###training data
model2=gensim.models.Phrases(sentences,threshold=5)
#examples
model.most_similar('pay')
model.similarity('pay','attention')
#process sentences
#example word='computer'




wordlist=['sun','part','love','take','apple']
#with open('./data/words.txt',encoding='utf-8') as fpw:
#    wordlist=fpw.readlines()

#swordlist=['as']
phrasedict={}
for phrase, score in model2.export_phrases(sentences):
    s=phrase.decode("utf-8")
    for word in wordlist:
        word=word.replace('\n','')
        if word in s.split():
            phrasedict[s]=score
        
sortphrase=sorted(phrasedict.items(), key=lambda x:x[1],reverse=True)
for i in range(len(sortphrase)):
    print(sortphrase[i])

for word in wordlist:    
    vec={}

    collocation={}    
    word=word.replace('\n','')
    
    #compute number of  sentences contain the word
    totalnum=0
    count_accept=0
   
    for line in open('./data/sample/'+word+'.txt',encoding='utf-8'):
        l=[x for x in re.split('[,.?;:!\'\"\t\n ]',line.lower()) if x != '']
        if word not in l:
            continue
        totalnum+=1         
#        #drop sentences too long/short            
        if len(l)<7 or len(l)>20:
            continue
        #compute the correlation of the  sentence       
        distance=0
        collocation=1
        length=1
        for w in l:     
            if w==word:
                continue    
            if w in model.vocab:
                collocation=1
                bonus=0
                for i in range(len(sortphrase)):
                    phra=sortphrase[i][0].split()
                    if w in phra and word in phra:
                        collocation=sortphrase[i][1]
                        bonus=1
                        #print("hit collocation:"+str(collocation))
                        break
                distance=distance+(model.similarity(word,w)+bonus)*collocation
                length+=collocation
        count_accept+=1        
        distance=distance/length
        vec[line]=distance
    #按照value降序排序
    sortvec=sorted(vec.items(), key=lambda x:x[1],reverse=True)
    
    with open('./data/sample/result3/'+word+'1.txt','a+',encoding='utf-8') as output:
        for i in range(len(sortvec)):
            output.write(sortvec[i][0])    
    
    
#    #输出结果
#    with open('./data/res3_418.txt','a+',encoding='utf-8') as output:
#        output.write("Keyword:"+word+"\n")
#        output.write("Total number:"+str(totalnum)+"\n")
#        output.write("Accepted number:"+str(count_accept)+"\n")
#        offset=int(count_accept/3)
#        rangenum=10
#        if offset<10:
#            rangenum=offset
#        output.write("*******Top "+str(rangenum)+" :*******"+"\n")
#        for i in range(rangenum):
#            output.write(sortvec[i][0])
#        output.write("*******Middle "+str(rangenum)+" :*******"+"\n")
#        for i in range(rangenum):
#            output.write(sortvec[i+offset][0])
#        output.write("*******Bottom "+str(rangenum)+" :*******"+"\n")
#        for i in range(rangenum):
#            output.write(sortvec[i+2*offset][0])
#        output.write("\n")

