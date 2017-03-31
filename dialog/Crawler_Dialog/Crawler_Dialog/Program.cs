using Crawler_Dialog_Grab;
using Crawler_Dialog_Interpret;
using Crawler_Dialog_Structs;
using HtmlAgilityPack;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using Nito.AsyncEx;
using NLog;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace Crawler_Dialog
{
    class Program 
    {
        private static Logger logger = LogManager.GetCurrentClassLogger();

        static void Main(string[] args)
        {
            AsyncContext.Run(() => MainAsync(args));
        }

        static async void MainAsync(string[] args)
        {
            List<HtmlNode> articles = Grab.GrabArticles();
            int articleNo = 0;
            foreach (HtmlNode a in articles)
            {
                articleNo++;                
                Console.Write($"Beginning scrapping article {articleNo}. ");
                PostMessage post;
                try
                {
                    Interpreter.Interpret(a, out post);
                    var json = JsonConvert.SerializeObject(post, new IsoDateTimeConverter() { DateTimeFormat = "yyyy-MM-dd" });
                    Console.WriteLine($"Post article {articleNo} API result: ");
                    Console.ForegroundColor = ConsoleColor.Red;                    
                    Console.WriteLine(await PostArticle.Post(json));
                    Console.ForegroundColor = ConsoleColor.White;
                    Console.WriteLine("-------------------------------------------------------");
                }
                catch (Exception ex)
                {
                    logger.Error(ex);
                }
            }
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"{articleNo} articles scrapped. Press any key to exit.");
            Console.ReadLine();

        }

    }
    public static class PostArticle
    {
        public static async Task<string> Post(string json)
        {
            var httpContent = new StringContent(json, Encoding.UTF8, "application/json");

            using (var httpClient = new HttpClient())
            {
                httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Token", "dialog-very-secret-key");
                var httpResponse = await httpClient.PostAsync("http://czl-api.code4.ro/api/publications/", httpContent);

                if (httpResponse.Content != null)
                {
                    var responseContent = await httpResponse.Content.ReadAsStringAsync();
                    return responseContent;
                }
            }
            return "";
        }
    }
}
