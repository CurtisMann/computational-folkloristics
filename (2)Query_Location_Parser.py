import re
import codecs
import nltk

################################
#BRING IT ON DOWN TO QUERY TOWN#
################################

#Variable declarations#########################
inputFileName = 'QueriesOut.txt'
queryOutputFileName = 'CleanQueries.txt'
locationOutputFileName = 'Locations.txt'

stop = nltk.corpus.stopwords.words('english')

################################################

#Remove stop words, puncuation, and numbers#####
def remove(localText):
    cleanQ = ""
    split = localText.split('\n')
    listLength = len(split) -1
    for i in split:
        querywords = i.split()
        resultwords  = [word for word in querywords if word.lower() not in stop]
        tempQ = ' '.join(resultwords)
        tempQ = re.sub(r'[^\w\s]','',tempQ)
        tempQ = re.sub("([0-9])",'', tempQ)
        if split.index(i) != listLength:
            cleanQ += tempQ + "\n"
        else:
            cleanQ += tempQ
    return cleanQ
################################################

#Begin the actual program#######################
#Get data
with open(inputFileName, "r", encoding='UTF8') as f:
    allQ = f.read()
f.close()

#Fixing this one weird formatting thing that happens sometimes
allQ = allQ.split('\n')
regexp = re.compile('([a-z]\d{1,3}(\.\d{1,3}){0,2}\. )')
allQ2 = []
for i in range(len(allQ)):
    if regexp.search(allQ[i]) is not None:
        tempQ = re.sub('\n', '', allQ[i]) + " "
        allQ2.append(tempQ)
        tempIndex = allQ2.index(tempQ)
    else:
        allQ2[tempIndex] += re.sub('\n', '', allQ[i]) + " "


allQ = ''
for i in allQ2:
    allQ += i + "\n"

#Remove ID's
allQ = re.sub('([a-z]\d{1,3}(\.\d{1,3}){0,2}\. )', '', allQ)
allQ = allQ.split('\n')

#Deal with the "South American Indians" that snuck into here via the "India" graveytrain
newQ = []
for i in allQ:
    if i.find("s. am. india") == -1 and i.find("so. am. india") == -1 and i.find("s. am.") == -1 and i.find("so. am.") == -1:
        newQ.append(i)

#Chunk it up
allQList = []
newQ2 = []
for i in newQ:
    tempQ = re.findall('(.+?\.)+?', i)
    if len(tempQ) == 0:
        continue
    else:
        newQ2.append(i)
        cleanTempQ = remove(tempQ[0])
        allQList.append(cleanTempQ)


allLocList = ["" for x in range(len(newQ2))]
counter = 0
for i in newQ2:
    if "irish" in i:
        allLocList[counter] += "irish "
    if "india" in i:
        allLocList[counter] += "india "
    if "chinese" in i:
        allLocList[counter] += "chinese "
    if "africa" in i:
        allLocList[counter] += "africa "
    counter += 1


################################################

#Output clean queries###########################
queryOutput = codecs.open(queryOutputFileName, 'w', 'utf-8')
locationOutput = codecs.open(locationOutputFileName, 'w', 'utf-8')
for i in range(len(allQList)):
    if allLocList[i] == '':
        continue
    if len(allQList[i].split()) == 1:
        continue
    else:
        queryOutput.write(allQList[i] + "\n")
        locationOutput.write(allLocList[i] + "\n")
locationOutput.close()
queryOutput.close()
################################################
#FIN

