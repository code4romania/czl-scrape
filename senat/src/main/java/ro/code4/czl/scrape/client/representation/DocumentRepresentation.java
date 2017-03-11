package ro.code4.czl.scrape.client.representation;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
@JsonInclude(Include.NON_NULL)
public class DocumentRepresentation {

  private String type;
  private String url;

  public DocumentRepresentation() {
  }

  public DocumentRepresentation(String type, String url) {
    this.type = type;
    this.url = url;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }

  @Override
  public String toString() {
    return new ToStringBuilder(this, ToStringStyle.SHORT_PREFIX_STYLE)
        .append("type", type)
        .append("url", url)
        .toString();
  }
}
