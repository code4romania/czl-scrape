import org.apache.commons.codec.digest.DigestUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import ro.code4.czl.scrape.client.CzlClient;
import ro.code4.czl.scrape.client.CzlClientConfig;
import ro.code4.czl.scrape.client.CzlClientSample;
import ro.code4.czl.scrape.client.authentication.TokenAuthenticationStrategy;
import ro.code4.czl.scrape.client.representation.ContactRepresentation;
import ro.code4.czl.scrape.client.representation.DocumentRepresentation;
import ro.code4.czl.scrape.client.representation.PublicationRepresentation;

import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.net.URL;
import java.net.URLConnection;
import java.nio.charset.Charset;
import java.util.*;
import java.util.List;

class ThreadMinister implements  Runnable{

    private static int countP = 1;

    private static final int DEPTH_LIMIT = 2;
    private static final int LINK_LIMIT = 50;
    private static final String BEGIN = "http://www.mmuncii.ro/j33/index.php/ro/transparenta/proiecte-in-dezbatere";
    private static final String SENAT = "www.mmuncii.ro";

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
        debug.setText(debug.getText() + "\nSurfing " + adr);
        String info = null;
        String descriere = null;
        String webName;
        String title = null;
        String type0 = null;
        String type1 = null;
        String type2 = null;
        PublicationRepresentation publicationRepresentation = new PublicationRepresentation();

        String[] links = new String[LINK_LIMIT];
        int linkIndex = 0;

        if (depth >= DEPTH_LIMIT) {
            if (main_frame.getComponentCount() < 3)
                end(0, "");
            else
                end(4, "");
        }

        try {
            info = getUrlSource(adr);
        } catch (IOException e) {
            end(1, adr);
        }
        if (info != null) {
            webName = adr.replace("https://", "").replace("http://", "").replace("www.", "").replace(".", "_").replace("/", "");
            debug.setText(debug.getText() + "\nGetting info from " + adr);
            //get info
            if ((adr.contains("http://www.mmuncii.ro/j33/index.php/ro/transparenta/proiecte-in-dezbatere/4")&&depth!=0)) {
            //suntem pe pg proiectului
                String thePdf = null;
                String thePdf2 = null;
                String lName = null;
                String dateInit = null;
                String dateFinal = null;
                try {
                    Document doc = Jsoup.parse(new URL(adr).openStream(), "UTF-8", adr);
                    doc.outputSettings().charset();
                    Charset.forName("UTF-8");
                    Elements nextLinks = doc.select("a[href]");
                    Iterator<org.jsoup.nodes.Element> it = nextLinks.iterator();
                    org.jsoup.nodes.Element element;
                    while (it.hasNext()) {
                        element = it.next();
                        if (element.attr("abs:href").contains("Transparenta-decizionala")||element.attr("abs:href").contains("http://www.mmuncii.ro/j33/images/Documente/Proiecte_in_dezbatere/2017/")||element.attr("abs:href").contains("http://www.mmuncii.ro/j33/images/Documente/Proiecte_in_dezbatere/2016/")){
                            if(thePdf==null) {
                                thePdf = element.attr("abs:href");
                                type1="Lege";
                                type0 = "LEGE";
                                if(element.text().startsWith("Ordin")||element.text().startsWith("ordin")) {
                                    type0 = "OG";
                                    type1 = "Ordonanta de guvern";
                                }
                                else
                                if(element.text().startsWith("Hotărâre")||element.text().startsWith("HOTĂRÂRE")) {
                                    type0 = "HG";
                                    type1 = "Hotarare";
                                }
                                title = "Proiect" + String.valueOf(countP);
                            }
                            else{
                                thePdf2 = element.attr("abs:href");
                                type2="Anexa";
                                if(element.text().contains("Notă")||element.text().contains("notă"))
                                    type2 = "Nota";
                                else
                                if(element.text().startsWith("Expunere")||element.text().startsWith("expunere"))
                                    type2 = "Expunere";

                            }
                        }
                    }
                    countP++;
                }catch (IOException e){
                    end(2, adr);
                }

                File dir = new File(System.getProperty("user.dir")+"\\muncii\\"+title);
                if(!dir.exists())
                    //noinspection ResultOfMethodCallIgnored
                    dir.mkdir();
                File desc = new File(System.getProperty("user.dir")+"\\muncii\\"+title+"\\Info.txt");

                try {
                    Document doc = Jsoup.parse(new URL(adr).openStream(), "UTF-8", adr);
                    doc.outputSettings().charset();
                    Charset.forName("UTF-8");
                    Elements elem = doc.select("h2[itemprop=headline]");
                    Iterator<org.jsoup.nodes.Element> it = elem.iterator();
                    org.jsoup.nodes.Element element;
                    while (it.hasNext()) {
                        element = it.next();
                        lName = element.text();
                    }
                    elem = doc.select("span");
                    it = elem.iterator();
                    while (it.hasNext()) {
                        element = it.next();
                        if(element.text().contains("Publicat la data")||element.text().contains("Publicat pe site")) {
                            String s = element.text().replace("Publicat la data ","").replace("Publicat pe site","").replace(" ","");
                            if(s.length()>=10)
                                dateInit = s.substring(0,10);
                        }
                        if(element.text().contains("în termen de")) {
                            dateFinal = "10";
                        }
                    }
                    elem = doc.select("title");
                    it = elem.iterator();
                    while (it.hasNext()) {
                        element = it.next();
                        descriere  = element.text();
                    }
                }catch (IOException e) {
                    end(2, adr);
                }

                try {
                    if(descriere==null)
                        descriere = "-";
                    if(dateFinal==null)
                        dateFinal="0";

                    publicationRepresentation.setIdentifier(DigestUtils.md5Hex(lName));
                    publicationRepresentation.setTitle(lName);
                    publicationRepresentation.setType(type0);
                    publicationRepresentation.setIssuer("munca");

                    String[] splitDate = Optional.ofNullable(dateInit).orElse("11.03.2017").split("\\.");
                    publicationRepresentation.setDate(splitDate[2] + "-" + splitDate[1] + "-" + splitDate[0]);
                    publicationRepresentation.setDescription(descriere);
                    publicationRepresentation.setFeedback_days(Optional.ofNullable(Integer.parseInt(dateFinal)).orElse(0));
                    ContactRepresentation contactRepresentation = new ContactRepresentation();
                    contactRepresentation.setEmail("dezbateri@mmuncii.ro");
                    contactRepresentation.setTel("-");
                    publicationRepresentation.setContact(contactRepresentation);
                    DocumentRepresentation documentRepresentation1 = null;
                    DocumentRepresentation documentRepresentation2 = null;
                    if(dateInit==null)
                        dateInit="-";
                    String infoF = "identifier proj"+String.valueOf(countP-1) + "\ntitle "+lName + "\ntype "+type0 + "\ninstitution munca" + "\ndate "+(dateInit).replace(".","-")+"\ndescription " + descriere + "\nfeedback_days "+dateFinal+"\ncontact dezbateri@mmuncii.ro"+"\ndocuments";
                    if(thePdf!=null&& type1!=null){
                        debug.setText(debug.getText() + "\nSaving " + thePdf);
                        infoF+="\ntype "+type1+"\nurl "+thePdf;
                       documentRepresentation1 =  new DocumentRepresentation();
                       documentRepresentation1.setType(type1);
                       documentRepresentation1.setUrl(thePdf);
                    }
                    if(thePdf2!=null && type2!=null) {
                        debug.setText(debug.getText() + "\nSaving " + thePdf2);
                        infoF+="\ntype "+type2+"\nurl "+thePdf2;
                        documentRepresentation2 =  new DocumentRepresentation();
                        documentRepresentation2.setType(type2);
                        documentRepresentation2.setUrl(thePdf2);
                    }
                    List<DocumentRepresentation> representations = new ArrayList<DocumentRepresentation>(2);
                    representations.add(documentRepresentation1);
                    representations.add(documentRepresentation2);
                    publicationRepresentation.setDocuments(representations);
                    //send publication

                    czlClient.apiV1().createPubliation(publicationRepresentation).execute();

                    //PrintWriter writerI = new PrintWriter(desc);
                    //writerI.print(infoF);
                    //writerI.close();
                } catch (Exception e) {
                    end(2, adr);
                }
            } else {

                try {
                    debug.setText(debug.getText() + "\nFetching links from " + adr);
                    if (webName != null) {
                        debug.setText(debug.getText() + "\nParsing info...");
                        Document doc = Jsoup.parse(new URL(adr).openStream(), "UTF-8", adr);
                        doc.outputSettings().charset();
                        Charset.forName("UTF-8");
                        Elements nextLinks = doc.select("a[href]");
                        Iterator<org.jsoup.nodes.Element> it = nextLinks.iterator();
                        org.jsoup.nodes.Element element;
                        while (it.hasNext() && (linkIndex < LINK_LIMIT)) {
                            element = it.next();
                            String aux = element.attr("abs:href");
                            if (adr.contains(SENAT)) {
                                if (aux.contains("http://www.mmuncii.ro/j33/index.php/ro/transparenta/proiecte-in-dezbatere/4"))
                                    if(!Arrays.asList(links).contains(aux)){
                                        links[linkIndex] = aux;
                                        debug.setText(debug.getText() + "\nGot link: " + links[linkIndex]);
                                        linkIndex++;
                                    }
                            } else {
                                if(!Arrays.asList(links).contains(aux)) {
                                    links[linkIndex] = aux;
                                    debug.setText(debug.getText() + "\nGot link: " + links[linkIndex]);
                                    linkIndex++;
                                }
                            }
                        }
                    }
                    //surf links
                    if(linkIndex>0)
                        for (int i = 0; i < linkIndex; i++)
                            surfWeb(links[i], depth + 1);

                    czlClient.close();
                } catch (Exception e) {
                    end(2, e.getMessage());
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
                debug.setText(debug.getText() + "\nFailed to create file info at " + link);
                return;
            }
            if (sig == 3) {
                debug.setText(debug.getText() + "\nError: " + link);
            }
        }
    }

    public void run(){

    }

    void start(){
        init(BEGIN);
        File dir = new File(System.getProperty("user.dir")+"\\muncii");
        if(!dir.exists())
            //noinspection ResultOfMethodCallIgnored
            dir.mkdir();
        surfWeb(BEGIN, 0);
        debug.setText(debug.getText() + "\nCrawling finished");
    }
}


public class Main {

    public static void main(String[] args) {
        new ThreadMinister().start();
    }

}
