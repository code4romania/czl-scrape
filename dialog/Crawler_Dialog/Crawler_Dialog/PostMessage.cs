using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Crawler_Dialog
{
    public class PostMessage
    {
        string identifier; // "lawproposal-first-document-name-slug-or-something", // un identificator unic, predictibil (repetabil), pereferabil human-readable
        string title; // "title": "Proiectul de ordin al ministrului justiției pentru aprobarea Regulamentului privind organizarea și desfășurarea activităților și programelor educative, de asistență psihologică și asistență socială din locurile de deținere aflate în subordinea Aministrației Naționale a Penitenciarelor", // titlul actului legislativ propus
        string type; // "type": "HG", // HG, OG, OUG, PROIECT
        string institution; //  "institution": "justitie", // ID-ul platformei din care provine actul legislativ
        DateTime date; //  "date": "2017-03-08", // ISO 8601
        string description; //  "description": "Cookie jelly-o sesame snaps donut sesame snaps sweet roll chocolate. Tootsie roll pie bonbon tart chocolate cake. Gummi bears gummies chupa chups ice cream croissant donut marzipan. Macaroon bear claw halvah carrot cake liquorice powder.",
        uint feedback_days; //  "feedback_days": 12, // numarul zilelor disponibile pentru feedback
        Contact contact; //  "contact": {"tel": "12345", "email": "feedback@example.org"}, // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr"
        List<Document> documents; //  "documents": [ // array de dictionare
    }
}
