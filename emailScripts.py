import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

instructors = pd.read_csv('no_emails')

instructor_list = instructors.instructor.to_list()

email_list = []
others = []
no_mail = []
for x in range(0, len(instructor_list)):
    if len(instructor_list[x].split(' ')) > 2:
        others.append(instructor_list[x])
    email_list.append('N/A')


failed = False

for i, name in enumerate(instructor_list):
    namelist = name.split(' ')

    hrefs = ['nothing in here', 'N/A']

    url = 'https://www.sjsuone.sjsu.edu/sjsuPhoneBook/SearchResults.aspx?firstname=' + \
        namelist[0]+'|StartsWith&'+'lastname='+namelist[1]+'|StartsWith'
    # print(full_name)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    result_count = soup.find(id='BodyPlaceHolder_lblDisplayRecs')
    counts = result_count.text[0]

    if counts == '0':
        url = 'https://www.sjsuone.sjsu.edu/sjsuPhoneBook/SearchResults.aspx?firstname=' + \
            namelist[0]+'+'+namelist[1]+'|StartsWith&' + \
            'lastname='+namelist[-1]+'|Contains'

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        result_count = soup.find(id='BodyPlaceHolder_lblDisplayRecs')
        counts = result_count.text[0]

    hrefs = soup.find_all('a', string=lambda text: namelist[0].lower() in str(
        text).lower() and namelist[-1].lower() in str(text).lower())

    if len(hrefs) == 0:
        # failed = True
        # print(counts)
        no_mail.append(name)
        print('failed at', name)
        continue

    if len(hrefs) == 1:
        nextEmail = hrefs[0].findNext('a')
        hrefs.append(nextEmail)

    print(hrefs[1].text)
    email_list[i] = hrefs[1].text

if not failed:
    finalized = pd.DataFrame(columns=['instructor', 'instructorEmail'])

    finalized.instructor = instructor_list
    finalized.instructorEmail = email_list

    finalized.to_csv('newMails', index=False)
    print(no_mail)
