var nightmare = require('nightmare')({ show: false }),
    cheerio = require('cheerio');

var parseFunction = require('./parseProject.js');

function parseParagraph(paragraph) {
    "use strict";

    var $ = cheerio.load(paragraph);

    var paragraphs = $('p');

    var projects = [];
    var projectsCounter = 0;
    for(var i = 0; i < paragraphs.length; i++) {
        if($(paragraphs[i]).text() == '—————–') {
            projectsCounter++;
        } else {
            if(!projects[projectsCounter]) projects[projectsCounter] = [];
            projects[projectsCounter].push(paragraphs[i])
        }
    }

    for(var i = 0; i < projects.length; i++) {
        parseFunction(projects[i]);
    }
}

// nightmare
//     .goto('http://www.dprp.gov.ro/documente-in-consultare-publica/')
//     .evaluate(function() {
//         return document.querySelector('#principal .entry-content').innerHTML;
//     })
//     .end()
//     .then(function(result) {
//         parseParagraph(result
//             .replace(/\n/g,'')
//             .replace(/\r/g,'')
//             .replace(/\t/g,''));
//     })
//     .catch(function(error) {
//         throw new Error(error);
//     });

var HTML = '<p><a href="http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2.png" data-slb-active="1" data-slb-asset="88663206" data-slb-internal="0" data-slb-group="2936"><img class="alignleft size-full wp-image-5837" src="http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2.png" alt="logo-2" width="620" height="349" srcset="http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2.png 620w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-300x169.png 300w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-480x270.png 480w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-2x1.png 2w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-140x78.png 140w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-190x107.png 190w" sizes="(max-width: 620px) 100vw, 620px"></a></p><p>Supunerea spre dezbatere publică a&nbsp; proiectului de lege privind modificarea şi completarea Legii nr. 321/2006 privind regimul acordării finanţărilor nerambursabile&nbsp; programelor, proiectelor sau acţiunilor pentru sprijinirea activităţii românilor de pretutindeni şi a organizaţiilor reprezentative ale acestora, precum şi a modului de repartizare şi de utilizare a sumei&nbsp; prevăzută în bugetul Ministerului Afacerilor Externe pentru această activitate.</p><p>În conformitate cu prevederile art. 6 din Legea nr. 52/2003 privind transparenţa decizională în administrația publică, republicată, cu modificările și completările ulterioare, supunem dezbaterii publice proiectul de lege privind modificarea şi completarea Legii nr. 321/2006 privind regimul acordării finanţărilor nerambursabile&nbsp; programelor, proiectelor sau acţiunilor pentru sprijinirea activităţii românilor de pretutindeni şi a organizaţiilor reprezentative ale acestora, precum şi a modului de repartizare şi de utilizare a sumei&nbsp; prevăzută în bugetul Ministerului Afacerilor Externe pentru această activitate.</p><p><span style="text-decoration: underline;"><span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="http://www.dprp.gov.ro/wp-content/uploads/2016/05/legea-321-cu-modificari.docx">Proiectul de lege privind modificarea şi completarea Legii nr. 321/2006</a></span></span></p><p><span style="text-decoration: underline;"><span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="http://www.dprp.gov.ro/wp-content/uploads/2016/05/expunere-motive-cu-modificari.docx">Expunere de motive proiectul de lege privind modificarea şi completarea Legii nr. 321/2006</a></span></span></p><p>Propunerile, sugestiile şi opiniile referitoare la modificările propuse cu privire la proiectul de Metodologie menţionat pot fi transmise în scris pe adresa Ministerului Afacerilor Externe, Departamentul Politici pentru Relaţia cu Românii de Pretutindeni, Bd. Primăverii nr.22, sector 1, Bucureşti, prin fax la nr. (004) 021.233.39.53.99 sau la adresa de e-mail &nbsp;<span style="text-decoration: underline;"><span style="color: #0000ff;"><a style="color: #0000ff; text-decoration: underline;" href="mailto:transparenta@dprp.gov.ro">transparenta@dprp.gov.ro</a></span></span>,&nbsp; până la data de 30&nbsp;iunie 2016.</p><p style="text-align: center;">—————–</p><p>Supunerea spre dezbatere publică a &nbsp;proiectului de lege privind modificarea şi completarea Legii nr. 321/2006 privind regimul acordării finanţărilor nerambursabile&nbsp; programelor, proiectelor sau acţiunilor pentru sprijinirea activităţii românilor de pretutindeni şi a organizaţiilor reprezentative ale acestora, precum şi a modului de repartizare şi de utilizare a sumei&nbsp; prevăzută în bugetul Ministerului Afacerilor Externe pentru această activitate.</p><p><em><strong>&nbsp;</strong></em>În conformitate cu prevederile art. 7 din Legea nr. 52/2003&nbsp;privind transparenţa decizională în administrația publică, republicată, cu modificările și completările ulterioare, supunem dezbaterii publice &nbsp;<strong>proiectul de lege privind modificarea şi completarea Legii nr. 321/2006 privind regimul acordării finanţărilor nerambursabile&nbsp; programelor, proiectelor sau acţiunilor pentru sprijinirea activităţii românilor de pretutindeni şi a organizaţiilor reprezentative ale acestora, precum şi a modului de repartizare şi de utilizare a sumei&nbsp; prevăzută în bugetul Ministerului Afacerilor Externe pentru această activitate.</strong></p><p><span style="text-decoration: underline;"><span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="http://www.dprp.gov.ro/wp-content/uploads/2015/10/LEGE-nr-321-varianta-avizata-de-MAE-si-DPRRP-5-oct.doc" target="_blank">Proiectul de lege privind modificarea şi completarea Legii nr. 321/2006</a></span></span></p><p><span style="text-decoration: underline;"><span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="http://www.dprp.gov.ro/wp-content/uploads/2015/10/expunere-motive-conf-DJLC-conf-HG-1361.docx" target="_blank">Expunere de motive proiectul de lege privind modificarea şi completarea Legii nr. 321/2006</a></span></span></p><p>Sugestiile şi opiniile referitoare la modificările propuse cu privire la proiectul de Lege menţionat pot fi transmise în scris pe adresa Ministerului Afacerilor Externe, Departamentul Politici pentru Relaţia cu Românii de Pretutindeni, Bd. Primăverii nr.22, sector 1, Bucureşti, prin fax la nr. (004) 021.233.39.53.99 sau la adresa de e-mail&nbsp;<a href="mailto:transparenta@dprp.gov.ro">transparenta@dprp.gov.ro</a>, &nbsp;până la data de &nbsp;<strong>3 noiembrie&nbsp;2015</strong>.</p><p align="center">—————–</p><p>Supunerea spre dezbatere publică a &nbsp;proiectului de METODOLOGIE privind organizarea alegerii delegaţilor Congresului românilor de Pretutindeni, pentru aplicarea prevederilor art.8 din Legea 299/2007 republicată.</p><p>În conformitate cu prevederile art. 7 din Legea nr. 52/2003&nbsp;privind transparenţa decizională în administrația publică, republicată, cu modificările și completările ulterioare, supunem dezbaterii publice&nbsp;<strong>proiectul de METODOLOGIE privind organizarea alegerii delegaţilor Congresului românilor de Pretutindeni, pentru aplicarea prevederilor art.8 din Legea 299/2007 republicată.</strong></p><p><span style="text-decoration: underline;"><span style="color: #0000ff;"><a style="color: #0000ff; text-decoration: underline;" title="Metodologie Congres" href="http://www.dprp.gov.ro/wp-content/uploads/2015/07/Metodologie_congres_cu_anexe.pdf" target="_blank">Metodologie privind organizarea alegerii delegaţilor&nbsp; Congresului românilor de Pretutindeni</a></span></span></p><p>Propunerile, sugestiile şi opiniile referitoare la modificările propuse cu privire la proiectul de Metodologie menţionat pot fi transmise în scris pe adresa Ministerului Afacerilor Externe, Departamentul Politici pentru Relaţia cu Românii de Pretutindeni, Bd. Primăverii nr.22, sector 1, Bucureşti, prin fax la nr. (004) 021.233.39.53.99 sau la adresa de e-mail &nbsp;<span style="text-decoration: underline;"><span style="color: #0000ff;"><a style="color: #0000ff; text-decoration: underline;" href="mailto:transparenta@dprp.gov.ro">transparenta@dprp.gov.ro</a></span></span>, &nbsp;până la data de &nbsp;<strong>8 august&nbsp;2015</strong>.</p><p align="center">—————–</p><p>&nbsp;</p><p>&nbsp;</p>            ';

parseParagraph(HTML);