
import nltk

from nltk.corpus import wordnet as wn

def converta(s):
    words = nltk.word_tokenize(s)
    tags = nltk.pos_tag(words)
    nouns = [t[0] for t in tags if (t[1]=="NNP" or t[1]=="NN")]
    synsets = [wn.synsets(n)[0] for n in nouns if len(wn.synsets(n))>0]
    hypernyms  = [s.hypernyms() for s in synsets if len(s.hypernyms())>0]
    #n_s = [(wn.synsets(n)[0]).hypernyms() for n in nouns if len((wn.synsets(n)[0]).hypernyms())>0]
    out = []
    for n in hypernyms:
        for x in n:
            out.append(str(x))
    print " ".join(out)

"""a = 'I am dog god cat girl'

converta(a)"""

import pandas as pd
df = pd.read_excel('D:\SRA\Data\TrainingData.xlsx')
#print df.columns
text = df[['Title']].apply(lambda x: '.'.join(x), axis=1).apply(lambda x: converta(x)).tolist()


