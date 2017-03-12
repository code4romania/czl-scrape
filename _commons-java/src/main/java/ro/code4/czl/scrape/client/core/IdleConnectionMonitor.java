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

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.TimeUnit;

/**
 * Monitors HTTP connection managers. Closes idle or expired connections.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
class IdleConnectionMonitor {

  private static final Logger logger = LoggerFactory.getLogger(IdleConnectionMonitor.class);

  /**
   * Interval of time after which connections are checked for idleness or expiry.
   */
  private static final int PERIOD_SECONDS = 30;

  private static IdleConnectionMonitor instance;

  private ScheduledExecutorService executorService;
  private Map<HttpClientConnectionManager, Future<?>> tasks;
  private volatile boolean isRunning;

  private IdleConnectionMonitor() {
    if (logger.isDebugEnabled()) {
      logger.debug("Starting up");
    }

    this.executorService = Executors.newSingleThreadScheduledExecutor();
    this.tasks = new HashMap<>();
    this.isRunning = true;
  }

  /**
   * Registers the given connection manager with this monitor. The connections maintained by the given connection manager will be checked for
   * idleness or expiration.
   *
   * @param connectionManager the connection manager to monitor
   * @param idleTime          the inactivity time in milliseconds after which connections are considered to be idle
   */
  static synchronized void registerConnectionManager(HttpClientConnectionManager connectionManager, int idleTime) {
    if (instance == null) {
      instance = new IdleConnectionMonitor();
    }

    instance.monitor(connectionManager, idleTime);
  }

  /**
   * Removes the given connection manager from this monitor. Shuts down the monitor thread if there are no more connection managers left.
   *
   * @param connectionManager the connection manager that should no longer be monitored
   */
  static synchronized void removeConnectionManager(HttpClientConnectionManager connectionManager) {
    if (instance != null) {
      instance.forget(connectionManager);

      if (!instance.isRunning()) {
        shutdown();
      }
    }
  }

  /**
   * Stops the monitor, if not already stopped, and clears its state.
   */
  private static synchronized void shutdown() {
    if (instance != null) {
      if (instance.isRunning()) {
        instance.stop();
      }

      instance = null;
    }
  }

  /**
   * Indicates whether this monitor is running or not.
   *
   * @return <code>true</code> if the monitor is running, <code>false</code> otherwise
   */
  private boolean isRunning() {
    return isRunning;
  }

  private void monitor(HttpClientConnectionManager connectionManager, int idleTime) {
    logger.debug("Monitoring connection manager {}", connectionManager);
    ScheduledFuture<?> task = executorService
        .scheduleWithFixedDelay(new CloseIdleConnectionsTask(connectionManager, idleTime), PERIOD_SECONDS, PERIOD_SECONDS, TimeUnit.SECONDS);
    tasks.put(connectionManager, task);
  }

  private void forget(HttpClientConnectionManager connectionManager) {
    logger.debug("No longer monitoring connection manager {}", connectionManager);
    Future<?> task = tasks.remove(connectionManager);

    if (task != null) {
      task.cancel(false);
    }

    if (tasks.isEmpty()) {
      stop();
    }
  }

  private void stop() {
    if (logger.isDebugEnabled()) {
      logger.debug("Stopping monitor");
    }
    executorService.shutdown();
    isRunning = false;
    tasks = null;
    executorService = null;
  }

}
