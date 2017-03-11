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

import org.apache.http.client.config.RequestConfig;
import org.apache.http.config.SocketConfig;
import org.apache.http.impl.conn.PoolingHttpClientConnectionManager;
import org.glassfish.jersey.apache.connector.ApacheClientProperties;
import org.glassfish.jersey.apache.connector.ApacheConnectorProvider;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.client.ClientProperties;
import org.glassfish.jersey.jackson.JacksonFeature;

import ro.code4.czl.scrape.client.ApiInvoker;
import ro.code4.czl.scrape.client.CzlClientConfig;
import ro.code4.czl.scrape.client.Request;
import ro.code4.czl.scrape.client.Response;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import javax.ws.rs.HttpMethod;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.Invocation;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;

/**
 * Implementation of {@linkplain ApiInvoker} using Jersey 2.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class JerseyClientApiInvoker implements ApiInvoker {

  private final Map<String, String> defaultHeaderMap;
  private final WebTarget webTarget;
  private final CzlClientConfig czlClientConfig;
  private PoolingHttpClientConnectionManager connectionManager;

  public JerseyClientApiInvoker(CzlClientConfig czlClientConfig) {
    this.webTarget = initializeTarget(czlClientConfig);
    this.czlClientConfig = czlClientConfig;
    this.defaultHeaderMap = new HashMap<>();
  }

  @Override
  public <T> Response<T> invokeAPI(Request<T> request) {
    if (czlClientConfig.getAuthenticationStrategy() != null) {
      czlClientConfig.getAuthenticationStrategy().process(request);
    }

    return this.invokeAPI(request.getPath(), request.getMethod(),
                          request.getPathParams(), request.getQueryParams(), request.getMatrixParams(), request.getHeaderParams(),
                          request.getMethod().equals(HttpMethod.OPTIONS) ? null : request.getBody(), request.getAcceptHeader(),
                          request.getBody() == null ? null : MediaType.APPLICATION_JSON,
                          request.getResponseType(),
                          request.isFollowRedirectsEnabled());
  }

  @Override
  public void addDefaultHeader(String key, String value) {
    defaultHeaderMap.put(key, value);
  }

  @Override
  public void shutdown() {
    if (connectionManager != null) {
      connectionManager.shutdown();
      IdleConnectionMonitor.removeConnectionManager(connectionManager);
    }
  }

  @Override
  public void close() throws Exception {
    this.shutdown();
  }

  private WebTarget initializeTarget(CzlClientConfig objectsObjectsClientConfig) {
    ClientConfig clientConfig = new ClientConfig()
        .connectorProvider(new ApacheConnectorProvider())
        .register(JacksonFeature.class)
        .register(JaxRsJacksonConfigurator.class)
        .register(LoggingFilter.class);

    String proxyUri = objectsObjectsClientConfig.getProxyUri();
    String proxyUser = null;
    String proxyPassword = null;

    if (proxyUri != null) {
      proxyUser = objectsObjectsClientConfig.getProxyUser();
      proxyPassword = objectsObjectsClientConfig.getProxyPass();
    }

    if (proxyUri != null) {
      clientConfig = clientConfig.property(ClientProperties.PROXY_URI, proxyUri);

      if (proxyUser != null && proxyPassword != null) {
        clientConfig = clientConfig.property(ClientProperties.PROXY_USERNAME, proxyUser);
        clientConfig = clientConfig.property(ClientProperties.PROXY_PASSWORD, proxyPassword);
      }
    }

    // Connection manager
    connectionManager = new PoolingHttpClientConnectionManager(objectsObjectsClientConfig.getConnectionTtl(), TimeUnit.MILLISECONDS);
    connectionManager.setDefaultMaxPerRoute(objectsObjectsClientConfig.getMaxConnectionCount());
    connectionManager.setMaxTotal(objectsObjectsClientConfig.getMaxConnectionCount());
    connectionManager.setDefaultSocketConfig(SocketConfig.custom().setSoTimeout(objectsObjectsClientConfig.getSocketTimeout()).build());
    clientConfig.property(ApacheClientProperties.CONNECTION_MANAGER, connectionManager);

    // Idle connection monitor
    IdleConnectionMonitor.registerConnectionManager(connectionManager, objectsObjectsClientConfig.getConnectionTtl());

    RequestConfig defaultRequestConfig = RequestConfig.custom()
        .setConnectionRequestTimeout(objectsObjectsClientConfig.getConnectionRequestTimeout())
        .setConnectTimeout(objectsObjectsClientConfig.getConnectTimeout())
        .setSocketTimeout(objectsObjectsClientConfig.getSocketTimeout())
        .setRedirectsEnabled(objectsObjectsClientConfig.isFollowRedirectsEnabled())
        .build();

    clientConfig.property(ApacheClientProperties.REQUEST_CONFIG, defaultRequestConfig);

    return ClientBuilder.newClient(clientConfig).target(objectsObjectsClientConfig.getEndpointURI());
  }

  /**
   * Creates a new HTTP request and executes it.
   *
   * @param path            the HTTP request URI path
   * @param method          the HTTP request method
   * @param pathParams      HTTP request path params
   * @param queryParams     HTTP request query params
   * @param matrixParams    HTTP request matrix params
   * @param headerParams    HTTP request headers
   * @param body            HTTP request body
   * @param accept          HTTP request accept header value
   * @param contentType     HTTP request body content type
   * @param expectedType    expected response type
   * @param <T>             the type that the response should be deserialized into
   * @param followRedirects whether to automatically follow redirects or not
   * @return a {@link Response} instance containing the response body deserialized into the desired type
   */
  private <T> Response<T> invokeAPI(String path, String method, Map<String, Object> pathParams, Map<String, String> queryParams,
                                    Map<String, String> matrixParams, Map<String, String> headerParams, Object body, String accept,
                                    String contentType, Class<T> expectedType, Boolean followRedirects) {
    WebTarget apiTarget = webTarget.path(path).resolveTemplates(pathParams);

    for (Map.Entry<String, String> queryParam : queryParams.entrySet()) {
      apiTarget = apiTarget.queryParam(queryParam.getKey(), queryParam.getValue());
    }

    for (Map.Entry<String, String> matrixParam : matrixParams.entrySet()) {
      if (matrixParam.getValue() != null) {
        apiTarget = apiTarget.matrixParam(matrixParam.getKey(), matrixParam.getValue());
      }
    }

    Invocation.Builder invocationBuilder = apiTarget.request(accept);

    for (Map.Entry<String, String> headerParam : headerParams.entrySet()) {
      if (headerParam.getValue() != null) {
        invocationBuilder.header(headerParam.getKey(), headerParam.getValue());
      }
    }

    for (Map.Entry<String, String> defaultHeader : defaultHeaderMap.entrySet()) {
      if (!headerParams.containsKey(defaultHeader.getKey())) {
        invocationBuilder.header(defaultHeader.getKey(), defaultHeader.getValue());
      }
    }

    if (followRedirects != null) {
      invocationBuilder.property(ClientProperties.FOLLOW_REDIRECTS, followRedirects);
    }

    javax.ws.rs.core.Response response;

    if (contentType == null) {
      response = invocationBuilder.method(method);
    } else {
      response = invocationBuilder.method(method, Entity.entity(body, contentType));
    }

    return new JaxRsResponse<>(response, expectedType);
  }
}
