let nightmare = require('nightmare')({ show: false }),
    cheerio = require('cheerio');

function parseParagraph(paragraph) {
    "use strict";


}

// nightmare
//     .goto('http://google.ro/')//http://www.dprp.gov.ro/documente-in-consultare-publica/
//     .evaluate(function() {
//         return ''; //document.querySelector('#principal .entry-content').innerHTML;
//     })
//     .end()
//     .then(function(result) {
        let res = `<p><a href="http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2.png" data-slb-active="1" data-slb-asset="1289645544" data-slb-internal="0" data-slb-group="2936"><img
             class="alignleft size-full wp-image-5837" src="http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2.png" alt="logo-2" width="620" height="349" srcset="http://www.dpr
            p.gov.ro/wp-content/uploads/2017/02/logo-2.png 620w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-300x169.png 300w, http://www.dprp.gov.ro/wp-content/uploads/
            2017/02/logo-2-480x270.png 480w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-2x1.png 2w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-140x78.png
            140w, http://www.dprp.gov.ro/wp-content/uploads/2017/02/logo-2-190x107.png 190w" sizes="(max-width: 620px) 100vw, 620px"></a></p><p>Supunerea spre dezbatere public&#x103;
             a&#xA0; proiectului de lege privind modificarea &#x15F;i completarea Legii nr. 321/2006 privind regimul acord&#x103;rii finan&#x163;&#x103;rilor nerambursabile&#xA0; pro
            gramelor, proiectelor sau ac&#x163;iunilor pentru sprijinirea activit&#x103;&#x163;ii rom&#xE2;nilor de pretutindeni &#x15F;i a organiza&#x163;iilor reprezentative ale ac
            estora, precum &#x15F;i a modului de repartizare &#x15F;i de utilizare a sumei&#xA0; prev&#x103;zut&#x103; &#xEE;n bugetul Ministerului Afacerilor Externe pentru aceast&#
            x103; activitate.</p><p>&#xCE;n conformitate cu prevederile art. 6 din Legea nr. 52/2003 privind transparen&#x163;a decizional&#x103; &#xEE;n administra&#x21B;ia public&#
            x103;, republicat&#x103;, cu modific&#x103;rile &#x219;i complet&#x103;rile ulterioare, supunem dezbaterii publice proiectul de lege privind modificarea &#x15F;i completa
            rea Legii nr. 321/2006 privind regimul acord&#x103;rii finan&#x163;&#x103;rilor nerambursabile&#xA0; programelor, proiectelor sau ac&#x163;iunilor pentru sprijinirea acti
            vit&#x103;&#x163;ii rom&#xE2;nilor de pretutindeni &#x15F;i a organiza&#x163;iilor reprezentative ale acestora, precum &#x15F;i a modului de repartizare &#x15F;i de utili
            zare a sumei&#xA0; prev&#x103;zut&#x103; &#xEE;n bugetul Ministerului Afacerilor Externe pentru aceast&#x103; activitate.</p><p><span style="text-decoration: underline;">
            <span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="http://www.dprp.gov.ro/wp-content/uploads/2016/05/l
            egea-321-cu-modificari.docx">Proiectul de lege privind modificarea &#x15F;i completarea Legii nr. 321/2006</a></span></span></p><p><span style="text-decoration: underline
            ;"><span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="http://www.dprp.gov.ro/wp-content/uploads/2016/0
            5/expunere-motive-cu-modificari.docx">Expunere de motive proiectul de lege privind modificarea &#x15F;i completarea Legii nr. 321/2006</a></span></span></p><p>Propunerile
            , sugestiile &#x15F;i opiniile referitoare la modific&#x103;rile propuse cu privire la proiectul de Metodologie men&#x163;ionat pot fi transmise &#xEE;n scris pe adresa M
            inisterului Afacerilor Externe, Departamentul Politici pentru Rela&#x163;ia cu Rom&#xE2;nii de Pretutindeni, Bd. Prim&#x103;verii nr.22, sector 1, Bucure&#x15F;ti, prin f
            ax la nr. (004) 021.233.39.53.99 sau la adresa de e-mail &#xA0;<span style="text-decoration: underline;"><span style="color: #0000ff;"><a style="color: #0000ff; text-deco
            ration: underline;" href="mailto:transparenta@dprp.gov.ro">transparenta@dprp.gov.ro</a></span></span>,&#xA0; p&#xE2;n&#x103; la data de 30&#xA0;iunie 2016.</p><p style="t
            ext-align: center;">&#x2014;&#x2014;&#x2014;&#x2014;&#x2014;&#x2013;</p><p>Supunerea spre dezbatere public&#x103; a &#xA0;proiectului de lege privind modificarea &#x15F;i
             completarea Legii nr. 321/2006 privind regimul acord&#x103;rii finan&#x163;&#x103;rilor nerambursabile&#xA0; programelor, proiectelor sau ac&#x163;iunilor pentru sprijin
            irea activit&#x103;&#x163;ii rom&#xE2;nilor de pretutindeni &#x15F;i a organiza&#x163;iilor reprezentative ale acestora, precum &#x15F;i a modului de repartizare &#x15F;i
             de utilizare a sumei&#xA0; prev&#x103;zut&#x103; &#xEE;n bugetul Ministerului Afacerilor Externe pentru aceast&#x103; activitate.</p><p><em><strong>&#xA0;</strong></em>&
            #xCE;n conformitate cu prevederile art. 7 din Legea nr. 52/2003&#xA0;privind transparen&#x163;a decizional&#x103; &#xEE;n administra&#x21B;ia public&#x103;, republicat&#x
            103;, cu modific&#x103;rile &#x219;i complet&#x103;rile ulterioare, supunem dezbaterii publice &#xA0;<strong>proiectul de lege privind modificarea &#x15F;i completarea Le
            gii nr. 321/2006 privind regimul acord&#x103;rii finan&#x163;&#x103;rilor nerambursabile&#xA0; programelor, proiectelor sau ac&#x163;iunilor pentru sprijinirea activit&#x
            103;&#x163;ii rom&#xE2;nilor de pretutindeni &#x15F;i a organiza&#x163;iilor reprezentative ale acestora, precum &#x15F;i a modului de repartizare &#x15F;i de utilizare a
             sumei&#xA0; prev&#x103;zut&#x103; &#xEE;n bugetul Ministerului Afacerilor Externe pentru aceast&#x103; activitate.</strong></p><p><span style="text-decoration: underline
            ;"><span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="http://www.dprp.gov.ro/wp-content/uploads/2015/1
            0/LEGE-nr-321-varianta-avizata-de-MAE-si-DPRRP-5-oct.doc" target="_blank">Proiectul de lege privind modificarea &#x15F;i completarea Legii nr. 321/2006</a></span></span><
            /p><p><span style="text-decoration: underline;"><span style="color: #0000ff; text-decoration: underline;"><a style="color: #0000ff; text-decoration: underline;" href="htt
            p://www.dprp.gov.ro/wp-content/uploads/2015/10/expunere-motive-conf-DJLC-conf-HG-1361.docx" target="_blank">Expunere de motive proiectul de lege privind modificarea &#x15
            F;i completarea Legii nr. 321/2006</a></span></span></p><p>Sugestiile &#x15F;i opiniile referitoare la modific&#x103;rile propuse cu privire la proiectul de Lege men&#x16
            3;ionat pot fi transmise &#xEE;n scris pe adresa Ministerului Afacerilor Externe, Departamentul Politici pentru Rela&#x163;ia cu Rom&#xE2;nii de Pretutindeni, Bd. Prim&#x
            103;verii nr.22, sector 1, Bucure&#x15F;ti, prin fax la nr. (004) 021.233.39.53.99 sau la adresa de e-mail&#xA0;<a href="mailto:transparenta@dprp.gov.ro">transparenta@dpr
            p.gov.ro</a>, &#xA0;p&#xE2;n&#x103; la data de &#xA0;<strong>3 noiembrie&#xA0;2015</strong>.</p><p align="center">&#x2014;&#x2014;&#x2014;&#x2014;&#x2014;&#x2013;</p><p>S
            upunerea spre dezbatere public&#x103; a &#xA0;proiectului de METODOLOGIE privind organizarea alegerii delega&#x163;ilor Congresului rom&#xE2;nilor de Pretutindeni, pentru
             aplicarea prevederilor art.8 din Legea 299/2007 republicat&#x103;.</p><p>&#xCE;n conformitate cu prevederile art. 7 din Legea nr. 52/2003&#xA0;privind transparen&#x163;a
             decizional&#x103; &#xEE;n administra&#x21B;ia public&#x103;, republicat&#x103;, cu modific&#x103;rile &#x219;i complet&#x103;rile ulterioare, supunem dezbaterii publice&
            #xA0;<strong>proiectul de METODOLOGIE privind organizarea alegerii delega&#x163;ilor Congresului rom&#xE2;nilor de Pretutindeni, pentru aplicarea prevederilor art.8 din L
            egea 299/2007 republicat&#x103;.</strong></p><p><span style="text-decoration: underline;"><span style="color: #0000ff;"><a style="color: #0000ff; text-decoration: underli
            ne;" title="Metodologie Congres" href="http://www.dprp.gov.ro/wp-content/uploads/2015/07/Metodologie_congres_cu_anexe.pdf" target="_blank">Metodologie privind organizarea
             alegerii delega&#x163;ilor&#xA0; Congresului rom&#xE2;nilor de Pretutindeni</a></span></span></p><p>Propunerile, sugestiile &#x15F;i opiniile referitoare la modific&#x10
            3;rile propuse cu privire la proiectul de Metodologie men&#x163;ionat pot fi transmise &#xEE;n scris pe adresa Ministerului Afacerilor Externe, Departamentul Politici pen
            tru Rela&#x163;ia cu Rom&#xE2;nii de Pretutindeni, Bd. Prim&#x103;verii nr.22, sector 1, Bucure&#x15F;ti, prin fax la nr. (004) 021.233.39.53.99 sau la adresa de e-mail &
            #xA0;<span style="text-decoration: underline;"><span style="color: #0000ff;"><a style="color: #0000ff; text-decoration: underline;" href="mailto:transparenta@dprp.gov.ro"
            >transparenta@dprp.gov.ro</a></span></span>, &#xA0;p&#xE2;n&#x103; la data de &#xA0;<strong>8 august&#xA0;2015</strong>.</p><p align="center">&#x2014;&#x2014;&#x2014;&#x2
            014;&#x2014;&#x2013;</p><p>&#xA0;</p><p>&#xA0;</p>`;

        let $ = cheerio.load(res
            .replace(/\n/g,'')
            .replace(/\r/g,'')
            .replace(/\t/g,''));

        let paragraphs = $('p');

        let projects = [];
        let projectsCounter = 0;
        for(let i = 0; i < paragraphs.length; i++) {
            if($(paragraphs[i]).text() == '—————–') {
                projectsCounter++;
            } else {
                if(!projects[projectsCounter]) {
                    projects[projectsCounter] = [];
                }
                projects[projectsCounter].push(paragraphs[i])
            }
        }

        projects.forEach((project, idx) => {
            console.log(`------------------- project ${idx + 1}`);
            project.forEach(pElem => {
              console.log($(pElem).html() + '\n');
            });
        });
    // })
    // .catch(function(error) {
    //     throw new Error(error);
    // });
