let removeDiacritics = require('diacritics').remove;

/** ====== MAIN ====== */

function parseProject($row, URL, $metaParagraph) {
    let parsedResult = {
        identifier: null, // un identificator unic, predictibil (repetabil), pereferabil human-readable
        title: null, // titlul actului legislativ propus
        type: null, // HG, OG, OUG, PROIECT
        institution: "cercetare", // ID-ul platformei din care provine actul legislativ
        date: null, // ISO 8601
        feedback_days: null, // numarul zilelor disponibile pentru feedback
        contact: {tel: null, email1: null, email2: null}, // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr"
        documents: [ // array de dictionare
            {
                type: null, // free text momentan
                url: null // da, este un link catre un document oficial de la MJ
            }
        ]
    };

    parsedResult.identifier = getIdentifier($row);
    parsedResult.title = getTitle($row);
    parsedResult.type = getType($row, parsedResult.title);
    parsedResult.date = getDate($row);
    parsedResult.feedback_days = getFeedbackDays($row, $metaParagraph);
    parsedResult.contact.email1 = getEmail1($row);
    parsedResult.contact.email2 = getEmail2($metaParagraph);
    parsedResult.contact.tel = getTel($metaParagraph);
    parsedResult.documents = getDocuments($row, URL);

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
    return $('td')
        .eq(1)
        .text()
        .replace(/\t+/g,'')
        .replace(/\n+/g,'')
        .trim();
}


/** ====== type ====== */

let regexClassificators = {
    OG: [
        'OG si',
        'OG şi',
        'OG privind'
    ],
    HG: [
        'PHG şi',
        'PHG si',
        'PHG privind',
        'HG privind',
        'PHG pentru',
        'Norme metodologice',
        'HG nr.'
    ],
    OUG: [
        'OUG si'
    ],
    LEGE: [
        'L E G E de',
        'LEGE de',
        'Proiect de Lege pentru'
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
    return $('td')
        .first()
        .text()
        .trim()
        .split('.')
        .reverse()
        .join('-');
}


/** ====== feedback days no. ====== */

function getFeedbackDays($, $metaParagraph) {
    let feedbackDaysPatternMatchingResult = $metaParagraph
        .text()
        .match(/în termen de (\d{1,3}) zile de la data/i);

    let daysString = feedbackDaysPatternMatchingResult
                    && feedbackDaysPatternMatchingResult[1];

    return parseInt(daysString) || null;
}


/** ====== email1 ====== */

function getEmail1($) {

    return $('tr>td>p')
        .last()
        .text()
        .split(':')[1];
}


/** ====== email2 ====== */

function getEmail2($feedbackDays) {

    return $feedbackDays('p>a')
        .text();
}


/** ====== tel ====== */

function getTel($feedbackDays) {

    return $feedbackDays('p>span')
        .text()
        .split(',')[1]
        .split('+')[1];
}


/** ====== documents ====== */

function getDocuments($, URL) {
    let documents = $('td').find('a'),
        parsedDocs = [];

    documents.each(function (i, document) {
        let $doc = $(document);

        if ($doc.text()) {
            parsedDocs.push({
                type: $doc.text().trim(),
                url: URL + $doc.attr('href')
            });
        }
    });

    return parsedDocs;
}


module.exports = parseProject;