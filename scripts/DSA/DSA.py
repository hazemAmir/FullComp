# -*- coding: utf-8 -*-
#________________________________________ *** DSA *** _____________________________________________-
#																								   -
# 							  Distributional Standard Approach									   -
# 																							       - 
# --------------------------------------  DSA library ---------------------------------------------
# 									                                                               -
# Author  : Amir HAZEM  			                                                               -
# Created : 19/01/2019				                       		                                   -
# Updated :	24/01/2019						                                                       -
#---------------------------------------------------------------------------------------------------
#!/usr/bin/env python


# Libraries ----------------------------------------------------------------------------------------
from __future__ import division
import codecs
import argparse
# --------------------------------------------------------------------------------------------------

# Functions ----------------------------------------------------------------------------------------

# Load arguments ---------------------------------------------------------------------------------
def load_args():
	parser = argparse.ArgumentParser(description = 'Get preprocessing parameters...')
	parser.add_argument('--corpus', '-c', help='Corpus name', action = "store", dest="corpus", default="breast_cancer")
	parser.add_argument('--lang', '-l', help='Source Corpus language', action = "store", dest="lang", default="en")
	parser.add_argument('--source_lang', '-s', help='Source Corpus language', action = "store", dest="source_lang", default="en")
	parser.add_argument('--target_lang', '-t', help='Corpus language', action = "store", dest="target_lang", default="fr")
	parser.add_argument('--corpus_type', '-ct', help='Corpus type: tok/lem/postag', action = "store", dest="corpus_type", default="postag")
	parser.add_argument('--flag_filter', '-f', help='Filter stopwords 1/0', action = "store", dest="flag_filter", default="False")
	parser.add_argument('--assoc', '-a', help='Association measure MI / JAC / ODDS ', action = "store", dest="assoc", default="mi")
	parser.add_argument('--window', '-w', help='window size 1/2/3... number of words surrounding the center word', action = "store", dest="w", default="3")
	parser.add_argument('--min_occ', '-min', help='filtering tokens with number of occurence less than min_occ', action = "store", dest="min_occ", default="5")
	parser.add_argument('--termlist_name', '-eval', help='Term list evaluation', action = "store", dest="termlist_name", default="en_fr_breast_cancer_248.csv")
	parser.add_argument('--dictionary_name', '-dico', help='Bilingual dictionary', action = "store", dest="dictionary_name", default="dicfrenelda-utf8.txt")
	parser.add_argument('--similarity', '-sim', help='Similarity measure: cos / jac ', action = "store", dest="sim", default="cos")

	args = parser.parse_args()
	#print parser.parse_args()
	return(args)

# Map language acronyms to natural language
def Language_MAP(lang_accr):

	if lang_accr.lower() == "en":
		Language = "English"
	if lang_accr.lower() == "fr":
		Language = "French"

	return Language	 	
# --------------------------------------------------------------------------------------------------	
# Map association acronyms to natural language
def Association_measure_MAP(assoc):

	if assoc.lower() == "mi":
		out = "Mutual Information"
	if assoc.lower() == "odds":
		out = "Discounted Odds Ratio"
	if assoc.lower() == "ll":
		out = "Log-Likelihood"	
	return out		

def Similarity_MAP(sim):

	if sim.lower() == "cos":
		out = "Cosinus"
	if sim.lower() == "jac":
		out = "Jaccard Index"
	return out	
# --------------------------------------------------------------------------------------------------
# Load stop words
def load_stopwords(path):
	stopwords = {}
	with  codecs.open(path,'r',encoding='utf-8') as f:
		for line in f:
			tab = (line).split()
			stopwords[tab[0]] = ((tab[0].strip()).lower())
	#print ('%s \tStopwords' % len(stopwords))
	return stopwords
# --------------------------------------------------------------------------------------------------
# Load termlist (evaluation list)
def load_termlist(path_termlist):
	termlist = {}
	termlist_inv = {}
	f = open(path_termlist,'r')
	with  codecs.open(path_termlist,'r',encoding='utf-8') as f:
		for line in f:
			vect = (line.strip()).split('\t')
			termlist[vect[0]] = vect[1]
			termlist_inv[vect[1]] = vect[0]
	#print ('%s \tTermlist size' % len(termlist))		
	return termlist,termlist_inv	
# --------------------------------------------------------------------------------------------------
# Load vocabulary 
def load_occurrence_vectors(path_occvec):
	occ = {}
	with  codecs.open(path_occvec,'r',encoding = 'utf-8') as f:
		for line in f:
			vect = (line.strip()).split('\t')
			if len(vect) > 1: # avoid '' # to be solved beforehand
				occ [vect[0]]= int(vect[1])
	return occ
# --------------------------------------------------------------------------------------------------
# Load context vectors
def load_context_vectors(path_ctxvec):
	context_vectors = {}
	with  codecs.open(path_ctxvec,'r',encoding = 'utf-8') as f:
		for line in f:
			vect = (line.strip()).split(':')
			context_vectors[(vect[0].split('#'))[0]]=line
	return context_vectors	
# --------------------------------------------------------------------------------------------------

# Print Map scores 
def print_MAP_scores(Rank,size_eval,map_):

	print "\n********************************"
	print "***	 Ranking results     ***"
	print "********************************\n"
	print "--> Accuracy @ TOP K"
	print "    ----------------"
	print " TOP"+"\t|"+ " Acc(%)|"


	for k in range(1,101):
		
		if k == 1:
			print " "+ str(k) +"\t| "+  str( round(((Rank[k]/size_eval)*100),2)) +"\t|"

		if k%5==0:
			print  " "+ str(k) +"\t| "+  str(round(((Rank[k]/size_eval)*100),2))  +"\t|"
	print "********************************"
	print "\n--> MAP Score (%)"
	print "    -------------"
	map_=(map_/size_eval)*100
	
	print "MAP =\t" + str(round(map_,2))
	
	print "********************************"

