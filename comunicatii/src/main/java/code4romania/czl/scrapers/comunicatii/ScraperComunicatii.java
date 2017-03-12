package code4romania.czl.scrapers.comunicatii;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import okhttp3.*;
import org.apache.commons.lang3.StringUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.nodes.Node;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.rmi.server.UID;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by radug on 11/03/2017.
 */
public class ScraperComunicatii {


    private static final String DATE_REGEX = "([0-2][0-9]|30|31)\\.[0|1][0-9]\\.[0-9]{4}";
    private static final String DATE_PUBLICARE_REGEX = "(publicat).+" + DATE_REGEX;
    private static final String DATE_FEEDBACK_REGEX = "(comentarii).+"+DATE_REGEX;

    public static void main(String[] args){

        List<ComunicatiiBean> outputList = new ArrayList<ComunicatiiBean>();

        String url = "http://www.comunicatii.gov.ro/?page_id=3517";
        Document document = null;
        try {
            document = Jsoup.connect(url).get();
//            document = Jsoup.parse(ScraperComunicatii.class.getResourceAsStream("/Proiecte de Acte Normative _ Comunicatii.gov.ro.html"), "UTF-8","");
        } catch (IOException e) {
            e.printStackTrace();
        }

        Elements div_wpb_wrappers = document.select("div.wpb_content_element").select("div.wpb_wrapper");
        String text = div_wpb_wrappers.first().text();
        System.out.println(div_wpb_wrappers.size());

//        div_wpb_wrappers.get(0)..forEach(
//                item -> System.out.println(item)
//        );

        List<Node> groupedElements = new ArrayList<>();
//        div_wpb_wrappers.spliterator().forEachRemaining();
        div_wpb_wrappers.listIterator().forEachRemaining(
                item1-> {
                    item1.childNodes().forEach(item -> {
//                                System.out.println(item);
                                if ("hr".equals(item.nodeName())) {

                                    ComunicatiiBean cBean = new ComunicatiiBean();
                                    outputList.add(cBean);
//                                    System.out.print("-------------------------");
                                    //System.out.println(groupedElements.size());
                                    StringBuffer description = new StringBuffer();

                                    groupedElements.forEach(gEl -> {
                                        gEl.childNodes().forEach(cNode ->{
//                                            System.out.println(cNode.nodeName());
                                            switch (cNode.nodeName()){
                                                case "#text" : {
                                                    description.append(cNode.toString());
                                                break;}
                                                case "a": {
                                                    description.append(getTextFromNode(cNode));
                                                    cBean.addDocument(cNode.attr("href"), getTextFromNode(cNode));
                                                }
                                            }


                                        });
                                    });
                                    cBean.setDescription(description.toString());
                                    cBean.setTitle(getTextFromNode(groupedElements.get(0)));

                                    extractDate(cBean);
                                    String feedback = extractFeedbackDate(cBean.getDescription(), DATE_FEEDBACK_REGEX);
                                    String start = extractFeedbackDate(cBean.getDescription(), DATE_PUBLICARE_REGEX);

                                    cBean.setFeedback_days(calculateFeedbackDays(start, feedback));
                                    cBean.setType(deductType(description.toString()));
//                                    System.out.println(cBean.toJson());

                                    cBean.setIdentifier(new UID().toString()+":"+cBean.getType()+":"+cBean.getDate());
                                    groupedElements.clear();
                                }else{
                                    if(StringUtils.isNotBlank(item.toString())) {
                                        groupedElements.add(item);
                                    }
                                }

                            });

//                    System.out.println(item)
                }
        );

        outputList.forEach(el -> {
            System.out.println(el.toJson());
            System.out.println("sending");
                    try {
                        String result = post("http://czl-api.code4.ro/api/publications/", el.toJson());
                        System.out.println(result);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
        );
       }

    private static void extractDate(ComunicatiiBean cBean) {
        Pattern p = Pattern.compile(DATE_REGEX);

        Matcher matcher = p.matcher(cBean.getDescription());
        while (matcher.find()){
            String date = cBean.getDate();
            cBean.setDate(matcher.group(), "dd.MM.yyyy");
            System.out.println( matcher.group());
        }
    }

    private static String  extractFeedbackDate(String description, String dateFeedbackRegex){
        Pattern pFeedback = Pattern.compile(dateFeedbackRegex);
        Pattern pDate = Pattern.compile(DATE_REGEX);
        Matcher m = pFeedback.matcher(description);
        try {
            m.find();
            Matcher mDate = pDate.matcher(m.group());
            mDate.find();
            return mDate.group();
        }catch (IllegalStateException e){
            e.printStackTrace();
        }
        return "";
    }


    private static String getTextFromNode(Node cNode) {
        StringBuffer text = new StringBuffer();
        cNode.childNodes().forEach(node -> {
            switch (node.nodeName()){
                case "#text": text.append(node.toString());break;
                case "a" : text.append(getTextFromNode(node));break;
            }
        });
        return text.toString();
    }

    private static void selectLinks(Document document) {
        Elements links = document.select("a");
        List<ComunicatiiBean> outputList = new ArrayList<ComunicatiiBean>();
        for (Element link : links) {
            ComunicatiiBean cBean = new ComunicatiiBean();
            outputList.add(cBean);
            ComunicatiiBean.Document cDoc = new ComunicatiiBean.Document();
            extractDocument(link, cBean, cDoc);

            link.textNodes().forEach(linknode -> System.out.println("link node: " + linknode.toString()));

            System.out.println(cBean);
        }
    }

    private boolean isSeparator(Element e){
        e.text();
        return false;
    }
    private void processRelatedElements(List<Element> elements){
     }

    private static void extractDocument(Element link, ComunicatiiBean cBean, ComunicatiiBean.Document cDoc) {
        String docUrl = link.attr("href");
        cDoc.setUrl(docUrl);
        try {
            cDoc.setType(docUrl.substring(docUrl.lastIndexOf('.')));

        }catch (Exception e){
            e.printStackTrace();
        }
        cBean.getDocuments().add(cDoc);
    }

    public static String calculateFeedbackDays(String dataPublicare, String dataFeedback){
        // Converting date to Java8 Local date
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("dd.MM.yyyy");
        try {
            LocalDate startDate = LocalDate.parse(dataPublicare, fmt);
            LocalDate endDate = LocalDate.parse(dataFeedback, fmt);
            // Range = End date - Start date
            Long range = ChronoUnit.DAYS.between(startDate, endDate);

            return range.toString();
        }catch (Exception e){
            e.printStackTrace();
        }
        return "0";
    }

    public static String deductType(String description){
        String type ="";
        if (description.contains("Proiect de Lege")){
            type = type + "LEGE";
        }
        if (description.contains("Ordonanță") || description.contains("Ordonanţă")){
            type = type + "OG";
        }
        if (description.contains("Hotărâre")){
            type = type + "HG";
        }
        return  type;
    }

    public static final MediaType JSON
            = MediaType.parse("application/json; charset=utf-8");

    static OkHttpClient client = new OkHttpClient();

    static String post(String url, String json) throws IOException {
        RequestBody body = RequestBody.create(JSON, json);
        Request request = new Request.Builder()
                .addHeader("Authorization", "token comunicatii-very-secret-key")
                .addHeader("Content-Type", "application/json; charset=utf-8")
                .url(url)
                .post(body)
                .build();
        Response response = client.newCall(request).execute();
        return response.body().string();
    }
}