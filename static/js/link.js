/* ************************************************
**************************************************

Website Name: Beyond
Website URL: borderxlab.com
Website Author: Aaron Cheng
Author URL: chengfolio.com
Copyright 2014. All Rights Reserved.

************************************************ */

/*----------------------------------------------
------------------------------------------------
1.1. deeplink function
------------------------------------------------
----------------------------------------------*/	
function goDeepLinkPDP(productID)
{
    var url = window.location.protocol + '//'+ window.location.host + '/api/v1/link-resolve';
    url = url + "?channel=curation&target=pdp&productId=" + productID;
    window.location.href = url;
}

function goDeepLinkPLP(queryString)
{
    var url = window.location.protocol + '//'+ window.location.host + '/api/v1/link-resolve';
    url = url + "?channel=curation&target=plp?" + queryString;
    window.location.href = url;

}

function goShareLink(link)
{
    var url = 'share://'+ window.location.host + '/' + link;    
    window.location.href = url;
}   

/*----------------------------------------------
------------------------------------------------
2.0. General
------------------------------------------------
----------------------------------------------*/	
$(document).ready(function(){	
    //hide share bar if outside app 
    var app_version_query = location.search;
    if (app_version_query.indexOf("showInstallbtn") < 0) {
        $(".inapp_hidden").css("display","none");
        $(".inapp_display").css("display","inline");
    }
	

});

