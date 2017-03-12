package ro.code4.czl.scrape.client.samples;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.code4.czl.scrape.client.CzlClient;
import ro.code4.czl.scrape.client.CzlClientConfig;
import ro.code4.czl.scrape.client.authentication.TokenAuthenticationStrategy;
import ro.code4.czl.scrape.client.representation.PublicationRepresentation.PublicationRepresentationBuilder;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CzlClientSample {

  private static final Logger logger = LoggerFactory.getLogger(CzlClientSample.class);

  public static void main(String[] args) {

    CzlClientConfig clientConfig = CzlClientConfig.builder()
        .endpointURI("http://czl-api.code4.ro/api/")
        .connectionRequestTimeout(500)
        .connectTimeout(500)
        .socketTimeout(3000)
        .authenticationStrategy(new TokenAuthenticationStrategy())
        .build();

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
  }
}
