from Rss_crawler import Crawler
import header
import ConfigParser
import os.path
import logging 
import sys
from AnalysisEngine import AnalysisEngine
import time

#
home = "D://SRA//Data//"
settings = ConfigParser.ConfigParser()
    
#settings._interpolation = ConfigParser.ExtendedInterpolation()
settings.read('Settings.config')
settings

def controller():
    LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}
    
    def setLoggingLevel():
        try:
            
            level = LEVELS.get(header.levelName , logging.NOTSET)
            
            logging.basicConfig(filename=header.logFileName , level=level)
        
            if level == logging.NOTSET:
                logging.warning("Logging level not set properly. Allowed levels are : critical , error , warning , info , debug ")
            
            
             
        except Exception as e:
            print e.message
            return     
    
    
    #home dir, default directory
    home = "D://SRA//Data//"
    settings = ConfigParser.ConfigParser()
    
    #settings._interpolation = ConfigParser.ExtendedInterpolation()
    settings.read('D://SRA//Data//Settings.config')
    
    
    
    # Initialize level of logging.
    header.levelName = settings.get('LOGGING_INPUTS', 'LEVEL_NAME')
    
    
    
    
    # Initialize file name to which logging will be dumped.
    log_dir_path = settings.get('LOGGING_INPUTS', 'LOG_DIR_PATH')
    
    if not os.path.isdir(log_dir_path):
        logging.warning("LOG_DIR_PATH not set properly. logs are redirected to log.txt placed at:" + home)
        log_dir_path = home
    
    header.logFileName = os.path.join(log_dir_path , "log.txt")
    
    
    setLoggingLevel()
    
    
    
    
    # File containing site information.
    header.siteInfoFilePath = settings.get('CRAWLER_INPUTS', 'SITE_INFO_FILE_PATH')
    if not os.path.isfile(header.siteInfoFilePath):
        logging.warning("SITE_INFO_FILE_PATH not set properly")
        header.siteInfoFilePath = os.path.join(home , "SiteTimestampInfo.p")
        #sys.exit  
        
    
    
    
    # File storing list of important keywords.
    header.keywordFilePath = settings.get('CRAWLER_INPUTS', 'KEYWORD_FILE_PATH')
    if not os.path.isfile(header.keywordFilePath):
        logging.critical("KEYWORD_FILE_PATH not set properly")
        sys.exit  
        
        
    # File which will store crawled data.
    out_dir_path = settings.get('CRAWLER_INPUTS', 'OUTPUT_DIR_PATH')
    if not os.path.isdir(out_dir_path):
        logging.warning("OUTPUT_DIR_PATH not set properly. Output.csv will be stored in " + home)
        out_dir_path = home
    
    header.outputFilePath = os.path.join(out_dir_path , "Output.csv")
    
        
    #TODO it shud be dir rather than file
    header.siteTimestampPickleFile = settings.get('CRAWLER_INPUTS' , 'SITE_PICKLE_DUMP_FILE')
    # if not os.path.isfile(header.siteTimestampPickleFile):
    #     logging.critical("SITE_PICKLE_DUMP_FILE not set properly. Make sure path is correct")
    #     sys.exit
    header.nounfilter = settings.get('ANALYSIS_ENGINE_INPUTS','NOUNFILTER')
    header.trainingFilePath = settings.get('ANALYSIS_ENGINE_INPUTS' , 'TRAINING_FILE_PATH')
    header.labelColNameRiskClassifier = settings.get('ANALYSIS_ENGINE_INPUTS' , 'LABEL_COL_NAME_RISK_CLASSIFIER')
    header.textFieldRiskClassifier = (settings.get('ANALYSIS_ENGINE_INPUTS' , 'TEXT_FIELDS_RISK_CLASSIFIER')).split(',')
    
    
    header.riskClassifierModelFilePath = settings.get('ANALYSIS_ENGINE_INPUTS' , 'RISK_CLASSIFIER_MODEL_FILE_PATH')
    header.textFieldTopicClassifier = (settings.get('ANALYSIS_ENGINE_INPUTS' , 'TEXT_FIELDS_TOPIC_CLASSIFIER')).split(',')
    header.labelColNameTopicClassifier = settings.get('ANALYSIS_ENGINE_INPUTS' , 'LABEL_COL_NAME_TOPIC_CLASSIFIER')
    header.topicClassifierModelFilePath = settings.get('ANALYSIS_ENGINE_INPUTS' , 'TOPIC_CLASSIFIER_MODEL_FILE_PATH')
    header.labelColNameSubTopicClassifier = settings.get('ANALYSIS_ENGINE_INPUTS'  , 'LABEL_COL_NAME_SUB_TOPIC_CLASSIFIER' )
    header.subTopicOneClassifierModelFilePath = settings.get('ANALYSIS_ENGINE_INPUTS' , 'SUB_TOPIC_ONE_CLASSIFIER_MODEL_FILE_PATH' )
    header.subTopicTwoClassifierModelFilePath = settings.get('ANALYSIS_ENGINE_INPUTS' , 'SUB_TOPIC_TWO_CLASSIFIER_MODEL_FILE_PATH' )
    header.subTopicThreeClassifierModelFilePath = settings.get('ANALYSIS_ENGINE_INPUTS' , 'SUB_TOPIC_THREE_CLASSIFIER_MODEL_FILE_PATH' )
    header.subTopicFourClassifierModelFilePath = settings.get('ANALYSIS_ENGINE_INPUTS' , 'SUB_TOPIC_FOUR_CLASSIFIER_MODEL_FILE_PATH' )
    if "true" in (settings.get('ANALYSIS_ENGINE_INPUTS' , 'IS_PARAM_TUNE')).lower():
        header.isParamTune = True
    
    
    
    header.riskClassifierRatioRemoveSkewness = float(settings.get('ANALYSIS_ENGINE_INPUTS' , 'RISK_CLASSIFIER_RATIO_REMOVE_SKEWNESS' ))
    if "true" in (settings.get('ANALYSIS_ENGINE_INPUTS' , 'IS_REMOVE_SKEWNESS')).lower():
        header.isRemoveSkewness = True
        
    # Invoke Crawler to crawl data from  sites
    
    #while(True):
       
        #crawler = Crawler()

         
        #del crawler
        # Run every 6hours
        #time.sleep(21600)
      
      
     


#      Commented to execute only analysis engine
#     crawler = Crawler()
#     del crawler
    
    analyzer = AnalysisEngine()
##    # 
    analyzer.performTrainingForAllTasks()
##    
    analyzer.analyze()
    
    sys.exit
    # Invoke Analysis Engine to process content of outputFilePath
    #########################################################################
    
    

if __name__ == '__main__':
    controller()
