import pandas as pd
from pandas import read_excel
from pandas.io.excel import read_excel
import sklearn
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfTransformer
#from numpy import *
from numpy.core.multiarray import arange
from numpy.random import randn 
from numpy.core.numeric import nditer
import pickle
from __builtin__ import str
from _ast import Str
from sklearn.feature_selection import SelectPercentile
from sklearn.preprocessing import Imputer
import nltk 
from nltk.corpus import wordnet as wn

#Automatic parameter tuning
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
import  header
from postagger import noun_extractor
from sklearn.feature_selection.univariate_selection import f_classif
import logging

class Text_Classsifier:
       
    
    def __init__(self):
        self.label=[]
        self.text=[]
        #TODO parameters values should be  populated from configuration file.
        # Try with clf__loss also, 'log' switches to logistic regression
        # Add options for select, for feature selection.
        self.parameters = {'vect__max_df': (0.5, 0.75, 1.0),
                           'vect__max_features': (None, 5000, 10000, 50000),
                           'vect__ngram_range': [(1, 1), (1, 2)],
                           'vect__lowercase' : (True, False),
                           'vect__use_idf' : (True, False),
                           'vect__sublinear_tf' : (True, False), 
                           
                           'tfidf__use_idf': (True, False),
                           'clf__alpha': (1e-2, 1e-3),
                           'clf__penalty': ('l2', 'elasticnet'),
                           'clf__n_iter': (10, 50, 80,100,300),
                           'select__percentile' : (6,7,8,10,11,12,13,14),}
    
    def performMasking(self, df , mask):
        if mask:
            colName = mask[0]
            colVal = mask[1]
            df = df[df[colName] == colVal]
        return df
        
    def converta(self,s):
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
        return " ".join(out)

    def loadTextFields(self , df , text_fields='Title',nounfilter = 1):
        
        
        if nounfilter==1:
            print 'it is a yes'
            text = df[text_fields].apply(lambda x: '.'.join(x), axis=1).apply(lambda x: converta(x)).tolist()
            print len(text)
            return text
        else:
            print 'not just nouns'
            text = df[text_fields].apply(lambda x: '.'.join(x), axis=1).tolist()
            print len(text)
            return text
            
        
        
        # Added code for noun extractor strategy
        #text = [noun_extractor(item) for item in text]
        
        #return text
    
    def loadTrainingData(self, trainingFilePath , text_fields , labelCol,nounfilter, mask =[]):
        df = read_excel(trainingFilePath )
        
        df = self.performMasking(df, mask)
        
        df['Title'] = df.Title.str.replace('[^\x00-\x7F]','')
         
        df['Content'] = df.Content.str.replace('[^\x00-\x7F]','')
        df[['Title' , 'Content' ]] = df[['Title' , 'Content' ]].astype(str)
        
        self.text = self.loadTextFields(df, text_fields,nounfilter)
        self.label = df[labelCol].tolist()
        
    def train(self):
        
      
        
        
        # Algo 1 orig
        
        #Feature selection
        
        #         self.textClf = Pipeline([('vect', TfidfVectorizer( analyzer="word" , sublinear_tf=True, max_df=0.5,
#                                  stop_words='english')),
#                                  ('select' , select),
#                   ('tfidf', TfidfTransformer()),
#                       ('clf', SGDClassifier( penalty='l2',
#                                             alpha=1e-3, n_iter=50,shuffle=True, random_state=42, class_weight='auto')),
#          ])
        
        #Risk Classifier
#         select = SelectPercentile(score_func=chi2, percentile=10)
#         
#         
# 
#         
#         self.textClf = Pipeline([('vect', TfidfVectorizer( analyzer="word" , sublinear_tf=True, max_df=0.5,
#                                  stop_words='english')),
#                                  ('select' , select),
#                   ('tfidf', TfidfTransformer()),
#                       ('clf', SGDClassifier( penalty='l2',
#                                             alpha=1e-4, n_iter=200,shuffle=True, random_state=42, class_weight='auto')),
#          ])
        
        #sorting features and selecting 
        select = SelectPercentile(score_func=chi2, percentile=100)
        
        

        
        self.textClf = Pipeline([('vect', TfidfVectorizer( analyzer="word" , sublinear_tf=True, max_df=0.5,
                                 stop_words='english')),
                                 ('select' , select),
                  ('tfidf', TfidfTransformer()),
                      ('clf', SGDClassifier( penalty='l2',
                                            alpha=1e-4, n_iter=5,shuffle=True, random_state=42)),
         ])
        
        
        # try for select percentile :: select = SelectPercentile(score_func=chi2, percentile=18)
        # Try for feature stacker :: ft = FeatureStacker([("badwords", badwords), ("chars", countvect_char), ])
        
        
        if header.isParamTune == True:
            logging.info("###Parameter tuning###")
            self.textClf = GridSearchCV(self.textClf, self.parameters, n_jobs=-1)
        
        
        logging.info("### parameters tuned,trying to fit data to model ###")
        self.textClf.fit(self.text , self.label)
        logging.info("### model is now trained ###")
        # Functionality to dump final value of parameters chosen by the grid search
        if header.isParamTune == True:
            best_parameters = self.textClf.best_estimator_.get_params()
            for param_name in sorted(self.parameters.keys()):
                print("\t%s: %r" % (param_name, best_parameters[param_name]))
                
    
    
    def loadTestDataFromFile(self , testDataFilePath , text_fields ,nounfilter ,mask=[]):
        df = pd.DataFrame.from_csv(testDataFilePath , index_col=False, encoding='latin-1') 
        
        
        # Remove non ascii characters before converting the type to str
        # TODO : Do it generically by using text_fields
        df['ArticleTitle'] = df.ArticleTitle.str.replace('[^\x00-\x7F]','')
        df['Summary'] = df.Summary.str.replace('[^\x00-\x7F]','')
        df['ArticleStory'] = df.ArticleStory.str.replace('[^\x00-\x7F]','')
#
        # To prevent feeds where article story starts with a full stop and make the data type as float for further processing of the data frame.
        df[['ArticleTitle' , 'Summary' , 'ArticleStory']] = df[['ArticleTitle' , 'Summary' , 'ArticleStory']].astype(str)
        
        
        df_sub = self.performMasking(df, mask)
       
        
        return  self.loadTextFields(df_sub, text_fields,nounfilter) , df
    
    def loadTestDataFromDataFrame(self , dataFrame , text_fields ,nounfilter, mask=[]):
        
        dataFrame_sub = self.performMasking(dataFrame, mask)
            
        return  self.loadTextFields(dataFrame_sub, text_fields,nounfilter) 
    
    def dumpModelFile(self , modelFilePath):
        with open(modelFilePath, "wb") as fp:
            pickle.dump(self.textClf, fp)
              
              
       
        
        
    def loadModel(self , modelFilePath):
        
        with open(modelFilePath) as fp:
            self.textClf = pickle.load(fp)
            
           

        
    def classify(self , text):
        
        return self.textClf.predict(text)
        



# trainingFilePath = "C:\Users\Jyoti.Gupta\Documents\crawler\DT_input.xlsx"
# testDataFilePath = "C:\Users\Jyoti.Gupta\Documents\crawler\DT_input.xlsx"
# clf = Text_Classsifier()
# clf.loadTrainingData(trainingFilePath, ['Title'] , "Risky")
# clf.train()
# clf.dumpModelFile("C:\Users\Jyoti.Gupta\Documents\crawler\Model.p")
# 
# predict_clf = Text_Classsifier()
# predict_clf.loadModel("C:\Users\Jyoti.Gupta\Documents\crawler\Model.p")
# test_data = predict_clf.loadTestData(testDataFilePath, ['Title'])
# print predict_clf.classify(test_data)



    
        