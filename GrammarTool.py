# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 13:10:22 2017

@author: therealwinster
"""

from nltk import pos_tag, word_tokenize,sent_tokenize
import language_check
from ginger import ginger_main,ColoredText
import re
import argparse
parser = argparse.ArgumentParser()                                               
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

def ginger_func(text):
    error_word_list,from_index,to_index = ginger_main(text)
#    print(error_word_list)    
    return error_word_list,from_index,to_index
  
     
def doit(text):      
  matches=re.findall(r"\'(.+?)\'",text)
  # matches is now ['String 1', 'String 2', 'String3']
  return ",".join(matches)

def colorise(listofwords,text):
    color_gap, fixed_gap = 0, 0 
    fixed_text = text
    for word_details in listofwords:
        x,y = word_details[1],word_details[2]
        colorederror,gap = ColoredText.colorize(sent[x:y],'red')
        fixed_text = fixed_text[:x-fixed_gap] + colorederror + fixed_text[y-fixed_gap:]
        color_gap += gap
        fixed_gap += y-x-len(colorederror)
    fixed_text += "\n"
    #            colorfile.write(fixed_text)
    print(fixed_text)
    fixed_text += "\n"
    colorfile.write(fixed_text)
    
#UK spellings

uk_spellings = open("UK spellings.txt","r")
uk_spellings = uk_spellings.read().split("\n")


file = open(args.file,'r')
temp = "Report - " + args.file
colorfile = open(temp,'a')
#Pre-processing.
text = file.read()
answers = sent_tokenize(text)
for i in range(len(answers)):
    temp = answers[i].split("\n")
    if len(temp) > 1:
        answers.remove(answers[i])
        for newsentences in temp:
            newsentences = re.sub(' +',' ',newsentences)            
            answers.append(newsentences)


ind = 0
#answers = [answers[12]]
combined_error_list = {}

for sent in answers:
    sent = re.sub('[‘’]',"'",sent)
    sent = re.sub("\'.*?\'","President",sent)
    sent = re.sub('\".*?\"',"President",sent)


    pos_tags = pos_tag(word_tokenize(sent))
    
    pos_dict= {}
    for x,y in pos_tags:
        pos_dict[x] = y
        
    #[WORKING] GingerList without NNP 
       
    ginger_spelling_errors = []
    gingererrors,from_index, to_index = ginger_func(sent)
             
    #    print(str(matches))
    if len(from_index) != 0:
        for x,y in zip(from_index,to_index):
            if y != 0:    
                ginger_spelling_errors.append([sent[x:y+1],x,y])
                
    
    #
#    print(ginger_spelling_errors)
    #    
    
    final_list,temp_list2 = [],[]
    for error_word,x,y in ginger_spelling_errors:
        if error_word != "No error":
            try:
                if pos_dict[error_word] != "NNP":
                    if error_word not in uk_spellings:
                        final_list.append([error_word,x,y])
            except:
                if error_word not in uk_spellings:
                    final_list.append([error_word,x,y])
 
    #LanguageTool list. 
   
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(sent)
    
    if matches:
        ltool_word,lword,error_list,errors = [],[],[],[]
        
        for m in matches:
            x,y = m.fromx,m.tox
            if m.ruleId != "COMMA_PARENTHESIS_WHITESPACE":
                if m.ruleId != "SENTENCE_WHITESPACE":
                    ltool_word.append([sent[x:y],x,y-1])                                                
        for word,x,y in ltool_word:
            try:
                if pos_dict[word] != "NNP":                
                    if word not in uk_spellings:
                        lword.append([word,x,y])
            except KeyError:
                if word not in uk_spellings:
                    lword.append([word,x,y])
                    
        if lword:
            u_set = set(map(tuple, final_list)).union(map(tuple, lword))
            error_list = list(map(list,u_set))
            
        #Coloring
        combined_error_list[ind] = error_list    
        if error_list:
            for i in error_list:
                errors.append(i[0])
            towrite = "Errors: "+str(errors)+"\n"
            colorfile.write(towrite)
            print("Errors: ",errors)            
            colorise(error_list,sent)
    
    else:
        combined_error_list[ind] = final_list
        #GingerColor code here.
        if final_list:
            towrite = "Errors: "+str(gingererrors)+"\n"
            colorfile.write(towrite)
            print("Errors: ",gingererrors)
            colorise(final_list,sent)
#        #GingerColor code ends.
    ind += 1
    
numberoferrors = 0    
for i in combined_error_list:
    numberoferrors += len(combined_error_list[i])
towrite = "Total errors: "+str(numberoferrors)
print(towrite)
colorfile.write(towrite)

    
file.close()
colorfile.close()
