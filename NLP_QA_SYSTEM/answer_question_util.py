import nltk
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
from nltk.tag import StanfordNERTagger
from nltk.tree import Tree
from pattern.en import conjugate

WHO = "who"
WHAT = "what"
HOW = "how"
WHERE = "where"
WHOM = "whom"
HOWMANY = "howmany"
WHY = "why"
WH = "SBARQ"
BI1 = "SQ"
BI2 = "SINV"
SUPPORT=[WHO,WHAT,HOW,WHERE,WHOM,HOWMANY]
DOLIST=["do","does","did"]
BELIST=["is","am","are","was","were"]
INF = 'VB'
PAST = 'VBD'
PLURAL = 'VBP'
P3SG = 'VBZ'
TENSE={PAST: 'p',PLURAL: 'inf', P3SG: '3sg'}
WH_PATTERN1=['WH','DO','NP','VP']
WH_PATTERN2=['WHO','VP']
WH_PATTERN3=['BE','NP','VP']
WH_PATTERN4=['WHO','BE','VP']

def question_classify(qword):
    if qword == "what":
        return WHAT
    elif qword == "who":
        return WHO
    elif qword == "how":
        return HOW
    elif qword == "where":
        return WHERE
    elif qword=="whom":
        return WHOM
    else:
        return None

def answer_subject(qphrase):
    tokens=qphrase.leaves()
    if len(qphrase)>1:
        if tokens[0] not in SUPPORT:
            return None,""
        if tokens[0]==WHAT:
            return WHAT," ".join(tokens[1:])
        elif tokens[0]=="how" and tokens[1]=="many":
            return HOWMANY," ".join(tokens[2:])
        else:
            return tokens[0],""
    else:
        return tokens[0],""

def predicate_form(question,parser):
    tree = list(parser.raw_parse(question))[0][0]
    tree.draw()
    q_type=None
    label=tree.label()
    answer_phrase=""
    try:
        if label!=WH and label!=BI1 and label!=BI2:
            return None,None,None
        else:
            q_type,answer_phrase=answer_subject(tree[0])
            if q_type==None:
                return None,None,None
            if label in WH:
                tree=tree[1]
        if len(tree)==1:
            return q_type,""," ".join(tree.leaves())
        auxv = tree[0]
        np = tree[1]
        if len(tree)>2:
            vp = tree[2]
            other = tree[2:] if len(tree) >3 else ""
            if auxv[0] in DOLIST:
                npt=" ".join(np.leaves())
                verb = vp[0]
                verb[0] = conjugate(verb[0], TENSE[auxv.label()])
                vpt=" ".join(vp.leaves())
                return q_type,npt+" "+vpt + " " + (" ".join(other.leaves()) if other!= "" else ""),answer_phrase
            elif auxv[0] in BELIST:
                npt=" ".join(np.leaves())
                vpt=" ".join(vp.leaves())
                return q_type,npt+" "+auxv[0]+" "+vpt+ (" ".join(other.leaves()) if other != "" else ""),answer_phrase
            else:
                return None,None,None
        else:
            if auxv[0] in BELIST:
                npt=" ".join(np.leaves())
                return q_type,npt+" "+auxv[0],answer_phrase
            else:
                return None,None,None
    except Exception as e:
        return None,None,None
    


if __name__ == "__main__":
    parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
    type,predicate,answer_phrase = predicate_form("who plays soccer".lower(),parser)
    print type,predicate,answer_phrase
