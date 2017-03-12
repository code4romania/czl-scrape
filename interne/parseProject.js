let removeDiacritics = require('diacritics').remove,
    cheerio = require('cheerio');

/** ====== MAIN ====== */

function parseProject($, URL) {
    let parsedResult = {
        identifier: null, // un identificator unic, predictibil (repetabil), pereferabil human-readable
        title: null, // titlul actului legislativ propus
        type: null, // HG, OG, OUG, PROIECT
        institution: "economie", // ID-ul platformei din care provine actul legislativ
        date: null, // ISO 8601
        feedback_days: null, // numarul zilelor disponibile pentru feedback
        contact: {email: null}, // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr"
        documents: [ // array de dictionare
            {
                type: null, // free text momentan
                url: null // da, este un link catre un document oficial de la MJ
            }
        ]
    };

    $ = cheerio.load(`
        <div style="width:100%; padding-top:5px; padding-bottom:1px; margin-bottom:2px; background-color:#1495F0; ">
                <p style="color:#FFFFFF"><!-- InstanceBeginEditable name="editare data transparenta" -->
                <strong>
                Publicat în data de - 21.11.2016                 </strong>
				<!-- InstanceEndEditable --></p>
              </div>
              
              <p>ORDINUL MINISTRULUI AFACERILOR INTERNE Nr. _____ din ____ . ____ 2016 pentru modificarea Ordinului ministrului administraţiei şi internelor nr.157/2012 privind forma şi conţinutul permisului de conducere [...]<br>
              <strong>Text integral</strong> <img src="images/arrow_red.png" vspace="2" align="bottom">&nbsp;&nbsp; <a href="documente/transparenta/Ordin forma permis conducere.pdf" target="_blank">( descarca fisier in format "pdf" )</a> </p>

              <p>Referat de aprobare [...]<br>
              <strong>Text integral</strong> <img src="images/arrow_red.png" vspace="2" align="bottom">&nbsp;&nbsp; <a href="documente/transparenta/Referat de aprobare permis conducere.pdf" target="_blank">( descarca fisier in format "pdf" )</a> </p>
              
              <p>Anexa 2 [...]<br>
              <strong>Text integral</strong> <img src="images/arrow_red.png" vspace="2" align="bottom">&nbsp;&nbsp; <a href="documente/transparenta/Anexa OMAI permis conducere.pdf" target="_blank">( descarca fisier in format "pdf" )</a> </p>
              
              <p>Propunerile, sugestiile şi opiniile persoanelor interesate cu privire la aceste proiecte de acte normative sunt aşteptate pe adresa de e-mail: dj-internațional@mai.gov.ro, în termen de 20 de zile de la data afișării pe site-ul MAI.</p>
    `);

    let proposalsSuggestionsOpinionsListItem = $('ul>li').last();
    parsedResult.identifier = getIdentifier($).substring(0, 128);
    parsedResult.title = getTitle($);
    parsedResult.type = getType($, parsedResult.title);
    parsedResult.date = getDate($);
    parsedResult.feedback_days = getFeedbackDays($, proposalsSuggestionsOpinionsListItem);
    parsedResult.contact.email = getEmail($, proposalsSuggestionsOpinionsListItem);
    parsedResult.documents = getDocuments($, URL);

    return parsedResult;
}


/** ====== identifier ====== */

function getIdentifier($) {
    return getTitle($)
        .toLowerCase()
        .replace(/\s+/, '-')
        .replace(/[`~!@#$%^&*()_|+=?;:'",.<>\{\}\[\]\\\/]/gi, '');
}


/** ====== title ====== */

function getTitle($) {
    return $('.item.column-1>b')
        .first()
        .text()
        .trim();
}


/** ====== type ====== */

let regexClassificators = {
    OG: [
        'Ordin al',
        'ordonanta pentru',
        'ORDONANȚĂ pentru',
        'ordonanta privind',
        'Ordonanţă privind'
    ],
    HG: [
        'hotarare a guvernului',
        'Hotărâre a Guvernului',
        'Hotarare a Guvernului',
        'HG',
        'hotarare pentru',
        'Hotărâre pentru',
        'Hotarare privind',
        'HOTĂRÂRE privind',
        'HOTĂRÂRE pentru',
        'HOTARARE pentru',
        'hotarare de guvern',
        'Hotărâre de Guvern'
    ],
    OUG: [
        'OUG',
        'ordonanta de urgenta a guvernului',
        'Ordonanţă de urgenţă a Guvernului',
        'ordonanta de urgenta pentru',
        'ORDONANŢĂ DE URGENȚĂ pentru',
        'Ordonanta de urgenta privind',
        'ORDONANŢĂ DE URGENȚĂ privind',
        'ordonanta pentru'
    ],
    LEGE: [
        'Schema de ajutor de minimis',
        'proiect hotarare a guvernului',
        'proiect Hotărâre a Guvernului',
        'proiect de hotarare a guvernului',
        'proiect de Hotărâre a Guvernului',
        'proiect ordonanta de urgenta',
        'Proiect Ordonanţă de urgenţă',
        /dezbaterea proiectului de Hotarare a Guvernului/,
        'LEGE ratificarea'
    ]
};
function getType($, title) {
    let type;

    Object.keys(regexClassificators)
        .forEach(function (key) {
            regexClassificators[key]
                .forEach(function (pattern) {
                    let result;

                    if (type) {
                        return;
                    }

                    if (typeof pattern === 'string') {
                        result = removeDiacritics(title)
                                .toLowerCase()
                                .indexOf(pattern.toLowerCase()) === 0
                    } else if (typeof pattern === 'object') {
                        result = pattern.test(title);
                    }

                    if (result) {
                        type = key;
                    }
                });
        });

    return type
        ? type
        : null;
}


/** ====== month ====== */

let months = {
    'ianuarie': '01',
    'februarie': '02',
    'martie': '03',
    'aprilie': '04',
    'mai': '05',
    'iunie': '06',
    'iulie': '07',
    'august': '08',
    'septembrie': '09',
    'octombrie': '10',
    'noiembrie': '11',
    'decembrie': '12'
};
function getDate($) {
    let digitsArr = $('.item.column-1>b')
        .eq(1)
        .text()
        .split(/\s/);

    digitsArr[1] = months[digitsArr[1]
        .toLowerCase()];
    // var scrappedDate = encodeURIComponent($(bolded[1]).text()).split('%C2%A0');
    // modelProject.date = scrappedDate[2] +'-'+ allMonths[scrappedDate[1]] +'-'+ scrappedDate[0];

    return digitsArr
        .reverse()
        .join('-');
}


/** ====== feedback days no. ====== */

function getFeedbackDays($, $listItem) {
    let feedbackDaysPatternMatchingResult = $listItem
        .text()
        .match(/se primesc in termen de (\d{1,3}) zile de la data/i);

    let daysString = feedbackDaysPatternMatchingResult
        && feedbackDaysPatternMatchingResult[1];

    return parseInt(daysString) || null;
}


/** ====== email ====== */

function getEmail($, $listItem) {
    return $listItem
        .find('span')
        .text();
}


/** ====== documents ====== */

function getDocuments($, URL) {
    let documents = $('li').find('a'),
        parsedDocs = [];

    documents.each(function (i, document) {
        let $doc = $(document);

        if ($doc.text()) {
            parsedDocs.push({
                type: $doc.text(),
                url: URL + $doc.attr('href')
            });
        }
    });

    return parsedDocs;
}


module.exports = parseProject;