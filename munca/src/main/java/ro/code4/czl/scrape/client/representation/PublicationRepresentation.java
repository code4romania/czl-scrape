package ro.code4.czl.scrape.client.representation;

import java.util.List;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class PublicationRepresentation {

  private String identifier;
  private String title;
  private String type;
  private String issuer;
  private String date;
  private String description;
  private int feedback_days;
  private ContactRepresentation contact;
  private List<DocumentRepresentation> documents;

  public String getIdentifier() {
    return identifier;
  }

  public void setIdentifier(String identifier) {
    this.identifier = identifier;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getIssuer() {
    return issuer;
  }

  public void setIssuer(String issuer) {
    this.issuer = issuer;
  }

  public String getDate() {
    return date;
  }

  public void setDate(String date) {
    this.date = date;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public int getFeedback_days() {
    return feedback_days;
  }

  public void setFeedback_days(int feedback_days) {
    this.feedback_days = feedback_days;
  }

  public ContactRepresentation getContact() {
    return contact;
  }

  public void setContact(ContactRepresentation contact) {
    this.contact = contact;
  }

  public List<DocumentRepresentation> getDocuments() {
    return documents;
  }

  public void setDocuments(List<DocumentRepresentation> documents) {
    this.documents = documents;
  }

  public static final class PublicationRepresentationBuilder {
    private String identifier;
    private String title;
    private String type;
    private String institution;
    private String date;
    private String description;
    private int feedback_days;
    private ContactRepresentation contact;
    private List<DocumentRepresentation> documents;

    private PublicationRepresentationBuilder() {
    }

    public static PublicationRepresentationBuilder aPublicationRepresentation() {
      return new PublicationRepresentationBuilder();
    }

    public PublicationRepresentationBuilder withIdentifier(String identifier) {
      this.identifier = identifier;
      return this;
    }

    public PublicationRepresentationBuilder withTitle(String title) {
      this.title = title;
      return this;
    }

    public PublicationRepresentationBuilder withType(String type) {
      this.type = type;
      return this;
    }

    public PublicationRepresentationBuilder withInstitution(String institution) {
      this.institution = institution;
      return this;
    }

    public PublicationRepresentationBuilder withDate(String date) {
      this.date = date;
      return this;
    }

    public PublicationRepresentationBuilder withDescription(String description) {
      this.description = description;
      return this;
    }

    public PublicationRepresentationBuilder withFeedback_days(int feedback_days) {
      this.feedback_days = feedback_days;
      return this;
    }

    public PublicationRepresentationBuilder withContact(ContactRepresentation contact) {
      this.contact = contact;
      return this;
    }

    public PublicationRepresentationBuilder withDocuments(List<DocumentRepresentation> documents) {
      this.documents = documents;
      return this;
    }

    public PublicationRepresentation build() {
      PublicationRepresentation publicationRepresentation = new PublicationRepresentation();
      publicationRepresentation.setIdentifier(identifier);
      publicationRepresentation.setTitle(title);
      publicationRepresentation.setType(type);
      publicationRepresentation.setIssuer(institution);
      publicationRepresentation.setDate(date);
      publicationRepresentation.setDescription(description);
      publicationRepresentation.setFeedback_days(feedback_days);
      publicationRepresentation.setContact(contact);
      publicationRepresentation.setDocuments(documents);
      return publicationRepresentation;
    }
  }
}
