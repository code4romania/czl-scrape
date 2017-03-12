package code4romania.czl.scrapers.comunicatii;


import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.codehaus.jackson.annotate.JsonAutoDetect;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import code4romania.czl.scrapers.comunicatii.Contact;

/**
 * Created by radug on 11/03/2017.
 * {
 "identifier": "lawproposal-first-document-name-slug-or-something", // un identificator unic, predictibil (repetabil), pereferabil human-readable
 "title": "Proiectul de ordin al ministrului justiției pentru aprobarea Regulamentului privind organizarea și desfășurarea activităților și programelor educative, de asistență psihologică și asistență socială din locurile de deținere aflate în subordinea Aministrației Naționale a Penitenciarelor", // titlul actului legislativ propus
 "type": "HG", // HG, OG, OUG, PROIECT
 "institution": "justitie", // ID-ul platformei din care provine actul legislativ
 "date": "2017-03-08", // ISO 8601
 "description": "Cookie jelly-o sesame snaps donut sesame snaps sweet roll chocolate. Tootsie roll pie bonbon tart chocolate cake. Gummi bears gummies chupa chups ice cream croissant donut marzipan. Macaroon bear claw halvah carrot cake liquorice powder.",
 "feedback_days": 12, // numarul zilelor disponibile pentru feedback
 "contact": {"tel": "12345", "email": "feedback@example.org"}, // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr"
 "documents": [ // array de dictionare
 {
 "type": "anexa", // free text momentan
 "url": "http://www.just.ro/wp-content/uploads/2017/02/Proiect.docx" // da, este un link catre un document oficial de la MJ
 }
 ]
 }
 *
 */
@JsonAutoDetect
public class ComunicatiiBean {
    String identifier;
    String title;

    @Override
    public String toString() {
        return "ComunicatiiBean{" +
                "identifier='" + identifier + '\'' +
                ", title='" + title + '\'' +
                ", type='" + type + '\'' +
                ", institution='" + institution + '\'' +
                ", date='" + date + '\'' +
                ", description='" + description + '\'' +
                ", feedback_days='" + feedback_days + '\'' +
                ", contact='" + contacts + '\'' +
                ", documents=" + (documents!=null ? Arrays.toString(documents.toArray()) : "null") +
                '}';
    }

    String type;
    String institution = "MCSI";
    String date;
    String description;
    String feedback_days = "0";
  //  String contact = "[\"email\":\"propuneri@comunicatii.gov.ro\"]";
    
 Contact contacts = new Contact();
    
   
    public String getInstitution() {
        return institution;
    }

    public void setInstitution(String institution) {
        this.institution = institution;
    }

    String institution = "comunicatii";

    List<Document> documents;

    static class Document {
        String type;
        String url;

        @Override
        public String toString() {
            return "Document{" +
                    "type='" + type + '\'' +
                    ", url='" + url + '\'' +
                    '}';
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
    }

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

    public String getInstitution() {
        return institution;
    }

    public void setInstitution(String institution) {
        this.institution = institution;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public void setDate(String date, String fmt){

        DateTimeFormatter in = DateTimeFormatter.ofPattern(fmt);
        DateTimeFormatter out = DateTimeFormatter.ofPattern("2017-03-08");
        try {
            LocalDate localDate = LocalDate.parse(date, in);

            this.date = localDate.format(out).toString();
        }catch (Exception e){
            e.printStackTrace();
        }
     }


    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getFeedback_days() {
        return feedback_days;
    }

    public void setFeedback_days(String feedback_days) {
        this.feedback_days = feedback_days;
    }

   public Contact getContact() {
       return contacts;
   }

    public void setContact(Contact contact) {
        this.contacts = contact;
    }
    public List<Document> getDocuments() {
        if (documents == null){
            documents = new ArrayList<Document>();
        }
        return documents;
    }

    public void setDocuments(List<Document> documents) {
        this.documents = documents;
    }

    public void addDocument(String url, String type) {
        Document doc = new Document();
        doc.setType(type);
        doc.setUrl(url);
        getDocuments().add(doc);
    }

    public String toJson() {
        try {
            String result = new ObjectMapper()
                    .writeValueAsString(this);
            return result;
        }catch (JsonProcessingException e) {
            e.printStackTrace();
        }

        return "{}";
    }


}