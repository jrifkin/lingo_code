def clean_word(word):
    """Gets rid of some unwanted characters from words"""
    chars = ['!','.','?','"','(',')',' ',',']
    chars_w_space = ['/','-']
    for letter in word:
        if letter in chars:
            word = word.replace(letter,'')
        if letter in chars_w_space:
            word = word.replace(letter,' ')

    return word


def unpack_dictionary(dict):
    """optional printing methods for sentiment analysis to return top and bottom verbatim lines in txt file"""
    my_ls = []
    for key in dict.keys():
        my_ls.append(dict[key])
    
    my_ls.sort(key = lambda x: x[0],reverse=True)

    print '\n****TOP 5 positive Open Ends****'

    for i,item in enumerate(my_ls):
        if i<5:
            print "\nNumber %s:\n\tSentiment score: %s\n\tVerbatim Response: %s" %(i+1,item[0],' '.join(item[1]))
        else:
            break

    my_ls.reverse()
    print '\n****BOTTOM 5 negative Open Ends****'
    for i,item in enumerate(my_ls):
        if i<5:
            print "\nNumber %s:\n\tSentiment score: %s\n\tVerbatim Response: %s" %(i+1,item[0],' '.join(item[1]))
        else:
            break

def findnth(haystack, needle, n):
    #takes in a serach string as haystack, a find string as needle, and n as an integer
    #returns an integer that represents the start position the nth iteration of needle
	return haystack.replace(needle,'XX',n-1).find(needle)

def count_matches(response,inv,liwc_counter):
    """drives LIWC analysis, returns dictionary of words found in a response, numbers of words in LIWC dictionary per response (serves as base),
    and total count of wrods per response"""
    n=0
    word_count = 0
   
    sorted_response = sorted(response)
    start_index = 0
    for word in sorted_response:
        word_count += 1
        if word in inv:
            liwc_counter[word] += 1
            n+=1
        else:
            for i in range(start_index,len(inv)):
                if inv[i].find('*')>0 and (inv[i].replace('*','') in word and inv[i][1] == word[1]):
                    liwc_counter[inv[i]]+=1
                    start_index = i
                    n+=1
                    break

    return liwc_counter,n,word_count

def category_counts(liwc_dict,liwc_counts):
    """creates category count dictionary object enabling tallying of words for LIWC analysis"""
    my_dict = create_cat_dict(liwc_dict)

    for k in liwc_counts.keys():
        if liwc_counts[k] != 0:
            mult = liwc_counts[k]
            for item in liwc_dict[k]:
                my_dict[item]+= (1 * mult)

    return my_dict


def create_cat_dict(container):
    """suppot function for creating category count placeholder"""
    dict={}
    for k,v in container.items():
        for item in v:
            dict[item] = 0
    return dict


def split_response(txt_file):
    """standard method of splitting text file into iteratable data conatined within list"""
    txt_file = open(txt_file,'r')
    data = []
    for line in txt_file:
        words = line.split(" ")
        for i,word in enumerate(words):
            if '\n' in word:
                nu_word = word.replace('\n',"")
                words[i] = nu_word
            else:
                nu_word = word
            words[i] = clean_word(nu_word)
        data.append(words)
    
    return data


def load_LabMT():
    """downloads LabMT document from journal attachment, converts to python dictionary"""
    import pandas as pd

    url = 'http://www.plosone.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pone.0026752.s001'
    
    labmt = pd.read_csv(url, skiprows=3, sep='\t', index_col=0)
    
    average = labmt.happiness_average.mean()
    sd = labmt.happiness_average.std()
    happiness_scores = ((labmt.happiness_average - average)/sd).to_dict()
    #print 'loaded labmt'
    return happiness_scores


def load_liwc_cats():
    """consumes enlgish LIWC category dictionary and creates python object"""
    import xlrd as xl
    #xlrd is 0 based in terms of cell referencing
    bPosEmo = False
    liwc_path = r"C:\_github\lingo_code\lingo_code\lingo_code\LIWC2007dictionary poster.xls"
    liwc = xl.open_workbook(liwc_path)
    ws = liwc.sheet_by_name("Official genome")
    num_rows = ws.nrows -1
    cat_dict = {}
    
    for j in range(0,64):
        my_lst=[]
        for i in range(3,num_rows):
            if ws.cell(i,j).value == "":
                break
            else:
                if str(ws.cell(i,j).value) in cat_dict:
                    cat_dict[str(ws.cell(i,j).value)].append(str(ws.cell(2,j).value))
                else:
                    cat_dict[str(ws.cell(i,j).value)] = [str(ws.cell(2,j).value)]
    
    return cat_dict


def print_liwc_results(tst_file,base,word_count,num_responses):
    """optional aggregate analysis on LIWC category scores"""
    print '/n',txt_file.name[findnth(txt_file,'\\',txt_file.count('\\'))-3:txt_file.find('.')].upper(),'/n'
    print 'Base = %s'%(base)
    print 'Total word count = %s'%(word_count)
    print 'Total # responses = %s'%(num_responses)
    print 'Avg words per response = %s'%(float(word_count)/num_responses)
    print overall_cats


def print_sent_analysis(txt_file,overall,sentiments,pos_ratio,neg_ratio):
    """optional aggregate analysis on LabMT sentiment"""
    print "~~@@~~~@@@~~ %s SENTIMENT ANALYSIS RESULTS ~~@@~~~@@@~~\n"%(txt_file[findnth(txt_file,'\\',txt_file.count('\\'))-3:txt_file.find('.')].upper())
    print "Overall sentiment score: %s"%(str(overall))
    print "Total number of responses: %s\n"%(len(sentiments.keys()))
    print "Ratio of positive comments: %s" %("{:.2%}".format(pos_ratio))
    print "Ratio of negative comments: %s" %("{:.2%}".format(neg_ratio))
    
    unpack_dictionary(sentiments)
    print '\n'


def validate_dir(args):
    """validates directory passed via argument contains text files"""
    import os
    import glob
    bValid = False
    try:
        rootdir = args[1]
    except:
        print 'Please specify a valid directory that contains at least 1 .txt file'
        return -1,bValid
    

    total_files = len(glob.glob1(rootdir,"*.txt"))
    if total_files>0:
        bValid = True
    else:
        print 'No .txt files in the specified directory'
        
    return rootdir,bValid,total_files

def setup_responses(txt_file,id_col=-1):
    """creates blank storage container for response level data per txt file analyzed"""
    txt_file = open(txt_file,'r')
    my_dict = {}
    
    my_dict = {i:[i] for i,line in enumerate(txt_file)}
    txt_file.close()
    return my_dict

def make_data(name,response_dict,header,wd):
    """creates CSV outputs of text scores for analysis in other programs"""
    import csv,os
    
    csv_name = name[findnth(name,'\\',name.count('\\'))-4:name.find('.')] + '_liwc_corr.csv'
    
    with open(csv_name,'wb') as fp:
        a = csv.writer(fp,delimiter=',')
        a.writerow(header)
        for response in response_dict.keys():
            a.writerow(response_dict[response])


def make_matrix(response_dict,headers,min_base=10):
    """creates data frame of text to split sentiment scores from LIWC category scores"""
    import pandas as pd
    return_lst = []
    
    data = pd.DataFrame.from_dict(response_dict,orient='index')
    data.columns = headers

    sentiment_scores = [i for i in data.sentiment_score]

    for col in data.columns:
        return_lst.append([i for i in data[col].values])
  
    return sentiment_scores,return_lst

def correlation_analysis(name,response_dict,header):
    """takes in text scores and produces heatmap of correlation between a LIWC category and the corresponding LabMT sentiment scores"""
    from numpy import corrcoef, arange
    from pylab import pcolor, show, colorbar, xticks, yticks
    
    sentiment_scores,liwc_cats = make_matrix(response_dict,header)
    
    #compare sentiment_scores v all liwc_cats
    R = corrcoef(sentiment_scores,liwc_cats[13:24])

    pcolor(R)
    colorbar()
    yticks(arange(0.5,13.5),header[13:24])
    xticks(arange(0.5,13.5),header[13:24])
    show()



