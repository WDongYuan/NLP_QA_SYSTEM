from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from sets import Set
from pycorenlp import StanfordCoreNLP
from nltk.corpus import stopwords
punctuation = [",",":",".",""]
def MyCompare1(a,b):
	if a[2][0]!=b[2][0]:
		# print(str(a)+"----"+str(b))
		return b[2][0]-a[2][0]
	elif a[2][1]!=b[2][1]:
		return a[2][1]-b[2][1]
	else:
		return b[1]-a[1]

def RemoveStopWord(tokens):
	stopWords = Set(stopwords.words('english'))
	for pun in punctuation:
		stopWords.add(pun)
	tmplist = []
	for tok in tokens:
		if tok not in stopWords:
			tmplist.append(tok)
	return tmplist

def MyTokenize(sentence):
	rawTokens = word_tokenize(sentence)
	myTokens = [rawTokens[i].encode("ascii","ignore") for i in range(len(rawTokens))]
	return myTokens
def SentencePOS(sentence):
	raw_pos = pos_tag(word_tokenize(sentence))
	pos = []
	for tup in raw_pos:
		pos.append([tup[0],tup[1]])
	return pos
def StanfordTokenize(sentence):
	nlp = StanfordCoreNLP('http://localhost:9000')
	# print("Port connected: 53510")
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,ner','outputFormat':'json'})
	tokens = []
	for token in output['sentences'][0]['tokens']:
		tokens.append(token['word'].encode('ascii', 'ignore'))
	return tokens

def StanfordNERPOS(sentence):
	# print("Connect to the port: 53510")
	nlp = StanfordCoreNLP('http://localhost:9000')
	# print("Port connected: 53510")
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,ner','outputFormat':'json'})
	# print(output)
	ner = []
	pos = []
	for token in output['sentences'][0]['tokens']:
		ner.append([token['word'].encode('ascii', 'ignore'),token['ner'].encode('ascii', 'ignore')])
		pos.append([token['word'].encode('ascii', 'ignore'),token['pos'].encode('ascii', 'ignore')])
	return ner,pos

def QueryClassification(query):
		queryarr = MyTokenize(query)
		ner,pos = StanfordNERPOS(query)
		if queryarr[0].lower()=="who":
			beV = Set(["is","are","was","were"])
			if queryarr[1] in beV and ner[2][1]=="PERSON":
				return "PERSON_ENTITY"
			else:
				return "PERSON"
		elif queryarr[0].lower()=="when":
			return "TIME"
		elif queryarr[0].lower()=="where":
			return "LOCATION"
		elif queryarr[0].lower()=="what":
			#DO_NP
			#What do you like?

			#DO_VP
			#What did they do in England?

			#IS_VP
			#What is Machine Learning?

			#SUBJ_DO
			#What make him successful?

			#DET_DO_NP
			#What drink would you like to choose?

			#DET_SUNJ_DO
			#What animal can climb tree?
			theobjflag = False
			theobj = ""
			dep = StanfordDependency(query)
			for onedep in dep:
				do = ["do","did","done"]
				if onedep["dep"]=="dobj" and onedep["dependentGloss"].lower()=="what":
					if onedep["governorGloss"].lower() in do:
						return "DO_VP"
					return "DO_NP"
				elif onedep["dep"]=="det" and onedep["dependentGloss"].lower()=="what":
					if onedep["governorGloss"].lower()=="time":
						return "TIME"
					else:
						theobj = onedep["governorGloss"]
						theobjflag = True
						break

				elif onedep["dep"]=="cop" and onedep["governorGloss"].lower()=="what":
					return "IS_NP"
				elif onedep["dep"]=="nsubj" and onedep["dependentGloss"].lower()=="what":
					return "SUBJ_DO"
			if theobjflag==True:
				# theobj = queryarr[1]
				for onedep in dep:
					if onedep["dep"]=="dobj" and onedep["dependentGloss"].lower()==theobj:
						return "DET_DO_NP"
					elif onedep["dep"]=="nsubj" and onedep["dependentGloss"].lower()==theobj:
						return "DET_SUBJ_DO"
		elif queryarr[0].lower()=="why":
			return "REASON"
		elif queryarr[0].lower()=="how":
			#HOW_JJ
			#HOW_DEGREE
			#HOW_ADV
			dep = StanfordDependency(query)
			ner,pos = StanfordNERPOS(query)
			# print(pos)
			bev = ["is","was","are","were"]
			if pos[1][0] in bev:
				return "HOW_JJ"
			howprase = ""
			for onedep in dep:
				if onedep['dep']=="advmod" and onedep["dependentGloss"].lower()=="how":
					howprase = onedep["governorGloss"]
			for onepos in pos:
				# print(onepos)
				if onepos[0]==howprase and (onepos[1][0]=="V" or onepos[1]=="MD"):
					return "HOW_DO"
				elif onepos[0]==howprase and (onepos[1]=="JJ" or onepos[1]=="RB"):
					return "HOW_DEGREE"
		elif queryarr[0].lower()=="which":
			theobj = ""
			dep = StanfordDependency(query)
			for onedep in dep:
				if onedep["dep"]=="det" and onedep["dependentGloss"].lower()=="which":
					theobj = onedep["governorGloss"]
				# theobj = queryarr[1]
			for onedep in dep:
				if onedep["dep"]=="dobj" and onedep["dependentGloss"].lower()==theobj:
					return "DET_DO_NP"
				elif onedep["dep"]=="nsubj" and onedep["dependentGloss"].lower()==theobj:
					return "DET_SUBJ_DO"


		# elif queryarr[0].lower()=="how":

		return None
def StanfordDependency(sentence):
	nlp = StanfordCoreNLP('http://localhost:9000')
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,depparse','outputFormat':'json'})
	dep = output['sentences'][0]["basicDependencies"]
	# for tmpdep in dep:
	# 	print(tmpdep)
	return dep

def StanfordStemmer(sentence):
	nlp = StanfordCoreNLP('http://localhost:9000')
	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,lemma','outputFormat':'json'})
	stem = []
	for token in output['sentences'][0]['tokens']:
		stem.append([token['word'].encode('ascii', 'ignore'),token['lemma'].encode('ascii', 'ignore')])
	return stem

def SentenceSimilarity(sen1,sen2):
	sen1 = StanfordTokenize(sen1)
	sen2 = StanfordTokenize(sen2)
	sen1 = RemoveStopWord(sen1)
	sen2 = RemoveStopWord(sen2)
	return 0