package ro.code4.czl.scrape.client;

import static ro.code4.czl.scrape.client.representation.PublicationRepresentation.PublicationRepresentationBuilder.aPublicationRepresentation;

import ro.code4.czl.scrape.client.representation.DocumentRepresentation;
import us.codecraft.webmagic.ResultItems;
import us.codecraft.webmagic.Task;
import us.codecraft.webmagic.pipeline.Pipeline;

import java.util.List;
import java.util.Map;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CzlApiUploadPipeline implements Pipeline {

  private final CzlClient czlClient;

  public CzlApiUploadPipeline(CzlClient czlClient) {
    this.czlClient = czlClient;
  }

  @SuppressWarnings("unchecked")
  @Override
  public void process(ResultItems resultItems, Task task) {
    Map<String, Object> extractedFields = resultItems.getAll();

    czlClient.apiV1()
        .createPublication(aPublicationRepresentation()
                               .withDate((String) extractedFields.get("date"))
                               .withInstitution((String) extractedFields.get("institution"))
                               .withIdentifier((String) extractedFields.get("identifier"))
                               .withDescription((String) extractedFields.get("description"))
                               .withDocuments((List<DocumentRepresentation>) extractedFields.get("documents"))
                               .withTitle((String) extractedFields.get("title"))
                               .withType((String) extractedFields.get("type"))
                               .withFeedback_days((int) extractedFields.get("feedbackDays"))
                               .withContact((Map<String, String>) extractedFields.get("contact"))
                               .build())
        .execute();
  }
}
