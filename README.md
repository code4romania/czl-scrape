# Salut

Bine ai venit in repo-ul scrapeathon-ului CZL. Prima etapa a aplicatiei "Ce zice legea", un proiect Code for Romania care isi propune sa ofere urmarirea la zi a tuturor schimbarilor legislative din Romania.

Etapa consta in crearea unor mecanisme care sa preia informatii la un interval regulat din platformele institutiilor statului. Impreuna cu alinierea acestora in procesul legislativ putem prezenta informatiile necesare oricarui cetatean interesat de o anumita categorie de legi, sau mai multe.

## Unelte
Fiecare echipa este libera sa-si aleaga tehnologiile si approach-urile asupra scraper-ului. Dorim insa sa incurajam o aliniere a modelelor de date. Am creat un API valabil pe perioada evenimentului in care se poate face POST cu urmatoarele modele:

http://czl-api.code4.ro/publication

```
{
	id: "UNIX_TIME-lawproposal-slug"
    title: "Proiectul de ordin al ministrului justiției pentru aprobarea Regulamentului privind organizarea și desfășurarea activităților și programelor educative, de asistență psihologică și asistență socială din locurile de deținere aflate în subordinea Aministrației Naționale a Penitenciarelor" // titlul actului legislativ propus
    type: "HG", // HG, OUG, PROIECT, OG
    issuer: "MINISTERUL_CERCETARII", // platforma din care provine actul legislativ
    date: 1488990972814 // unix time
    description: "Cookie jelly-o sesame snaps donut sesame snaps sweet roll chocolate. Tootsie roll pie bonbon tart chocolate cake. Gummi bears gummies chupa chups ice cream croissant donut marzipan. Macaroon bear claw halvah carrot cake liquorice powder."
    feedback_days: 12, // numarul zilelor necesare pentru feedback
}
```

http://czl-api.code4.ro/document

```
{
    publication: "UNIX_TIME-lawproposal-slug",
    url: "http://www.just.ro/wp-content/uploads/2017/02/Proiect.docx" // da, este un link catre un document oficial de la MJ
}
```

## Duminica
Am vrea sa avem o baza de date populata cu tool-uri care pot fi rulate regulat pentru a identifica ulterior statusul oricarei propuneri legislative.



## Reguli
- code review in echipa ta
- documentatie + notat exceptii

## Alta intrebare?
Orice interbare are un raspuns la colegii cu stickere code4. Primesti si tu la finalul zilei.


