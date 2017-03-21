# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 11:42:55 2016

@author: therealwinster
"""
from nltk import pos_tag, word_tokenize,sent_tokenize
import language_check
from ginger import ginger_main,ColoredText
import argparse
parser = argparse.ArgumentParser()                                               
parser.add_argument("--file", "-f", type=str, required=True)
args = parser.parse_args()

def ginger_func(text):
    error_word_list,corrected_sentence,from_index,to_index = ginger_main(text)
#    print(error_word_list)    
    return from_index,to_index
def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))
'''UK spellings
'''

uk_spellings = open("UK spellings.txt","r")
uk_spellings = uk_spellings.read().split("\n")


file = open(args.file,'r')

text = file.read()
answers = sent_tokenize(text)
#answers = ["The detailed or researched knowledge of any stream of organisation where all the regardings are to be categorised in sense. By this we got a brief knowledge of any topic."]
#sent = "Knwledge of variious topics, passion for writing and innovative ideas to put my ideas in words."
#sent = "The opinion present in the Indian commerce and industry ministry is overarching goal is to support IP as a marketable monetary assed and economical bolster, and make a holistic system that gives an financial development while preventing the people interest. "
combined_error_list = {}
colored_dict = {}
coloredtext = []
ind = 0
#answers = answers[3] 
for sent in answers:
    
    pos_tags = pos_tag(word_tokenize(sent))
    
    pos_dict= {}
    for x,y in pos_tags:
        pos_dict[x] = y
        
    #[WORKING] GingerList without NNP 
       
    ginger_spelling_errors = []
    from_index, to_index = ginger_func(sent)
             
    #    print(str(matches))
    if len(from_index) != 0:
        for x,y in zip(from_index,to_index):
            if y != 0:    
                ginger_spelling_errors.append([sent[x:y+1],x,y])
    else:
        ginger_spelling_errors.append(["No error",0,0])                
    
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
        else:
            final_list.append([error_word,x,y])
    
    for x in final_list:
            temp_list2.append(x[0])
    #
#    print(final_list)
    #
    
    #LanguageTool list. 
    '''
    1. Using RegEx, obtain the indexes.
    2. Straight forward from then on.
    '''
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(sent)
    
    if matches:
        ltool_word = []
        lword = []
        
        color_gap, fixed_gap = 0, 0 
        fixed_text = sent 
        
        for m in matches:
            x,y = m.fromx,m.tox
            '''New changes
            '''
            if m.ruleId != "COMMA_PARENTHESIS_WHITESPACE":
                if m.ruleId != "SENTENCE_WHITESPACE":
                    ltool_word.append([sent[x:y],x,y])
                                                 
        for word,x,y in ltool_word:
            try:
                if pos_dict[word] != "NNP":                
                    if word not in uk_spellings:
                        lword.append([word,x,y])
            except KeyError:
                if word not in uk_spellings:
                    lword.append([word,x,y])
        #
#        print(lword)
        #
        temp_list1 = []
        for x in lword:
            temp_list1.append(x[0])
        
        combined_error_list[ind] = union(temp_list1,temp_list2)
        
        
        
                
        
    else:
        combined_error_list[ind] = temp_list2
        #GingerColor code here.
#        color_gap, fixed_gap = 0, 0 
#        fixed_text = sent
#        if final_list[0][0] != "No error":
#            for word_details in final_list:
#                x,y = word_details[1],word_details[2]
#                colorederror,gap = ColoredText.colorize(sent[int(x):int(y)],'blue')
#                
#                fixed_text = fixed_text[:x-fixed_gap] + colorederror + fixed_text[y-fixed_gap:]
#                color_gap += gap
#                fixed_gap += y-x-len(colorederror)
#            print(fixed_text)  
#        #GingerColor code ends.
    ind += 1
print("Output: \n")
print(combined_error_list)
def colorchange(word):
    CBLUE   = '\33[33m'
    word = CBLUE + word + CBLUE
    return word
    
file.close()
