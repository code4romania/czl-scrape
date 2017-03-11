import requests


item = {'contact': {'addr': u'Apolodor, nr. 17, sector 5',
             'email': u'iulia.matei@mdrap.ro',
             'fax': u'0372.114.569.'},
 'date': u'22-02-2017',
 'description': u'\xcen temeiul art. 7 din Legea nr. 52/2003 privind transparen\u0163a decizional\u0103 \xeen administra\u0163ia public\u0103, republicat\u0103, Ministerul Dezvolt\u0103rii Regionale, Administra\u0163iei Publice si Fondurilor Europene aduce la cuno\u015ftin\u0163a publicului textul urm\u0103torului proiect de act normativ \u2013 Ordin al viceprim-ministrului, ministrul dezvolt\u0103rii regionale, administra\u0163iei publice \u0219i fondurilor europene pentru aplicarea prevederilor art. III, alin. (11) din Ordonan\u0163a de urgen\u0163\u0103 a Guvernului nr. 63/2010 pentru modificarea \u015fi completarea Legii nr. 273/2006 privind finan\u0163ele publice locale, precum \u015fi pentru stabilirea unor m\u0103suri financiare.',
 'documents': [{'type': u'Referat de aprobare',
                'url': '/userfiles/referat_ordin_oug63.doc'}],
 'feedback_days': u'10',
 'identifier': u'proiect-de-omdrapfe-pentru-aplicarea-prevederilor-art-iii-alin-11-din-ordonanta-de-urgenta-a-guvernului-nr-632010-pentru-modificarea-si-completarea-legii-nr-2732006-privind-finantele-publice-locale-precum-si-pentru-stabilirea-unor-masuri-financiare-22-02-2017',
 'institution': 'dezvoltare',
 'title': u'Proiect de OMDRAPFE pentru  aplicarea prevederilor art. III, alin. (11) din Ordonan\u0163a de urgen\u0163\u0103 a  Guvernului nr. 63/2010 pentru modificarea \u015fi completarea Legii nr.  273/2006 privind finan\u0163ele publice locale, precum \u015fi pentru stabilirea  unor m\u0103suri financiare ',
 'type': 'OMDRAPFE'}

r = requests.post('http://czl-api.code4.ro/api/publications/', headers={'Authorization': 'Token dezvoltare-very-secret-token'}, data=item)
