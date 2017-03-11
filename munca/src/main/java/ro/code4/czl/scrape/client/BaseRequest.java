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

import javax.ws.rs.HttpMethod;
import javax.ws.rs.core.HttpHeaders;
import java.util.HashMap;
import java.util.Map;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public abstract class BaseRequest<T> implements Request<T> {

  private final ApiInvoker apiInvoker;

  private String path;
  private String method;
  private Map<String, Object> pathParams = new HashMap<>();
  private Map<String, String> queryParams = new HashMap<>();
  private Map<String, String> matrixParams = new HashMap<>();
  private Map<String, String> headerParams = new HashMap<>();
  private Object body;
  private String accept;
  private Boolean followRedirectsEnabled;
  private Credential credential;

  public BaseRequest(BaseRequestBuilder<?, ?> builder, String url, String method, String accept, ApiInvoker apiInvoker) {
    this.apiInvoker = apiInvoker;
    this.path = url;
    this.method = method;
    this.accept = accept;

    // HEAD instead of GET ?
    if (builder.head && method.equals(HttpMethod.GET)) {
      this.method = HttpMethod.HEAD;
    }

    // caching
    setHeaderParam(HttpHeaders.IF_NONE_MATCH, builder.ifNoneMatch);
    setHeaderParam(HttpHeaders.IF_MATCH, builder.ifMatch);

    // custom headers
    for (Map.Entry<String, String> customHeaderParam : builder.customHeaders.entrySet()) {
      if (customHeaderParam.getValue() != null) {
        setHeaderParam(customHeaderParam.getKey(), customHeaderParam.getValue());
      }
    }

    if (builder.followRedirects != null) {
      this.followRedirectsEnabled = builder.followRedirects;
    }

    this.credential = builder.credential;
  }

  @Override
  public Response<T> execute() {
    return apiInvoker.invokeAPI(this);
  }

  @Override
  public String getPath() {
    return path;
  }

  @Override
  public String getMethod() {
    return method;
  }

  @Override
  public Map<String, Object> getPathParams() {
    return pathParams;
  }

  @Override
  public Map<String, String> getQueryParams() {
    return queryParams;
  }

  @Override
  public Map<String, String> getMatrixParams() {
    return matrixParams;
  }

  @Override
  public Map<String, String> getHeaderParams() {
    return headerParams;
  }

  @Override
  public Object getBody() {
    return body;
  }

  @Override
  public String getAcceptHeader() {
    return accept;
  }

  @Override
  public Boolean isFollowRedirectsEnabled() {
    return followRedirectsEnabled;
  }

  @Override
  public Credential getCredential() {
    return credential;
  }

  protected void setPathParam(String parameterName, String parameterValue) {
    this.pathParams.put(parameterName, parameterValue);
  }

  protected void setQueryParam(String parameterName, String parameterValue) {
    this.queryParams.put(parameterName, parameterValue);
  }

  protected void setQueryParam(String parameterName, Integer parameterValue) {
    this.queryParams.put(parameterName, parameterValue.toString());
  }

  protected void setMatrixParam(String parameterName, String parameterValue) {
    this.matrixParams.put(parameterName, parameterValue);
  }

  protected void setHeaderParam(String parameterName, String parameterValue) {
    this.headerParams.put(parameterName, parameterValue);
  }

  protected void setBody(Object body) {
    this.body = body;
  }

}
