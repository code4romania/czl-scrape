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

import java.util.Date;
import java.util.Map;

/**
 * Contract for a response to a request made by the client.
 *
 * @param <T> the expected type of the response body
 * @author Ionut -Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public interface Response<T> {

  /**
   * Returns the status code of the response.
   *
   * @return the status code.
   */
  int getStatusCode();

  /**
   * Returns the entity in the response.
   *
   * @return the entity.
   */
  T getEntity();

  /**
   * Returns the content type of the response.
   *
   * @return the content type.
   */
  String getContentType();

  /**
   * Returns the content length of the response.
   *
   * @return the content length.
   */
  long getContentLength();

  /**
   * Returns the <code>ETag</code> header value, if any.
   *
   * @return the <code>ETag</code> header value.
   */
  String getETag();

  /**
   * Returns the date of the response.
   *
   * @return the date.
   */
  Date getDate();

  /**
   * Returns the value of a given response header.
   *
   * @param headerName the header name.
   * @return the header value.
   */
  String getHeaderString(String headerName);

  /**
   * Returns all the response headers.
   *
   * @return the response headers.
   */
  Map<String, String> getHeaders();
}
