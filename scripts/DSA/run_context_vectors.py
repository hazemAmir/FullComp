# -*- coding: utf-8 -*-
#________________________________________ *** DSA *** _____________________________________________-
#																								   -
# 							  Distributional Standard Approach									   -
# 																							       - 
# * Standard Approach: Step 2 --------> Context Vectors --------------------------------------------
# 									                                                               -
# Author  : Amir HAZEM  			                                                               -
# Created : 19/11/2018				                       		                                   -
# Updated :	25/01/2019						                                                       -
# source  : 									 												   -
# 		  python run_context_vectors.py breast_cancer en postag 1 3							       - 
#									                                                               -
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
from operator import itemgetter, attrgetter
import codecs
import DSA
import argparse
#---------------------------------------------------------------------------------------------------

# Fix seeds to reproduce the same results #--
os.environ['PYTHONHASHSEED'] = '0'		  #--
np.random.seed(42)					  	  #--
rn.seed(12345)						  	  #--	
# ----------------------------------------#--

# Normalize postags among several languages (en,fr) / other languages are to be added soon
def postag_norm(tag,lang):
	
	if lang =="fr": #------------------------------------------------------------------------------- 
		# Verb TAGS: VER:cond conditional, VER:futu futur, VER:impe imperative, VER:impf imperfect, 
		# VER:infi infinitive, VER:pper past participle, VER:ppre present participle, VER:pres present, 
		# VER:simp simple past, VER:subi subjunctive imperfect, VER:subp subjunctive present
		# Noun Tags: N = NAM proper name, NOM	noun
		# Adjective Tags: ADJ
		if tag in ['VER:cond', 'VER:futu', 'VER:impe', 'VER:impf','VER:infi','VER:pper', 'VER:ppre','VER:pres','VER:simp', 'VER:subi','VER:subp']: tag = 'v'
		if tag in ['NOM','NAM']: tag = 'n'
		if tag in ['ADJ']:		 tag = 'a'

	if lang =="en": #------------------------------------------------------------------------------- 	
		# Verb TAGS: VB  base form, VBD past tense, VBG gerund or present participle, VBN past participle
		# VBP non-3rd person singular present, VBZ 3rd person singular present 
		# Noun Tags: NN singular or mass, NNS plural, NNP Proper noun singular,	NNPS Proper noun plural 
		# Adjective Tags: JJ Adjective, JJR	Adjective comparative, JJS 	Adjective superlative 
		if tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']: tag = 'v'
		if tag in ['NN', 'NNS', 'NNP', 'NNPS']: 			 tag = 'n' 
		if tag in ['JJ', 'JJR', 'JJS']: 					 tag = 'a' 

	return tag	
#----------------------------------------------------------------------------------------------------

# Save vocabulary 
def write_vocab(path_vocab,occ):

	tab_res = []
	for tok in occ:
		tab_res.append((tok,occ[tok]))	
	# Sort vocabulary	
	result = sorted(tab_res,key=itemgetter(1),reverse=True)	
	with  codecs.open(path_vocab,'w',encoding = 'utf-8') as f :	
		for tok in result:
			f.write (tok[0] + '\t' + str(tok[1])+ '\n')
#----------------------------------------------------------------------------------------------------

# Save word context vectors 
def write_context_vectors(path_ctxvec,coocc, occ):

	context_vectors={}
	for pair in coocc:
		xy = pair.split(' ')
		head = xy[0]
		tail = xy[1]+"#"+ str(coocc[pair])

		if context_vectors.has_key(head):
			context_vectors[head] = context_vectors[head] + ":" + tail
		else:
			context_vectors[head] = tail	
	
	with  codecs.open(path_ctxvec,'w',encoding = 'utf-8') as f :	
		for x in context_vectors:
			count = occ[x] 
			line = x + '#'+ str(count) +':'+ context_vectors[x]				
			f.write (line + '\n')			
#----------------------------------------------------------------------------------------------------

# Build word context vectors
def build_context_vectors(corpus_dir,lang,corpus_type,stopwords,w):

	tab_occ = {}
	tab_coocc = {}
	# read all files of a given directory (corpus_dir)
	onlyfiles = [f for f in listdir(corpus_dir) if isfile(join(corpus_dir, f))]
	
	for filename in onlyfiles:
		print filename
		
		with  codecs.open(corpus_dir+"/"+filename,'r',encoding = 'utf-8') as f :
			for line in f:
				line = ((line)).strip()
				
				print "Ori : ---> " + line+ "\n" 
				sent = ""
				if corpus_type == 'tok' or corpus_type == 'lem':
					if flag_filter:
						# Filter stopwords
						
						sent = ' '.join(x for x in line.split(' ') if not stopwords.has_key(x) and x.isalpha())

					else:
						sent = ' '.join(x for x in line.split(' ') if x.isalpha())	

				if corpus_type == "postag" :
					
					if flag_filter == "True" :
						# Filter stopwords
						print "Stop words filtering"
						
						#sent = ' '.join(x for x in line.split(' ') if not stopwords.has_key((x.split('_pos:')[0]).lower()) and (x.split('_pos:')[0]).isalpha() and postag_norm(x.split('_pos:')[1],lang) in ['n','v','a'])
						sent = ' '.join(x for x in line.split(' ') if not stopwords.has_key((x.split('_pos:')[0]).lower()) and (x.split('_pos:')[0]).isalpha() )
						
					else:
						#print "No stop words filtering"
						sent = ' '.join(x for x in line.split(' ') if (x.split('_pos:')[0]).isalpha() and postag_norm(x.split('_pos:')[1],lang) in ['n','v','a'])		

				# count cooccurences :		
				print "FILT : ---> " + sent		
				cpt = 0
				seg = sent.split(' ')
				for i in seg:
					print i + " "+ str(cpt)
					# Count vocabulary occurence --------
					token = (i.split('_pos:')[0]).lower()
					if tab_occ.has_key(token):
						tab_occ[token] += 1
					else:
						tab_occ[token] = 1
					# -----------------------------------	

					# Count cooccurence pairs -------------------------------------------
					for j in range(cpt-w,cpt+w+1):
						#print j
						if j >= 0 and j < len(seg):
							if i != seg[j]:
								pair = token + " "+ (seg[j].split('_pos:')[0]).lower()
								if 	tab_coocc.has_key(pair): 
									tab_coocc[pair]+=1 
								else: 
									tab_coocc[pair]= 1
								#print pair
					cpt+=1
					# --------------------------------------------------------------------	
	return tab_occ,tab_coocc
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Main 
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':

	stopwords = {}
	occ   	  = {}
	coocc 	  = {}
	tab_res   = []


	# Load arguments ---------------------------------------------------------------------------------
	args = DSA.load_args()
	
	# Parameters:---------------------------------------------------------------------------------------
	corpus 		= args.corpus 			# sys.argv[1]
	lang 		= args.lang			    # sys.argv[2]	# Language : en/fr/...	
	corpus_type = args.corpus_type		# sys.argv[3]	# Flag     : tok/lem/postag
	flag_filter = args.flag_filter		# True if  int(sys.argv[4]) == 1 else False	# Filter stopwords 1/0
	w 			= int(args.w) 			# int(sys.argv[5]) # : window size 1/2/3... number of words before and after the center word

	corpus_dir  	= "../data/corpora/" + corpus + '/' + lang + '/' + corpus_type 
	stopwords_path 	= "../data/stopwords/" + "stopwords_" + lang + ".txt" 
	path_vocab      = "../data/corpora/" + corpus + '/' + lang + '/vocab_'+lang + ".csv"
	path_ctxvec		= "../data/context_vectors/" +corpus+'_'+lang + '_w' + str(w) + ".vect"





	try: 
		print "Building " + DSA.Language_MAP(lang) + " context vectors..."

		# Load stopwords
		stopwords = DSA.load_stopwords(stopwords_path)
		# Build word context vectors
		occ,coocc = build_context_vectors(corpus_dir,lang,corpus_type, stopwords,w)	
		# Save vocabulary
		write_vocab(path_vocab,occ)	 
		# Save Context vectors
		write_context_vectors(path_ctxvec,coocc,occ)

		print "Done."	
	#except:
	except Exception as e:
		print 'My exception occurred, value:', e	
		#print "Unexpected error ", sys.exc_info()[0]	
