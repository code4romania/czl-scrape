package ro.code4.czl.scrape.spider.senat;

import org.apache.commons.lang3.StringUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Element;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.code4.czl.scrape.client.representation.DocumentRepresentation;
import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.processor.PageProcessor;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class SenatPageProcessor implements PageProcessor {

  private static final Logger logger = LoggerFactory.getLogger(SenatPageProcessor.class);

  private final SimpleDateFormat siteFormat = new SimpleDateFormat("dd-MM-yyyy");
  private final SimpleDateFormat expectedFormat = new SimpleDateFormat("yyyy-MM-dd");

  private Site site = Site.me()
      .setRetryTimes(3)
      .setTimeOut(30_000)
      .setSleepTime(200)
      .setUserAgent("Chrome/56.0.2924.87");

  @Override
  public void process(Page page) {
    logger.info("Got status={} for url={}", page.getStatusCode(), page.getUrl());

    if (page.getUrl().toString().equalsIgnoreCase("https://www.senat.ro/LegiProiect.aspx")) {
      // seed URL
      List<String> proposalLinks = page.getHtml().xpath("//*[@id='GridViewProiecte']/tbody/tr/td[@align='center']").links().all();
      logger.info("Got proposalCount={} for url={}", proposalLinks.size(), page.getUrl());
      page.addTargetRequests(proposalLinks);
      page.setSkip(true);
    } else {
      // proposal URL
      String identifier = page.getHtml().xpath("//*[@id='ctl00_B_Center_ctl06_viewFisa_lblNr']/text()").toString();
      String description = page.getHtml().xpath("//*[@id='ctl00_B_Center_ctl06_grdTitlu_ctl02_Label1']/text()").toString();
      String title = description;
      String type = "LEGE";
      String institution = "senat";
      String extractedDate = null;
      Date date;
      try {
        extractedDate = page.getHtml().xpath("//*[@id='ctl00_B_Center_ctl06_grdDerulare_ctl02_Label1']/text()").toString();
        date = siteFormat.parse(extractedDate);
      } catch (ParseException e) {
        date = new Date();
        logger.warn("Failed to parse date from string={} and defaulted to today", extractedDate);
      }
      String expectedDate = expectedFormat.format(date);
      Map<String, String> contact = new HashMap<>();
      contact.put("tel", "021 315 8942");
      contact.put("email", "infopub@senat.ro");

      List<DocumentRepresentation> documents = new ArrayList<>();

      page.getHtml().xpath("//*[@id='ctl00_B_Center_Accordion1']/div[6]/a").all().forEach(htmlLink -> {
        Element documentLink = Jsoup.parse(htmlLink).select("a").first();
        documents.add(new DocumentRepresentation(StringUtils.capitalize(documentLink.text().replaceFirst("^[^a-zA-Z]+", "").trim()),
                                                 documentLink.attr("href").replace("\\", "/")));
      });

      page.putField("identifier", identifier);
      page.putField("description", description);
      page.putField("title", title);
      page.putField("type", type);
      page.putField("institution", institution);
      page.putField("date", expectedDate);
      page.putField("documents", documents);
      page.putField("contact", contact);
    }
  }

  @Override
  public Site getSite() {
    return site;
  }
}
