<?php

if ( isset( $argv[1] ) ) {
    $strToken = $argv[1];
    $strMainURL = 'http://www.aippimm.ro/categorie/propuneri_lg/';
    $strSubMainURL = 'http://www.aippimm.ro/categorie/transparenta-decizionala---modificare-hg-96-2011/';
    $strOtherDocuments = 'http://www.aippimm.ro/categorie/info_util/legislatie/';

    print_r("Starting to parse $strSubMainURL \n");
    $strContent = _getURL($strSubMainURL);
    if (!$strContent) {
        print_r('!!ERROR!! Pagina de transparenta decizionala nu este functionala sau a fost schimbata, verifica ' . $strMainURL . PHP_EOL);
        return false;

    }
    _parseContent($strContent,$strToken);

    print_r("Starting to parse $strOtherDocuments \n");
    $strContent = _getURL($strOtherDocuments);
    if (!$strContent) {
        print_r('!!ERROR!! Pagina de transparenta decizionala nu este functionala sau a fost schimbata, verifica ' . $strMainURL . PHP_EOL);
        return false;

    }
    _parseContent($strContent,$strToken);
    return true;
}
else
{
    print_r('!!ERROR!! No token inputed'. PHP_EOL);
    return false;
}

function _parseContent($strContent,$strToken)
{
    $strPostURl = 'http://czl-api.code4.ro/api/publications/';
    /* regex that gets about all the info we need about the documents */
    if(preg_match_all('%<a class="lead_subcat" href="(?<url_article>.*?)" title="[\w\d \/-]+"><strong>(?<title>.*?)<\/strong><\/a> - (?<date>\d{1,2}\.\d{1,2}\.\d{1,4})[\w- <>\/]+?(<div class="files_container">(?<docs_raw>.*?))?<\/div>%s', $strContent, $arrArticlesInfo))
    {
        $arrPostDocuments = array();
        $intCount = count($arrArticlesInfo[0]);
        if($intCount === 0)
        {
            print_r('!!NOTICE!! ' . PHP_EOL);
            return false;
        }
        for($intI = 0; $intI < $intCount; $intI++)
        {
            $arrItem = array(
                'identifier' => '',
                'title' => '',
                'type' => '',
                'institution' => 'afaceri',
                'date' => '',
                'description' => '',
                'feedback_days' => null,
                'contact' => array('email' => 'directia.imm@imm.gov.ro'),
                'documents' => array()
            );
            $arrItem['title'] = $arrArticlesInfo['title'][$intI];
            $arrItem['description'] = $arrItem['title'];
            /* format the date into ISO 8601 */
            $date = DateTime::createFromFormat('d.m.Y', $arrArticlesInfo['date'][$intI]);
            $output = $date->format('Y-m-d');
            $arrItem['date'] = $output;
            /* gets the corresponding type of document */
            $type = _getCorrespondingType($arrItem['title']);
            $arrItem['type'] = ($type) ? $type : '';

            /* gets the document links */

                if(preg_match_all('%href="((.*?)\.\w{1,4})"%s', $arrArticlesInfo['docs_raw'][$intI], $arrDocuments))
            {
                if(count($arrDocuments[1]) < 1)
                    continue;
                foreach($arrDocuments[1] as $key=>$document)
                {
                    $arrItem['documents'][$key]['url'] = $document;
                    $mxdDocType = _getCorrespondingDocumentType($document);
                    $arrItem['documents'][$key]['type'] = ($mxdDocType) ? $mxdDocType : $type;
                }
                /* the identifier is calculated using the name of the document */
                $arrRawIdentifier = explode('/', $arrDocuments[2][0]);
                $arrItem['identifier'] = $arrItem['institution'] . '-aippimm-' . strtolower($arrRawIdentifier[count($arrRawIdentifier)-1]);
            }
            else
            {
                if(isset($arrArticlesInfo['url_article'][$intI]))
                {
                    $arrItem['documents'][0]['url'] = $arrArticlesInfo['url_article'][$intI];
                    $arrItem['documents'][0]['type'] = $type;
                    $arrItem['identifier'] = $arrItem['institution'] . '-aippimm-' . strtolower(str_replace(' ', '-', trim($arrItem['title'])));
                }
                else
                {
                    print_r('!!NOTICE!! Articolul nu contine documente' . PHP_EOL);
                    continue;
                }
            }
            array_push($arrPostDocuments, $arrItem);
            unset($arrItem);
        }
        print_r($arrPostDocuments);
        foreach($arrPostDocuments as $document)
        {
            $jsonEncoded = json_encode($document);
            /*API CALL*/
            $strResponse = _getURL($strPostURl, $strToken, $jsonEncoded);
            print_r($strResponse . PHP_EOL);
        }
        return true;
    }
    else
    {
        print_r('!!ERROR!! Informatiile pentru articole nu au putut fi luate' . PHP_EOL);
        return false;
    }
}

/**
 * Function that translates the title into corresponding document types
 *
 * @param $strTitle
 * @return string
 */
function _getCorrespondingType($strTitle){
    if(strpos($strTitle, 'OUG') !== false || strpos($strTitle, 'Ordonanta de Urgenta') !== false || strpos($strTitle, 'ORDONANTA DE URGENTA') !== false)
        return 'OUG';
    else if(strpos($strTitle, 'HG') !== false || strpos($strTitle, 'Hotarare') !== false)
        return 'HG';
    else if(strpos($strTitle, 'LEGE') !== false)
        return 'LEGE';
    else
        return 'OTHER';
}

/**
 * Function that gets a document title and conceives a title out of it
 *
 * @param $strDocTitle
 */
function _getCorrespondingDocumentType($strDocTitle){
    $strDocTitle = strtolower($strDocTitle);
    if(strpos($strDocTitle, 'fundam') !== false || strpos($strDocTitle, 'nf-') !== false)
        return 'nota_fundamentare';
    else
        return false;
}

/**
 * Function that executes a request
 *
 * @param $strURL
 * @param bool $mxdPost
 * @return bool|mixed
 */
function _getURL($strURL, $strToken=false, $mxdPost = false){
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