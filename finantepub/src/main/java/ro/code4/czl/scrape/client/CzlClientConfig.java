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
 * General client settings. Uses a fluent builder pattern.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CzlClientConfig {

  /**
   * The default maximum time to live that connections created by an SDK client will be configured to. Value is in milliseconds.
   */
  public static final int DEFAULT_CONNECTION_TTL = 60 * 1000;

  /**
   * The default maximum number of connections that an SDK client is allowed to create.
   */
  public static final int DEFAULT_MAX_CONNECTION_COUNT = 4;

  /**
   * The default socket timeout ({@code SO_TIMEOUT}) in milliseconds, which is the timeout for waiting for data  or, put differently, a maximum
   * period inactivity between two consecutive data packets).
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   */
  public static final int DEFAULT_SOCKET_TIMEOUT = 30 * 1000;

  /**
   * The default timeout in milliseconds used when requesting a connection from the connection manager.
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   */
  public static final int DEFAULT_CONNECTION_REQUEST_TIMEOUT = -1;

  /**
   * The default timeout in milliseconds until a connection is established.
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   */
  public static final int DEFAULT_CONNECT_TIMEOUT = 30 * 1000;

  private String endpointURI;
  private String proxyUri;
  private String proxyUser;
  private String proxyPass;
  private boolean followRedirectsEnabled;
  private int connectionTtl;
  private int maxConnectionCount;
  private int socketTimeout;
  private int connectionRequestTimeout;
  private int connectTimeout;
  private AuthenticationStrategy authenticationStrategy;

  public static EndpointURIProvider builder() {
    return new Builder();
  }

  /**
   * Retrieves the service endpoint that the client will target.
   */
  public String getEndpointURI() {
    return endpointURI;
  }

  /**
   * Sets the service endpoint that the client should target.
   *
   * @param endpointURI a valid service endpoint
   */
  public void setEndpointURI(String endpointURI) {
    this.endpointURI = endpointURI;
  }

  /**
   * Indicates whether this client has automatic following of redirects enabled. By default, this feature is enabled.
   *
   * @return <code>true</code> if automatic following of redirects is enabled, <code>false</code> otherwise
   */
  public boolean isFollowRedirectsEnabled() {
    return followRedirectsEnabled;
  }

  /**
   * Enables or disables the automatic following of redirects.
   *
   * @param followRedirectsEnabled <code>true</code> to enable automatic following of redirects, <code>false</code> otherwise
   */
  public void setFollowRedirectsEnabled(boolean followRedirectsEnabled) {
    this.followRedirectsEnabled = followRedirectsEnabled;
  }

  /**
   * Retrieves the proxy server to use.
   */
  public String getProxyUri() {
    return proxyUri;
  }

  /**
   * Sets the proxy server to use.
   *
   * @param proxyUri a proxy server
   */
  public void setProxyUri(String proxyUri) {
    this.proxyUri = proxyUri;
  }

  /**
   * Retrieves the proxy user to use.
   */
  public String getProxyUser() {
    return proxyUser;
  }

  /**
   * Sets the proxy user to use.
   *
   * @param proxyUser the proxy user
   */
  public void setProxyUser(String proxyUser) {
    this.proxyUser = proxyUser;
  }

  /**
   * Retrieves the proxy password to use.
   */
  public String getProxyPass() {
    return proxyPass;
  }

  /**
   * Sets the proxy password to use.
   *
   * @param proxyPass the proxy password
   */
  public void setProxyPass(String proxyPass) {
    this.proxyPass = proxyPass;
  }

  /**
   * Retrieves the maximum time to live that connections created by this client will be configured to.
   */
  public int getConnectionTtl() {
    return connectionTtl;
  }

  /**
   * Sets the time to live for all connections created by this client.
   *
   * @param connectionTtl the time to live in milliseconds
   */
  public void setConnectionTtl(int connectionTtl) {
    this.connectionTtl = connectionTtl;
  }

  /**
   * Retrieves the maximum number of connections that this client is allowed to create.
   */
  public int getMaxConnectionCount() {
    return maxConnectionCount;
  }

  /**
   * Sets the maximum number of connections created by this client.
   *
   * @param maxConnectionCount the maximum number of connections
   */
  public void setMaxConnectionCount(int maxConnectionCount) {
    this.maxConnectionCount = maxConnectionCount;
  }

  /**
   * Returns the socket timeout ({@code SO_TIMEOUT}) in milliseconds, which is the timeout for waiting for data  or, put differently, a maximum
   * period inactivity between two consecutive data packets).
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   * <p>
   * Default: {@code 2000}
   * </p>
   */
  public int getSocketTimeout() {
    return socketTimeout;
  }

  /**
   * Sets the socket timeout ({@code SO_TIMEOUT}) in milliseconds, which is the timeout for waiting for data  or, put differently, a maximum
   * period inactivity between two consecutive data packets).
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   *
   * @param socketTimeout the socket timeout in milliseconds
   */
  public void setSocketTimeout(int socketTimeout) {
    this.socketTimeout = socketTimeout;
  }

  /**
   * Returns the timeout in milliseconds used when requesting a connection from the connection manager. A timeout value of zero is interpreted
   * as an infinite timeout.
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   * <p>
   * Default: {@code -1}
   * </p>
   */
  public int getConnectionRequestTimeout() {
    return connectionRequestTimeout;
  }

  /**
   * Sets the timeout in milliseconds used when requesting a connection from the connection manager. A timeout value of zero is interpreted
   * as an infinite timeout.
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   *
   * @param connectionRequestTimeout the connection request timeout in milliseconds
   */
  public void setConnectionRequestTimeout(int connectionRequestTimeout) {
    this.connectionRequestTimeout = connectionRequestTimeout;
  }

  /**
   * Returns the timeout in milliseconds until a connection is established. A timeout value of zero is interpreted as an infinite timeout.
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   * <p>
   * Default: {@code 500}
   * </p>
   */
  public int getConnectTimeout() {
    return connectTimeout;
  }

  /**
   * Sets the timeout in milliseconds until a connection is established. A timeout value of zero is interpreted as an infinite timeout.
   * <p>
   * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
   * </p>
   *
   * @param connectTimeout the connection timeout in milliseconds
   */
  public void setConnectTimeout(int connectTimeout) {
    this.connectTimeout = connectTimeout;
  }

  /**
   * Returns the global authentication strategy to be used by the client.
   *
   * @return an {@linkplain AuthenticationStrategy} instance if a strategy has been set, <code>null</code> otherwise
   */
  public AuthenticationStrategy getAuthenticationStrategy() {
    return authenticationStrategy;
  }

  /**
   * Sets a global authentication strategy to be used by the client.
   *
   * @param authenticationStrategy an {@linkplain AuthenticationStrategy} instance
   */
  public void setAuthenticationStrategy(AuthenticationStrategy authenticationStrategy) {
    this.authenticationStrategy = authenticationStrategy;
  }

  public interface EndpointURIProvider {

    /**
     * Sets the service endpoint that the client should target.
     *
     * @param endpointURI a valid service endpoint
     */
    Build endpointURI(String endpointURI);
  }

  public interface Build {

    /**
     * Enables or disables the automatic following of redirects. This feature is enabled by default.
     *
     * @param followRedirects <code>true</code> to enable automatic following of redirects, <code>false</code> otherwise.
     */
    Build followRedirects(boolean followRedirects);

    /**
     * Enables proxying of requests via the given proxy server.
     *
     * @param proxyUri a proxy server
     */
    Build enableProxying(String proxyUri);

    /**
     * Enables proxying of requests via the given proxy server.
     *
     * @param proxyUri  a proxy server
     * @param proxyUser a proxy user
     * @param proxyPass a proxy password
     */
    Build enableProxying(String proxyUri, String proxyUser, String proxyPass);

    /**
     * Sets the time to live for all connections created by this client.
     *
     * @param connectionTtl the time to live in milliseconds
     */
    Build connectionTtl(int connectionTtl);

    /**
     * Sets the maximum number of connections created by this client.
     *
     * @param maxConnectionCount the maximum number of connections
     */
    Build maxConnectionCount(int maxConnectionCount);

    /**
     * Sets the socket timeout ({@code SO_TIMEOUT}) in milliseconds, which is the timeout for waiting for data  or, put differently, a maximum
     * period inactivity between two consecutive data packets).
     * <p>
     * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
     * </p>
     *
     * @param socketTimeout the socket timeout in milliseconds
     */
    Build socketTimeout(int socketTimeout);

    /**
     * Sets the timeout in milliseconds used when requesting a connection from the connection manager. A timeout value of zero is interpreted
     * as an infinite timeout.
     * <p>
     * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
     * </p>
     *
     * @param connectionRequestTimeout the connection request timeout in milliseconds
     */
    Build connectionRequestTimeout(int connectionRequestTimeout);

    /**
     * Sets the timeout in milliseconds until a connection is established. A timeout value of zero is interpreted as an infinite timeout.
     * <p>
     * A timeout value of zero is interpreted as an infinite timeout. A negative value is interpreted as undefined (system default).
     * </p>
     *
     * @param connectTimeout the connection timeout in milliseconds
     */
    Build connectTimeout(int connectTimeout);

    /**
     * Sets the global authentication strategy to be used by the client.
     *
     * @param authenticationStrategy an {@linkplain AuthenticationStrategy} instance
     */
    Build authenticationStrategy(AuthenticationStrategy authenticationStrategy);

    /**
     * Build a new client configuration instance using all the settings previously specified in this configuration builder.
     *
     * @return a new client configuration instance.
     */
    CzlClientConfig build();
  }

  public static class Builder implements EndpointURIProvider, Build {

    private String endpointURI;
    private boolean followRedirectsEnabled = true;
    private String proxyUri;
    private String proxyUser;
    private String proxyPass;
    private int connectionTtl = DEFAULT_CONNECTION_TTL;
    private int maxConnectionCount = DEFAULT_MAX_CONNECTION_COUNT;
    private int socketTimeout = DEFAULT_SOCKET_TIMEOUT;
    private int connectionRequestTimeout = DEFAULT_CONNECTION_REQUEST_TIMEOUT;
    private int connectTimeout = DEFAULT_CONNECT_TIMEOUT;
    private AuthenticationStrategy authenticationStrategy;

    @Override
    public Build endpointURI(String endpointURI) {
      this.endpointURI = endpointURI;
      return this;
    }

    @Override
    public Build followRedirects(boolean followRedirects) {
      this.followRedirectsEnabled = followRedirects;
      return this;
    }

    @Override
    public Build enableProxying(String proxyUri) {
      this.proxyUri = proxyUri;
      return this;
    }

    @Override
    public Build enableProxying(String proxyUri, String proxyUser, String proxyPass) {
      this.proxyUri = proxyUri;
      this.proxyUser = proxyUser;
      this.proxyPass = proxyPass;
      return this;
    }

    @Override
    public Build connectionTtl(int connectionTTl) {
      this.connectionTtl = connectionTTl;
      return this;
    }

    @Override
    public Build maxConnectionCount(int maxConnectionCount) {
      this.maxConnectionCount = maxConnectionCount;
      return this;
    }

    @Override
    public Build socketTimeout(int socketTimeout) {
      this.socketTimeout = socketTimeout;
      return this;
    }

    @Override
    public Build connectionRequestTimeout(int connectionRequestTimeout) {
      this.connectionRequestTimeout = connectionRequestTimeout;
      return this;
    }

    @Override
    public Build connectTimeout(int connectTimeout) {
      this.connectTimeout = connectTimeout;
      return this;
    }

    @Override
    public Build authenticationStrategy(AuthenticationStrategy authenticationStrategy) {
      this.authenticationStrategy = authenticationStrategy;
      return this;
    }

    @Override
    public CzlClientConfig build() {
      CzlClientConfig clientConfig = new CzlClientConfig();
      clientConfig.setEndpointURI(this.endpointURI);
      clientConfig.setFollowRedirectsEnabled(this.followRedirectsEnabled);
      clientConfig.setConnectionTtl(this.connectionTtl);
      clientConfig.setMaxConnectionCount(this.maxConnectionCount);
      clientConfig.setSocketTimeout(this.socketTimeout);
      clientConfig.setConnectionRequestTimeout(this.connectionRequestTimeout);
      clientConfig.setConnectTimeout(this.connectTimeout);
      clientConfig.setAuthenticationStrategy(this.authenticationStrategy);
      clientConfig.setProxyUri(this.proxyUri);
      clientConfig.setProxyUser(this.proxyUser);
      clientConfig.setProxyPass(this.proxyPass);
      return clientConfig;
    }
  }
}
