using Crawler_Dialog_Grab;
using Crawler_Dialog_Interpret;
using Crawler_Dialog_Structs;
using HtmlAgilityPack;
using Newtonsoft.Json;
using NLog;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace Crawler_Dialog
{
    class Program
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();
        static void Main(string[] args)
        {
            List<HtmlNode> articles = Grab.GrabArticles();
            
            foreach (HtmlNode a in articles)
            {
                PostMessage post;
                try
                {
                    Interpreter.Interpret(a, out post);
                    var json = JsonConvert.SerializeObject(post);
                    string result = "";
                    using (var client = new WebClient())
                    {
                        client.Headers[HttpRequestHeader.ContentType] = "application/json";
                        result = client.UploadString("http://czl-api.code4.ro/api/", "POST", json);
                    }
                    Console.WriteLine(result);
                }
                catch(Exception ex)
                {
                    logger.Error(ex);
                }
            }
            
        }
    }
}
