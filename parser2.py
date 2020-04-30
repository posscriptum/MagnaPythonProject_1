import requests
from bs4 import BeautifulSoup
import array
from funSQLQuery import mysqlquery

url = 'http://192.168.99.55/awp/index/index.html'

page = requests.get(url)

# print(page.status_code)

soup = BeautifulSoup(page.text, "html.parser")

table = soup.find('table')

table_rows = table.find_all('tr')

tr_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
i = 0
for tr in table_rows:
    td = tr.find_all('td')
    tr_data[i] = td[1].text
    i = i + 1
    print(tr_data)

tr_columns = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
i = 0
for tr in table_rows:
    td = tr.find_all('td')
    tr_columns[i] = td[0].text
    i = i + 1
    print(tr_columns[0])



if   tr_data[1] > '0':
        mysqlquery(tr_data[0], tr_data[4], tr_data[5],
                    tr_data[6], tr_data[7], tr_data[8],
                    tr_data[9], tr_data[2], tr_data[3])


