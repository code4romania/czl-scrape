import requests
from bs4 import BeautifulSoup as bs
import re
from unidecode import unidecode

r = requests.get('http://www.mmediu.gov.ro/articol/mm-supune-dezbaterii-publice-proiectul-de-hg-pentru-aprobarea-bugetului-de-venituri-si-cheltuieli-pe-anul-2017-al-fondului-pentru-mediu-si-al-administratiei-fondului-pentru-mediu/2145')
soup = bs(r.text, 'lxml')
article_paragraphs = soup.find('div', class_='text').find_all('p')
text = unidecode(article_paragraphs[3].text)

# print 'email: ' in unidecode(text)
# with open('test.txt','w') as f:
	# f.write(text)
email_regex = r"[eE]-*mail:* ([\w\.@]+)"
email_search = re.search(email_regex, text)
print '-----'
print email_search
# print '-----'
print email_search.groups()