window.onload = function(){
    var xhr=new XMLHttpRequest();
    xhr.open('GET', "https://s.taobao.com/search?data-key=s&data-value=0&ajax=true&q=%E6%89%8B%E6%9C%BA&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20191017&ie=utf8&bcoffset=4&p4ppushleft=%2C48", true);
    xhr.send();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 || xhr.readyState==200){
            if(xhr.status==200 || xhr.status==304){
                // JsonDate = eval(xhr.responseText);
                console.log(xhr.responseText)
            }
        }
    }
};