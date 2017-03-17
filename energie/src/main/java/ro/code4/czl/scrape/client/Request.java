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

import java.util.Map;

/**
 * Contract for a request made by the client.
 *
 * @param <T> the expected type of the response body
 * @author Ionut -Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public interface Request<T> {

  /**
   * Executes the request and returns the response.
   *
   * @return the result of the execution. If the response contains a body, it will be automatically deserialized and ready for use.
   */
  Response<T> execute();

  /**
   * Returns the type of response body, if any; <code>null</code> otherwise.
   *
   * @return the response type
   */
  Class<T> getResponseType();

  /**
   * Returns the absolute path of the target of this request.
   *
   * @return the absolute path.
   */
  String getPath();

  /**
   * Returns the HTTP method used by this request.
   *
   * @return the method.
   */
  String getMethod();

  /**
   * Returns the path parameters used by this request.
   *
   * @return the path parameters.
   */
  Map<String, Object> getPathParams();

  /**
   * Returns the query parameters used by this request.
   *
   * @return the query parameters.
   */
  Map<String, String> getQueryParams();

  /**
   * Returns the matrix parameters used by this request.
   *
   * @return the matrix parameters.
   */
  Map<String, String> getMatrixParams();

  /**
   * Returns the header parameters used by this request.
   *
   * @return the header parameters.
   */
  Map<String, String> getHeaderParams();

  /**
   * Returns the body used by this request, if any.
   *
   * @return the body if one has been specified, <code>null</code> otherwise.
   */
  Object getBody();

  /**
   * Returns the value of the <code>Accept</code> used by this request.
   *
   * @return the value of the <code>Accept</code> header.
   */
  String getAcceptHeader();

  /**
   * Indicates whether this request is supposed to follow redirects or not.
   *
   * @return <code>true</code> if the request is supposed to follow redirects, <code>false</code> otherwise.
   */
  Boolean isFollowRedirectsEnabled();

  /**
   * Returns the value of the credential used by this request.
   *
   * @return the credential, if any.
   */
  Credential getCredential();
}
