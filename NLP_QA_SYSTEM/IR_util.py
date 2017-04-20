import pysolr
from __future__ import print_function
import re
import sys
from nltk.tokenize import sent_tokenize,blankline_tokenize
import itertools

def index(fname,query,solr):
    solr.delete(q='*:*')
    with open(fname,"r") as f:
        text=f.read()
        paragraphs=blankline_tokenize(text.decode("utf8"))
        for i in range(len(paragraphs)):
            paragraphs[i]=sent_tokenize(paragraphs[i])
        sentences=list(itertools.chain(*paragraphs))
        del paragraphs
    for i in range(len(sentences)):
        index={'id':str(i),"_text_":sentences[i]}
        solr.add([index])
    return sentences

def retrieval(solr,query,sentences):
    results = solr.search(query)
    print("Saw {0} result(s).".format(len(results)))
    for result in results:
        print("The title is '{0}'.".format(result['id']))
        print(sentences[int(result['id'])])
        yield sentences[int(result['id'])]



    