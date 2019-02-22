import nltk
from nltk.tag.util import untag
from Tagalog import tagalogdata 
from Tagalog import tagalog_stemmer
from sklearn_crfsuite import metrics
from sklearn_crfsuite import CRF
import sklearn
import pickle
import os
import argparse


def features(sentence, index):
##modified from https://nlpforhackers.io/crf-pos-tagger/

    """ sentence: [w1, w2, ...], index: the index of the word """
    #get affixes of tagalog word
    
    root,prefix,infix,suffix,redup=stemmer.get_affixes(sentence[index])
    
    return {
        'word': sentence[index],
        'root':root,
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix': prefix,
        'suffix': suffix,
        'infix':infix,
        'redup':redup,
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'is_numeric': sentence[index].isdigit(),
        'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }

def pos_tag(sentence,model):
##source  https://nlpforhackers.io/crf-pos-tagger/
    sentence_features = [features(sentence, index) for index in range(len(sentence))]
    return list(zip(sentence, model.predict([sentence_features])[0]))

def transform_to_dataset(tagged_sentences):
##source  https://nlpforhackers.io/crf-pos-tagger/
    X, y = [], []
    for tagged in tagged_sentences:
         
        X.append([features(untag(tagged), index) for index in range(len(tagged))])
        y.append([tag for _, tag in tagged])
 
    return X, y

def token_accuracy(y_test,y_predict):
    correct=0
    total_tokens=0
    for test,pred in zip(y_test,y_predict):
        for t, p in zip(test,pred):
            if t==p:   
               correct+=1
            total_tokens+=1
    acc= (correct/total_tokens)
    return acc  
   
def train_model(tagged_sentences):
     model_filename='Model/tagalog_pos_tagger.model'
     model=CRF()
     cutoff = int(.75 * len(tagged_sentences))
     print('extracting data ...')
     training_sentences = tagged_sentences[:cutoff]
     test_sentences = tagged_sentences[cutoff:]
     X_train, y_train = transform_to_dataset(training_sentences)
     X_test, y_test = transform_to_dataset(test_sentences)  
     print('training model ...')
     model.fit(X_train,y_train)
     print('saving pos tagger ...')
     pickle.dump(model,open(model_filename,"wb"))
     y_predict = model.predict(X_test)
     print(y_predict[0])
     print(y_test[0])
     acc = token_accuracy(y_test,y_predict)
     print("Accuracy: ", acc)
     return model

def argument():


    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--mode', type=str)
    arg_parser.add_argument('--sent', default='')
    arg_parser.add_argument('--model', default='Model/tagalog_pos_tagger.model')
    arg_parser.add_argument('--tagalogdata', default='Data/tagalog_nltk_tagged.txt')
    args = arg_parser.parse_args()

    return args


if __name__=='__main__':
    args = argument()
    stemmer=tagalog_stemmer()
    if args.mode == 'train':
       tagalog=tagalogdata(args.tagalogdata)
       tagged_sentences=tagalog.tagged_sentences()
       train_model(tagged_sentences)
    elif args.mode == 'tag':
         model_name=args.model
         if os.path.exists(model_name):
            model=pickle.load(open(model_name,"rb"))

            sentence = nltk.word_tokenize(args.sent)
            print(pos_tag(sentence,model))

         else:
            print('Model', model_name,'does not exist')


