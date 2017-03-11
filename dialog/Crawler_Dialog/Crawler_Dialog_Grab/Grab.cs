using HtmlAgilityPack;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Crawler_Dialog_Grab
{
    public static class Grab
    {
        private const string dialog_path = "http://dialogsocial.gov.ro/categorie/proiecte-de-acte-normative/";
        public static List<HtmlNode> GrabArticles(string path = dialog_path)
        {
            HtmlWeb htmlWeb = new HtmlWeb();
            HtmlDocument document = htmlWeb.Load(path);
            List<HtmlNode> articles = document.GetElementbyId("content").Elements("article").ToList();
            return articles;
        }
    }
}
