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

import org.apache.http.conn.HttpClientConnectionManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.TimeUnit;

/**
 * Closes idle or expired connections created by a specific connection manager.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
class CloseIdleConnectionsTask implements Runnable {

  private static final Logger logger = LoggerFactory.getLogger(CloseIdleConnectionsTask.class);

  private final HttpClientConnectionManager connectionManager;
  private final int idleTime;

  /**
   * Creates a new task.
   *
   * @param connectionManager the connection manager that will be periodically checked
   * @param idleTime          the inactivity time in milliseconds after which connections are considered to be idle
   */
  CloseIdleConnectionsTask(HttpClientConnectionManager connectionManager, int idleTime) {
    this.connectionManager = connectionManager;
    this.idleTime = idleTime;
  }

  @Override
  public void run() {
    try {
      connectionManager.closeExpiredConnections();
      connectionManager.closeIdleConnections(idleTime, TimeUnit.MILLISECONDS);
    } catch (Exception t) {
      logger.warn("Unable to close idle connections", t);
    }
  }
}
