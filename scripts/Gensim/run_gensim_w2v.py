# -*- coding: utf-8 -*-
# --------  Gensim word2vec ------------------------------------------------------------------------
# 									                                                               -
# Author  : Amir HAZEM  			                                                               -
# Created : 10/09/2018				                                                               -
# Updated :	27/09/2019						                                                               -
# source  : https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/word2vec.ipynb -
# 			https://radimrehurek.com/gensim/install.html                                           - 
#									                                                               -
#---------------------------------------------------------------------------------------------------

# Libraries ----------------------------------------------------------------------------------------
import gensim, logging, os, sys, re
import numpy as np
import tensorflow as tf
import random as rn
import os
import argparse

# Fix seeds to reproduce the same results ---
os.environ['PYTHONHASHSEED'] = '0'    	  #--
np.random.seed(42)					  	  #--
rn.seed(12345)						  	  #--	
# -------------------------------------------

# -------------------------------------------------------------------------------------------------

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 



# Classe and Functions ----------------------------------------------------------------------------


def load_args():
	parser = argparse.ArgumentParser(description = 'Get preprocessing parameters...')
	parser.add_argument('--corpus', '-c', help='Corpus name (wind/br)',         action = "store", dest="corpus", default="wind") # wind / br
	parser.add_argument('--lang',   '-l', help='Corpus language (en/fr)',     action = "store", dest="lang", default="en")  # en / fr
	parser.add_argument('--model',  '-m', help='Embedding model (sg/cbow)',     action = "store", dest="model", default="sg") # sg / cbow
	parser.add_argument('--dim',    '-d', help='Embedding dimension (100/300/500...)', action = "store", dest="dim", default="100")
	parser.add_argument('--window', '-w', help='window size (1/2/3...) number of words surrounding the center word', action = "store", dest="w", default="3")
		
	args = parser.parse_args()
	#print parser.parse_args()
	return(args)




class LoadSentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()
#----------------------------------
def get_vocab_size(model):
	#cpt=0 
	#for word in model.wv.vocab: # uncomment for older gensim version
	#	cpt+=1
	cpt=0
	for word in model.wv.vocab:
		cpt+=1
	return cpt	
#----------------------------------
def save_model(model_output,cpt,dim,w):
	with  open(model_output,'w') as fi:
		ch=str(cpt)+" "+ str(dim)
		fi.write(str(ch)+"\n")	
	#for word in model.wv.vocab:#uncomment for older versions
		for word in model.wv.vocab:
			x=str(model[word]).split('[')
			y=x[1].split(']')
			z=re.split('\s+',y[0])
			cpt=0
			ch=""
			for i in z:
				if i.strip()!= " ":
					#print "*"+ i.strip()+ "*"  
					ch=ch+" "+ i.strip()
			fi.write(word+str(ch)+"\n")
# -------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
# Main 
#--------------------------------------------------------------------------------------------------

if __name__=='__main__':

	# Load arguments ---------------------------------------------------------------------------------
	args = load_args()

	# Parameters:--------------------------------------------------------------------------------------
	corpus =	args.corpus 		# Data set 							                             --
	lang   =	args.lang	   		# Language (en/fr/...)				                             --	
	models =	args.model 			# Embedding model (cbow/skipgram(sg))                            --	 
	dim    =	int(args.dim) 		# Dimension size (50,100,200,...n)                               --	
	w      =	int(args.w) 	    # Window size (1,2,...n)			                             --
	#--------------------------------------------------------------------------------------------------


	# Path data ---------------------------------------------------------------------------------------
	data_dir     ="../data/corpora/"+corpus+"/"+ lang + "/lem/"
	model_output ="../data/embedding_vectors/"

	#--------------------------------------------------------------------------------------------------

	sentences = LoadSentences(data_dir) # a memory-friendly iterator







	if models=="sg":
		sg_=1
		hs_=1
		#hs_=0
		#model = gensim.models.Word2Vec(sentences, workers=1,window=w, size=dim,min_count=5,sg=sg_,hs=hs_,iter=15)#,negative=5,sample=1e-4,alpha=0.05)
		model = gensim.models.Word2Vec(sentences, workers=1,window=w, size=dim,min_count=5,sg=sg_,hs=hs_,iter=1,negative=15)#,sample=1e-4,alpha=0.05)
		
	else:
		sg_=0
		hs_=0
		model = gensim.models.Word2Vec(sentences, workers=1,window=w, size=dim,min_count=5,sg=sg_,hs=hs_,iter=15)#,negative=5,sample=1e-4,alpha=0.05)

	# get vocab size
	vocab_size=get_vocab_size(model)
	# save word embedding model
	model_output=model_output+str(corpus)+"_"+str(lang)+"_vec"+str(dim)+"_w"+str(w)+"_"+str(models)+".txt"
	save_model(model_output,vocab_size,dim,w)
#--------------------------------------------------------------------------------------------------

