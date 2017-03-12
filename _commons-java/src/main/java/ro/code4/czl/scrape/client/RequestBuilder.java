/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
  *
  *    ADOBE CONFIDENTIAL
  *    ___________________
  *
  *    Copyright 2016 Adobe Systems Incorporated
  *    All Rights Reserved.
  *
  *    NOTICE:  All information contained herein is, and remains
  *    the property of Adobe Systems Incorporated and its suppliers,
  *    if any.  The intellectual and technical concepts contained
  *    herein are proprietary to Adobe Systems Incorporated and its
  *    suppliers and are protected by all applicable intellectual property
  *    laws, including trade secret and copyright laws.
  *    Dissemination of this information or reproduction of this material
  *    is strictly forbidden unless prior written permission is obtained
  *    from Adobe Systems Incorporated.
  *
  * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * **/
package ro.code4.czl.scrape.client;

/**
 * Contract for builders of {@linkplain Request} instances.
 *
 * @param <T> the request type
 * @param <U> the expected type of the response body
 * @author Ionut -Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public interface RequestBuilder<T extends Request<U>, U> {

  /**
   * Sets the <code>If-None-Match</code> header to the given value. Useful when making conditional requests.
   *
   * @param ifNoneMatch the value of the header.
   * @return the request builder.
   */
  RequestBuilder<T, U> ifNoneMatch(String ifNoneMatch);

  /**
   * Sets the <code>If-Match</code> header to the given value. Useful when making conditional requests.
   *
   * @param ifMatch the value of the header.
   * @return the request builder.
   */
  RequestBuilder<T, U> ifMatch(String ifMatch);

  /**
   * Make the request to only ask for headers. Only applies when the original request is using <code>GET</code>.
   *
   * @return the request builder.
   */
  RequestBuilder<T, U> headersOnly();

  /**
   * Enables or disables following redirects.
   *
   * @param followRedirects set to <code>true</code> to enable following redirects, otherwise to <code>false</code>.
   * @return the request builder.
   */
  RequestBuilder<T, U> followRedirects(boolean followRedirects);

  /**
   * Use the given credential for this request.
   *
   * @param credential the credential to use for this request.
   * @return the request builder.
   */
  RequestBuilder<T, U> credential(Credential credential);

  /**
   * Adds a custom header to this request.
   *
   * @param headerName  the header name for this request.
   * @param headerValue the header value for this request.
   * @return the request builder.
   */
  RequestBuilder<T, U> header(String headerName, String headerValue);

  /**
   * Build the request. Does not execute it.
   *
   * @return the request.
   */
  T build();

  /**
   * Builds and executes the request.
   *
   * @return the result of the execution of the request.
   */
  Response<U> execute();

}
