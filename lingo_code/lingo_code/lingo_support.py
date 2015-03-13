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

def count_matches(input,inv,liwc_counter):
    n=0
    word_count = 0
    responses = 0

    for response in input:
        responses+=1
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
    #print 'count_matches complete'
    return liwc_counter,n,word_count,responses

def category_counts(liwc_dict,liwc_counts):

    my_dict = create_cat_dict(liwc_dict)

    for k in liwc_counts.keys():
        if liwc_counts[k] != 0:
            mult = liwc_counts[k]
            for item in liwc_dict[k]:
                my_dict[item]+= (1 * mult)

    for k in my_dict.keys():
        if my_dict[k] == 0:
            del my_dict[k]
    return my_dict


def create_cat_dict(container):
    dict={}
    for k,v in container.items():
        for item in v:
            dict[item] = 0
    return dict


def split_response(txt_file):
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
    print 'split responses'
    return data


def load_LabMT():
    import pandas as pd

    url = 'http://www.plosone.org/article/fetchSingleRepresentation.action?uri=info:doi/10.1371/journal.pone.0026752.s001'
    
    labmt = pd.read_csv(url, skiprows=3, sep='\t', index_col=0)
    
    average = labmt.happiness_average.mean()
    sd = labmt.happiness_average.std()
    happiness_scores = ((labmt.happiness_average - average)/sd).to_dict()
    #print 'loaded labmt'
    return happiness_scores


def load_liwc_cats():
    """ *** may have trouble with odd characters such as accent e, for now encoded in unicode and translate to py string"""
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
    print '/n',txt_file.name[ls.findnth(txt_file.name,'\\',txt_file.name.count('\\'))-3:txt_file.name.find('.')].upper(),'/n'
    print 'Base = %s'%(base)
    print 'Total word count = %s'%(word_count)
    print 'Total # responses = %s'%(num_responses)
    print 'Avg words per response = %s'%(float(word_count)/num_responses)
    print overall_cats


def print_sent_analysis(txt_file,overall,sentiments,pos_ratio,neg_ratio):
    print "~~@@~~~@@@~~ %s SENTIMENT ANALYSIS RESULTS ~~@@~~~@@@~~\n"%(txt_file.name[ls.findnth(txt_file.name,'\\',txt_file.name.count('\\'))-3:txt_file.name.find('.')].upper())
    print "Overall sentiment score: %s"%(str(overall))
    print "Total number of responses: %s\n"%(len(sentiments.keys()))
    print "Ratio of positive comments: %s" %("{:.2%}".format(pos_ratio))
    print "Ratio of negative comments: %s" %("{:.2%}".format(neg_ratio))
    
    ls.unpack_dictionary(sentiments)
    print '\n'


def validate_dir(args):
    import os
    bValid = False
    try:
        rootdir = args[1]
    except:
        print 'Please specify a valid directory that contains at least 1 .txt file'
        return -1,bValid
        
    for filename in os.listdir(rootdir):
        if '.txt' in filename:
            bValid = True
            break
    else:
        print 'No .txt files in the specified directory'

    return rootdir,bValid   

def setup_responses(txt_file,id_col=-1):
    txt_file = open(txt_file,'r')
    my_dict = {}
    if id_col == -1:
        #assumes there are no ids and will create, in the future, will have to acommodate pre-existing ids
        print 'placeholder'
    
    my_dict = {i:[] for i,line in enumerate(txt_file)}
    txt_file.close()
    return my_dict