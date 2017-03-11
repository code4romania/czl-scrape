using Crawler_Dialog_Grab;
using Crawler_Dialog_Structs;
using HtmlAgilityPack;
using Microsoft.VisualStudio.TestTools.UnitTesting;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;


namespace Crawler_Dialog_Interpret
{
    [TestClass]
    public class CreateJson
    {
        private const string EndOfArticleMarker = ".*(?=<!-- Facebook Comments Plugin for WordPress: http://peadig.com/wordpress-plugins/facebook-comments/)";
        List<string> validFileExtensions = new List<string> {
            ".docs", ".doc", ".txt", ".crt", ".xls", ".xml", ".pdf", "", ".docx", ".xlsx"
        };
        [TestMethod]
        public void Identifier()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg.identifier, "czl_dialog_category-proiecte-de-acte-normative_post-6300");
            
            #endregion
        }
        [TestMethod]
        public void Title()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg.title, "Consultare publică CONECT Catalogul Organizațiilor Neguvernamentale pentru Evidență, Consultare și Transparență");

            #endregion
        }
        [TestMethod]
        public void Type()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg, "");

            #endregion
        }
        [TestMethod]
        public void Institution()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT

            Assert.AreEqual(PostMsg.institution, "dialog");

            #endregion
        }
        [TestMethod]
        public void Date()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT            
            Assert.AreEqual(PostMsg.date, DateTime.Parse("2017-01-19T11:22:06+00:00"));
            #endregion
        }
        [TestMethod]
        public void Description()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT
            //Console.WriteLine(PostMsg.description);
            Assert.AreEqual(PostMsg.description, "Ministerul Consultării Publice și Dialogului Social (MCPDS) lansează, astăzi, 19 ianuarie a.c. în consultare publică instrumentul CONECT Catalogul organizațiilor neguvernamentale pentru evidență, consultare și transparență. „Ne dorim să oferim cât mai mult sprijin comunităților de expertiză și să le aducem mai aproape de decizia publică. Acest lucru...");

            #endregion
        }
        [TestMethod]
        public void FeedbackDays()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT

            Assert.AreEqual(PostMsg, "");

            #endregion
        }
        [TestMethod]
        public void ContactEmail()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg.contact.email, "conect@dialogsocial.gov.ro");

            #endregion
        }
        [TestMethod]
        public void Documents()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpret(articles[0].OuterHtml, out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg.documents[0].url, "http://dialogsocial.gov.ro/2017/01/consultare-publica-conect-catalogul-organizatiilor-neguvernamentale-pentru-evidenta-consultare-si-transparenta/");

            #endregion
        }

        private void Interpret(string input, out PostMessage postMsg)
        {
            postMsg = new PostMessage();

            #region DATE
            string dateMatch = Regex.Match(input, "(?<=datetime=\").*(?=\")").Value;

            postMsg.date = DateTime.Parse(CustomTrimText(dateMatch));

            #endregion

            #region DESCRIPTION
            Match descriptionMatch = GetMatches(input, "<p>(.*)</p>")[0];

            postMsg.description = CustomTrimText(descriptionMatch.Value);
            #endregion

            #region LIST OF DOCUMENTS && CONTACT

            MatchCollection links = GetMatches(input, "<a[^>]* href=\"([^ \"]*)\"");
            Match link = links[links.Count - 1];
            List<Document> docs = new List<Document> { new Document { url = CustomTrimText(link.ToString()).Replace("\"", ""), type = "article" } };
            
            //First doc is full article
            HtmlNode FullArticle = Grab.GrabArticles(docs[0].url)[0];

            #region CONTACT            

            string fullArt = GetMatches(FullArticle.InnerText, EndOfArticleMarker)[0].ToString();
            string emails = AppendEmails(fullArt);
            postMsg.contact = new Contact { email = emails.ToString() };

            #endregion

            #region LIST OF PDFS, LINKS, YOUTUBE VIDEOS ETC           
            string searchForLinksToDocs = GetMatches(FullArticle.InnerHtml, EndOfArticleMarker)[0].ToString();
           
            var docsMatches = GetMatches(searchForLinksToDocs, "(?<=<a href=\")(.*?)(?=\")");

            List<Document> docsToAdd = ExtractDocs(docsMatches);

            docs.AddRange(docsToAdd);
            #endregion

            //< !--Facebook Comments Plugin for WordPress: http://peadig.com/wordpress-plugins/facebook-comments/ -->	
            postMsg.documents = docs;

            #endregion

            #region IDENTIFIER
            //
            string id = GetMatches(input, "post-[\\d]+")[0].ToString();
            postMsg.identifier = $"czl_dialog_category-proiecte-de-acte-normative_{CustomTrimText(id)}";
            #endregion

            #region INSTITUTION
            postMsg.institution = "dialog";
            #endregion

            #region TITLE            

            string titleMatch = Regex.Match(input, "(?<=title=\").*(?=\" rel)").Value;
            postMsg.title = CustomTrimText(titleMatch);

            #endregion


            //postMsg.identifier = GetMatches(input, "(< h2)(.*\n ?)(<\/h2)")[0].ToString();
        }

        private List<Document> ExtractDocs(MatchCollection docsMatches)
        {
            List<Document> docsToReturn = new List<Document>();
            try
            {                
                foreach(var d in docsMatches )
                {
                    string path = d.ToString();
                    if(Path.HasExtension(path))
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
            catch
            {
                
            }
            return docsToReturn;
        }

        private static string AppendEmails(string fa)
        {
            Regex emailsRgx = new Regex(@"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*",
                            RegexOptions.Compiled | RegexOptions.IgnoreCase);
            StringBuilder emails = new StringBuilder();
            foreach (var e in emailsRgx.Matches(fa))
            {
                if (emails.Length > 0)
                {
                    emails.Append("; ");
                }
                emails.Append(e);
            }

            return emails.ToString();
        }

        private static MatchCollection GetMatches(string input, string pattern)
        {
            return Regex.Matches(input, pattern, 
                            RegexOptions.Multiline & RegexOptions.IgnoreCase | RegexOptions.Singleline | RegexOptions.IgnoreCase);
        }

        private string CustomTrimText(string description)
        {
            description = Regex.Replace(description, "&hellip;", "...");
            description = Regex.Replace(Regex.Replace(description,
                @"(\r)|(\n)|(\t)|(&nbsp;)|<a href=|<p>|&([^;]*);|</p>|(\\s+){2,}", " "), @"(\s+)", " ").Trim();
            return description;
        }
    }
}
