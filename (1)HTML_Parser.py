from bs4 import BeautifulSoup
import re
import codecs

#Praise StackOverflow#
#These two pages made my life much easier#
#http://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
#http://stackoverflow.com/questions/22799990/beatifulsoup4-get-text-still-has-javascript

outputFileName = 'QueriesOut.txt'

#open file
with open(r"thompson.htm", "r", encoding='UTF8') as f:
    page = f.read()
soup = BeautifulSoup(page, "html.parser")

# get text and make lowercase
text = soup.get_text().lower()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# drop blank lines
text = '\n'.join(line for line in lines if line)

#process text to make parsing easier
text = re.sub('\(cf. .+\)', '', text)
text = text.split("\n")
regex = re.compile('[a-z]\d{1,3}(\.\d{1,3}){0,2}\.')
tempIndex = 0
continueVar = False
newText = []
for i in text:
    if regex.search(i) is not None:
        newText.append(re.sub('\n', '', i) + " ")
        tempIndex = len(newText) - 1
        if not continueVar:
            continueVar = True
    else:
        if continueVar:
            newText[tempIndex] += (re.sub('\n', '', i) + " ")
newTextString = ''
for i in newText:
    newTextString += i + "\n"

queries = re.findall('([a-z]\d{1,3}(\.\d{1,3}){0,2}\. .+?\.?(\n?.+?)( ?.+?\;)?((--)| {0,2})(irish|india|chinese|africa))', newTextString, re.MULTILINE)


output = codecs.open(outputFileName, 'w', 'utf-8')

for i in queries:
    tempOut = i[0] + "\n"
    output.write(tempOut)

output.close()

