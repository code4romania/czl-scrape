import re

mapping = {
	'hg': 'HG',
	'lege': 'LEGE',
	'ordin': 'ORDIN',
	'omdrapfe': 'OMDRAPFE',
	'hotarare a guvernului': 'HG'
}
pp = [
'PROIET HG',
'PROIECT HG',
'PROIECT HG',
'Proiect de Hotarare a Guvernului',
'Proiect de Lege',
'Proiect de HG privind aprobarea stemei comunei Magura Ilvei, judetul Bistrita-Nasaud',
'PROIECT HG',
'Proiect de LEGE',
'Proiect  de Hotarare  a Guvernului',
'Proiect de ORDIN',
'Proiect de Hotarare a Guvernului',
'Proiect de OMDRAPFE',
'Proiect de LEGE',
'Proiect de OMDRAPFE',
'Proiect de LEGE',
'Proiect de Hotarare  a Guvernului',
]

regex = r'HG|Lege|ORDIN|OMDRAPFE|HotarAre a guvernului'

for p in pp:
	# print p
	m = re.search(regex, p.replace('  ',' '), re.IGNORECASE)
	print p, mapping[m.group().lower()]