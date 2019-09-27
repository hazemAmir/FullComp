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
 


### Code and data sets will be soon available...
