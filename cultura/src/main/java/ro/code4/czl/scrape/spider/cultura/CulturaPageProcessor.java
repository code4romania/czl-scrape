package ro.code4.czl.scrape.spider.cultura;

import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.ObjectUtils;
import org.apache.commons.lang3.StringUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Element;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.code4.czl.scrape.client.representation.DocumentRepresentation;
import ro.code4.czl.scrape.text.ProposalType;
import ro.code4.czl.scrape.text.RomanianMonth;
import us.codecraft.webmagic.Page;
import us.codecraft.webmagic.Site;
import us.codecraft.webmagic.processor.PageProcessor;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * @author Ionut-Maxim Margelatu (ionut.margelatu@gmail.com)
 */
public class CulturaPageProcessor implements PageProcessor {

  private static final Logger logger = LoggerFactory.getLogger(CulturaPageProcessor.class);

  private static final Pattern PATTERN_PROJECT_TYPE = Pattern
      .compile("(?:proiect de|proiectul de|proiect|proiectul) (?<projectType>\\w+)", Pattern.CASE_INSENSITIVE);

  private static final Pattern PATTERN_FEEDBACK_DEADLINE = Pattern
      .compile("(?:pana la data de|pana la data) (?<feedbackDeadlineDate>\\d{1,2}\\.\\d{2}\\.\\d{4})", Pattern.CASE_INSENSITIVE);

  private static final Pattern PATTERN_PROPOSAL_DATE = Pattern
      .compile("(?<day>\\d{1,2}) (?<month>\\w+) (?<year>\\d{4})", Pattern.CASE_INSENSITIVE);

  private static final Pattern PATTERN_CONTACT_EMAIL = Pattern
      .compile("(?:adresa de e-mail:|adresa de e-mail) (?<email>[A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,6})", Pattern.CASE_INSENSITIVE);

  private final SimpleDateFormat siteFeedbackDateFormat = new SimpleDateFormat("dd MM yyyy");
  private final DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("yyyy-MM-dd");

  private Site site = Site.me()
      .setRetryTimes(3)
      .setTimeOut(30_000)
      .setSleepTime(200)
      .setUserAgent("Chrome/56.0.2924.87");

  @Override
  public void process(Page page) {
    logger.info("Got status={} for url={}", page.getStatusCode(), page.getUrl());

    if (page.getUrl().toString().equalsIgnoreCase("http://www.cultura.ro/proiecte-acte-normative")) {
      // seed URL
      List<String> proposalLinks = page.getHtml().xpath("//*[@id='recomended-articles']/div/div/div/div[@class='recommended-title']").links().all();
      logger.info("Got proposalCount={} for url={}", proposalLinks.size(), page.getUrl());

      page.addTargetRequests(proposalLinks);
      page.setSkip(true);
    } else {
      // proposal URL

      // by default we ignore this result. only if we can extract all the data we need do we consider this result
      page.setSkip(true);

      String proposalPageTitle = page.getHtml().xpath("//*[@id='block-continutprincipalpagina']/div/article/div/div[2]/h1/span/text()").toString();

      String identifier = null;
      ProposalType type = null;
      String title = null;
      String description = null;
      final String institution = "cultura";
      String date = null;
      long feedbackDays = 0;
      Map<String, String> contact = new HashMap<>();
      List<DocumentRepresentation> documents = new ArrayList<>();

      if (proposalPageTitle.contains("|")) {
        // single proposal on the page

        logger.info("pageTitle={}", proposalPageTitle);

        title = proposalPageTitle;
        identifier = DigestUtils.md5Hex(title);

        List<String> proposalPageTitleParts = Arrays.stream(proposalPageTitle.split("\\|")).map(String::trim).collect(Collectors.toList());
        if (proposalPageTitleParts.size() == 2) {
          String proposalTitleType = proposalPageTitleParts.get(0);
          String proposalTitle = StringUtils.stripAccents(proposalPageTitleParts.get(1));
          if (proposalTitleType.toLowerCase().startsWith("dezbatere")) {
            Matcher projectTypeMatcher = PATTERN_PROJECT_TYPE.matcher(proposalTitle);
            String projectTypeLabel = projectTypeMatcher.find() ? projectTypeMatcher.group("projectType") : null;
            if (projectTypeLabel != null) {
              type = ProposalType.fromLabel(projectTypeLabel);
              logger.info("projectType={} projectTypeLabel={}", type, projectTypeLabel);
            }
          } else if (proposalTitleType.toLowerCase().startsWith("proiect")) {
            Matcher projectTypeMatcher = PATTERN_PROJECT_TYPE.matcher(proposalTitleType);
            String projectTypeLabel = projectTypeMatcher.find() ? projectTypeMatcher.group("projectType") : null;
            if (projectTypeLabel != null) {
              type = ProposalType.fromLabel(projectTypeLabel);
              logger.info("projectType={} projectTypeLabel={}", type, projectTypeLabel);
            }
          } else {
            logger.warn("Don't know how to parse {}", proposalPageTitle);
          }
        } else if (proposalPageTitleParts.size() >= 3) {

        }

        String extractedPageContent = page.getHtml().xpath("//*[@id='block-continutprincipalpagina']/div/article/div/div[2]/div[4]/div").toString();
        description = Jsoup.parse(extractedPageContent
                                      .replaceAll("<a([^>]+)>(.+?)</a>", "")
                                      .replaceAll("Fisiere[^:]*:", "<br/>")
                                      .replaceAll("Anexe:", "<br/>"))
            .text();

        page.getHtml().xpath("//*[@id='block-continutprincipalpagina']/div/article/div/div[2]/div[4]/div/ul/li/a").all().forEach(htmlLink -> {
          Element documentLink = Jsoup.parse(htmlLink).select("a").first();
          documents.add(new DocumentRepresentation(StringUtils.capitalize(documentLink.text().replaceFirst("^[^a-zA-Z]+", "").trim()),
                                                   documentLink.attr("href")));
        });

        String strippedContent = StringUtils.stripAccents(description);
        Matcher feedbackDeadlineMatcher = PATTERN_FEEDBACK_DEADLINE.matcher(strippedContent);
        String extractedFeedbackDeadlineDate = feedbackDeadlineMatcher.find() ? feedbackDeadlineMatcher.group("feedbackDeadlineDate") : null;
        if (extractedFeedbackDeadlineDate != null) {
          Date feedbackDeadlineDate;
          try {
            feedbackDeadlineDate = siteFeedbackDateFormat.parse(extractedFeedbackDeadlineDate.replaceAll("\\.", " "));
          } catch (ParseException e) {
            feedbackDeadlineDate = null;
          }
          if (feedbackDeadlineDate != null) {
            LocalDate now = LocalDate.now();
            LocalDate then = feedbackDeadlineDate.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();

            if (now.isBefore(then)) {
              feedbackDays = ChronoUnit.DAYS.between(then, now);
            }
          }
        }

        Matcher contactEmailMatcher = PATTERN_CONTACT_EMAIL.matcher(strippedContent);
        String contactEmail = contactEmailMatcher.find() ? contactEmailMatcher.group("email") : null;
        if (contactEmail != null) {
          contact.put("email", contactEmail);
        }

      } else {
        // multiple proposals on the page (sigh..)
        logger.warn("Found a page with multiple proposals url={}", page.getUrl());
      }

      String extractedDate = page.getHtml()
          .xpath("//*[@id='block-continutprincipalpagina']/div/article/div/div[2]/div[2]/span[3]/text()")
          .toString()
          .trim();
      Matcher proposalDateMatcher = PATTERN_PROPOSAL_DATE.matcher(extractedDate);
      if (proposalDateMatcher.find()) {
        int day = Integer.parseInt(proposalDateMatcher.group("day"));
        int month = RomanianMonth.fromLabel(proposalDateMatcher.group("month")).getNumber();
        int year = Integer.parseInt(proposalDateMatcher.group("year"));

        date = dateFormat.format(LocalDate.of(year, month, day));
      }

      if (ObjectUtils.allNotNull(identifier, description, title, type, institution, feedbackDays, date)) {
        // page.setSkip(false);

        page.putField("identifier", identifier);
        page.putField("description", description);
        page.putField("title", title);
        page.putField("type", type);
        page.putField("institution", institution);
        page.putField("feedbackDays", feedbackDays);
        page.putField("date", date);
        page.putField("documents", documents);
        page.putField("contact", contact);

        logger.info(page.getResultItems().toString());
      }
    }
  }

  @Override
  public Site getSite() {
    return site;
  }
}
