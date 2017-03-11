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

/**
 * Contract for an ro.code4.czl.scrape.client.authentication strategy.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public interface AuthenticationStrategy {

  /**
   * Processes the request with the goal of applying the ro.code4.czl.scrape.client.authentication strategy. This is called before the request is executed.
   *
   * @param request the request.
   * @param <T>     the expected type of the response body
   */
  <T> void process(Request<T> request);

}
