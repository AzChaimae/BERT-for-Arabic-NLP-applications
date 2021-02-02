#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 10:40:33 2019

@author: AZROUMAHLI Chaimae
"""

"""create training developpe,et, testing data from the 28 annotated NER corpus""" 

# =============================================================================
# Libraries 
# =============================================================================
import regex 
import re
import os 
import csv 
from os import listdir
from os.path import isfile, join
import random

# =============================================================================
# Reading, preprocessing & Layering the labeled Data
# =============================================================================
#AQMAR NER tag needs to be cleaned as well there is a lot of emty and non arabic entries
def remove_diacritics(text):
    arabic_diacritics = re.compile(" ّ | َ | ً | ُ | ٌ | ِ | ٍ | ْ | ـ", re.VERBOSE)
    text = re.sub(arabic_diacritics,'',(regex.sub('[^\p{Arabic}]','',text)))
    return text 

def normalizing(text):
    a='ا'
    b='ء'
    c='ه'
    d='ي'
    text=regex.sub('[آ]|[أ]|[إ]',a,text)
    text=regex.sub('[ؤ]|[ئ]',b,text)
    text=regex.sub('[ة]',c,text)
    text=regex.sub('[ي]|[ى]',d,text)
    return remove_diacritics(text)

def remove_empty_lines(filename):
    #Overwrite the file, removing empty lines and lines that contain only whitespace.
    with open(filename,encoding='utf-8-sig') as in_file, open(filename,'r+',encoding='utf-8-sig') as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()

def normalizing_labels(text):
    text=regex.sub('--ORG','-ORG',text)
    text=regex.sub('MIS2','MIS',text)
    text=regex.sub('MIS0','MIS',text)
    text=regex.sub('MIS1','MIS',text)
    text=regex.sub('MIS-1','MIS',text)
    text=regex.sub('MIS3','MIS',text)
    text=regex.sub('MISS1','MIS',text)
    text=regex.sub('MIS`','MIS',text)
    text=regex.sub('IO','O',text)
    return text

#get the NER annotated data 
def get_data(files_directory):
    NER_test=[]
    NER_files=[f for f in listdir(files_directory) if isfile(join(files_directory,f))]
    random.shuffle(NER_files)
    os.chdir(files_directory)
    for file in NER_files:
        remove_empty_lines(file)
        f=open(file,'r',encoding='utf-8-sig')
        reader=csv.reader(f)
        rows=list(reader)
        for row in rows:
            try:
                NER_test.append([normalizing(row[0].split(' ')[0]),normalizing_labels(row[0].split(' ')[1])])
            except:
                pass
        f.close()
    NER_test_annotations=[row for row in NER_test if row[0]!='']
    return NER_test_annotations


def get_data_labels(labeled_data):
    labels=[row[1] for row in labeled_data]
    return list(set(labels))

def get_data_words(labeled_data):
    words=[row[0] for row in labeled_data]
    return words

def list_to_file(list_name,file_name):
    with open(file_name, 'w', encoding='utf-8-sig') as file:
        writer=csv.writer(file)
        for line in list_name:
            writer.writerow(line)
    return

def devide_data(labeled_data):
    N=len(labeled_data)
    test_size=int(N*0.15)+1
    test=labeled_data[:test_size]
    dev=labeled_data[test_size+1:test_size*2]
    train=labeled_data[(test_size*2)+1:]
    return train,test,dev

labeled_data=get_data("/home/khaosdev-6/AZROUMAHLI Chaimae/Embeddings analysis/Accuracy/My Arabic word-embeddings benchmarks/NER tags")
labels=get_data_labels(labeled_data)

#creaing the files in the server
labeled_data=get_data("/home/ubuntu/embeddings_analysis/Accuracy/benchmarks/txt_NER tags")

train,test,dev=devide_data(labeled_data)
os.chdir("/home/ubuntu/embeddings_analysis/Bert/Pre & Training data/NER training data")
list_to_file(train,"train.txt")
list_to_file(dev,"dev.txt")
list_to_file(test,"test.txt")