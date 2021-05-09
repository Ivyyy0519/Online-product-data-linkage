# Put task1b.py code here
import pandas as pd
import nltk
import re
from string import punctuation
from fuzzywuzzy import process

#pre-processing for punctuation
dicts={i:'' for i in punctuation}
punc_table=str.maketrans(dicts)

abt = pd.read_csv('abt.csv', encoding='ISO-8859-1')
abt = abt.where(abt.notnull(), None)
buy = pd.read_csv('buy.csv', encoding='ISO-8859-1')
buy = buy.where(buy.notnull(), None)
truth = pd.read_csv('abt_buy_truth.csv', encoding='ISO-8859-1')

#extract unique brand names
brand = set()

for name in abt['name'].tolist():
    if name is not None:
        brand.add((name.split()[0]).lower())
        
#allocate abt products to blocks by brand names
abt_blocks = pd.DataFrame(columns=('block_key', 'product_id'))
for i in range(len(abt)):
    name = abt.iloc[i,1].split()[0].lower()  #match the brand set with first word of name
    abt_blocks = abt_blocks.append([{'block_key': name,'product_id':abt.iloc[i,0]}], ignore_index=True)

#allocate buy products to blocks by product information
buy_blocks = pd.DataFrame(columns=('block_key', 'product_id'))

for j in range(len(buy)):
    if buy.iloc[j,3] is not None:
        name = buy.iloc[j,3].split()[0].lower()
        key = process.extractOne(name, brand)[0]
        buy_blocks = buy_blocks.append([{'block_key': key,'product_id':buy.iloc[j,0]}], ignore_index=True)
    else:
        for word in buy.iloc[j,1].split():
            if word.lower() in brand:
                key = word.lower()
                buy_blocks = buy_blocks.append([{'block_key': key,'product_id':buy.iloc[j,0]}], ignore_index=True)

buy_blocks.to_csv("buy_blocks.csv",index=False,sep=',')
abt_blocks.to_csv("abt_blocks.csv",index=False,sep=',')