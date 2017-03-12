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
 * An REST client object. {@link CzlClient} instances are heavyweight objects that should be created sparingly. A {@link CzlClient} object is
 * thread-safe and should be reused when targeting the same service endpoint.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CzlClient extends ApiClient {

  /**
   * Build a new client instance using all the settings specified by the given configuration object. {@link CzlClient} instances are heavyweight objects
   * that should be created sparingly. A {@link CzlClient} object is thread-safe and should be reused when targeting the same service endpoint.
   *
   * @param czlClientConfig a client configuration object
   * @return a new SDK client instance
   */
  public static CzlClient newClient(CzlClientConfig czlClientConfig) {
    return new CzlClient(czlClientConfig);
  }

  private CzlClient(CzlClientConfig czlClientConfig) {
    super(czlClientConfig);
  }


  /**
   * Access the API.
   *
   * @return an object describing the API.
   */
  public CzlApiV1 apiV1() {
    return new CzlApiV1(apiInvoker);
  }

}
