# Tagalog_POSTagger

   The original work made use of (32) fine-grained tags to capture semantic information of verbs.
  ```
   Factors Affecting Part-of-Speech Tagging for Tagalog (2009)
   E. Manguilimotan and Y. Matsumoto
   Proceedings of the 23rd Pacific Asia Conference on Language, Information and Computation, Hong Kong 
  ```
  http://aclweb.org/anthology/Y09-2039
 
  However, this Tagalog POS tagger makes use of the universal tagset. (https://universaldependencies.org/u/pos/)

## Python Packages required

  (nltk) (https://www.nltk.org/install.html)

  (sklearn-crfsuite) (https://pypi.org/project/sklearn-crfsuite/)

## Tagalog.py 
     ** tagalogdata() class ** to load data for training
     ** tagalog_stemmer() class ** to stem affixes and root

## Tagalog data
    The tagged data are tokenized word/token pair. (Data/tagalog_nltk_tagged.txt)
    The data is then converted into nltk tagged data convention: (token,tag) tuple, using the tagalogdata() class
    
## Features
   The features are described in the features method in tagalog_tagger.py
   **root, prefix, infix, suffix, reduplication** are important in identifying the POS tag of a tagalog word.

## Train a New Model
  
   $ python tagalog_tagger.py --mode "train" --model <modelname> --tagalogdata <trainingdata>
  
   Example:
  
   $ python tagalog_tagger.py --mode "train" --model Model/tagalog_pos_tagger.model --tagalogdata Data/tagalog_nltk_tagged.txt

   
## Tag sentence
  
   $ python tagalog_tagger.py --mode "tag" --sent "Ang bata ay naglalaro sa daan."
   [('Ang', 'DET'), ('bata', 'NOUN'), ('ay', 'X'), ('naglalaro', 'VERB'), ('sa', 'ADP'), ('daan', 'NOUN'), ('.', '.')]
 

## Other Works
   ```
   Dependency-based Analysis for Tagalog Sentences (2011)
   E. Manguilimotan and Y. Matsumoto 
   Proceedings of the 25th Pacific Asia Conference on Language, Information and Computation, Singapore 
   ```
   [ http://aclweb.org/anthology/Y11-1036 ]
