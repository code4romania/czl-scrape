# Ministerul Culturii si Identitatii Nationale
http://www.cultura.ro/proiecte-acte-normative

## Tehnologie
* [Java 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
* [Maven 3](http://maven.apache.org/download.html)
* [Webmagic](https://github.com/code4craft/webmagic) pentru crawling
* [Jsoup](https://jsoup.org/) pentru parsing de HTML

## Instructiuni
Build & executie:

```bash
$ mvn clean package
$ java -Dczl.scrape.token=<token> -jar target/czl-scrape-cultura.jar http://www.cultura.ro/proiecte-acte-normative
```

Logurile sunt scrise in `stdout` si in fisierul `scraper-cultura.log`.
