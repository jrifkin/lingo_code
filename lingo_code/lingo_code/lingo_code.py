#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import lingo_support as ls

"""goal is to create binary variables with which we can run correlation analysis on"""

def liwc_analysis(txt_file,liwc_dict):

    liwc_counter = {k:0 for k in liwc_dict.keys()}
    data = ls.split_response(txt_file)

    #make list of liwc_words and sort alphabetically
    liwc_words = liwc_dict.keys()
    liwc_words.sort(key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())

    """binary search still does not work, implemented andy's method of sorting both search and lookup lists and caching where it left off"""
    counts,base,word_count,num_responses = ls.count_matches(data,liwc_words,liwc_counter)    
    
    overall_cats = ls.category_counts(liwc_dict,counts)
    
    ls.print_liwc_results(txt_file,base,word_count,num_responses)


def sentiment_score(data,sent_file,response_dict,name = 'File1',threshold = 0):
    """goal of this function is to create a varaible for positivity returned in the response_dict"""
  
    sentiments = {}
    
    for i,response in enumerate(data):
        sentiment = 0       
        for word in response:
            if sent_file.has_key(word.lower()):
                sentiment+=int(sent_file[word.lower()])
        sentiments[i] = [sentiment,response]
        response_dict[i] = response_dict[i].append(sentiment)

    #aggregate analysis
    overall = 0
    for score in sentiments.keys():
        overall += sentiments[score][0]

    pos=0
    neg=0
    for key in sentiments.keys():
        if sentiments[key][0]>threshold:
            pos+=1
        elif sentiments[key][0]<-(threshold):
            neg+=1

    pos_ratio = pos/float(len(sentiments.keys()))
    neg_ratio = neg/float(len(sentiments.keys()))

    ls.print_sent_analysis(txt_file,overall,sentiments,pos_ratio,neg_ratio)

    return response_dict




def main():
    """pass it a directory and it will loop through all .txt. files and run the sntiment_score and common_word_analysis methods"""    
    
    rootdir,b_val = ls.validate_dir(sys.argv)

    if not(b_val):
        return

    for subdir,dirs,files in os.walk(rootdir):
        for file in files:
            if file[file.find('.'):] == '.txt':
                txt_file = os.path.join(rootdir,file)
                
                run_analysis(txt_file)


def run_analysis(txt_file):
    
    response_dict = ls.setup_responses(txt_file)

    data = ls.split_response(txt_file)
    liwc_dict = ls.load_liwc_cats()
    sent_file = ls.load_LabMT()
    
    tmep = sentiment_score(data,sent_file,response_dict,txt_file)
    final = liwc_analysis(data,liwc_dict,temp,txt_file)

    #output final dictionary as CSV


if __name__ == '__main__':
    import datetime as dt
    
    d1 = dt.datetime.now()

    try:
        main()
        d2 = dt.datetime.now()
        print 'Elapsed time = %s'%(d2-d1)
    except Exception,e:
        print 'Error'
        print e.message