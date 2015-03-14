# lingo_code
a python script to analyze free text and display correlations of positive emotion versus other LIWC based tags

lingo_code.py is the main module. To run this script, pass lingo_code.py a valid directory containing at least 1 .txt file. lingo_code.py requires lingo_support.py to be in the same directory as lingo_code.py

This script requires python 2.X and the following packages to be installed on the users computer:
 * pandas
 * numpy
 * pylab
 
High Level Description:
	lingo_code.py iterates through a directory and runs an analysis on each .txt file in the specified directory.  The script produces both a CSV and a heat map of correlations per .txt file in the specified directory.  If no directory is specified, the script errors out gracefully.


For more information about LabMT sentiment analysis, please visit:
	http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0026752#pone-0026752-g017
		
For more information about LIWC, please visit:
	http://www.liwc.net/