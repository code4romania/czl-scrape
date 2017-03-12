using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Crawler_Dialog_Structs
{
    public class PostMessage
    {
        public string identifier; // "lawproposal-first-document-name-slug-or-something", // un identificator unic, predictibil (repetabil), pereferabil human-readable
        public string title; // "title": "Proiectul de ordin al ministrului justiției pentru aprobarea Regulamentului privind organizarea și desfășurarea activităților și programelor educative, de asistență psihologică și asistență socială din locurile de deținere aflate în subordinea Aministrației Naționale a Penitenciarelor", // titlul actului legislativ propus
        public string type; // "type": "HG", // HG, OG, OUG, PROIECT
        public string institution; //  "institution": "justitie", // ID-ul platformei din care provine actul legislativ
        public DateTime date; //  "date": "2017-03-08", // ISO 8601
        public string description; //  "description": "Cookie jelly-o sesame snaps donut sesame snaps sweet roll chocolate. Tootsie roll pie bonbon tart chocolate cake. Gummi bears gummies chupa chups ice cream croissant donut marzipan. Macaroon bear claw halvah carrot cake liquorice powder.",
        public uint feedback_days; //  "feedback_days": 12, // numarul zilelor disponibile pentru feedback OPTIONAL
        public Contact contact; //  "contact": {"tel": "12345", "email": "feedback@example.org"}, // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr" OPTIONAL
        public List<Document> documents; //  "documents": [ //array de dictionare

        public override string ToString()
        {
            string s = string.Empty;
            foreach (var d in documents)
            {
                s += documents.ToString() + " ";
            }
            return s;
        }
    }
}
