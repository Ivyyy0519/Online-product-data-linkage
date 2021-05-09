# Put task1a.py code here
import pandas as pd
import nltk
import re
from string import punctuation
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#pre-processing for punctuation
dicts={i:'' for i in punctuation}
punc_table=str.maketrans(dicts)

task1a = pd.DataFrame(columns=('idAbt', 'idBuy'))
abt = pd.read_csv('abt_small.csv', encoding='ISO-8859-1')
abt = abt.where(abt.notnull(), None)
buy = pd.read_csv('buy_small.csv', encoding='ISO-8859-1')
buy = buy.where(buy.notnull(), None)
truth = pd.read_csv('abt_buy_truth_small.csv', encoding='ISO-8859-1')

#pre-processing for punctuation
dicts={i:'' for i in punctuation}
punc_table=str.maketrans(dicts)

task1a = pd.DataFrame(columns=('idAbt', 'idBuy'))

matchscore = 80
matchscore_code = 92

#extract product code for abt
for i in range(len(abt)):
    code = abt.iloc[i,:]['name'].split()[-1]   #for exact match
    abt_info = abt.iloc[i,:]['name'].translate(punc_table)  #for fuzzy match in case no exact match
    found = 0   #found exact match
    score = {}   #establish a dict to store fuzzy matching score
    code_dict = {}  #establish an array to store potential code
    
    for j in range(len(buy)):
        buy_info = buy.iloc[j,:]['name'].translate(punc_table)
        if (buy.iloc[j,:]['description']is not None):
            buy_info = buy_info + ' '+ buy.iloc[j,:]['description'].translate(punc_table)
        
        #get the fuzzy matching score
        if (fuzz.token_set_ratio(abt_info, buy_info) >= matchscore):
            score[buy.iloc[j,:]['idBuy']] = fuzz.token_set_ratio(abt_info, buy_info)
        
        #get the potential code
        for word in buy_info.split():
            score_code = fuzz.token_set_ratio(code, word)
            if score_code >= matchscore_code:
                code_dict[buy.iloc[j,:]['idBuy']] = score_code
            
        #match the abt product code with buy product information(try to find the code)
        if re.search(code, buy_info):
            task1a = task1a.append([{'idAbt':abt.iloc[i,:]['idABT'],'idBuy':buy.iloc[j,:]['idBuy']}], ignore_index=True)
            found = 1
            break
            
    #using the fuzzy matching
    if (not found):
        #match the code first
        if code_dict != {}:
            matched_buyID = sorted(code_dict.items(), key=lambda d:d[1], reverse = True)[0][0]
            task1a = task1a.append([{'idAbt':abt.iloc[i,:]['idABT'],'idBuy':matched_buyID}], ignore_index=True)
        elif score != {}:  
            matched_buyID = sorted(score.items(), key=lambda d:d[1], reverse = True)[0][0]
            task1a = task1a.append([{'idAbt':abt.iloc[i,:]['idABT'],'idBuy':matched_buyID}], ignore_index=True)

task1a.to_csv("task1a.csv",index=False,sep=',') 