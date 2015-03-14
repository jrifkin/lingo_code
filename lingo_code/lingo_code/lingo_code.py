#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,re
import lingo_support as ls

"""Script that consumes a directory containing text files and returns 1) a CSV file per text file containing the LabMT sentiment score 
and LIWC category scores per line in file and 2) a heatmap of correlations between LabMT sentiment and LIWC categories per txt file analyzed"""

def liwc_analysis(data,liwc_dict,response_dict,name='File1'):
    """method for running LIWC analysis on each line in txt file. Returns response_dict with appended LIWC category scores per line in txt file"""

    total_word_count = 0
    total_base = 0

    liwc_counter = {k:0 for k in liwc_dict.keys()}
    
    liwc_words = liwc_dict.keys()
    liwc_words.sort(key=lambda x: re.sub('[^A-Za-z]+', '', x).lower())

    for i,response in enumerate(data):
        counts,base,word_count = ls.count_matches(response,liwc_words,liwc_counter)
        total_word_count+=word_count
        total_base+=base 

        overall_cats = ls.category_counts(liwc_dict,counts)

        for key in overall_cats.keys():
            tmp_lst = response_dict[i]
            tmp_lst.append(liwc_score(key,overall_cats,base))
            response_dict[i] = tmp_lst
    
        liwc_counter = dict.fromkeys(liwc_dict,0)
    headers = overall_cats.keys()

    return response_dict,headers
    
    #ls.print_liwc_results(txt_file,total_base,total_word_count,len(data))


def liwc_score(cat,overall_cats,base):
    """simplistic calculation of LIWC category score"""
    if base == 0:
        return 0.0
    else:
        return float(overall_cats[cat])/base


def sentiment_score(data,sent_file,response_dict,name = 'File1',threshold = 0):
    """calculates sentiment score per line in txt file and appends scores to response_dict"""
  
    sentiments = {}

    for i,response in enumerate(data):
        sentiment = 0       
        word_count = 0
        for word in response:
            word_count+=1
            if sent_file.has_key(word.lower()):
                sentiment+=float(sent_file[word.lower()])
        sentiments[i] = [sentiment,response]
        
        #add to score as first var in response_dict
        tmp_lst = response_dict[i]
        tmp_lst.append(sentiment)
        tmp_lst.append(word_count)
        response_dict[i] = tmp_lst
        

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

    #ls.print_sent_analysis(name,overall,sentiments,pos_ratio,neg_ratio)

    return response_dict


def main():
    """main control method that quarterbacks the analyses and outputs per text file"""
    
    rootdir,b_val,total_files = ls.validate_dir(sys.argv)
    
    if not(b_val):
        return

    liwc_dict = ls.load_liwc_cats()
    sent_file = ls.load_LabMT()

    counter = 0
    for subdir,dirs,files in os.walk(rootdir):
        for file in files:
            if file[file.find('.'):] == '.txt':
                counter+=1
                txt_file = os.path.join(rootdir,file)
                print 'Analyzing file %s of %s. File name = %s'%(counter,total_files,txt_file[ls.findnth(txt_file,'\\',txt_file.count('\\'))-4:])
                responses,header = run_analysis(txt_file,liwc_dict,sent_file)

                ls.make_data(txt_file,responses,header,rootdir)

                ls.correlation_analysis(txt_file,responses,header)


def run_analysis(txt_file,liwc_dict,sent_file):
    """method to run sentiment and LIWC analyses"""
    
    response_dict = ls.setup_responses(txt_file)

    data = ls.split_response(txt_file)
    
    temp = sentiment_score(data,sent_file,response_dict,txt_file)
    final,header = liwc_analysis(data,liwc_dict,temp,txt_file)

    header.insert(0,'response_id')
    header.insert(1,'sentiment_score')
    header.insert(2,'word_count')
    return final,header

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