#!/home/erlyn/anaconda3/bin/python

import sys
import json
import nltk

datasource = open("/home/erlyn/POSTagger/codes/Data/tagalog-unitags1.txt")
savefile = open("/home/erlyn/POSTagger/codes/Data/tagalog_nltk_tagged.txt","w")

tagged_sentences = []
countSentences =0
sentences=[]
PUNC=['.','?','!']
for entry in datasource.readlines():

    lines = entry.split('\t')
    if len(lines) > 0:
        
        if  lines[0].strip() in PUNC:
             print((lines[0].strip()+"/"+lines[0].strip()))
             savefile.write((lines[0].strip()+"/"+lines[0].strip())+"\n")
             countSentences+=1
             print()
             savefile.write('\'')
        elif lines[len(lines)-1] =="SYM":
             print((lines[0].strip()+"/"+lines[0].strip()))
             savefile.write((lines[0].strip()+"/"+lines[0].strip())+" ")
        
        elif lines[len(lines)-1]== 'X':
              print (lines[0].strip()+"/"+ "MARKER")
              savefile.write (lines[0].strip()+"/"+ "MARKER"+" ")

        elif len(lines[0].strip())==0:
              continue
        else:
              print (lines[0].strip()+"/"+lines[len(lines)-1].strip())
              savefile.write(lines[0].strip()+"/"+lines[len(lines)-1].strip()+" ")
       
     
savefile.close()
savefile=open("/home/erlyn/POSTagger/codes/Data/tagalog_nltk_tagged.txt")

sent=savefile.readlines()[0]
print(sent)
tagged_tagalog=[nltk.tag.str2tuple(t) for t in sent.split()]
print(tagged_tagalog)
savefile.close()
