<?php

if ( isset( $argv[1] ) ) {

    $strToken = $argv[1];
    $strMainURL = 'http://dlaj.mapn.ro/';
    //$strMainURL = 'http://dlaj.mapn.ro/arhiva2016.php';
    $strPostURl = 'http://czl-api.code4.ro/api/publications/';

    $strContent = _getURL($strMainURL); //for prod
    $strContent = html_entity_decode(mb_convert_encoding($strContent, 'UTF-8', 'ISO-8859-2'));

    if(!$strContent)
    {
        print_r("!!ERROR!! Siteul a picat. Incearca mai tarziu \n");
        print_r($strContent);
        return false;
    }

    $arrPostDocuments = array();
    /* intai sunt luate titlurile proiectelor */
    if(preg_match_all('%<img src="assets\/premium\.gif" width="\d{1,}" height="\d{1,}" \/>(.*?)<\/strong>%s', $strContent, $arrTitles))
    {
        /* sunt luate apoi fisierele disponibile */
        if(preg_match_all('%<em>FISIERE DISPONIBILE(.*?)<\/em>%s', $strContent, $arrAvailableDocuments))
        {
            /* daca numarul de titluri de proiecte si numarul de grupuri de documente nu este acelasi, va returna false */
            if (count($arrAvailableDocuments[0]) !== count($arrTitles[0])) {
                print_r('!!ERROR!! Numar diferit de taguri de documente si titluri de documente (proiect fara documente)' . PHP_EOL);
                return false;
            }
            $bolFeedback = false;
            /* se incearca a se lua date suplimentare legate de feedback */
            if(preg_match_all('%<em> Propunerile,.*?adresa de e-mail(.*?),.*?termen de ([0-9]+) de%s', $strContent, $arrProposals))
            {
                $bolFeedback = true;
            }
            else
            {
                print_r('!!ERROR!! Datele de feedback nu au putut fi luate' . PHP_EOL);
            }
            foreach ($arrAvailableDocuments[1] as $keyRaw => $arrAvailableDocumentsRaw) {
                $arrItem = array(
                    'identifier' => '',
                    'title' => '',
                    'type' => '',
                    'institution' => 'aparare',
                    'date' => '',
                    'description' => '',
                    'feedback_days' => null,
                    'contact' => array(),
                    'documents' => array()
                );
                /* replaces needed to be made in order */
                $strTitle = str_replace("\n", '', str_replace("\r", ' ', trim($arrTitles[1][$keyRaw])));
                while (strpos($strTitle, '  ') !== false)
                    $strTitle = str_replace("  ", ' ', $strTitle);
                $arrItem['title'] = $strTitle;
                $arrItem['description'] = $strTitle;
                /* gets the corresponding item type */
                $strType = _getCorrespondingType($arrItem['title']);
                $arrItem['type'] = ($strType) ? $strType : '';
                /* checks if the feedback info is available*/
                if($bolFeedback && isset($arrProposals[1]) && isset($arrProposals[2]))
                {
                    $arrItem['contact']['email'] = trim($arrProposals[1][$keyRaw],chr(0xC2).chr(0xA0));
                    $arrItem['feedback_days'] = intval($arrProposals[2][$keyRaw]);;
                }
                /* se gasesc documentele pentru item, daca nu exista, itemul este sarit */
                if (preg_match_all('%<a href="(http:\/\/dlaj\.mapn\.ro\/documents\/acts\/(.*?)\..*?)">%s', $arrAvailableDocumentsRaw, $arrDocuments)) {
                    foreach ($arrDocuments[1] as $key => $strDocumentLink) {
                        $arrItem['documents'][$key]['url'] = $strDocumentLink;
                        $arrItem['documents'][$key]['type'] = _getCorrespondingDocumentType($strDocumentLink);
                    }
                    /* titlul este al celui de-al doilea document de regula */
                    if(isset($arrDocuments[2][1]))
                        $arrItem['identifier'] = $arrItem['institution'] . '-' . str_replace('_', '-', strtolower($arrDocuments[2][1]));
                    else
                        $arrItem['identifier'] = $arrItem['institution'] . '-' . str_replace('_', '-', strtolower($arrDocuments[2][0]));
                } else {
                    print_r('!!NOTICE!! Nu am gasit documente pentru ' . $arrTitles[1][$keyRaw] . PHP_EOL);
                    continue;
                }
                /* se ia data afisarii */
                if (preg_match('%\(DATA AFISARII: (.*?)\)%s', $arrAvailableDocumentsRaw, $arrDate)) {
                    $arrItem['date'] = $arrDate[1];
                } else {
                    print_r('!!NOTICE!! Nu am gasit data afisarii pentru ' . $arrTitles[1][$keyRaw] . PHP_EOL);
                }
                array_push($arrPostDocuments, $arrItem);
                unset($arrItem);
            }
        }
        else
        {
            print_r('!!ERROR!! Documentele nu au putut fi luate' . PHP_EOL);
            return false;
        }
        print_r($arrPostDocuments);
        foreach($arrPostDocuments as $document)
        {
            $jsonEncoded = json_encode($document);
            //API CALL
            $strResponse = _getURL($strPostURl, $strToken, $jsonEncoded);
            print_r($strResponse . PHP_EOL);
        }
        return true;
    }
    else
    {
        print_r('!!ERROR!! Informatiile nu au putut fi luate, pagina a fost schimbata, verifica ' . $strMainURL . PHP_EOL);
        return false;
    }
}
print_r('!!ERROR!! No token inputed'. PHP_EOL);
return false;
/**
 * Function that translates the title into corresponding document types
 *
 * @param $strTitle
 * @return string
 */
function _getCorrespondingType($strTitle){
    $arrWords = explode(' ',$strTitle);
    $strFirstWordsOfTitle = trim(strtolower(current($arrWords)), chr(0xC2).chr(0xA0));
    switch($strFirstWordsOfTitle)
    {
        case 'hotărâre':
        case 'hotărârea':
            return 'HG';
        case 'proiectul':
        case 'proiect':
            if(strpos($strTitle, 'hotărâre') !== false)
                return 'HG';
            else if(strpos($strTitle, 'ordin') !== false)
                return 'OM';
            else
                return 'OTHER';
        case 'ordin':
            return 'OM';
        case 'ordonanţă':
            if(strpos($strTitle, 'urgenţă') !== false)
                return 'OUG';
            else
                return 'OG';
        case 'lege':
            return 'LEGE';
        case 'dezbatere':
        case 'anuntprivind':
            return 'OTHER';
        default:
            print_r("!!NOTICE!! Tip nou de element: " . $strFirstWordsOfTitle . PHP_EOL);
            return 'OTHER';
    }
}

/**
 * Function that gets a document title and conceives a title out of it
 *
 * @param $strDocTitle
 */
function _getCorrespondingDocumentType($strDocTitle){
    $strDocTitle = strtolower($strDocTitle);
    if(strpos($strDocTitle, 'proiect') !== false || strpos($strDocTitle, 'hg') !== false)
        return 'proiect_act_normativ';
    else
        return 'nota_fundamentare';
}

/**
 * Function that executes a request
 *
 * @param $strURL
 * @param bool $mxdPost
 * @return bool|mixed
 */
function _getURL($strURL, $strToken = false, $mxdPost = false){
    $intRetries = 5;
    $strResponse = false;
    $ch = curl_init();
    curl_setopt($ch,CURLOPT_URL,$strURL);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch,CURLOPT_CONNECTTIMEOUT ,3);
    curl_setopt($ch,CURLOPT_TIMEOUT, 20);
    $header = array('User-Agent: Jesus');
    curl_setopt($ch,CURLOPT_HTTPHEADER, $header);
    if($mxdPost !== false)
    {
        array_push($header, "Content-type: application/json");
        array_push($header, "Authorization: Token $strToken");
        curl_setopt($ch, CURLOPT_HTTPHEADER, $header);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $mxdPost);

    }
    for($intI=0; $intI<$intRetries; $intI++)
    {
        $strResponse = curl_exec($ch);
        $responseCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        if($responseCode >= 300 || $strResponse == '')
            continue;
        break;
    }
    if(!$strResponse)
        return false;
    curl_close($ch);
    print_r("Request finished with status code: $responseCode \n");
    return $strResponse;
}

?>