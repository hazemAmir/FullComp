# -*- coding: utf-8 -*-
#________________________________________ *** DSA *** _____________________________________________-
#																								   -
# 							  Distributional Standard Approach									   -
# 																							       - 
# * Standard Approach: Step 3 -----> Association Measures ------------------------------------------
# 									                                                               -
# Author  : Amir HAZEM  			                                                               -
# Created : 19/11/2018				                       		                                   -
# Updated :	19/11/2018						                                                       -
# source  : 																				       - 
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
import nltk
import math
from operator import itemgetter, attrgetter
import DSA
import codecs 
import argparse
#---------------------------------------------------------------------------------------------------

# Fix seeds to reproduce the same results #--
os.environ['PYTHONHASHSEED'] = '0'		  #--
np.random.seed(42)					  	  #--
rn.seed(12345)						  	  #--	
# ----------------------------------------#--


# Save context vectors
def write_context_vectors(path_ctxvec, context_vectors_assoc, occ, min_occ,path_termlist_csv,source_lang,target_lang):

	termlist,termlist_inv = DSA.load_termlist(path_termlist_csv)
	with  codecs.open(path_ctxvec,'w',encoding='utf-8') as f1 :		
		for x in context_vectors_assoc:
			count = occ[x] 
			if count >= min_occ : 
				f1.write(context_vectors_assoc[x] + '\n')
			else: # If token has a frequency less than min_occ keep it as it is part of the evaluation list
				if termlist.has_key(x)  and lang == source_lang:
					# keep the reference list
					line = context_vectors_assoc[x].split(':')
					token0 = line[0].split('#')
					result = str(token0[0]) + '#' + str(min_occ)+ ":" + ':'.join(line[1:]) 
					f1.write(result.encode('utf-8') + '\n')
				else:
					if termlist_inv.has_key(x) and 	lang == target_lang:
						line = (context_vectors_assoc[x].split(':'))
						token0 = line[0].split('#')
						print token0
						result = ((token0[0]) + '#' + (str(min_occ)) + ":" + (':'.join( line[1:])))
						print result
						f1.write(result + '\n')
# ----------------------------------------------------------------------------------------------------
# Comput contingency table for association measures
def compute_contingency_table(coocc):
	Tab_occ_X ={}
	Tab_cooc_XY ={}
	Tab_cooc_X_ALL ={}
	Tab_cooc_ALL_Y ={}
	Total = 0

	for word in coocc:

		line = coocc[word].split(':')
		x_word = word  
		x_freq = (line[0].split('#'))[1]
		Tab_occ_X[x_word] = int(x_freq)
		for i in range(1,len(line)):

			y_word = (line[i].split('#'))[0]  
			y_freq = int((line[i].split('#'))[1])
			Tab_cooc_XY[x_word+" "+y_word] = y_freq
			
			if Tab_cooc_X_ALL.has_key(x_word): 
				Tab_cooc_X_ALL[x_word]+=y_freq
			else:
				Tab_cooc_X_ALL[x_word]=y_freq	
			if Tab_cooc_ALL_Y.has_key(y_word): 
				Tab_cooc_ALL_Y[y_word]+=y_freq
			else:
				Tab_cooc_ALL_Y[y_word]=y_freq		

		Total += Tab_cooc_X_ALL[x_word]		

	return 	Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total
# ----------------------------------------------------------------------------------------------------			 	
# Compute mutual information
def compute_MI(coocc,Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total):
	Tab_MI = {}
	for x_word in coocc:
		line = coocc[x_word].split(':') 
		vec = line[0] 
		for i in range(1,len(line)):

			y_word = (line[i].split('#'))[0]  
			y_freq = int((line[i].split('#'))[1])		
			a = Tab_cooc_XY[x_word+" "+y_word]
			b = Tab_cooc_X_ALL[x_word]
			c = Tab_cooc_ALL_Y[y_word]
			result = Total * a 
			result = math.log(result / (b * c))
			vec = vec + ':' + y_word + "#"+ str(result) 
		Tab_MI [x_word] = vec
	return Tab_MI		
# ----------------------------------------------------------------------------------------------------
# Compute the discounted odds ration
def compute_ODDS(coocc,Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total):
	Tab_ODDS = {}
	for x_word in coocc:
		line = coocc[x_word].split(':') 
		vec = line[0] 
		for i in range(1,len(line)):

			y_word = (line[i].split('#'))[0]  
			y_freq = int((line[i].split('#'))[1])		
			a = Tab_cooc_XY[x_word+" "+y_word]
			b = Tab_cooc_X_ALL[x_word] - a
			c = Tab_cooc_ALL_Y[y_word] - a 
			N = Total
			d = N - a - b -c
			result = math.log( ((a + 0.5) * (d + 0.5))  / ((b + 0.5) * (c + 0.5)))
			vec = vec + ':' + y_word + "#"+ str(result) 

		Tab_ODDS [x_word] = vec

	return Tab_ODDS
# ----------------------------------------------------------------------------------------------------
# Compute log-likelihood
def compute_LL(coocc,Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total):

	Tab_LL = {}
	for x_word in coocc:
		
		line = coocc[x_word].split(':') 
		vec = line[0] 
		for i in range(1,len(line)):

			y_word = (line[i].split('#'))[0]  
			y_freq = int((line[i].split('#'))[1])		
			a = Tab_cooc_XY[x_word+" "+y_word]
			b = Tab_cooc_X_ALL[x_word] - a
			c = Tab_cooc_ALL_Y[y_word] - a 
			N = Total
			d = N - a - b -c

			if a > 0 :
				result  = a * math.log(a)
			if b > 0 :
				result += b * math.log(b) 
			if c > 0:
				result += c * math.log(c) 
			if d > 0 :	
				result += d * math.log(d) 
			if N > 0:	
				result += N * math.log(N)
			
			result +=  - (a+b) * math.log(a+b) - (a+c) * math.log(a+c) - (b+d) * math.log(b+d) - (c+d) * math.log(c+d)
			vec = vec + ':' + y_word + "#"+ str(result) 

		Tab_LL [x_word] = vec

	return Tab_LL
# ----------------------------------------------------------------------------------------------------			
#-----------------------------------------------------------------------------------------------------
# Main 
#-----------------------------------------------------------------------------------------------------

if __name__=='__main__':

	context_vectors = {}
	Tab_occ_X ={}
	Tab_cooc_XY ={}
	Tab_cooc_X_ALL ={}
	Tab_cooc_ALL_Y ={}
	Total = 0
	context_vectors_assoc = {} 
	occ = {}
	# Load arguments ---------------------------------------------------------------------------------
	args = DSA.load_args()
	# ----------------------------------------------------------------------------------------------------

	# Parameters:---------------------------------------------------------------------------------------
	corpus 				= args.corpus 	    	# sys.argv[1]	   # Corpus	
	lang 				= args.lang 	    	# sys.argv[2]	   # Language : en/fr/...
	source_lang			= args.source_lang		# sys.argv[3]	   # 
	target_lang			= args.target_lang		# sys.argv[4]	   # 
	assoc       		= args.assoc			# sys.argv[5]	   # MI / JAC / ODDS 
	w 					= int(args.w)			# int(sys.argv[6]) # : window size 1/2/3... number of words before and after the center word
	min_occ				= int(args.min_occ)		# int(sys.argv[7]) # : filtering tokens with number of occurence less than min_occ
	termlist_name		= args.termlist_name	# sys.argv[8]	   # Term list name (evaluation list name)					   

	path_vocab      	= "../data/train/corpora/" + corpus + '/tmp/vocab_'+lang + ".csv"
	path_ctxvec			= "../data/train/corpora/" + corpus + '/context_vectors/'+corpus+'_'+lang + '_w' + str(w) + ".vect"
	path_ctxvec_assoc	= "../data/train/corpora/" + corpus + '/context_vectors/'+corpus+'_'+lang + '_w' + str(w) + "_min" + str(min_occ)+ "_"+ assoc + ".assoc"
	path_termlist_csv	= "../data/train/termlists/" + termlist_name
	# ----------------------------------------------------------------------------------------------------





	try: 
		print "Building " +  DSA.Association_measure_MAP(assoc) + " for " + DSA.Language_MAP(lang) + " Corpus ..."
		# Load occurrence vectors
		occ = DSA.load_occurrence_vectors(path_vocab)
	
		# Load cooccurrence vectors
		context_vectors = DSA.load_context_vectors(path_ctxvec)

		# Compute Contingency Table
		Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total = compute_contingency_table(context_vectors)	

		if assoc.lower() == "mi":

			#Compute Mutual Information
			 context_vectors_assoc = compute_MI(context_vectors,Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total)

		if assoc.lower() == "odds":	
			# Compute Mutual Information
			context_vectors_assoc = compute_ODDS(context_vectors,Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total) 

		if assoc.lower() == "ll":	
			# Compute Mutual Information
			context_vectors_assoc = compute_LL(context_vectors,Tab_occ_X,Tab_cooc_XY,Tab_cooc_X_ALL,Tab_cooc_ALL_Y,Total)		

		# Save Association context vectors
		write_context_vectors(path_ctxvec_assoc, context_vectors_assoc, occ, min_occ,path_termlist_csv,source_lang,target_lang)

		print "Done."	
	except:
		print "Unexpected error ", sys.exc_info()[0]	

