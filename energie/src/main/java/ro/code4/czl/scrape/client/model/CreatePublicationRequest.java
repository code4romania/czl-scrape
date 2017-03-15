package ro.code4.czl.scrape.client.model;

import ro.code4.czl.scrape.client.ApiInvoker;
import ro.code4.czl.scrape.client.BaseRequest;
import ro.code4.czl.scrape.client.BaseRequestBuilder;
import ro.code4.czl.scrape.client.representation.PublicationRepresentation;

import javax.ws.rs.HttpMethod;
import javax.ws.rs.core.MediaType;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CreatePublicationRequest extends BaseRequest<PublicationRepresentation> {

  private CreatePublicationRequest(CreatePublicationRequest.Builder builder) {
    super(builder, "publications/", HttpMethod.POST, MediaType.APPLICATION_JSON, builder.apiInvoker);

    setBody(builder.spaceRepresentation);
  }

  public static CreatePublicationRequest.Builder builder(PublicationRepresentation spaceRepresentation, ApiInvoker apiInvoker) {
    return new CreatePublicationRequest.Builder(spaceRepresentation, apiInvoker);
  }

  @Override
  public Class<PublicationRepresentation> getResponseType() {
    return PublicationRepresentation.class;
  }

  public static class Builder extends BaseRequestBuilder<CreatePublicationRequest, PublicationRepresentation> {

    private final ApiInvoker apiInvoker;
    private final PublicationRepresentation spaceRepresentation;

    Builder(PublicationRepresentation spaceRepresentation, ApiInvoker apiInvoker) {
      this.apiInvoker = apiInvoker;
      this.spaceRepresentation = spaceRepresentation;
    }

    @Override
    public CreatePublicationRequest build() {
      return new CreatePublicationRequest(this);
    }
  }

}
