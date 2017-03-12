using Crawler_Dialog_Grab;
using Crawler_Dialog_Structs;
using HtmlAgilityPack;
using Microsoft.VisualStudio.TestTools.UnitTesting;
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
    [TestClass]
    public class CreateJson
    {        
        [TestMethod]
        public void Identifier()
        {
            #region ARRANGE

            List<HtmlNode> articles = Grab.GrabArticles();
            PostMessage PostMsg;

            #endregion

            #region ACT
            Interpreter.Interpret(articles[0], out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg.identifier, "dialog_category-proiecte-de-acte-normative_post-6300");
            
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
            Interpreter.Interpret(articles[0], out PostMsg);
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
            Interpreter.Interpret(articles[0], out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg.type, "OTHER");

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
            Interpreter.Interpret(articles[0], out PostMsg);
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
            Interpreter.Interpret(articles[0], out PostMsg);
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
            Interpreter.Interpret(articles[0], out PostMsg);
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
            Interpreter.Interpret(articles[0], out PostMsg);
            #endregion

            #region ASSERT

            Assert.AreEqual(PostMsg.feedback_days, (uint)14);

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
            Interpreter.Interpret(articles[0], out PostMsg);
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
            Interpreter.Interpret(articles[0], out PostMsg);
            #endregion

            #region ASSERT
            
            Assert.AreEqual(PostMsg.documents[0].url, "http://dialogsocial.gov.ro/2017/01/consultare-publica-conect-catalogul-organizatiilor-neguvernamentale-pentru-evidenta-consultare-si-transparenta/");

            #endregion
        }

        

       
    }
}
