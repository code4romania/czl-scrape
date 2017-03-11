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


import ro.code4.czl.scrape.client.model.CreatePublicationRequest;
import ro.code4.czl.scrape.client.representation.PublicationRepresentation;

/**
 * A class describing the API for Ce Zice Legea. Uses a fluent builder interface to create requests.
 *
 * @author Ionut -Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CzlApiV1 {

  private final ApiInvoker apiInvoker;

  /**
   * Creates a new request builder.
   *
   * @param apiInvoker the {@linkplain ApiInvoker} implementation to use for every request built via this class.
   * @see ApiInvoker
   */
  CzlApiV1(ApiInvoker apiInvoker) {
    this.apiInvoker = apiInvoker;
  }

  /**
   * Starts preparing a new request for creating a publication.
   *
   * @param publicationRepresentation the ro.code4.czl.scrape.client.representation of the publication to create.
   * @return a request builder.
   */
  public CreatePublicationRequest.Builder createPubliation(PublicationRepresentation publicationRepresentation) {
    return CreatePublicationRequest.builder(publicationRepresentation, apiInvoker);
  }

}
