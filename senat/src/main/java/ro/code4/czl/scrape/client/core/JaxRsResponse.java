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
package ro.code4.czl.scrape.client.core;

import jersey.repackaged.com.google.common.collect.Maps;
import ro.code4.czl.scrape.client.Response;

import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Map;

/**
 * Wrapper over {@linkplain javax.ws.rs.core.Response} that provides a safe body deserialization mechanism along with some syntactic sugar.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
class JaxRsResponse<T> implements Response<T> {

  private final javax.ws.rs.core.Response originalResponse;
  private final Map<String, String> simplifiedHeaders;
  private final T entity;

  JaxRsResponse(javax.ws.rs.core.Response originalResponse, Class<T> expectedType) {
    this.originalResponse = originalResponse;
    this.entity = new JaxRsResponseDeserializationStrategy().read(originalResponse, expectedType);
    this.simplifiedHeaders = Collections.unmodifiableMap(
        Maps.transformEntries(originalResponse.getStringHeaders(), new StringListToStringEntryTransformer()));
  }

  @Override
  public int getStatusCode() {
    return originalResponse.getStatus();
  }

  @Override
  public T getEntity() {
    return entity;
  }

  @Override
  public String getContentType() {
    return originalResponse.getMediaType().toString();
  }

  @Override
  public long getContentLength() {
    return originalResponse.getLength();
  }

  @Override
  public String getETag() {
    return originalResponse.getEntityTag().getValue();
  }

  @Override
  public Date getDate() {
    return originalResponse.getDate();
  }

  @Override
  public String getHeaderString(String headerName) {
    return originalResponse.getHeaderString(headerName);
  }

  @Override
  public Map<String, String> getHeaders() {
    return simplifiedHeaders;
  }

  private static class StringListToStringEntryTransformer implements Maps.EntryTransformer<String, List<String>, String> {

    @Override
    public String transformEntry(String s, List<String> strings) {
      if (strings == null || strings.isEmpty()) {
        return null;
      }
      return strings.get(0);
    }
  }
}
