package ro.code4.czl.scrape.client;/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
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

import ro.code4.czl.scrape.client.core.JerseyClientApiInvoker;

/**
 * {@link ApiClient} instances are heavyweight objects that should be created sparingly. A {@link ApiClient} object is
 * thread-safe and should be reused when targeting the same service endpoint.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public abstract class ApiClient implements AutoCloseable {

  protected final ApiInvoker apiInvoker;

  /**
   * Creates a new client instance using all the settings specified by the given configuration object.
   *
   * @param config a client configuration object
   */
  protected ApiClient(CzlClientConfig config) {
    this(config, new JerseyClientApiInvoker(config));
  }

  /**
   * Creates a new client instance using all the settings specified by the given configuration object and a custom {@link ApiInvoker} instance.
   *
   * @param config     a client configuration object
   * @param apiInvoker a custom API invoker object
   */
  private ApiClient(CzlClientConfig config, ApiInvoker apiInvoker) {
    this.apiInvoker = apiInvoker;
  }

  /**
   * Retrieves the API invoker object used by this client.
   *
   * @return a {@link ApiInvoker} instance
   */
  public ApiInvoker getApiInvoker() {
    return apiInvoker;
  }

  @Override
  public void close() throws Exception {
    this.shutdown();
  }

  /**
   * Shuts down the connection manager used by this client and releases allocated resources. This includes closing all connections, whether they are
   * currently used or not.
   */
  private void shutdown() {
    apiInvoker.shutdown();
  }
}
