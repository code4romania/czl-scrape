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

import javax.ws.rs.core.Response;
import java.io.InputStream;

/**
 * Deserialization strategy that ensures the response body is safely deserialized and that the input stream is properly closed.
 *
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
class JaxRsResponseDeserializationStrategy {

  @SuppressWarnings("unchecked")
  <T> T read(Response response, Class<T> expectedType) {
    if (!response.hasEntity()) {
      response.close();
      return null;
    }

    if (InputStream.class.isAssignableFrom(expectedType)) {
      return (T) response.getEntity();
    } else {
      if (response.getStatusInfo().getFamily() == Response.Status.Family.SUCCESSFUL) {
        try {
          return response.readEntity(expectedType);
        } finally {
          response.close();
        }
      }
    }

    response.close();
    return null;
  }
}
