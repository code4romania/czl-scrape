package ro.code4.czl.scrape.client.representation;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
@JsonInclude(Include.NON_NULL)
public class ContactRepresentation {

  private String tel;
  private String email;

  public ContactRepresentation() {
  }

  public ContactRepresentation(String tel, String email) {
    this.tel = tel;
    this.email = email;
  }

  public String getTel() {
    return tel;
  }

  public void setTel(String tel) {
    this.tel = tel;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }
}
