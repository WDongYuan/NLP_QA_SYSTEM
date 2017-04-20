# from search import search
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from sets import Set
from common_filter import CommonFilter
from MyFilter import MyFilter
from pycorenlp import StanfordCoreNLP
import CommonFunction as cf
# from Person_Filter import PersonFilter
import common_filter
import re
import math


symbol = "_"
N_GRAM = 4
INFINITY = 1000000
# def MyCompare1(a,b):
# 	if a[2][0]!=b[2][0]:
# 		# print(str(a)+"----"+str(b))
# 		return b[2][0]-a[2][0]
# 	else:
# 		return a[2][1]-b[2][1]
# def MyTokenize(sentence):
# 	rawTokens = word_tokenize(sentence)
# 	myTokens = [rawTokens[i].encode("ascii","ignore") for i in range(len(rawTokens))]
# 	return myTokens

# def SentencePOS(sentence):
# 	raw_pos = pos_tag(word_tokenize(sentence))
# 	pos = []
# 	for tup in raw_pos:
# 		pos.append([tup[0],tup[1]])
# 	return pos

# def QueryKeyword(query):
# 	stopWords = Set(stopwords.words('english'))
# 	pos = SentencePOS(query)
# 	pp = 0
# 	while pp<len(pos):
# 		if pos[pp][1][0]!="N" and pos[pp][1][0]!="V":
# 			pos.pop(pp)
# 		elif pos[pp][0] in stopWords:
# 			pos.pop(pp)
# 		else:
# 			pp += 1
# 	keyword = [pos[i][0] for i in range(len(pos))]
# 	return Set(keyword)

# def GramQueryDst(gram,qWordList,senTokens):
# 	gramWord = gram.split(symbol)
# 	idxs = [i for i in range(len(senTokens)) if senTokens[i]==gramWord[0]]
# 	if idxs == 0:
# 		return [0,0]
# 	position = []
# 	for idx in idxs:
# 		if idx+len(gramWord)-1>=len(senTokens):
# 			continue
# 		head = idx
# 		end = -1
# 		matchFlag = True
# 		for i in range(len(gramWord)):
# 			if matchFlag and gramWord[i] != senTokens[head+i]:
# 				matchFlag = False
# 		if matchFlag:
# 			end = head+len(gramWord)-1
# 			position.append([head,end])
# 	# print(gram+":"+str(senTokens))
# 	# print(position)

# 	qWordIdx = {}
# 	for word in qWordList:
# 		for i in range(len(senTokens)):
# 			if senTokens[i]==word:
# 				if word not in qWordIdx:
# 					qWordIdx[word] = []
# 				qWordIdx[word].append(i)
# 	# print(qWordIdx)

# 	minDst = INFINITY
# 	for onePos in position:
# 		tmpWholeMin = 0
# 		for qWord,idxs in qWordIdx.items():
# 			tmpMinDst = INFINITY
# 			for idx in idxs:
# 				if idx<onePos[0] and tmpMinDst>(onePos[0]-idx):
# 					tmpMinDst = onePos[0]-idx
# 				elif idx>onePos[1] and tmpMinDst>(idx-onePos[1]):
# 					tmpMinDst = idx-onePos[1]
# 			tmpWholeMin += tmpMinDst
# 		if minDst>tmpWholeMin:
# 			minDst = tmpWholeMin
# 	# print(minDst)
# 	if minDst==0:
# 		minDst = INFINITY	

# 	return [len(qWordIdx),minDst]








# def StanfordNERPOS(sentence):
# 	# print("Connect to the port: 53510")
# 	nlp = StanfordCoreNLP('http://localhost:9000')
# 	# print("Port connected: 53510")
# 	output = nlp.annotate((sentence),properties={'annotators':'tokenize,pos,ner','outputFormat':'json'})
# 	ner = []
# 	pos = []
# 	for token in output['sentences'][0]['tokens']:
# 		ner.append([token['word'].encode('ascii', 'ignore'),token['ner'].encode('ascii', 'ignore')])
# 		pos.append([token['word'].encode('ascii', 'ignore'),token['pos'].encode('ascii', 'ignore')])
# 	return ner,pos

def WriteFile(data,path):
	file = open(path,"w+")
	for one in data:
		file.write(str(one)+"\n")
	file.close()
# query = query.lower()#Convert query to lower case
def GenerateNGram(n,doc,grampos,gramner):
	gram = {}
	pos = grampos
	gram_count = 0
	stemlist = []
	for line in doc:
		# print(line)
		# linepos = pos_tag(word_tokenize(line))
		linener,linepos = cf.StanfordNERPOS(line)
		linestem = cf.StanfordStemmer(line)
		stemlist += linestem
		# print(linener)
		# print("-----------"+str(linepos))
		line = [linepos[i][0] for i in range(len(linepos))]
		# print(line)
		for i in range(len(line)-n+1):
			tup = ""
			for j in range(n):
				tup += line[i+j]
				if j!=n-1:
					tup += symbol
			if tup not in gram:
				gram[tup] = 0
				posgram = ""
				nergram = ""
				for posi in range(n):
					posgram += linepos[i+posi][1]
					if posi != n-1:
						posgram += symbol
				pos[tup] = posgram

				for neri in range(n):
					nergram += linener[i+neri][1]
					if neri != n-1:
						nergram += symbol
				gramner[tup] = nergram
			gram[tup] += 1
			gram_count += 1
	return [gram,gram_count,stemlist]

def ProcessData(irresult):
	result = []
	# print(irresult)
	puntuation = Set([",",".",":"])
	for ss in irresult:
		ss = ss.encode('ascii', 'ignore').strip().split("\n")
		for onestring in ss:
			result.append(onestring)
		# ss = re.split(r'\s',ss)
		# tmps = []
		# for word in ss:
		# 	if word[len(word)-1] in puntuation:
		# 		# tmps.append(word[0:len(word)-1].lower())
		# 		tmps.append(word[0:len(word)-1])
		# 		tmps.append(word[len(word)-1])
		# 	else:
		# 		# tmps.append(word.lower())
		# 		tmps.append(word)
		# newss = " ".join(tmps)
		# newfile.write(newss+"\n")
		# result.append(newss)
	return result

def NGramTiling(query,answerlist):
	#IR Process
	# print("IR processing")
	# irresult = search(MY_SEARCH_FILE,QUERY)
	irresult = answerlist
	QUERY = query


	#Preprocess irresult
	pro_data = ProcessData(irresult)
	WriteFile(pro_data,"irresult.txt")
	# for onesample in pro_data:
	# 	print(ne_chunk(pos_tag(word_tokenize(onesample))))
	# 	print(pos_tag(word_tokenize(onesample)))


	# Genrate the ngram first
	# print("Generating N-gram")
	n = N_GRAM #The number of grams it will use, begin with unigram
	# file = open("processed_data.txt")
	# file = open("ptb.2-21.txt")
	# ss = file.readline().strip()
	# ss = file.readline().strip().lower()
	doc = []
	gram = []
	grampos = {}
	gramner = {}
	wordstem = {}
	for ss in pro_data:
		doc .append(ss)
		# ss = file.readline().strip()
		# ss = file.readline().strip().lower()
	for i in range(n):
		tmpgram,tmpcount,tmpstem = GenerateNGram(i+1,doc,grampos,gramner)
		# print(tmpstem)
		gram.append(tmpgram)
		for tup in tmpstem:
			wordstem[tup[0]] = tup[1]
	# print(grampos)
	# print(gram)

	#Get the stem for query
	qstem = cf.StanfordStemmer(query)
	for onestem in qstem:
		wordstem[onestem[0]] = onestem[1]
	# print(wordstem)

	# Voting: Calculate the score for every snippet
	# print("Voting.")
	score = []
	for i in range(n):
		for k,v in gram[i].items():
			score.append([k,v])
	score = sorted(score,key=lambda onescore:onescore[1], reverse = True)
	# print(len(score))
	WriteFile(score,"voteresult.txt")
	# print(score)


	# General Filtering 
	# print("Filter process.")
	# score = CommonFilter(QUERY,score)
	myfilter = MyFilter()
	score = myfilter.Filter(score,QUERY,grampos,gramner,pro_data,wordstem)
	# print(score)

	#Combination
	# print("Combination.")
	combination = []
	for tup in score:
		word = tup[0]
		arr = word.split(symbol)
		tmpscore = tup[1]
		for i in range(len(arr)):
			tmpscore += gram[0][arr[i]]
		combination.append([word,tmpscore])
		# print(word)
	combination = sorted(combination, key=lambda tup:tup[1],reverse = True)
	WriteFile(combination,"Combination.txt")


	#Measure the distance of between the ngram and the keyword of the query
	# qKeyWord = QueryKeyword(query)
	# # print(len(qKeyWord))
	# for oneCom in combination:
	# 	gram = oneCom[0]
	# 	keyWordNum,keyWordDst = 0,0
	# 	for sen in answerlist:
	# 		senTokens = MyTokenize(sen)
	# 		nn,dd = GramQueryDst(gram,qKeyWord,senTokens)
	# 		if nn>keyWordNum and dd!=INFINITY:
	# 			keyWordNum = nn
	# 			keyWordDst = dd
	# 		elif nn==keyWordNum and keyWordDst>dd:
	# 			keyWordNum = nn
	# 			keyWordDst = dd
	# 	oneCom.append([keyWordNum,keyWordDst])
	# candidateList = combination
	# candidateList = sorted(candidateList,cmp=MyCompare1)
	candidateList = combination
	queryType = cf.QueryClassification(QUERY)
	print(queryType)
	what = Set(["DO_VP","DO_NP","IS_NP"])
	how = Set(["HOW_JJ","HOW_ADV","HOW_DEGREE"])
	why = Set(["REASON"])
	if queryType == "PERSON":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
		# None
	elif queryType == "PERSON_ENTITY":
		# candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query)
		None
	elif queryType == "TIME":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	elif queryType == "DO_NP":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	elif queryType == "SUBJ_DO":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	elif queryType == "DET_DO_NP":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	elif queryType == "DET_SUBJ_DO":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	elif queryType == "IS_NP":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	elif queryType == "HOW_DEGREE":
		candidateList = myfilter.KeyWordDistance(candidateList,answerlist,query,wordstem)
	elif queryType in what or queryType in how or queryType in why:
		# print(answerlist[0])
		return [answerlist[0]]
	else:
		return [answerlist[0]]
	WriteFile(candidateList,"CandidateList.txt")


	#Read Document Frequency
	# file = open("./doc_frequency.txt")
	# docmunet_count = int(file.readline().strip().split(" ")[1])
	# frequency = {}
	# ss = file.readline().strip()
	# word_in_corpus = 0
	# while ss!="":
	# 	arr = ss.split(" ")
	# 	frequency[arr[0]] = int(arr[1])
	# 	word_in_corpus += int(arr[1])
	# 	ss = file.readline().strip()

	# #Score
	# print("Rescore.")
	# for tup in combination:
	# 	arr = tup[0].split(symbol)
	# 	tmpsum = 0
	# 	for i in range(len(arr)):
	# 		df = 0
	# 		if arr[i] not in frequency:
	# 			df = 1
	# 		else:
	# 			df = frequency[arr[i]]
	# 		tmpsum += math.log(float(docmunet_count)/df)
	# 	tup[1] = tup[1]*1.0/len(arr)*tmpsum
	# combination = sorted(combination, key=lambda tup:tup[1],reverse = True)
	if len(candidateList)==0 or candidateList[0][2][0]==0:
		return [answerlist[0]]
	answer_phrase = candidateList[0][0].split(symbol)
	# print(combination[0:11])
	return answer_phrase
	# WriteFile(combination,"finalresult.txt")


def TestCode():
	qfile = open("/Users/weidong/Downloads/Question_Answer_Dataset_v1.2/S09/querydata.txt")
	QQ = []
	ss = qfile.readline().strip()
	while ss!="":
		QQ.append(ss)
		ss = qfile.readline().strip()
	for qq in QQ:
		filepath = qq.split("\t")[1]
		Q = qq.split("\t")[0]
		print(Q)
		MY_SEARCH_FILE = "/Users/weidong/Downloads/Question_Answer_Dataset_v1.2/S09/"+filepath+".txt"
		answerlist = search(MY_SEARCH_FILE,Q)
		if len(answerlist)>20:
			answerlist = answerlist[0:21]
		answer = NGramTiling(Q,answerlist)
		for word in answer:
			print(word),
		print("")


if __name__ == "__main__":
	# TestCode()
	# print(pos_tag(word_tokenize("Welcome to Carnegie Mellon University.")))
	# Q = "When was Dempsey born ?"
	# Q = "Who is John Terry ?"
	# Q = "Who is the Chelsea Captain ?"
	# Q = "When did Dempsey join Seattle Sounders ?"
	# Q = "When was Donovan born ?"
	# Q = "When Terry became the captain ?"
	# Q = "Who is Chelsea Captain ?"
	# Q = "Where does Terry play football?"
	# # print(QueryKeyword(QUERY))
	# Q = "Where was Solo born ?"
	# Q = "Who did Alessandro Volta marry?"
	Q = "Who made Volta a count?"
	# Q = "When did Volta retire?"
	# Q = "Where was Volta born?"
	Q = "Who showed that Avogadro's theory held in dilute solutions?"
	Q = "Who wrote about ants in A Tramp Abroad?"
	Q = "Where are bullet ants located?"
	Q = "Where is the city of Antwerp?"
	Q = "When was the first photgraph of lincoln taken?"
	Q = "When did he publish another memoria?"
	Q = "When did he become a professor?"
	Q = "What is the battery made by Alessandro Volta credited as?"
	Q = "What are the three segments of an ant?"
	Q = "What is the only variety of modern Arabic that has acquired official language status?"
	Q = "How long was Lincoln's formal education?"
	Q = "When did the Gettysburg address argue that America was born?"
	Q = "What is the smallest suborder of turtles?"
	Q = "What does the word Ghana mean?"
	# Q = "What do river otters eat?"
	Q = "What does a polar bear's fur provide?"
	Q = "What caused Calvin Jr.'s death?"
	Q = "What does violincello mean?"
	# *Q = "What kind of ducks feed on land?"
	Q = "What do most recognizable international company and largest employer have in common?"
	Q = "What district was Ford elected from?"
	Q = "What shares land borders with Papua New Guinea, East Timor and Malaysia?"
	Q = "What type of creatures breathe air and don't lay eggs underwater?"
	Q = "What did Uruguay win in 1828?"
	Q = "What is the largest ethnic minority in Romania?"
	Q = "What is actually black in color?"
	Q = "What is the last word on the page?"
	Q = "What is the largest living species of penguin?"
	Q = "What is an otter's den called?."
	Q = "What is a collective noun for kangaroos?"
	Q = "What is now part of Adams National Historical Park?"
	# Q = "Which spice originally attracted Europeans to Indonesia?"
	Q = "Which Russian army general conquered Finland in 1809?"
	Q = "Which future Heisman Trophy winner did Ford tackle?"
	Q = "Which temperature scale did Celsius propose?"
	Q = "Which part of the strings does the left hand touch?"
	Q = "How long do most foxes live?"
	Q = "How many people did the 1970 Bhola cyclone kill?"
	Q = "How much area does Dhaka cover?"
	Q = "How many groups are turtles broken down into?"
	Q = "How did civil wars affect England during the Middle Ages?"
	Q = "How old was Celsius when he died?"
	Q = "How does a trumpet produce sound?"
	Q = "What did Pascal argue was as perfect as possible?"
	Q = "When did Charles-Augustin de Coulomb retire to a small estate he possessed at Blois?"
	Q = "How many people speak the Arabic language?"
	Q = "How long are cougar adult males (from nose to tail)?"
	Q = "How long is an adult cougar's paw print?"
	Q = "How many verb paradigms are there in Korean?"
	Q = "What butterfly is migratory?"
	Q = "What is the standardized form of spoken chinese?"
	Q = "What part of the cymbal is the bell?"

	print(Q)
	# MY_SEARCH_FILE = "./data/set4/a8.txt"
	MY_SEARCH_FILE = "/Users/weidong/Downloads/Question_Answer_Dataset_v1.2/S10/data/set2/a6.txt"
	answerlist = search(MY_SEARCH_FILE,Q)
	if len(answerlist)>20:
		answerlist = answerlist[0:21]
	answer = NGramTiling(Q,answerlist)
	for word in answer:
		print(word),
	# print(answer[0])

	# print(cf.StanfordNERPOS("In 2007, he became the first captain to lift the FA Cup "+\
	# 	"at the new Wembley Stadium in Chelsea\'s 10 win over Manchester United, and "+\
	# 	"also the first player to score an international goal there, scoring a header "+\
	# 	"in England\'s 11 draw with Brazil."))






