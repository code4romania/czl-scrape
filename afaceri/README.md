# Ministerul pentru Mediul de Afaceri, Comerț și Antreprenoriat

Surse de documente este http://www.antreprenoriat.gov.ro/categorie/transparenta-decizionala/proiecte-in-dezbatere-publica/ .

### Tehnologie
*NodeJS* - serverul se conecteaza la URL-ul setat in fisierul din config, descarca fisierele PDF, parseaza continutul lor, trimite obiectele generate la API si sterge fisierele PDF de pe disc.

### Instructiuni
Token-ul de autentificare la API trebuie setat in fisierul *config.json*.

Continutul PDF-urilor se proceseaza in paragrafe. Serverul obtine datele necesare din paragraful relevant. Paragraful relevant reprezinta primul paragraf cu un numar total mai mare de 8 cuvinte si 50 de litere (configurabil in *config.json*)
```
npm install
node server/server.js
```

### Exceptii
Datele documentelor nu exista intr-un format standardizat. Date interpretabile exista in URL-urile fisierelor si in numele acestora.

La fiecare rulare a server-ului, sunt (re)procesate fisierele din URL-ul principal.
