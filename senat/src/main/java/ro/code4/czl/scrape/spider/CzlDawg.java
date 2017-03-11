package ro.code4.czl.scrape.spider;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.code4.czl.scrape.client.CzlClient;
import ro.code4.czl.scrape.client.CzlClientConfig;
import ro.code4.czl.scrape.client.authentication.TokenAuthenticationStrategy;
import us.codecraft.webmagic.Spider;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CzlDawg {

  private static final Logger logger = LoggerFactory.getLogger(CzlDawg.class);

  public static void main(String[] args) {
    CzlClientConfig clientConfig = CzlClientConfig.builder()
        .endpointURI("http://czl-api.code4.ro/api/")
        .connectionRequestTimeout(500)
        .connectTimeout(500)
        .socketTimeout(3000)
        .authenticationStrategy(new TokenAuthenticationStrategy())
        .build();

    try (CzlClient czlClient = CzlClient.newClient(clientConfig)) {
      Spider.create(new CzlPageProcessor())
          .thread(3)
          .addUrl(args)
          .addPipeline(new CzlUploadPipeline(czlClient))
          .run();
    } catch (Exception e) {
      logger.error("Error caught while processing urls={}", args, e);
    }
  }

}
