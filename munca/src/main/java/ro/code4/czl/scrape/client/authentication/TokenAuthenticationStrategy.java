package ro.code4.czl.scrape.client.authentication;

import ro.code4.czl.scrape.client.AuthenticationStrategy;
import ro.code4.czl.scrape.client.Request;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class TokenAuthenticationStrategy implements AuthenticationStrategy {

  private final String tokenValue = System.getProperty("czl.scrape.token");

  @Override
  public <T> void process(Request<T> request) {
    request.getHeaderParams().put("Authorization", "Token " + tokenValue);
  }
}
