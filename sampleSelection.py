# -*- coding: utf-8 -*-
"""
Created on Mon May  1 13:54:49 2017

@author: user
"""
import re,random
words=['apple','take']

for word in words:
    totalnum=0
    for line in open('./data/tatoeba/tatoeba-english.txt',encoding='utf-8'):
        l=[x for x in re.split('[,.?;:!\t\n ]',line.lower()) if x != '']
        if word not in l:
            continue
        if len(l)<7 or len(l)>20:
            continue
        if random.randint(0,100)>50:
            continue
        if totalnum>=30:
            break
        else:
            totalnum+=1
        with open('./data/sample/'+word+'.txt','a+',encoding='utf-8') as fp:
            fp.write(line)

