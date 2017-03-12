<?php

$strMainURL = 'http://www.aippimm.ro/categorie/propuneri_lg/';
$strSubMainURL = 'http://www.aippimm.ro/categorie/transparenta-decizionala---modificare-hg-96-2011/';
$strPostURl = 'http://czl-api.code4.ro/api/publications/';
$arrPostDocuments = array();

$strContent= _getURL($strSubMainURL);
if($strContent)
{
    file_put_contents('test.txt', $strContent);
    if(preg_match_all('%<a class="lead_subcat" href="(?<url_article>.*?)" title="(?<title>.*?)"><strong>.*?<\/strong><\/a> - (?<date>\d{1,2}\.\d{1,2}\.\d{1,4}).*?<div class="files_container">(?<docs_raw>.*?)<\/div>%s', $strContent, $arrArticlesInfo))
    {
        $intCount = count($arrArticlesInfo[0]);
        if($intCount !== 0)
        {
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
                $date = DateTime::createFromFormat('d.m.Y', $arrArticlesInfo['date'][$intI]);
                $output = $date->format('Y-m-d');
                $arrItem['date'] = $output;
                $type = _getCorrespondingType($arrItem['title']);
                $arrItem['type'] = ($type) ? $type : '';

                if(preg_match_all('%href="((.*?)\.\w{1,4})"%s', $arrArticlesInfo['docs_raw'][$intI], $arrDocuments))
                {
                    if(count($arrDocuments[1]) < 1)
                        continue;
                    foreach($arrDocuments[1] as $key=>$document)
                    {
                        $arrItem['documents'][$key]['url'] = $document;
                        $arrItem['documents'][$key]['type'] = ($arrItem['type'] === '') ? 'oug' : $arrItem['type']  ;
                    }
                    $arrRawIdentifier = explode('/', $arrDocuments[2][0]);
                    $arrItem['identifier'] = $arrItem['institution'] . '-' . strtolower($arrRawIdentifier[count($arrRawIdentifier)-1]);
                    array_push($arrPostDocuments, $arrItem);
                    unset($arrItem);
                }
                else
                {
                    print_r('!!NOTICE!! Articolul nu are documente' . PHP_EOL);
                }
            }
            print_r($arrPostDocuments);
            foreach($arrPostDocuments as $document)
            {
                $jsonEncoded = json_encode($document);
                //API CALL
//                $strResponse = _getURL($strPostURl, $jsonEncoded);
                print_r($strResponse . PHP_EOL);
            }
            return true;
        }
    }
    else
    {
        print_r('!!ERROR!! Informatiile pentru articole nu au putut fi luate' . PHP_EOL);
        return false;
    }
}
else
{
    print_r('!!ERROR!! Pagina de transparenta decizionala nu este functionala sau a fost schimbata, verifica ' . $strMainURL . PHP_EOL);
    return false;
}

return false;


function _getCorrespondingType($strTitle){
    if(strpos($strTitle, 'OUG') !== false || strpos($strTitle, 'Ordonanta de Urgenta') !== false)
        return 'OUG';
    else if(strpos($strTitle, 'HG') !== false)
        return 'HG';
    else
        return 'OTHER';
}


function _getURL($strURL, $mxdPost = false){
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
        array_push($header, "Authorization: Token afaceri-very-secret-key");
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