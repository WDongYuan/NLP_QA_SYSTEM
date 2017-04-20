from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from common_filter import CommonFilter
import common_filter
from sets import Set
import CommonFunction as cf
symbol = "_"
INFINITY = 1000000
class MyFilter:

	
		
	def Filter(self,candidate,query,grampos,gramner,irresult,wordstem):
		queryclass = cf.QueryClassification(query)
		result = []
		if queryclass=="PERSON":
			candidate = CommonFilter(query,candidate)
			for gram in candidate:
				if self.IsName(gram[0],grampos,gramner) or self.IsPerson(gram[0],grampos,gramner):
						result.append(gram)
		elif queryclass=="PERSON_ENTITY":
			candidate = CommonFilter(query,candidate)
			for gram in candidate:
				if self.IsPerson(gram[0],grampos,gramner):
						result.append(gram)
		elif queryclass=="TIME":
			candidate = CommonFilter(query,candidate)
			# print(candidate)
			for gram in candidate:
				if self.IsTime(gram[0],grampos,gramner):
					result.append(gram)
		elif queryclass=="LOCATION":
			candidate = CommonFilter(query,candidate)
			for gram in candidate:
				if self.IsLocationOrganization(gram[0],grampos,gramner):
					result.append(gram)
		elif queryclass == "DO_NP":
			candidate = common_filter.RemoveNotWord(candidate)
			candidate = common_filter.RemoveQueryWord(query,candidate)
			dep = cf.StanfordDependency(query)
			keyword = ""
			for onedep in dep:
				if onedep["dep"]=="dobj" and onedep["dependentGloss"].lower()=="what":
					keyword = onedep["governorGloss"]
					break
			keywordlist = []
			for tmpsen in irresult:
				tmpdep = cf.StanfordDependency(tmpsen)
				for onedep in tmpdep:
					if onedep["dep"]=="dobj" and wordstem[onedep["governorGloss"]]==wordstem[keyword]:
						keywordlist.append(wordstem[onedep["dependentGloss"]])
			for gram in candidate:
				if self.HasKeyword(gram[0],keywordlist,wordstem):
					result.append(gram)
			return result
		elif queryclass == "SUBJ_DO":
			candidate = common_filter.RemoveNotWord(candidate)
			candidate = common_filter.RemoveQueryWord(query,candidate)
			dep = cf.StanfordDependency(query)
			keyword = ""
			for onedep in dep:
				if onedep["dep"]=="nsubj" and onedep["dependentGloss"].lower()=="what":
					keyword = onedep["governorGloss"]
					break
			keywordlist = []
			for tmpsen in irresult:
				tmpdep = cf.StanfordDependency(tmpsen)
				for onedep in tmpdep:
					if onedep["dep"]=="nsubj" and wordstem[onedep["governorGloss"]]==wordstem[keyword]:
						keywordlist.append(wordstem[onedep["dependentGloss"]])
			for gram in candidate:
				if self.HasKeyword(gram[0],keywordlist,wordstem):
					result.append(gram)
			return result
		elif queryclass == "DET_DO_NP":
			dep = cf.StanfordDependency(query)
			# queryarr = cf.MyTokenize(query)
			keyword = ""
			theobj = ""
			for onedep in dep:
				if onedep["dep"]=="det" and onedep["dependentGloss"].lower()=="what"\
				or onedep["dependentGloss"].lower()=="which":
					theobj = onedep["governorGloss"]
					break

			notremoved = Set([theobj])
			for onedep in dep:
				if onedep["dep"]=="compound":
					if onedep["dependentGloss"]==theobj:
						notremoved.add(onedep["governorGloss"])
					elif onedep["governorGloss"]==theobj:
						notremoved.add(onedep["dependentGloss"])
			candidate = common_filter.RemoveNotWord(candidate)
			# print(candidate)
			candidate = common_filter.RemoveQueryWord(query,candidate,notremoved)
			# print(candidate)
			# print(theobj)
			for onedep in dep:
				if onedep["dep"]=="dobj" and onedep["dependentGloss"].lower()==theobj:
					keyword = onedep["governorGloss"]
					break
			keywordlist = []
			for tmpsen in irresult:
				tmpdep = cf.StanfordDependency(tmpsen)
				for onedep in tmpdep:
					if onedep["dep"]=="dobj" and wordstem[onedep["governorGloss"]]==wordstem[keyword]:
						keywordlist.append(wordstem[onedep["dependentGloss"]])
			# print(keywordlist)
			for gram in candidate:
				# print(gram)
				if self.HasKeyword(gram[0],keywordlist,wordstem):
					result.append(gram)
			return result
		elif queryclass == "DET_SUBJ_DO":
			# candidate = common_filter.RemoveNotWord(candidate)
			# candidate = common_filter.RemoveQueryWord(query,candidate,notremoved)
			dep = cf.StanfordDependency(query)
			# queryarr = cf.MyTokenize(query)
			keyword = ""
			theobj = ""
			for onedep in dep:
				if onedep["dep"]=="det" and onedep["dependentGloss"].lower()=="what"\
				or onedep["dependentGloss"].lower()=="which":
					theobj = onedep["governorGloss"]
					break

			notremoved = Set([theobj])
			for onedep in dep:
				if onedep["dep"]=="compound":
					if onedep["dependentGloss"]==theobj:
						notremoved.add(onedep["governorGloss"])
					elif onedep["governorGloss"]==theobj:
						notremoved.add(onedep["dependentGloss"])
			candidate = common_filter.RemoveNotWord(candidate)
			candidate = common_filter.RemoveQueryWord(query,candidate,notremoved)

			for onedep in dep:
				if onedep["dep"]=="nsubj" and onedep["dependentGloss"].lower()==theobj:
					keyword = onedep["governorGloss"]
					break
			keywordlist = []
			for tmpsen in irresult:
				tmpdep = cf.StanfordDependency(tmpsen)
				for onedep in tmpdep:
					# try:
					if onedep["dep"]=="nsubj" and wordstem[onedep["governorGloss"]]==wordstem[keyword]:
						keywordlist.append(wordstem[onedep["dependentGloss"]])
					# except:
					# 	print(onedep)
			for gram in candidate:
				if self.HasKeyword(gram[0],keywordlist,wordstem):
					result.append(gram)
			return result
		elif queryclass == "IS_NP":
			keyword = ""
			dep = cf.StanfordDependency(query)
			for onedep in dep:
				if onedep["dep"]=="nsubj" and onedep["governorGloss"].lower()=="what":
					keyword = onedep["dependentGloss"]
			keywordlist = []
			for tmpsen in irresult:
				tmpdep = cf.StanfordDependency(tmpsen)
				for onedep in tmpdep:
					if onedep["dep"]=="nsubj" and wordstem[onedep["governorGloss"]]==wordstem[keyword]:
						keywordlist.append(wordstem[onedep["dependentGloss"]])
					elif onedep["dep"]=="nsubj" and wordstem[onedep["dependentGloss"]]==wordstem[keyword]:
						keywordlist.append(wordstem[onedep["governorGloss"]])
			for gram in candidate:
				if self.HasKeyword(gram[0],keywordlist,wordstem):
					result.append(gram)
			return result
		elif queryclass == "HOW_DO":
			return []
		elif queryclass == "HOW_DEGREE":
			candidate = common_filter.RemoveQueryWord(query,candidate)
			candidate = common_filter.RemoveStopWord(query,candidate)
			candidate = common_filter.RemoveNotWordWithNumber(candidate,grampos)
			for gram in candidate:
				if self.HasNumber(gram[0],grampos)==True:
					result.append(gram)
			return result
		# elif queryclass=="LOCATION":
		# 	candidate = CommonFilter(query,candidate)
		# 	for 
		return result

	def IsLocationOrganization(self,gram,grampos,gramner):
		arr = gram.split(symbol)
		pos = grampos[gram].split(symbol)
		ner = gramner[gram].split(symbol)
		if ner[-1]=="LOCATION" or ner[-1]=="ORGANIZATION":
			return True
		else:
			return False
		





	def IsName(self,gram,grampos,gramner):
		arr = gram.split(symbol)
		pos = grampos[gram].split(symbol)
		ner = gramner[gram].split(symbol)
		for i in range(len(arr)):
			word = arr[i]
			if word=="":
				return False
			if not word[0].isupper() or ner[i]!="PERSON":
				return False
		return True

	def IsPerson(self,gram,grampos,gramner):
		arr = gram.split(symbol)
		pos = grampos[gram].split(symbol)
		if pos[-1][0]!="N":
			return False
		word = arr[-1]
		if word[0].isupper():
			return False
		syn = wn.synsets(word)
		# print(syn)
		if len(syn)==0:
			return False
		syn = syn[0]
		hyperpath = syn.hypernym_paths()
		# print(hyperpath)
		for onehyperpath in hyperpath:
			for onehyper in onehyperpath:
				obj = onehyper.name().split(".")[0]
				if obj=="person":
					return True
		return False

	def IsTime(self,gram,grampos,gramner):
		pos = grampos[gram].split(symbol)
		ner = gramner[gram].split(symbol)
		gram = gram.split(symbol)
		if ner[-1]=="TIME" or ner[-1]=="DATE":
			return True
		return False

	def HasNumber(self,gram,grampos):
		arr = gram.split(symbol)
		for word in arr:
			if grampos[word]=="CD":
				return True
		return False




	##Keyword distance measurement.
	
	def QueryKeyword(self,query):
		stopWords = Set(stopwords.words('english'))
		ner,pos = cf.StanfordNERPOS(query)
		# print(pos)
		pp = 0
		while pp<len(pos):
			# if pos[pp][1][0]!="N" and pos[pp][1][0]!="V":
			# 	pos.pop(pp)
			if pos[pp][0] in stopWords:
				pos.pop(pp)
			else:
				pp += 1
		keyword = [pos[i][0] for i in range(len(pos))]
		return Set(keyword)

	def GramQueryDst(self,gram,qWordList,senTokens,wordstem):
		gramWord = gram.split(symbol)
		idxs = [i for i in range(len(senTokens)) if senTokens[i]==wordstem[gramWord[0]]]
		# if gram=="2_to_3_years":
		# 	print(idxs)
		if idxs == 0:
			return [0,0]
		position = []
		for idx in idxs:
			if idx+len(gramWord)-1>=len(senTokens):
				continue
			head = idx
			end = -1
			matchFlag = True
			for i in range(len(gramWord)):
				if matchFlag and wordstem[gramWord[i]] != senTokens[head+i]:
					# if gram=="2_to_3_years":
					# 	print(gramWord[i])
					# 	print(senTokens[head+i])
					matchFlag = False
			if matchFlag:
				end = head+len(gramWord)-1
				position.append([head,end])
		# print(gram+":"+str(senTokens))
		# print(position)
		# if gram=="2_to_3_years":
		# 	print(position)

		qWordIdx = {}
		for word in qWordList:
			for i in range(len(senTokens)):
				if senTokens[i]==word:
					if word not in qWordIdx:
						qWordIdx[word] = []
					qWordIdx[word].append(i)
		# print(qWordIdx)

		minDst = INFINITY
		for onePos in position:
			tmpWholeMin = 0
			for qWord,idxs in qWordIdx.items():
				tmpMinDst = INFINITY
				for idx in idxs:
					if idx<onePos[0] and tmpMinDst>(onePos[0]-idx):
						tmpMinDst = onePos[0]-idx
					elif idx>onePos[1] and tmpMinDst>(idx-onePos[1]):
						tmpMinDst = idx-onePos[1]
				if tmpMinDst!=INFINITY:
					tmpWholeMin += tmpMinDst
				# if gram=="2_to_3_years":
				# 	print(tmpMinDst)
			if minDst>tmpWholeMin:
				minDst = tmpWholeMin
		# print(minDst)
		if minDst==0:
			minDst = INFINITY	
		# if gram=="temperature_scale_in_a":
		# 	print([len(qWordIdx),minDst])
		return [len(qWordIdx),minDst]

	def KeyWordDistance(self,candidateList,answerList, query,wordstem):
		qKeyWord = self.QueryKeyword(query)
		# print(qKeyWord)
		#Get the stem of qKeyWord
		qKeyWord = [wordstem[tmpw] for tmpw in qKeyWord]
		# print(qKeyWord)

		# print(len(qKeyWord))
		for oneCom in candidateList:
			gram = oneCom[0]
			keyWordNum,keyWordDst = 0,0
			for sen in answerList:
				senTokens = cf.MyTokenize(sen)
				# print(senTokens)
				#Get the stem for a candidate sentence
				senTokens = [wordstem[senTokens[i]] for i in range(len(senTokens)) if senTokens[i] in wordstem]

				nn,dd = self.GramQueryDst(gram,qKeyWord,senTokens,wordstem)
				if nn>keyWordNum and dd!=INFINITY:
					keyWordNum = nn
					keyWordDst = dd
				elif nn==keyWordNum and keyWordDst>dd:
					keyWordNum = nn
					keyWordDst = dd
			oneCom.append([keyWordNum,keyWordDst])
		candidateList = candidateList
		candidateList = sorted(candidateList,cmp=cf.MyCompare1)
		return candidateList

	def HasKeyword(self,gram,kwl,wordstem):
		arr = gram.split(symbol)
		for word in arr:
			if wordstem[word] in kwl:
				return True
		return False







	def TestIsPerson(self,gram):
		arr = gram.split(symbol)
		word = arr[-1]
		syn = wn.synsets(word)
		# print(syn)
		if len(syn)==0:
			return False
		syn = syn[0]
		hyperpath = syn.hypernym_paths()
		print(hyperpath)
		for onehyperpath in hyperpath:
			for onehyper in onehyperpath:
				obj = onehyper.name().split(".")[0]
				if obj=="person":
					return True
		return False

# myfilter = PersonFilter()
# print(myfilter.TestIsPerson('profile'))
# syn = wn.synsets('professor')[0]
# print(syn.name())
# print(syn.hypernym_paths())

