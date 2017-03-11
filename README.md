# Salut

Bine ai venit in repo-ul scrapeathon-ului CZL. Prima etapa a aplicatiei "Ce zice legea", un proiect Code for Romania care isi propune sa ofere urmarirea la zi a tuturor schimbarilor legislative din Romania.

Etapa consta in crearea unor mecanisme care sa preia informatii la un interval regulat din platformele institutiilor statului. Impreuna cu alinierea acestora in procesul legislativ putem prezenta informatiile necesare oricarui cetatean interesat de o anumita categorie de legi, sau mai multe.

## Unelte
Fiecare echipa este libera sa-si aleaga tehnologiile si approach-urile asupra scraper-ului. Dorim insa sa incurajam o aliniere a modelelor de date. Am creat un API valabil pe perioada evenimentului in care se poate face POST cu urmatoarele modele:

http://czl-api.code4.ro/api/publications/

```js
{
  "identifier": "lawproposal-first-document-name-slug-or-something", // un identificator unic, predictibil (repetabil), pereferabil human-readable
  "title": "Proiectul de ordin al ministrului justiției pentru aprobarea Regulamentului privind organizarea și desfășurarea activităților și programelor educative, de asistență psihologică și asistență socială din locurile de deținere aflate în subordinea Aministrației Naționale a Penitenciarelor", // titlul actului legislativ propus
  "type": "HG", // HG, OUG, LEGE, OG, OM
  "institution": "justitie", // ID-ul platformei din care provine actul legislativ
  "date": "2017-03-08", // ISO 8601
  "description": "Cookie jelly-o sesame snaps donut sesame snaps sweet roll chocolate. Tootsie roll pie bonbon tart chocolate cake. Gummi bears gummies chupa chups ice cream croissant donut marzipan. Macaroon bear claw halvah carrot cake liquorice powder.",
  "feedback_days": 12, // numarul zilelor disponibile pentru feedback
  "contact": {"tel": "12345", "email": "feedback@example.org"}, // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr"
  "documents": [ // array de dictionare
    {
      "type": "anexa", // free text momentan
      "url": "http://www.just.ro/wp-content/uploads/2017/02/Proiect.docx" // da, este un link catre un document oficial de la MJ
    }
  ]
}
```

POST-ul catre API va fi autentificat cu o cheie-token, trimisa cu un header HTTP `Authorization`. Cheia va primi ca prefix string-ul literal "Token", de care este separata printr-un spatiu:

```
Authorization: Token am-un-token-si-fac-ce-vreau-cu-el
```
*Token-urile vor fi distribuite pe parcursul evenimentului. API-ul este hostat pe AWS, va rugam sa nu le distribuiti in afara echipei in care lucrati.*

## Instituții publice
Institutiile de la care vom trage datele necesare dezvoltarii aplicatiei le gasesti in tabelul de mai jos si in [endpoint-ul de aici](http://czl-api.code4.ro/api/institutions/). Iti recomandam sa-l folosesti, are cateva informatii in plus pentru mentinerea standardelor in date.

Nume|URL
-----|-----
Ministerul Justiţiei|http://www.just.ro/transparenta-decizionala/acte-normative/proiecte-in-dezbatere/
Ministerul Sănătăţii|http://www.ms.ro/acte-normative-in-transparenta/
Ministerul Comunicaţiilor şi pentru Societatea Informaţională|https://www.comunicatii.gov.ro/?page_id=3517
Ministerul Apelor și Pădurilor|http://apepaduri.gov.ro/proiecte-de-acte-normative/
Ministerul Afacerilor Externe|http://www.mae.ro/node/2011
Ministerul Afacerilor Interne|http://www.mai.gov.ro/index05_1.html
Ministerul Agriculturii Şi Dezvoltării Rurale|http://www.madr.gov.ro/transparenta-decizionala/proiecte-de-acte-normative.html
Ministerul Apărării Naţionale|http://dlaj.mapn.ro
Ministerul Culturii|http://www.cultura.ro/proiecte-acte-normative
Ministerul Dezvoltării Regionale, Administrației Publice și Fondurilor Europene|http://www.mdrap.gov.ro/transparenta/consultari-publice
Ministerul pentru Mediul de Afaceri, Comerț și Antreprenoriat|http://www.antreprenoriat.gov.ro/categorie/transparenta-decizionala/proiecte-in-dezbatere-publica/
Ministerul Economiei, Comerțului și Relațiilor cu Mediul de Afaceri|http://economie.gov.ro/transparenta-decizionala/proiecte-in-dezbatere-publica
Ministerul Energiei|http://energie.gov.ro/transparenta-si-integritate/transparenta-decizionala-2/
Ministerul Educaţiei Naţionale și Cercetării Științifice|http://www.edu.ro/proiecte-acte-normative-0
Ministerul Finanţelor Publice|http://www.mfinante.gov.ro/transparent.html?method=transparenta&pagina=acasa&locale=ro
Ministerul Mediului|http://www.mmediu.gov.ro/categorie/proiecte-de-acte-normative/41
Ministerul Muncii, Familiei, Protecţiei Sociale și Persoanelor Vârstnice|http://www.mmuncii.ro/j33/index.php/ro/transparenta/proiecte-in-dezbatere
Ministerul Tineretului și Sportului|http://mts.ro/proiecte-legislative-in-dezbatere-publica/
Ministerul Transporturilor|http://mt.gov.ro/web14/transparenta-decizionala/consultare-publica/acte-normative-in-avizare
Ministerul Turismului|http://turism.gov.ro/transparenta-decizionala-2/
Ministerul Consultărilor Publice și Dialogului Social|http://dialogsocial.gov.ro/categorie/proiecte-de-acte-normative/
Ministerul pentru Relaţia cu Parlamentul|http://mrp.gov.ro/web/category/consultare-publica/?future=false
Ministerul pentru Românii de Pretutindeni|http://www.dprp.gov.ro/documente-in-consultare-publica/
Ministerul Cercetării și Inovării|http://www.research.gov.ro/ro/articol/1029/despre-ancs-legislatie-proiecte-de-acte-normative
Secretariatul General al Guvernului |http://www.sgg.ro/legislativ/
Camera Deputatilor|www.cdep.ro/pls/proiecte/upl_pck.home
Senatul|https://www.senat.ro/LegiProiect.aspx
Presedintia|http://www.presidency.ro/ro/presedinte/decrete-si-acte-oficiale

## Duminica
Am vrea sa avem o baza de date populata cu tool-uri care pot fi rulate regulat pentru a identifica ulterior statusul oricarei propuneri legislative.


## Reguli
- code review in echipa ta
- documentatie + notat exceptii

## Alta intrebare?
Orice intrebare are un raspuns la colegii cu stickere code4. Primesti si tu la finalul zilei.


