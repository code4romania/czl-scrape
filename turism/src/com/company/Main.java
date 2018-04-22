package com.company;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.*;
import java.net.URL;
import java.net.URLConnection;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;
import java.nio.charset.Charset;
import java.util.Iterator;
import java.util.Vector;

class Scraper extends Thread{
    String root;
    Vector<String> keywords;
    String out;

    Scraper(String root,String pathOutput){
        this.root = root;
        out = pathOutput;
        keywords = new Vector<>();
    }

    void addKeywords(String ... keywords){
        for(String keyword : keywords)
            this.keywords.add(keyword);
    }

    public void run(){
        try {
            String content = getUrlSource(root);

            Document docI = Jsoup.parse(content, root);
            docI.outputSettings().charset();
            Charset.forName("UTF-8");
            Elements nextLinksI = docI.select("p");
            Iterator<Element> itI = nextLinksI.iterator();
            //initializam citirea
            while (itI.hasNext()) {
                org.jsoup.nodes.Element elementI = itI.next();
                if(elementI.text().contains("Proiect")){
                    String link = elementI.child(0).attr("abs:href");
                    if(link.contains("pdf")) {
                        String[] nr = link.split("/");
                        String name = out+"Proiecte/"+nr[nr.length-1];
                        try{
                            URL website = new URL(link);
                            ReadableByteChannel rbc = Channels.newChannel(website.openStream());
                            FileOutputStream fos = new FileOutputStream(name);
                            fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
                        }catch (Exception e){
                            e.printStackTrace();
                        }
                    }
                }
            }

            nextLinksI = docI.select("a");
            itI = nextLinksI.iterator();
            //initializam citirea
            while (itI.hasNext()) {
                org.jsoup.nodes.Element elementI = itI.next();
                if(elementI.text().contains("anexa")||elementI.text().contains("Anexa")){
                    String link = elementI.attr("abs:href");
                    if(link.contains("pdf")) {
                        String[] nr = link.split("-");
                        String name = out+"Anexe/Anexa" +nr[nr.length-1];
                        try{
                            URL website = new URL(link);
                            ReadableByteChannel rbc = Channels.newChannel(website.openStream());
                            FileOutputStream fos = new FileOutputStream(name);
                            fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
                        }catch (Exception e){
                            e.printStackTrace();
                        }
                    }
                }
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }

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
}

public class Main {

    public static void main(String[] args) {
        // write your code here
        Scraper scraper = new Scraper("http://turism.gov.ro/transparenta-decizionala-2/","out_files/");

        scraper.addKeywords();  //TODO - keywords??
        scraper.start();
    }
}
