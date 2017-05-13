# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 14:34:33 2017

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
model=gensim.models.Phrases(sentences,threshold=5)




wordlist=['sun','part','love','take','apple']
#with open('./data/words.txt',encoding='utf-8') as fpw:
#    wordlist=fpw.readlines()


phrasedict={}
for phrase, score in model.export_phrases(sentences):
    s=phrase.decode("utf-8")
    for word in wordlist:
        word=word.replace('\n','')
        if word in s.split():
            phrasedict[s]=score
        
sortphrase=sorted(phrasedict.items(), key=lambda x:x[1],reverse=True)
for i in range(len(sortphrase)):
    print(sortphrase[i])

for word in wordlist:
    #sentences containing keyword
    word=word.replace('\n','')
    l_of_word=[]
    res_of_word=[]
    totalnum=0
    
    for line in open('./data/sample/'+word+'.txt',encoding='utf-8'):
        l=[x for x in re.split('[,.?;:!\'\"\t\n ]',line.lower()) if x != '']
        if len(l)<7 or len(l)>20:
            continue
        
        if word in l:
            totalnum+=1
            for i in range(len(sortphrase)):
                pp=sortphrase[i][0].split()
                if word in pp:
                    if pp[0] in l and pp[1] in l:
                        res_of_word.append(line)
                        break
    
    with open('./data/sample/result2/'+word+'.txt','a+',encoding='utf-8') as output:
        for res in res_of_word:
            output.write(res)
                    
#    length=int(len(res_of_word)/3)
#    offset=10
#    if length<10:
#        offset=length
#    with open('./data/res2_313.txt','a+',encoding='utf-8') as output:
#        output.write("Keyword:"+word+"\n")
#        output.write("Total number:"+str(totalnum)+"\n")
#        output.write("Accepted number:"+str(len(res_of_word))+"\n")
#        output.write("*******Top "+str(offset)+" :*******"+"\n")
#        for i in range(offset):
#            output.write(res_of_word[i+length*0])
#        output.write("*******Middle "+str(offset)+" :*******"+"\n")
#        for i in range(offset):
#            output.write(res_of_word[i+length*1])
#        output.write("*******Bottom "+str(offset)+" :*******"+"\n")
#        for i in range(offset):
#            output.write(res_of_word[i+length*2])
#        output.write("\n")

        

            
    
    
        