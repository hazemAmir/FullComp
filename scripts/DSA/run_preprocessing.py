# -*- coding: utf-8 -*-
#________________________________________ *** DSA *** _____________________________________________-
# 																							       - 
# * Standard Approach: Step 0 ---------> Pre-processing --------------------------------------------
# 									                                                               -
# Author  : Amir HAZEM  			                                                               -
# Created : 19/11/2018				                       		                                   -
# Updated :	28/01/2019						                                                       -
# source  : python run_preprocessing.py -c breast_cancer -l en --lem --postag --default_inout	   -
#---------------------------------------------------------------------------------------------------
#!/usr/bin/env python


# Libraries ----------------------------------------------------------------------------------------
from __future__ import division
import sys
import os 
from os import listdir
from os.path import isfile, join
import numpy as np
import random as rn
import nltk
import treetaggerwrapper
import argparse
import codecs
#---------------------------------------------------------------------------------------------------

# Fix seeds to reproduce the same results #--
os.environ['PYTHONHASHSEED'] = '0'		  #--
np.random.seed(42)					  	  #--
rn.seed(12345)						  	  #--	
# ----------------------------------------#--

# Functions #---------------------------------------------------------------------------------------
# Preprocesses the corpus tokenization lemmatization and postagging regarding the parameters
def preprocessings(corpus_dir,LANG,TAGDIR,lem_flag,pos_flag):

	corpus_in = corpus_dir + "/raw/"+ LANG

	print corpus_in
	onlyfiles = [f for f in listdir(corpus_in) if isfile(join(corpus_in, f))]

	tagger = treetaggerwrapper.TreeTagger(TAGLANG=LANG,TAGINENC='utf-8',TAGOUTENC='utf-8',TAGDIR=TAGDIR)

	if lem_flag: print "Lemmatization... ok"
	if pos_flag: print "PosTagging... ok"
	
	out_tok =  corpus_dir + "/tok/" + LANG
	out_lem =  corpus_dir + "/lem/" + LANG
	out_pos =  corpus_dir + "/postag/" + LANG

	print out_tok
	for filename in onlyfiles:
		print filename
	
		#with  open(out_tok+'/'+filename,'w') as f1 ,open(out_lem+'/'+filename,'w') as f2,open(out_pos+'/'+filename,'w') as f3:
		with  codecs.open(out_tok+'/'+filename,'w',encoding = 'utf-8') as f1,codecs.open(out_lem+'/'+filename,'w',encoding = 'utf-8') as f2,codecs.open(out_pos+'/'+filename,'w',encoding = 'utf-8') as f3:	

			with codecs.open(corpus_in+'/'+filename,'r',encoding = 'utf-8') as f:
				for line in f:
					line = (line).strip()
					
					# Tokenization ---------------------------------------
					sent_tok  = (' '.join(nltk.word_tokenize(line.lower())))
					#print sent_tok
					f1.write(sent_tok+'\n')

					if lem_flag:
						tags = tagger.tag_text(unicode(sent_tok))
						# Lemmatization ------------------------------------------------------------
						sent_lem = ' '.join(x.split('\t')[2] for x in tags if len(x.split('\t'))==3)
						f2.write(sent_lem+'\n')
						# PosTagging ---------------------------------------------------------------
						if pos_flag:
							sent_pos = ' '.join( [x.split('\t')[2]+"_pos:"+x.split('\t')[1] for x in tags if len(x.split('\t'))==3]) 
							f3.write(sent_pos+'\n')
							#print "PosTagging... ok"
#--------------------------------------------------------------------------------------------------
# Load command line  parameters
def load_argparse():
		
	parser = argparse.ArgumentParser(description = 'Get preprocessing parameters...')
	parser.add_argument('--corpus', '-c', help='Corpus name', 				 			action = "store", dest="corpus" 	   ,default="breast_cancer")
	parser.add_argument('--lang', '-l',   help='Corpus language', 			 			action = "store", dest="lang" 		   ,default="en")
	parser.add_argument('--lem',   		  help='Corpus lemmatazation (lem)', 			action = "store_true", dest="lem_flag"      ,default="lem" )
	parser.add_argument('--postag', 	  help='Corpus postagging (postag)', 			action = "store_true", dest="postag_flag"   ,default="postag")
	parser.add_argument('--default_inout', help='Default corpus directory', 			action = "store_true", dest="default_flag"  )
	parser.add_argument('--input',        help='Raw Corpus input directory', 			action = "store", dest="input_dir"     ,default="")
	parser.add_argument('--output',       help='pre-processed corpus output directory', action = "store", dest="output_dir"   ,default="")

	args = parser.parse_args()
	return args
	
#--------------------------------------------------------------------------------------------------
# Main 
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':


	TAGDIR		= "./tree-tagger-linux/"

	args = load_argparse()
	corpus_name      		 = args.corpus
	default_corpus_dir 		 = args.input_dir 
	lang 			 		 = args.lang
	lem_flag    	 		 = args.lem_flag
	postag_flag 	 		 = args.postag_flag
	default_flag 	 		 = args.default_flag
	


	try: 
		print "Create pre-processed corpus directories... "

		if default_flag:

			default_corpus_dir  = "../data/train/corpora/" 
			default_output		= default_corpus_dir + corpus_name  
			corpus_dir = default_corpus_dir+ corpus_name 
		else:
				
			default_corpus_dir  = args.input_dir
			default_output		= args.output_dir 
			corpus_dir 			= args.input_dir + '/'+corpus_name 

		path = default_corpus_dir + corpus_name
		if not os.path.isdir(path):
			os.mkdir(path,0755)
		

		path = 	default_output + "/tok/"
		if not os.path.isdir(path):
			os.mkdir(path,0755)

		path = 	default_output + "/tok/" + lang
		if not os.path.isdir(path):
			os.mkdir(path,0755)		


		path = 	default_output + "/lem/"
		if not os.path.isdir(path):
			os.mkdir(path,0755)

		path = 	default_output + "/lem/" + lang
		if not os.path.isdir(path):
			os.mkdir(path,0755)	

		path = 	default_output + "/postag/"
		if not os.path.isdir(path):
			os.mkdir(path,0755)

		path = 	default_output + "/postag/" + lang
		if not os.path.isdir(path):
			os.mkdir(path,0755)	
			
		
		path = 	default_output  + "/context_vectors/"
		if not os.path.isdir(path):
			os.mkdir(path,0755)	

		path = 	default_output  + "/tmp/"
		if not os.path.isdir(path):
			os.mkdir(path,0755)	


		#print "corpus name " + corpus_name
		#print "corpus_input	" + corpus_dir
		#print "corpus_output 	" + args.output_dir

		print "Start pre_processing..."
		 	
		preprocessings(corpus_dir ,lang,TAGDIR,lem_flag,postag_flag)			
		print "done!"

	except:
		print "Unexpected error ", sys.exc_info()[0]	













