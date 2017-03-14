# Ministerul Apărării Naţionale
Sursa documente: http://dlaj.mapn.ro/
## Tehnologie
*PHP* - Script simplu old-school
## Instructiuni
Nu are instructiuni speciale. 

Tokenul va fi transmis ca argument:
```bash
$ php mapn_plugin.php TOKEN
```
## Exceptii
Din cauza faptului ca pagina html nu e consistenta, au fost folosite RegExuri pentru a lua informatiile. 

O problema a constat in faptul ca o intrare este constituita pe site-ul acesta din 2 elemente practic, mai exact
titlul proiectului si documentele aferente, dar ele nu pot fi legate una de cealalta logic. De aceea, scriptul
va functiona doar in cazul in care gaseste acelasi numar de titluri si grupuri de documente.

Scriptul va intoarce <b>false</b> in urmatoarele situatii:
* pagina este down
* unul din elementele cheie de content este schimbat (titlurile nu mai au *, calea spre documente este schimbata)
* numarul de titluri si numarul de grupuri de documente nu este acelasi 