using Crawler_Dialog_Grab;
using Crawler_Dialog_Structs;
using HtmlAgilityPack;
using NLog;
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace Crawler_Dialog_Interpret
{
    public static class Interpreter
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        // List of possible keywords
        static Dictionary<string, string> filtruActNormativ = new Dictionary<string, string> {
           { "lege", "LEGE" },
           { "hotarare de guvern", "HG" },
           { "hotarare a guvernului", "HG" },
           { "ordonanta de guvern", "OG" },
           { "ordonanta de urgenta", "OUG"},
           { "ordin de ministru", "OM" },
           { "ordinul", "OM" }
       };

        

           
        private const string EndOfArticleMarker = ".*(?=<!-- Facebook Comments Plugin for WordPress: http://peadig.com/wordpress-plugins/facebook-comments/)";
        private static string[] validFileExtensions = new string[] {
            ".docs", ".doc", ".txt", ".crt", ".xls", ".xml", ".pdf", "", ".docx", ".xlsx"
        };
        public static void Interpret(HtmlNode input, out PostMessage postMsg)
        {
            postMsg = new PostMessage();
            HtmlNode FullArticle = null;
            List<Document> docs = null;
            #region LIST OF DOCUMENTS && CONTACT
            try
            {
                MatchCollection links = GetMatches(input.OuterHtml, "<a[^>]* href=\"([^ \"]*)\"");
                Match link = links[links.Count - 1];
                docs = new List<Document> { new Document { url = CustomTrimText(link.ToString()).Replace("\"", ""), type = "article" } };

                //First doc is full article
                FullArticle = Grab.GrabArticles(docs[0].url)[0];
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #region CONTACT            
            try
            {
                Match fullArt = GetMatches(FullArticle.InnerText, EndOfArticleMarker)[0];
                if (fullArt.Success)
                {
                    postMsg.contact = new Contact { email = AppendEmails(fullArt.Value) };
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #endregion

            #region LIST OF PDFS, LINKS, YOUTUBE VIDEOS ETC   
            try
            {
                Match searchForLinksToDocs = GetMatches(FullArticle.InnerHtml, EndOfArticleMarker)[0];
                if (searchForLinksToDocs.Success)
                {
                    MatchCollection docsMatches = GetMatches(searchForLinksToDocs.Value, "(?<=<a href=\")(.*?)(?=\")");
                    if (docsMatches.Count > 0)
                    {
                        List<Document> docsToAdd = ExtractDocs(docsMatches);
                        docs.AddRange(docsToAdd);
                    }
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #endregion

            //< !--Facebook Comments Plugin for WordPress: http://peadig.com/wordpress-plugins/facebook-comments/ -->	
            postMsg.documents = docs;

            #endregion

            #region DATE && FEEDBACK_DAYS
            try {
                Match dateMatch = Regex.Match(input.OuterHtml, "(?<=datetime=\").*(?=\")");
                if (dateMatch.Success)
                {
                    postMsg.date = DateTime.Parse(CustomTrimText(dateMatch.Value));

                    #region FEEDBACK DAYS
                    Match untilDateMatch = GetUntilDateMatch(FullArticle);
                    if (untilDateMatch.Success)
                    {
                        string untilDateToParse = untilDateMatch.Value.Substring(0, untilDateMatch.Value.IndexOf('.'));
                        Thread.CurrentThread.CurrentCulture = new CultureInfo("ro-RO");
                        DateTime ParsedDate = DateTime.Parse(untilDateToParse);
                        DateTime ProcessedDate = new DateTime(postMsg.date.Year, ParsedDate.Month, ParsedDate.Day);
                        if (ProcessedDate < postMsg.date)
                        {
                            ProcessedDate.AddYears(1);
                        }
                        if (ProcessedDate > postMsg.date)
                        {
                            postMsg.feedback_days = (uint)Math.Abs((ProcessedDate - postMsg.date.Date).Days);
                        }
                    }

                    postMsg.date = DateTime.Parse(CustomTrimText(dateMatch.Value));
                    #endregion

                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #endregion

            #region DESCRIPTION
            try
            {
                Match descriptionMatch = GetMatches(input.OuterHtml, "<p>(.*)</p>")[0];
                if (descriptionMatch.Success)
                {
                    postMsg.description = CustomTrimText(descriptionMatch.Value);
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #endregion

            #region IDENTIFIER
            try
            {
                Match id = GetMatches(input.OuterHtml, "post-[\\d]+")[0];
                if (id.Success)
                {
                    postMsg.identifier = $"dialog_category-proiecte-de-acte-normative_{CustomTrimText(id.Value)}";
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #endregion

            #region INSTITUTION
            try
            {
                postMsg.institution = "dialog";
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #endregion

            #region TITLE            
            try
            {
                Match titleMatch = Regex.Match(input.OuterHtml, "(?<=title=\").*(?=\" rel)");
                if (titleMatch.Success)
                {
                    postMsg.title = CustomTrimText(titleMatch.Value);
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            #endregion

            #region TYPE
            // Default value, in case title contains no matches
            postMsg.type = "OTHER";
            // Check if input text contains keywords, and adjust type to the first match.

            string txtForType = RemoveDiacritics(postMsg.title);
            foreach (var e in filtruActNormativ)
            {
                if (txtForType.ToLower().Contains(e.Key))
                {
                    postMsg.type = e.Value;
                    break;
                }
            }


            #endregion

        }

        #region UTILS
        private static Match GetUntilDateMatch(HtmlNode FullArticle)
        {
            try
            {
                string normalizedString = RemoveDiacritics(FullArticle.InnerText);

                Match returnValue = Regex.Match(normalizedString, @"(?<=pana la data de).*",
                        RegexOptions.Multiline & RegexOptions.IgnoreCase);

                if (returnValue.Success == false)
                {
                    returnValue = Regex.Match(normalizedString, @"(?<=pana pe data de).*",
                        RegexOptions.Multiline & RegexOptions.IgnoreCase);
                }
                if (returnValue.Success == false)
                {
                    returnValue = Regex.Match(normalizedString, @"(?<=data de).*",
                       RegexOptions.Multiline & RegexOptions.IgnoreCase);
                }

                return returnValue;
            }
            catch (Exception ex)
            {
                logger.Error(ex);
                throw ex;
            }
        }
        static string RemoveDiacritics(string input)
        {
            StringBuilder builder = new StringBuilder();
            try
            {
                string normalized = input.Normalize(NormalizationForm.FormD);


                foreach (char ch in normalized)
                {
                    if (CharUnicodeInfo.GetUnicodeCategory(ch) != UnicodeCategory.NonSpacingMark)
                    {
                        builder.Append(ch);
                    }
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            return builder.ToString().Normalize(NormalizationForm.FormC);
        }
        private static List<Document> ExtractDocs(MatchCollection docsMatches)
        {
            List<Document> docsToReturn = new List<Document>();
            try
            {
                foreach (var d in docsMatches)
                {
                    string path = d.ToString();
                    if (Path.HasExtension(path))
                    {
                        if (validFileExtensions.Contains(Path.GetExtension(path)))
                        {
                            Document newDoc = new Document()
                            {
                                type = Path.GetExtension(path),
                                url = path
                            };
                            docsToReturn.Add(newDoc);
                        }
                    }
                    else
                    {
                        Document newDoc = new Document()
                        {
                            type = "link",
                            url = path
                        };
                        docsToReturn.Add(newDoc);
                    }
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            return docsToReturn;
        }
        private static string AppendEmails(string fa)
        {
            StringBuilder emails = new StringBuilder();
            try
            {
                Regex emailsRgx = new Regex(@"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*",
                                RegexOptions.Compiled | RegexOptions.IgnoreCase);
                foreach (var e in emailsRgx.Matches(fa))
                {
                    if (emails.Length > 0)
                    {
                        emails.Append("; ");
                    }
                    emails.Append(e);
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex);
            }
            return emails.ToString();
        }
        private static MatchCollection GetMatches(string input, string pattern)
        {
            try
            {
                return Regex.Matches(input, pattern,
                            RegexOptions.Multiline & RegexOptions.IgnoreCase | RegexOptions.Singleline | RegexOptions.IgnoreCase);
            }
            catch (Exception ex)
            {
                logger.Error(ex);
                throw ex;
            }
        }
        private static string CustomTrimText(string description)
        {
            try
            {
                description = Regex.Replace(description, "&hellip;", "...");
                description = Regex.Replace(Regex.Replace(description,
                    @"(\r)|(\n)|(\t)|(&nbsp;)|<a href=|<p>|&([^;]*);|</p>|(\\s+){2,}", " "), @"(\s+)", " ").Trim();
                return description;
            }
            catch (Exception ex)
            {
                logger.Error(ex);
                throw ex;
            }
        }
        #endregion
    }
}
