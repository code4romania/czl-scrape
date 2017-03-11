# Page:

[http://www.just.ro/transparenta-decizionala/acte-normative/proiecte-in-dezbatere/?lcp_page0=](http://www.just.ro/transparenta-decizionala/acte-normative/proiecte-in-dezbatere/?lcp_page0=)<page>  
page: start at 1  

## Page links:

**Selector().xpath: //ul[@class="lcp_paginator"]/li**  

## Publication:

 # fully qualified, not approved by the scraping gods:  
**Selector().css('#content div.entry-content ul.lcp_catlist li')**  

Proposed, simplified:  
**Selector().css('#content .entry-content .lcp_catlist li')**  

### Identifier

Proposale  
- title - sanitized (URL-escaped?) // a nu se   

## Title

Full path: h3.lcp_post  
not sure: .lcp_post or h3 or both?  

### Type

HG, OG, OUG, PROIECT  

Notes:  

*   case-insesitive search :)
*   diacritice-insensitive search
*   pare că înainte de primul ("pentru" sau "privind") e ce ne trebuie nouă

*   Tricky stuff: proiectele astea pot modifica alte legi/hotărâri etc. Deci trebuie să avem grijă la cum ne bazăm pe cuvintele cheie.
*   contraexemplu: ANUNŢ privind Ordinul ministrului justiţiei pentru completarea Normelor privind tarifele de onorarii pentru serviciile prestate de notarii publici, aprobate prin Ordinul ministrului justiţiei nr. 46/C/2011, aprobat în data de 29.09.2016

Exemple:  
HG:  

*   Proiectul de Hotărâre a Guvernului privind unele măsuri pentru organizarea și desfășurarea Adunării Generale a Confederației Europene de Probațiune și  a Conferinței Alternative la detenție, la București, în perioada 5 – 7 octombrie 2016
*   Proiectul de Hotărâre a Guvernului pentru aprobarea Regulamentului privind distribuirea sumelor prevăzute la art. 37 din Legea nr. 318/2015 pentru înființarea, organizarea şi funcționarea Agenției Naționale de Administrare a Bunurilor Indisponibilizate şi pentru modificarea şi completarea unor acte normative
*   Proiectul de hotărâre a Guvernului pentru aprobarea cuantumului și a plății cotizației anuale de participare a României la Conferința de la Haga de Drept Internațional Privat, pentru anul financiar 1 iulie 2016-30 iunie 2017
*   Proiect de hotărâre privind înfiinţarea, organizarea şi funcționarea Institutului Național de Criminologie, precum și pentru modificarea Hotărârii Guvernului nr. 652/2009 privind organizarea și funcționarea Ministerului Justiției

LEGE: (= proiect de lege)  

*   Proiectul de Lege pentru modificarea și completarea Legii nr. 302/2004 privind cooperarea judiciară internațională în materie penală, republicată, cu modificările și completările ulterioare
*   Proiectul de Lege pentru modificarea și completarea O.G. nr. 89/2000 privind unele măsuri pentru autorizarea operatorilor și efectuarea înscrierilor în Arhiva Electronică de Garanții Reale Mobiliare și a Legii nr. 71/2011 pentru punerea în aplicare a Legii nr. 287/2009 privind Codul civil
*   Proiectul de lege pentru modificarea și completarea Legii nr. 302/2004 privind cooperarea judiciară internațională în materie penală, republicată, cu modificările și completările ulterioare
*   Proiectul Legii pentru ratificarea celui de-al treilea Protocol adițional la Convenția Europeană privind Extrădarea, deschis spre semnare la Strasbourg  la 10 noiembrie 2010 și semnat de România la Viena la 20 septembrie 2012

OUG  

*   Proiectul Ordonanței de urgență pentru modificarea și completarea Codului Penal și a Codului de Procedură Penală

OM (Ordin de ministru):   

*   Proiectul de ordin al ministrului justiției privind modificarea Ordinului Ministrului Justiţiei nr. 2412/C din 12 august 2013 pentru aprobarea Metodologiei de organizare şi desfăşurare a concursului de admitere în Şcoala Naţională de Pregătire a Agenţilor de Penitenciare Târgu Ocna şi a Metodologiei de organizare şi desfăşurare a examenului de absolvire a cursurilor cu durata de un an la Şcoala Naţională de Pregătire a Agenţilor de Penitenciare Târgu Ocna, însoțit de referatul de aprobare
*   Proiectul de Ordin al ministrului justiției pentru aprobarea normelor privind asigurarea gratuită de către administrația locului de deținere a unui număr de ziare sau publicații
*   Proiectul de ordin privind stabilirea condițiilor în care poate fi valorificat, pe piața liberă, excedentul de produse realizat în gospodăriile agrozootehnice, precum și referatul de aprobare.

Others:  

*   Dezbatere publică privind proiectul de Ordonanță de urgență a Guvernului pentru modificarea și completarea Codului Penal și a Codului de Procedură Penală și proiectul de Ordonanță de urgență a Guvernului privind grațierea unor pedepse.
*   Regulamentului de organizare și desfășurare a concursului pentru ocuparea funcțiilor vacante de inspector de urmărire și administrare bunuri

### Date

e textul li-ului (turnat direct), în română (:first-node)  
exemple  

*   5 septembrie 2016
*   19 septembrie 2016

**xpath: text()[1]**  

### Description

Proposal: tot ce-i în element - date - documents  

### Feedback_days

poate apărea ceva gen  
"Propunerile, sugestiile şi opiniile cu valoare de recomandare referitoare la proiectul de act normativ supus dezbaterii pot fi transmise în scris, până la data de 7.10.2016" (edited)  
Nu avem default  

### Contact

#### Email

Dacă există, pare a fi un `<p>` care are un `<a href='mailto:..'` (care ar putea să conțină  un <em> .. </em>` cu emailul duplicat). Și ar trebui sanitizat (am găsit emailul “dean@just.ro.”)   

#### Fax

Free text  
exemple:  
pe fax, la nr. 037 204 1196  
pe fax la nr. 037.204.10.61  

### Documents

Dacă există un <p> care conține unul sau mai multe <a>-uri, separate de “ | "
