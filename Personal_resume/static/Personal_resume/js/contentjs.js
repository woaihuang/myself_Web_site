window.onload = function(){
    var urlstr = location.search;
    var bookUrl = "http://www.xbiquge.la"+urlstr.match((/(\S*)&/))[1].substring(1);
    var bookname = urlstr.match((/&(\S*)/))[1];
    contentText(bookUrl, bookname)
};



function contentText(bookUrl, AccessName) {
    var xhr=new XMLHttpRequest();
    var b = window.location.host;
    xhr.open('post', "http://"+b+"/Personal_resume/Access_to_the_body/", true);
    xhr.setRequestHeader('content-type','application/x-www-form-urlencoded');
    var a = "bookUrl="+String(bookUrl)+"&bookname="+AccessName;
    xhr.send(a);
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4){
            if(xhr.status==200){
                document.getElementById(eval(xhr.responseText)[2]).className="active";
                document.getElementById("content").style.width="90%";
                document.getElementById("content").style.background="#F7F7F7";
                document.getElementById("content").style.fontSize="22px";
                document.getElementById("content").style.marginLeft="100px";
                document.getElementById("content").style.height="90%";
                document.getElementById("bookName").innerText="     "+eval(xhr.responseText)[0];
                document.getElementById("content").innerText=eval(xhr.responseText)[1];
            }
        }
    }
}




