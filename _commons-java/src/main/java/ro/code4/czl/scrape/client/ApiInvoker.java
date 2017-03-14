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
 * Basic API invoker contract.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public interface ApiInvoker extends AutoCloseable {

  /**
   * Configures a request header that should be added to every request made via this API invoker.
   *
   * @param key   request header name
   * @param value request header value
   */
  void addDefaultHeader(String key, String value);

  /**
   * Executes a request.
   *
   * @param request the request to execute
   * @param <T>     the type that the response should be deserialized into
   * @return a {@link Response} instance containing the response body deserialized into the desired type
   */
  <T> Response<T> invokeAPI(Request<T> request);

  /**
   * Shuts down the connection manager used by this API invoker and releases allocated resources. This includes closing all connections, whether they
   * are currently used or not.
   */
  void shutdown();
}
