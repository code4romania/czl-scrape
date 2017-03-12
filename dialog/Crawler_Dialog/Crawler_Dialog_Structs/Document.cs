using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Crawler_Dialog_Structs
{
    public class Document
    {
        public string type; // "type": "anexa", // free text momentan
        public string url; //      "url": "http://www.just.ro/wp-content/uploads/2017/02/Proiect.docx" // da, este un link catre un document oficial de la MJ
        public override string ToString()
        {
            return $"type: {type} + url: {url}";
        }
    }
}
