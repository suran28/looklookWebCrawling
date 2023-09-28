import requests
from bs4 import BeautifulSoup
import json
import pprint

'''
USERAGENT는 밑의 사이트에서 확인한다.
https://www.whatismybrowser.com/detect/what-is-my-user-agent/
'''
USERAGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
headers = {'User-Agent':USERAGENT}
URL = 'https://www.musinsa.com/app/cs/faq/000'
reponse = requests.get(URL, headers=headers)

def ExtractTag(soup):
    for a_tag in soup.find_all('a'):
        a_tag.extract()
    for br_tag in soup.find_all('br'):
        br_tag.extract()

reponseContent = reponse.content
soup = BeautifulSoup(reponseContent, 'html.parser')
rawData = soup.find_all('div', class_='CFaqTableItem')

#####################################################
dataset = {}


# print("="*50)
# print(len(rawData))

for i in range(len(rawData)):


    rawDataSoup = BeautifulSoup(str(rawData[i]), 'html.parser')
    ExtractTag(rawDataSoup)

    categoryTag = rawDataSoup.find('em', class_='CFaqTableItem__category')
    questionTag = rawDataSoup.find('p', class_='CFaqTableItem__question')
    answerTag = rawDataSoup.find('div', class_='CFaqTableItem__contents')

    category = categoryTag.text
    question = questionTag.text
    answer = answerTag.text

    contentList = []
    categoryDict = {}
    questionDict = {}
    answerDict = {}

    categoryDict['카테고리'] = category
    questionDict['질문'] = question
    answerDict['답변'] = answer

    contentList.append(categoryDict)
    contentList.append(questionDict)
    contentList.append(answerDict)
    # dictionary의 키는 변경 불가능한 값이어야 하기 때문에 questionDict을 str()로 감싸서 저장

    dataset[i+1] = contentList


json_string = json.dumps(dataset, ensure_ascii=False, indent=4)
print(json_string)
# pp = pprint.PrettyPrinter(indent=4, compact=True)   # 들여쓰기(indent) 설정
# pp.pprint(json_string)