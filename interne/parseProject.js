let removeDiacritics = require('diacritics').remove;

/** ====== MAIN ====== */

function parseProject($, URL) {
    let parsedResult = {
        identifier: null, // un identificator unic, predictibil (repetabil), pereferabil human-readable
        title: null, // titlul actului legislativ propus
        type: null, // HG, OG, OUG, LEGE, OM
        institution: 'interne', // ID-ul platformei din care provine actul legislativ
        date: null, // ISO 8601
        feedback_days: null, // numarul zilelor disponibile pentru feedback
        contact: {email: null}, // dictionar cu datale de contact. chei sugerate: 'tel', 'email', 'addr'
        documents: [ // array de dictionare
            {
                type: null, // free text momentan
                url: null // da, este un link catre un document oficial de la MJ
            }
        ]
    };

    let $proposalsSuggestionsOpinionsListItem = $('p').last();
    parsedResult.identifier = getIdentifier($);
    parsedResult.title = getTitle($);
    parsedResult.type = getType($, parsedResult.title);
    parsedResult.date = getDate($);
    parsedResult.feedback_days = getFeedbackDays($, $proposalsSuggestionsOpinionsListItem);
    parsedResult.contact.email = getEmail($proposalsSuggestionsOpinionsListItem);
    parsedResult.documents = getDocuments($, URL, parsedResult.type);

    if(!parsedResult.contact.email) {
        delete parsedResult.contact.email;
    }
    if(!parsedResult.feedback_days) {
        delete parsedResult.feedback_days;
    }

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
    OM: [
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
        'L E G E pentru',
        'Proiectul Legii pentru'
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
    return $('div')
        .text()
        .trim()
        .split('-')[1]
        .trim()
        .split(' ')[0]
        .trim()
        .split('.')
        .reverse()
        .join('-');
}


/** ====== feedback days no. ====== */

function getFeedbackDays($, $metaParagraph) {
    let feedbackDaysPatternMatchingResult = searchParagraphForFeedbackDays($metaParagraph);

    // treating edge case in which the feedback days paragraph gets pushed between the documents' paragraphs(e.g. improved doc versions added)
    if (!feedbackDaysPatternMatchingResult) {
        $('p').each(function(idx, paragraph) {
            if (!feedbackDaysPatternMatchingResult) {
                feedbackDaysPatternMatchingResult = searchParagraphForFeedbackDays($(paragraph));
            }
        });
    }

    let daysString = feedbackDaysPatternMatchingResult && feedbackDaysPatternMatchingResult[1];

    return parseInt(daysString) || null;
}

function searchParagraphForFeedbackDays($paragraph) {
    return removeDiacritics($paragraph
        .text())
        .match(/in termen de (\d{1,3}) /i);
}


/** ====== email ====== */

function getEmail($listItem) {
    try {
        let matches = removeDiacritics($listItem.text())
            .match(/([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})/i)[0];

        return matches.trim();
    } catch(e) {
        return null;
    }
}


/** ====== documents ====== */

function getDocuments($, URL, type) {
    let documents = $('p')
            .not(function(i, el) {
                return $(el).find('img').length === 0;
            })
            .find('a'),
        parsedDocs = [];

    documents.each(function (i, document) {
        let $doc = $(document),
            docType,
            docURL = $doc.attr('href');

        //set docType
        if (i > 0) {
            docType = $doc
                .parent()
                .text()
                .split('[...]')[0]
                .replace('( descarca fisier in format \"pdf\" )', '')
                .trim();

            if (docType.length > 20) {
                docType = getType(null, docType);
            }
        } else if (i === 0) {
            //first document's type
            docType = type;
        }

        //set docURL
        if (docURL.indexOf('/') !== 0) {
            docURL = '/' + docURL;
        }
        docURL = URL + docURL;

        if ($doc.text()) {
            parsedDocs.push({
                type: docType,
                url: docURL
            });
        }
    });

    return parsedDocs;
}


module.exports = parseProject;