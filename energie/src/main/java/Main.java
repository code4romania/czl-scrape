import org.apache.commons.codec.digest.DigestUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.code4.czl.scrape.client.CzlClient;
import ro.code4.czl.scrape.client.CzlClientConfig;
import ro.code4.czl.scrape.client.authentication.TokenAuthenticationStrategy;
import ro.code4.czl.scrape.client.representation.DocumentRepresentation;
import ro.code4.czl.scrape.client.representation.PublicationRepresentation;
import ro.code4.czl.scrape.client.samples.CzlClientSample;

import java.awt.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import javax.swing.*;

class ThreadMinister implements Runnable {

  private static int countP = 1;

  private static final int DEPTH_LIMIT = 2;
  private static final int LINK_LIMIT = 50;
  private static final String BEGIN = "http://energie.gov.ro/transparenta-si-integritate/transparenta-decizionala-2/";

  private static JFrame main_frame;
  private static TextArea debug;

  private static String getUrlSource(String url) throws IOException {
    URL w = new URL(url);
    URLConnection yc = w.openConnection();
    BufferedReader in = new BufferedReader(new InputStreamReader(
        yc.getInputStream(), "UTF-8"));
    String inputLine;
    StringBuilder a = new StringBuilder();
    while ((inputLine = in.readLine()) != null) {
      a.append(inputLine);
      a.append('\n');
    }
    in.close();

    return a.toString();
  }

  private static Logger logger;
  private static CzlClientConfig clientConfig;
  private static CzlClient czlClient;

  private static void init(String begin) {
    main_frame = new JFrame("Crawler on " + begin);
    main_frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
    main_frame.setSize(800, 300);
    debug = new TextArea("Starting at... " + begin + "\n");
    debug.setEditable(false);
    JScrollPane scroll = new JScrollPane(debug, ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED, ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
    main_frame.add(scroll);
    main_frame.setVisible(true);
    //TODO
    logger = LoggerFactory.getLogger(CzlClientSample.class);
    clientConfig = CzlClientConfig.builder()
        .endpointURI("http://czl-api.code4.ro/api/")
        .connectionRequestTimeout(500)
        .connectTimeout(500)
        .socketTimeout(3000)
        .authenticationStrategy(new TokenAuthenticationStrategy())
        .build();

    czlClient = CzlClient.newClient(clientConfig);
  }

  private static void surfWeb(String adr, int depth) {
    String info = null;
    String descriere = null;
    String webName;
    String title = null;
    String type0 = null;
    String[] type = null;
    String[] thePdfL = null;//continut
    String lName = null;//numele legii
    String dateInit = null;//data la care a fost propusa
    String feedDays = null;//feedback days
    PublicationRepresentation publicationRepresentation = new PublicationRepresentation();
    int i;

    String[] links = new String[LINK_LIMIT];
    int linkIndex = 0;

    if (depth >= DEPTH_LIMIT) {
      if (main_frame.getComponentCount() < 3) {
        end(0, "");
      } else {
        end(4, "");
      }
    }

    try {
      info = getUrlSource(adr);
    } catch (IOException e) {
      end(1, adr);
    }
    if (info != null) {
      webName = adr.replace("https://", "").replace("http://", "").replace("www.", "").replace(".", "_").replace("/", "");
      //get info
      if ((adr.contains(BEGIN) && depth == 0)) {
        //suntem pe pg proiectului
        try {
          //Document docI = Jsoup.connect(adr).get();
          Document docI = Jsoup.parse(info, adr);
          docI.outputSettings().charset();
          Charset.forName("UTF-8");
          Elements nextLinksI = docI.select("strong");
          Iterator<org.jsoup.nodes.Element> itI = nextLinksI.iterator();
          org.jsoup.nodes.Element elementI = itI.next();
          int first = 0;
          //initializam citirea
          while (!elementI.text().contains("2017") && itI.hasNext()) {
            itI.next();
          }

          while (itI.hasNext()) {
            type = new String[10];
            thePdfL = new String[10];
            dateInit = null;
            if (!elementI.text().endsWith("2016")) {
              countP = 0;
              dateInit = elementI.text();
              //nume sau descriere lege
              elementI = itI.next();
              lName = elementI.text();
              descriere = lName;
              if (descriere.contains("HG") || descriere.contains("Hotărâre")) {
                type0 = "HG";
              } else if (descriere.contains("Proiect")) {
                type0 = "LEGE";
              } else {
                type0 = "OUG";
              }
              // docs
              elementI = itI.next();
              first = 1;
              while (
                  !elementI.text().matches("([0-9]{2}).([0-9]{2}).([0-9]{4})") && countP < 10 && itI.hasNext() && (!elementI.text().contains("OUG"))
                  || elementI.text().contains("Not")) {
                first = 0;

                if (elementI.child(0).attr("abs:href") != null) {
                  thePdfL[countP] = elementI.child(0).attr("abs:href");
                  String titleL = elementI.text();
                  //type doc
                  if (titleL.contains("Not")) {
                    type[countP] = "Nota";
                  } else if (titleL.contains("Expunere")) {
                    type[countP] = "Expunere motive";
                  } else if (titleL.contains("Partea")) {
                    type[countP] = "Partea dispozitiva";
                  } else {
                    type[countP] = "Anexa";
                  }
                  countP++;
                }
                elementI = itI.next();
              }
            } else {
              break;
            }

            if (dateInit != null) {
              try {
                if (descriere == null) {
                  descriere = "-";
                }
                if (feedDays == null) {
                  feedDays = "0";
                }

                publicationRepresentation.setIdentifier(DigestUtils.md5Hex(lName));
                publicationRepresentation.setTitle(lName);

                publicationRepresentation.setType(type0);
                publicationRepresentation.setInstitution("energie");

                String[] splitDate = Optional.ofNullable(dateInit).orElse("11.03.2017").split("\\.");
                publicationRepresentation.setDate(splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0]);
                publicationRepresentation.setDescription(descriere);
                publicationRepresentation.setFeedback_days(Optional.ofNullable(Integer.parseInt(feedDays)).orElse(0));
                Map<String, String> contactMap = new HashMap<>();
                contactMap.put("email", "comunicare@energie.gov.ro");
                contactMap.put("tel", "0214079921");
                publicationRepresentation.setContact(contactMap);
                DocumentRepresentation[] documentRepresentation = new DocumentRepresentation[countP];
                debug.setText(debug.getText() + "\nName " + lName);
                debug.setText(debug.getText() + "\nType " + type0);
                debug.setText(debug.getText() + "\nInstitution " + "energie");
                debug.setText(debug.getText() + "\nDescriere " + descriere);
                debug.setText(debug.getText() + "\nFeedback days " + Optional.ofNullable(Integer.parseInt(feedDays)).orElse(0));
                if (dateInit == null) {
                  dateInit = "-";
                }
                i = 0;
                while (i < countP) {
                  documentRepresentation[i] = new DocumentRepresentation();
                  documentRepresentation[i].setType(type[i]);
                  debug.setText(debug.getText() + "\nType " + type[i] + "\nUrl " + thePdfL[i]);
                  documentRepresentation[i].setUrl(thePdfL[i]);
                  i++;
                }
                List<DocumentRepresentation> representations = new ArrayList<DocumentRepresentation>(countP);
                i = 0;
                while (i < countP) {
                  representations.add(documentRepresentation[i]);
                  i++;
                }
                publicationRepresentation.setDocuments(representations);
                //send publication

                //TODO
                czlClient.apiV1().createPublication(publicationRepresentation).execute();
              } catch (Exception e) {
                end(2, adr + " 1");
              }
            }
          }
        } catch (Exception e) {
          end(2, adr + " 2");
        }
      }
    }
  }

  private static void end(int sig, String link) {
    if (main_frame != null) {
      if (sig == 0) {
        return;
      }
      if (sig == 1) {
        debug.setText(debug.getText() + "\nFailed to connect to " + link);
        return;
      }
      if (sig == 2) {
        debug.setText(debug.getText() + "\nError at " + link);
        return;
      }
      if (sig == 3) {
        debug.setText(debug.getText() + "\nError: " + link);
      }
    }
  }

  public void run() {

  }

  void start() {
    init(BEGIN);
    surfWeb(BEGIN, 0);
    debug.setText(debug.getText() + "\nCrawling finished");
  }
}


public class Main {

  public static void main(String[] args) {
    new ThreadMinister().start();
  }

}
