from IR_util import *
from answer_question_util import *
from ngram_tiling_func import *
import sys

docname=sys.argv[1]
qocname=sys.argv[2]
parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
solr = pysolr.Solr('http://localhost:8983/solr/gettingstarted/', timeout=10)
sentences=index(docname,solr)
with open(qocname,"r") as qfile:
    questions=[q.rstrip() for q in qfile.readlines()]
    for question in questions:
        candidates=retrieval(solr,question.lower(),sentences)
        type,predicate,answer_phrase = predicate_form(question.lower(),parser)
        if type ==None:
            print candidates[0]
        else:
            

