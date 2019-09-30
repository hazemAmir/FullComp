# -*- coding: utf-8 -*-
# --------  Synonym extraction of Single word terms (SWT) -----------------------------------------
# 									                                                              -
# Author  : Amir HAZEM  			                                                              -
# Created : 13/09/2018				                                                              -
# Updated :	13/09/2018				                                                              -
# source  : 																				      -		
# 														                                          -
#									                                                              -
#--------------------------------------------------------------------------------------------------

# this source code aims at providing a broad evaluation of word embedding models on the main word  
# similarity datasets 


# Libraries ---------------------------------------------------------------------------------------
import os, sys, re
import numpy as np
import random as rn
import os
import matplotlib.pyplot as plt
import math
import scipy
from scipy import stats,linalg,mat,dot
from operator import itemgetter, attrgetter
# -------------------------------------------------------------------------------------------------


# Parameters --------------------------------------------------------------------------------------

lang="en"
termlist_path = "../termlists/"
termlist_name =  lang+"_swt_syn.csv"

spec_corpus_name = "wind_train_lem.txt"
spec_corpus_path = "../data/wind/" +lang +"/lem"


# Functions ---------------------------------------------------------------------------------------

# Load evaluation termlist  
def load_termlist(termlist_path,termlist_name):
	termlist_tmp={}
	f=open(os.path.join(termlist_path,termlist_name))
	cpt_tmp=0
	for line in f:
		values=line.rstrip().split('\t')
		term1=values[0]
		term2=values[1]
		if termlist_tmp.has_key(term1):
			# duplicate terms with multiple synonymique variants by adding a temporary flag cpt_tmp
			cpt_tmp+=1
			term_tmp=term1+"_"+str(cpt_tmp)
			termlist_tmp[term_tmp]=term2
		else:
			termlist_tmp[term1]=term2
	return termlist_tmp


# print termlist
def print_tab(tab):
	for input_ in tab:
		print input_ + " "+ str(tab[input_])

# Load word embedding model


# Load vocabulary

def load_vocab(corpus_path,corpus_name):
	
	vocab_tmp={}

	f=open(os.path.join(corpus_path,corpus_name))

	for line in f:

		tokens=line.rstrip().split()
		for i in tokens:
			if vocab_tmp.has_key(i):
				vocab_tmp[i]+=1
			else:
				vocab_tmp[i]=1		

	return vocab_tmp			

# Extract terms (apply a filtering using statistical measures)



#--------------------------------------------------------------------------------------------------
# Main 
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':

	termlist={}
	spec_vocab={}

	termlist=load_termlist(termlist_path,termlist_name)
	print_tab(termlist)
	

	spec_vocab=load_vocab(spec_corpus_path,spec_corpus_name)

	print_tab(spec_vocab)

	print len(spec_vocab)
