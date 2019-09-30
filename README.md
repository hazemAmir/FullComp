# FullComp
## Word Embedding Approach for Synonym Extraction of Multi-Word Terms.

We introduce Semi-Compositional **Semi-Comp** and Full-Compositional **FullComp** approaches to deal with synonym acquisition of multiword terms. We conducted experiments on two specialized domains using wind energy and breast cancer data sets in French and English. Our results show significant improvements over the state of the art.

The paper can be found [here](http://www.amirhazem.ovh/publications/year/2018/LREC/LREC_2018_Paper_Synonym_Extraction.pdf)

When citing **FullComp** in academic papers and theses, please use the following BibTeX entry:
```
@InProceedings{HAZEM18.36,
  author = {Amir Hazem and BÃ©atrice Daille},
  title = "{Word Embedding Approach for Synonym Extraction of Multi-Word Terms}",
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018)},
  year = {2018},
  month = {May 7-12, 2018},
  address = {Miyazaki, Japan}
  }
```
## Features
- For distributional approaches (Semi-Comp (MI-COS), Semi-Comp (LO-COS) and Semi-Comp (LLR-JAC)), we used steps one and two described in the DSA approach https://github.com/hazemAmir/DSA
- For context word representation, we trained Skip-Gram  and CBOW models using **Gensim** toolkit released by [Radim Rehurek](https://github.com/RaRe-Technologies/gensim). 
 
## Requirements

- **Gensim** toolkit [Radim Rehurek](https://github.com/RaRe-Technologies/gensim).
- Python 2.7  
- NumPy
- SciPy

## Usage
The following steps are requiered:
- preprocess the data sets
- compute word context vectors using association measures such as mutual information (MI) discounted odds ratio (LO) and Log-likelihood ration (LLR).
- compute word embedding vectors using gensim 
- the resulting vectors are used for compositionality.
## 0) Pre-processing
python run_preprocessing.py -c corpus -l lang --lem --postag --default_inout 

```
- corpus	: Corpus name (-c corpus)
- lang		: Corpus language (-l language) 
- lem		: Corpus lemmatization (--lem)
- postag	: Corpus postagging (--postag)
- default_inout	: Default corpus directory (--default_inout), if specified default directories are used to load the corpus.
		  the corpus should be in the directory DSA/data/train/corpus_name/raw/source_language and
		  DSA/data/train/corpus_name/raw/target_language	
- input		: Raw Corpus input directory, if default_inout is not used  (--input corpus path )
- output	: Pre-processed corpus output directory, if default_inout is not used  (--output corpus path)

--> Breast cancer pre-processing example:

python run_preprocessing.py -c breast_cancer -l en --lem --postag --default_inout

python run_preprocessing.py -c breast_cancer -l fr --lem --postag --default_inout

```

## 1) Context vectors

### Build source and target context vectors 
```
	 python run_context_vectors.py -c $corpus -l $source_lang -ct postag -f  $filter -w $w 
example: python DSA/run_context_vectors.py -c wind -l en -ct postag -f True -w 3

	 python run_context_vectors.py -c $corpus -l $target_lang -ct postag -f  $filter -w $w
	 python DSA/run_context_vectors.py -c wind -l fr -ct postag -f True -w 3
```

## 2) Embedding vectors

### Build source and target embedding vectors 
```
	python run_gensim_w2v.py -c $corpus -l $lang -m $model -d $dim -w $w 
	
```



### Code and data sets will be soon available...
