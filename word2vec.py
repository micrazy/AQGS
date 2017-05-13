# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 12:38:16 2016

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
###training data
#省略频度<5的单词
model = gensim.models.Word2Vec(sentences, min_count=5,negative=5)

#model1=gensim.models.Phrases(sentences,threshold=20)
#for phrase, score in model1.export_phrases(sentences):
#    print(u'{0}   {1}'.format(phrase, score))

#save model
model.save_word2vec_format('./data/model_vec',binary=True)




#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#load model
model = gensim.models.Word2Vec.load_word2vec_format('./data/model_vec',binary=True) 
#examples
model['as']
model.most_similar('school')
model.similarity('bed','home')
#process sentences
#example word='computer'


wordlist=['sun','part','love','take','apple']
#with open('./data/words.txt',encoding='utf-8') as fpw:
#    wordlist=fpw.readlines()

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
        if len(l)<7 or len(l)>20:
            continue
        
        
    #print(l_of_word)    
        
        #compute the correlation of the  sentence       
        correlation=0
        
        length=1
        for w in l:     
            if w==word:
                continue    
            if w in model.vocab:
                correlation=correlation+model.similarity(word,w)
                length+=1
            else:
                print(w)
                
                
        #drop sentences too long/short    
#        if length<5 or length>15:
#            continue
        count_accept+=1        
        correlation=correlation/length
        


        
        p_of_l=correlation        
        
        vec[line]=p_of_l
    #按照value降序排序
    sortvec=sorted(vec.items(), key=lambda x:x[1],reverse=True)
    
    with open('./data/sample/result/'+word+'.txt','a+',encoding='utf-8') as output:
        for i in range(len(sortvec)):
            output.write(sortvec[i][0])
    
    
#    #输出结果
#    with open('./data/res_313.txt','a+',encoding='utf-8') as output:
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


    



        



