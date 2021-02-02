#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:46:04 2019

@author: AZROUMAHLI Chaimae
"""
import csv
import collections
import os
from os import listdir
from os.path import isfile, join

def extract_vocab(input_file):
    sentences=[]
    with open(input_file,'r',encoding='utf-8-sig', errors='ignore') as f:
        reader=csv.reader(f)
        sentences.extend(list(reader))
    text=' '.join(' '.join(row) for row in sentences)
    print('the sentences appended and the text is created')
    print("1")
    tokens=text.split(' ')
    vocab_count=collections.Counter(tokens)
    print('the vocabulary occurence is counted')
    vocab=sorted(set(tokens))
    print("the vocab is extraxted")
    vocab=[v for v in vocab if vocab_count[v]>10]
    print('the new vocab is counted for')
    return vocab

def vocab_in_file(input_file,vocab_file):
    vocab=extract_vocab(input_file)
    with open(vocab_file,'a',encoding='utf-8-sig') as f:
        writer=csv.writer(f,delimiter='\n')
        writer.writerow([v for v in vocab])
    return

def list_in_file(list_name,file_name):
    with open(file_name,'a',encoding='utf-8-sig') as f:
        writer=csv.writer(f,delimiter='\n')
        writer.writerow([l for l in list_name])
    return

def return_num_vocab(list_of_input_files):
    return len(extract_vocab(list_of_input_files))

def two_in_one(list_of_input_files,outputfile):
    sentences=[]
    for input_file in list_of_input_files:
        with open(input_file,'r',encoding='utf-8-sig') as f:
            reader=csv.reader(f)
            sentences.extend(list(reader))
    with open(outputfile,'w',encoding='utf-8-sig') as out:
        Writer=csv.writer(out)
        Writer.writerows(sentences)
    return

files_directorty="/home/ubuntu/embeddings_analysis/Bert/Pre_Training_data/Wikipedia/splited_files"
Wiki_files=[f for f in listdir(files_directorty) if isfile(join(files_directorty,f))]
os.chdir(files_directorty)
print("Directory opend && files read")
Vocab=[]
for file in Wiki_files:
    Vocab.extend(extract_vocab(file))
    Vocab=sorted(set(Vocab))
    print('%s is open, and appended to the list'%(file))

print("All the lists are read and appended and cleaned")
os.chdir("/home/ubuntu/embeddings_analysis/Bert/Pre_Training_data/Wikipedia/splited_files")
list_in_file(Vocab,"wiki_vocab")
