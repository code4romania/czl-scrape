let removeDiacritics = require('diacritics').remove;
    // cheerio = require('cheerio');

/** ====== MAIN ====== */

function parseProject($, URL) {
    let parsedResult = {
        identifier: null, // un identificator unic, predictibil (repetabil), pereferabil human-readable
        title: null, // titlul actului legislativ propus
        type: null, // HG, OG, OUG, LEGE, ORDIN DE MINISTRU
        institution: "interne", // ID-ul platformei din care provine actul legislativ
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

    // $ = cheerio.load(`
    //   <div style="width:100%; padding-top:5px; padding-bottom:1px; margin-bottom:2px; background-color:#1495F0; ">
    //     <p style="color:#FFFFFF"><!-- InstanceBeginEditable name="editare data transparenta" -->
    //     <strong>
    //     Publicat în data de - 21.11.2016                 </strong>
    //     <!-- InstanceEndEditable --></p>
    //   </div>
    //
    //   <p>ORDINUL MINISTRULUI AFACERILOR INTERNE Nr. _____ din ____ . ____ 2016 pentru modificarea Ordinului ministrului administraţiei şi internelor nr.157/2012 privind forma şi conţinutul permisului de conducere [...]<br>
    //   <strong>Text integral</strong> <img src="images/arrow_red.png" vspace="2" align="bottom">&nbsp;&nbsp; <a href="documente/transparenta/Ordin forma permis conducere.pdf" target="_blank">( descarca fisier in format "pdf" )</a> </p>
    //
    //   <p>Referat de aprobare [...]<br>
    //   <strong>Text integral</strong> <img src="images/arrow_red.png" vspace="2" align="bottom">&nbsp;&nbsp; <a href="documente/transparenta/Referat de aprobare permis conducere.pdf" target="_blank">( descarca fisier in format "pdf" )</a> </p>
    //
    //   <p>Anexa 2 [...]<br>
    //   <strong>Text integral</strong> <img src="images/arrow_red.png" vspace="2" align="bottom">&nbsp;&nbsp; <a href="documente/transparenta/Anexa OMAI permis conducere.pdf" target="_blank">( descarca fisier in format "pdf" )</a> </p>
    //
    //   <p>Propunerile, sugestiile şi opiniile persoanelor interesate cu privire la aceste proiecte de acte normative sunt aşteptate pe adresa de e-mail dj-internațional@mai.gov.ro, în termen de 20 de zile de la data afișării pe site-ul MAI.</p>
    // `);

    let proposalsSuggestionsOpinionsListItem = $('p').last();
    parsedResult.identifier = getIdentifier($);
    parsedResult.title = getTitle($);
    parsedResult.type = getType($, parsedResult.title);
    parsedResult.date = getDate($);
    parsedResult.feedback_days = getFeedbackDays(proposalsSuggestionsOpinionsListItem);
    parsedResult.contact.email = getEmail(proposalsSuggestionsOpinionsListItem);
    parsedResult.documents = getDocuments($, URL, parsedResult.type);

    console.log(parsedResult);

    return parsedResult;
}


/** ====== identifier ====== */

function getIdentifier($) {
    return removeDiacritics(getTitle($)
        .toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[`~!@#$%^&*()_|+=?;:'",.<>\{\}\[\]\\\/]/gi, '')
        .substring(0, 128));
}


/** ====== title ====== */

function getTitle($) {
    return $('p')
        .eq(1)
        .contents()
        .eq(0)
        .text()
        .trim();
}


/** ====== type ====== */

let regexClassificators = {
    OG: [
        'ORDONANŢĂ pentru',
    ],
    'ORDIN DE MINISTRU': [
        'ORDINUL MINISTRULUI',
        'ORDIN Nr.',
        'INSTRUCŢIUNILE MINISTRULUI',
        'OMAI pentru',
        'Proiectul de Ordin al',
        'Proiectul Ordinului ministrului',
        'Proiectul instrucțiunilor ministrului',
        'ORDIN AL MINISTRULUI',
        'ORDIN privind',
        'ORDIN pentru',
        'O R D I N U L MINISTRULUI'
    ],
    HG: [
        'Hotărâre pentru',
        'HOTĂRÂRE pentru',
        'Proiectul Hotărârii',
        'HOTĂRÂRE privind',
        'Proiect HOTARARE GUVERN',
        'Proiect de Hotatare a',
        'Proiectul de HOTĂRÂRE pentru',
        'Proiectul de Hotarare a',
        'HOTĂRÂREA GUVERNULUI',
        'HOTĂRÂRE Nr.',
        'HOTĂRÂREA nr.'
    ],
    OUG: [
        ''
    ],
    LEGE: [
        'LEGE pentru',
        'Lege pentru',
        'LEGE privind',
        'Proiectul OMAI privind',
        'Proiectul de lege pentru',
        'Lege privind',
        'L E G E pentru'
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

function getDate($) {
    let digitsArr = $('div')
        .text()
        .trim()
        .split('-')[1]
        .trim()
        .split(' ')[0]
        .trim()
        .split('.');


    return digitsArr
        .reverse()
        .join('-');
}


/** ====== feedback days no. ====== */

function getFeedbackDays($metaParagraph) {
    let feedbackDaysPatternMatchingResult = $metaParagraph.text().match(/în termen de (\d{1,3}) de zile de la data/i);

    let daysString = feedbackDaysPatternMatchingResult && feedbackDaysPatternMatchingResult[1];

    return parseInt(daysString) || null;
}


/** ====== email ====== */

function getEmail($listItem) {
    let matches = removeDiacritics($listItem.text())
        .match(/([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})/i)[0];

    return matches.trim();
}


/** ====== documents ====== */

function getDocuments($, URL, type) {
    let documents = $('p').find('a'),
        parsedDocs = [];

    documents.each(function (i, document) {
        let $doc = $(document);

        if ($doc.text()) {
            parsedDocs.push({
                type: i==0 ? type : $doc.parent().text().split('[...]')[0].trim(),
                url: URL + ($doc.attr('href').indexOf('/') === 0
                    ? $doc.attr('href')
                    :'/'+$doc.attr('href'))
            });
        }
    });

    return parsedDocs;
}


module.exports = parseProject;