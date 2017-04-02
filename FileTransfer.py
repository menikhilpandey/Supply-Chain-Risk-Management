# import socket
# 
# file = open("C:\Users\Jyoti.Gupta\Desktop\Rss_crawler\src\Settings.config", "rb")
# sock = socket.socket()
# sock.connect(("192.168.1.73", 8021))
# 
# while True:
#     chunk = file.read(65536)
#     if not chunk:
#         break  # EOF
#     sock.sendall(chunk)

import sklearn
import pandas as pd
from sklearn.metrics import f1_score


resultFile = "C:\\Users\\Jyoti.Gupta\\Documents\\crawler\\temprisktype_50.csv"

df = pd.read_csv(resultFile )

actual = df['actual']

column="class_weighttoauto"
f_score = f1_score(actual , df[column])
print column + " :: " + str(f_score)


# for column in df:
#     if column == "actual":
#         continue
#  
#    
#     f_score = f1_score(actual , df[column])
#     print column + " :: " + str(f_score)



