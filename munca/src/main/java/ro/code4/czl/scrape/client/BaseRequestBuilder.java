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

import java.util.HashMap;
import java.util.Map;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public abstract class BaseRequestBuilder<T extends Request<U>, U> implements RequestBuilder<T, U> {

  String ifNoneMatch;
  String ifMatch;
  Map<String, String> customHeaders = new HashMap<>();
  boolean head;
  Boolean followRedirects;
  Credential credential;

  @Override
  public RequestBuilder<T, U> ifNoneMatch(String ifNoneMatch) {
    this.ifNoneMatch = ifNoneMatch;
    return this;
  }

  @Override
  public RequestBuilder<T, U> ifMatch(String ifMatch) {
    this.ifMatch = ifMatch;
    return this;
  }

  @Override
  public RequestBuilder<T, U> headersOnly() {
    this.head = true;
    return this;
  }

  @Override
  public RequestBuilder<T, U> followRedirects(boolean followRedirects) {
    this.followRedirects = followRedirects;
    return this;
  }

  @Override
  public RequestBuilder<T, U> credential(Credential credential) {
    this.credential = credential;
    return this;
  }

  @Override
  public RequestBuilder<T, U> header(String headerName, String headerValue) {
    this.customHeaders.put(headerName, headerValue);
    return this;
  }

  @Override
  public Response<U> execute() {
    return build().execute();
  }
}
