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
    var url = window.location.protocol + '//'+ 'fifth-ave-api.borderxlab.com' + '/api/v1/link-resolve';
    url = url + "?channel=curation&target=pdp&productId=" + productID + "&source=bieyang-app";
    window.location.href = url;
}

function goDeepLinkPLP(queryString)
{
    var url = window.location.protocol + '//'+ 'fifth-ave-api.borderxlab.com' + '/api/v1/link-resolve';
    url = url + "?channel=curation&target=plp?" + queryString + "&source=bieyang-app";
    window.location.href = url;

}

function goShareLink(link)
{
    var url = 'share://'+ 'fifth-ave-api.borderxlab.com' + '/' + link;    
    window.location.href = url;
}   

/*----------------------------------------------
------------------------------------------------
2.0. General
------------------------------------------------
----------------------------------------------*/
var readyFunc = function(){
    //hide share bar if outside app

    // var app_version_query = location.search;
    // if (app_version_query.indexOf("showInstallbtn") < 0) {
    //     $(".inapp_hidden").css("display","none");
    //     $(".inapp_display").css("display","inline");
    // }

    var user_location = 0;
    var standalone = window.navigator.standalone,
        userAgent = window.navigator.userAgent.toLowerCase(),
        safari = /safari/.test( userAgent ),
        ios = /iphone|ipod|ipad/.test( userAgent );


    if( ios ) {
        // in wechat;
        if ( !standalone && !safari && userAgent.match(/MicroMessenger/i)=="micromessenger") {
            user_location = 1;
            // in app;
        }else if (!standalone && !safari){
            user_location = 2;

        }
    } else {
        // outside app
        // user_location = 0;

        // $(".inapp_hidden").css("display","inline");
        // $(".inapp_display").css("display","none");
    }

    if (user_location === 2) {
        $(".inapp_hidden").css("display","none");
        $(".inapp_display").css("display","inline");
    }else if (user_location === 1){
        $(".inapp_hidden").css("display","inline");
        $(".inapp_display").css("display","none");

        $(".btn--download").on('tap', function(){
            window.location.replace("http://fifth-ave-api.borderxlab.com/static/curation/app_store.html");
        });
    }else{
        $(".inapp_hidden").css("display","inline");
        $(".inapp_display").css("display","none");

        $(".btn--download").on('tap', function(){
            window.location.replace("http://r.yoz.io/tR.c.cK");
        });
    }
};

$(document).ready(readyFunc);


