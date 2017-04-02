import logging 
import logging.handlers
from fileinput import filename


# Initialize level of logging.
levelName = ""

# Initialize file name to which logging will be dumped.
logFileName = ""

# File containing site information.
siteInfoFilePath = ""

# File storing list of important keywords.
keywordFilePath = ""

# File which will store crawled data.
outputFilePath = ""

siteTimestampPickleFile = ""
nounfilter = 0

trainingFilePath = ""

labelColNameRiskClassifier = ""

textFieldRiskClassifier = ""

riskClassifierModelFilePath=""


textFieldTopicClassifier=""

labelColNameTopicClassifier=""

topicClassifierModelFilePath=""

labelColNameSubTopicClassifier=""

subTopicOneClassifierModelFilePath=""

subTopicTwoClassifierModelFilePath=""

subTopicThreeClassifierModelFilePath=""

subTopicFourClassifierModelFilePath=""

isParamTune=False

isRemoveSkewness=False

riskClassifierRatioRemoveSkewness=1

