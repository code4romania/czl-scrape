/** ====== MAIN ====== */

function parseProject($, URL) {
    let parsedResult = {
        identifier: "***lawproposal-first-document-name-slug-or-something", // un identificator unic, predictibil (repetabil), pereferabil human-readable
        title: "***Proiectul de ordin al ministrului justiției pentru aprobarea Regulamentului privind organizarea și desfășurarea activităților și programelor educative, de asistență psihologică și asistență socială din locurile de deținere aflate în subordinea Aministrației Naționale a Penitenciarelor", // titlul actului legislativ propus
        type: "***HG", // HG, OG, OUG, PROIECT
        institution: "economie", // ID-ul platformei din care provine actul legislativ
        date: "***2017-03-08", // ISO 8601
        description: null,
        feedback_days: 0x10, // numarul zilelor disponibile pentru feedback
        contact: {tel: null, email: "***feedback@example.org"}, // dictionar cu datale de contact. chei sugerate: "tel", "email", "addr"
        documents: [ // array de dictionare
            {
                type: "***anexa", // free text momentan
                url: "***http://www.just.ro/wp-content/uploads/2017/02/Proiect.docx" // da, este un link catre un document oficial de la MJ
            }
        ]
    };

    let proposalsSuggestionsOpinionsListItem = $('ul>li').last();
    parsedResult.identifier = getIdentifier($);
    parsedResult.title = getTitle($);
    parsedResult.type = getType($, parsedResult.title);
    parsedResult.date = getDate($);
    parsedResult.feedback_days = getFeedbackDays($, proposalsSuggestionsOpinionsListItem);
    parsedResult.contact.email = getEmail($, proposalsSuggestionsOpinionsListItem);
    parsedResult.documents = getDocuments($, URL);

    // console.log(JSON.stringify(parsedResult, null, 4));

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
    HG: [
        'Hotărâre a Guvernului',
        'Hotarare a Guvernului',
        'HG',
        'Hotărâre pentru',
        'Hotarare privind',
        'HOTĂRÂRE privind',
        'HOTĂRÂRE pentru',
        'HOTARARE pentru',
        'Hotărâre de Guvern'
    ],
    OG: [
        'Ordin al',
        'ORDONANȚĂ pentru',
        'Ordonanţă privind'
    ],
    OUG: [
        'OUG',
        'Ordonanţă de urgenţă a Guvernului',
        'Ordonanta de urgenta privind',
        'ORDONANŢĂ DE URGENȚĂ pentru',
        'ORDONANŢĂ DE URGENȚĂ privind'
    ],
    PROIECT: [
        'Schema de ajutor de minimis',
        'proiect Hotărâre a Guvernului',
        'proiect de Hotărâre a Guvernului',
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
                        result = title
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

    if (!daysString) {
        return null; //TODO log helpful warn
    }

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