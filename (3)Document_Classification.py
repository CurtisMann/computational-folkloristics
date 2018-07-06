#Curtis Mann

import re
import math
import nltk

queryFileName = "CleanQueries.txt"
locationFileName = "Locations.txt"
folkloreFileName = "test.txt"
outputFileName = "ClassificationOutput.txt"
answerKeyFileName = "key.txt"
scoresFileName = "scores.txt"

stop = nltk.corpus.stopwords.words('english')

#Classes###################################
#Q Class
class Q:
    def __init__(self, query):
        self.Q = query
        self.Ve = {}
        self.cosSim = {}
    
    def setQ(self, query):
        self.Q = query

    def setVe(self, vector):
        self.Ve = vector

    def setSim(self, sim):
        self.cosSim = sim

#F Class
class F:
    def __init__(self, folklore, ID):
        self.F = folklore
        self.ID = ID
        self.Ve = {}
        self.cosSim = {}
    
    def setF(self, folklore):
        self.F = folklore

    def setVe(self, vector):
        self.Ve = vector

    def setSim(self, sim):
        self.cosSim = sim  
###########################################

#Cosine similarity function################
def cosineSimilarity(list1,list2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(list1)):
        x = list1[i]
        y = list2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
        
    if sumxx * sumyy == 0:
        return 0
    else:
        return sumxy/(math.sqrt(sumxx*sumyy))
###########################################

regions = ["irish", "india", "china", "africa"]
locCountDic = {}
for i in regions:
    locCountDic[i] = 0

regionList = []

irishCos = []
indiaCos = []
chineseCos = []
africaCos = []

irishQ = Q("")
indiaQ = Q("")
chineseQ = Q("")
africaQ = Q("")

#Get input and create vectors for queries##
lData = open(locationFileName, 'r', encoding="utf8")
qData = open(queryFileName, 'r', encoding="utf8")
lSplit = lData.read().split('\n')
qSplit = qData.read().split('\n')
qData.close()
lData.close()

qListLength = len(qSplit)
qList = [] #List of Q (query) objects
qIDF = {} #Dict of words and their IDF scores

#Create list of Q Objects#
for i in qSplit:
    qList.append(Q(i))

#Set Location/location count#
tempIndex = 0
for i in lSplit:
    if "irish" in i:
        irishQ.setQ(irishQ.Q + qList[tempIndex].Q + " ")
        locCountDic["irish"] += 1
    if "india" in i:
        indiaQ.setQ(indiaQ.Q + qList[tempIndex].Q + " ")
        locCountDic["india"] += 1
    if "chinese" in i:
        chineseQ.setQ(chineseQ.Q + qList[tempIndex].Q + " ")
        locCountDic["china"] += 1
    if "africa" in i:
        africaQ.setQ(africaQ.Q + qList[tempIndex].Q + " ")
        locCountDic["africa"] += 1
    tempIndex += 1

regionList = [irishQ, indiaQ, chineseQ, africaQ]

#Calculate IDF scores for each word#
for i in regionList:
    for x in i.Q.split():
        if x not in qIDF:
            qIDF[x] = 0
for i in qIDF:
    for x in regionList:
        if i in x.Q:
            qIDF[i] += 1
for i in qIDF:
    qIDF[i] = math.log(len(regionList)/qIDF[i])

#Calculate TF-IDF scores for queries#
#For every region
for i in regionList:
    tempVector = {}

    #For every word in that region's query
    for x in i.Q.split():

        #If that word is not in the tempVector, add it
        if x not in tempVector:
            tempVector[x] = i.Q.split().count(x) * qIDF[x]
    i.setVe(tempVector)

###########################################

#Get input and create vectors for folklore#

fData = open(folkloreFileName, 'r', encoding='latin-1')
fSplit = fData.read().split('\n')
fData.close()

fListLength = 0 #Number of stories #Updated later
fList = [] #List of F (folktale) objects
fIDF = {} #Dict of words and their IDF scores

#Create F objects#
tempID = 1
for i in fSplit:
    if ("ID: " + str(tempID)) in i:
        if tempID != 1:
            fList.append(tempF)
        tempF = F("", tempID)
        tempID += 1
        continue
    tempF.setF(tempF.F + i)

fListLength = len(fList)

#Clean folklore#
for x in fList:
    cleanQ = ""
    split = x.F.split('\n')
    listLength = len(split) -1
    querywords = x.F.split()
    for i in split:
        resultwords  = [word for word in querywords if word.lower() not in stop]
        tempQ = ' '.join(resultwords)
        tempQ = re.sub(r'[^\w\s]','',tempQ)
        tempQ = re.sub("([0-9])",'', tempQ)
        if split.index(i) != listLength:
            cleanQ += tempQ + "\n"
        else:
            cleanQ += tempQ
    x.setF(cleanQ)

#Calculate IDF scores for each word#
for i in fList:
    for x in i.F.split():
        if x not in fIDF:
            fIDF[x] = 0
for i in fIDF:
    for x in fList:
        if i in x.F:
            fIDF[i] += 1
for i in fIDF:
    fIDF[i] = math.log(fListLength/fIDF[i])
    
#Calculate TF-IDF scores for folklore#
for i in fList:
    tempVector = {}
    for x in i.F.split():
        if x not in tempVector:
            tempVector[x] = i.F.split().count(x) * fIDF[x]
    i.setVe(tempVector)

##############################################

#Cosine similarity############################

#For every folklore story
for i in fList:
    
    #For every region's query
    for z in range(len(regionList)):
        qVector = []
        fVector = []
            
        #For every every word in that query
        for y in regionList[z].Ve:
                
            #Match words for each story and query to create vectors
            if y in i.Ve:
                fVector.append(i.Ve[y])
                qVector.append(regionList[z].Ve[y])

        #Calculate cosineSimilarity
        cosSim = cosineSimilarity(fVector, qVector)
                            
        #Assign similarities
        if z == 0:
            irishCos.append(cosSim)
        if z == 1:
            indiaCos.append(cosSim)
        if z == 2:
            chineseCos.append(cosSim)
        if z == 3:
            africaCos.append(cosSim)
        
##############################################

#Sort and Print###############################
output = open(outputFileName, 'w')
scoresOut = open(scoresFileName, 'w')
keyData = open(answerKeyFileName, 'r', encoding="utf8")
keySplit = keyData.read().split('\n')

winnersDict = {}
answerDict = {}
for i in regions:
    answerDict[i] = 0
    winnersDict[i] = 0

winnerScore = []
winnerLoc = []

for i in range(len(irishCos)):
    tempHighest = irishCos[i]
    tempRegion = "irish"
    
    scoresOut.write(str(i + 1) + "\n")
    scoresOut.write("  Irish: " + str(irishCos[i]) + "\n")
    scoresOut.write("  India: " + str(indiaCos[i]) + "\n")
    scoresOut.write("  China: " + str(chineseCos[i]) + "\n")
    scoresOut.write(" Africa: " + str(africaCos[i]) + "\n")
    
    if indiaCos[i] > tempHighest:
        tempHighest = indiaCos[i]
        tempRegion = "india"
    if chineseCos[i] > tempHighest:
        tempHighest = chineseCos[i]
        tempRegion = "china"   
    if africaCos[i] > tempHighest:
        tempHighest = africaCos[i]
        tempRegion = "africa"
    winnerScore.append(tempHighest)
    winnerLoc.append(tempRegion)

tempID = 0

output.write("ID:  ANSWER MATCH   SIMILARITY" + "\n\n")
    
for i in keySplit:
    output.write(str(tempID + 1) + ":   " + i + "  " + winnerLoc[tempID] + "   " + str(winnerScore[tempID]) +"\n")
    answerDict[i] = answerDict[i] + 1
    if i == winnerLoc[tempID]:
        winnersDict[winnerLoc[tempID]] = winnersDict[winnerLoc[tempID]] + 1
    tempID += 1

output.write("\nRESULTS \n\n")

for i in regions:
    output.write(i + ":   " + str(winnersDict[i]) + "/" + str(answerDict[i]) + ", " + str(winnersDict[i]/answerDict[i]) + "\n")

output.close()
scoresOut.close()
