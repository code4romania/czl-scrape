# Cod comun pentru scrapere Java
Modulul contine cod comun folosit de scraperele Java, inclusiv un client pentru API-ul de upload de date.


## Import in proiect
Adauga modulul in pom.xml:

```xml
<dependency>
    <groupId>ro.code4.czl</groupId>
    <artifactId>czl-scrape-commons</artifactId>
    <version>0.0.1-SNAPSHOT</version>
</dependency>
```

## Clientul pentru API
Libraria impinge date in API-ul CZL.

#### Initializare
Clasa `CzlClient` este clasa principala din librarie. Este thread-safe ; o instanta de client poate fi refolosita pentru apeluri multiple.

Inainte de a crea o instanta de client, trebuie construita o configuratie.

```java
    CzlClientConfig clientConfig = CzlClientConfig.builder()
        .endpointURI("http://czl-api.code4.ro/api/")
        .connectionRequestTimeout(500)
        .connectTimeout(500)
        .socketTimeout(3000)
        .authenticationStrategy(new TokenAuthenticationStrategy())
        .build();
```

O instanta de client se construieste folosind configuratia data:

```java
  CzlClient czlClient = CzlClient.newClient(clientConfig);
```

#### Cereri catre API
Parametrii obligatorii sunt necesari ca sa poti crea un obiect de tipul request. Parametrii optionali se pot pasa printr-un fluent builder.

```java
    PublicationRepresentation publication = PublicationRepresentationBuilder.aPublicationRepresentation()
                                                                                         .withIdentifier("1")
                                                                                         .withInstitution("finantepub")
                                                                                         .withType("HG")
                                                                                         .withDate("2017-03-08")
                                                                                         .build();
    czlClient.apiV1().createPublication(publication).execute();
```

#### Managementul conexiunilor
Libraria face managementul conexiunilor. Exista cateva setari care controleaza ciclul de viata al conexiunilor.

| Proprietate | Descriere |
|--------------|-------------|
| connectionTtl | Timpul de viata al tuturor conexiunilor create de un client. |
| maxConnectionCount | Numarul maxim de conexiuni create de un client. |
| socketTimeout | Socket timeout (`SO_TIMEOUT`) in milisecunde. Reprezinta perioada maxima de inactivitate intre doua pachete consecutive. O valoare de zero reprezinta valoarea infinit. O valoare negativa este interpretata ca o valoare nedefinita; in acest caz se foloseste valoarea default din sistem. |
| connectionRequestTimeout | Valoarea maxima de asteptare in milisecunde ca o conexiune sa se elibereze in managerul de conexiuni. O valoare de zero reprezinta valoarea infinit. O valoare negativa este interpretata ca o valoare nedefinita; in acest caz se foloseste valoarea default din sistem. |
| connectionTimeout | Valoarea maxima de asteptare in milisecunde ca o conexiune sa fie stabilita. O valoare de zero reprezinta valoarea infinit. O valoare negativa este interpretata ca o valoare nedefinita; in acest caz se foloseste valoarea default din sistem. |


#### Shutdown
Clasa `CzlClient` implementeaza `AutoCloseable`. Metoda `close()` e apelata automat la iesirea dintr-un bloc `try-with-resources`. Toate resursele consumate sunt eliberate in acest caz.

```java
    try (CzlClient czlClient = CzlClient.newClient(clientConfig)) {
      czlClient.apiV1().createPublication(PublicationRepresentationBuilder
                                             .aPublicationRepresentation()
                                             .withIdentifier("1")
                                             .withInstitution("finantepub")
                                             .withType("HG")
                                             .withDate("2017-03-08")
                                             .build())
          .execute();
    } catch (Exception e) {
      logger.error("Met an error.", e);
    }
```
