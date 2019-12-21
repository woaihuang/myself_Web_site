window.onload = function(){
    var urlstr = location.search;
    var bookUrl = "http://www.xbiquge.la"+urlstr.match((/(\S*)&/))[1].substring(1);
    var bookname = urlstr.match((/&(\S*)/))[1];
    GetCatalogue(bookUrl, bookname);
    getcata(bookUrl, bookname);
};




function getcata(bookUrl, bookname) {
    var xhr=new XMLHttpRequest();
    var b = window.location.host;
    xhr.open('post', "http://"+b+"/Personal_resume/cataloguepage/", true);
    xhr.setRequestHeader('content-type','application/x-www-form-urlencoded');
    var a = "bookUrl="+String(bookUrl)+"&bookname="+bookname;
    xhr.send(a);
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4){
            if(xhr.status==200){
                console.log(xhr.responseText);
            }
        }
    }
}




function GetCatalogue(bookUrl, bookname) {
    var xhr=new XMLHttpRequest();
    var b = window.location.host;
    xhr.open('post', "http://"+b+"/Personal_resume/GetCatalogue/", true);
    xhr.setRequestHeader('content-type','application/x-www-form-urlencoded');
    var a = "bookUrl="+String(bookUrl)+"&bookname="+bookname;
    xhr.send(a);
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4){
            if(xhr.status==200){
                JsonDate = eval(xhr.responseText);
                document.getElementById(JsonDate[2]).className="active";
                createCatalogue(JsonDate[1]['DateList'], JsonDate[0])
            }
        }
    }
}


function createCatalogue(jsondata, bookname) {
    var tableId = document.getElementById('tablebox');
    document.getElementById("bookName").innerText=" "+bookname;
    for (i = 0; i < jsondata.length; i+=3){
        var tr=document.createElement("tr");
        var td=document.createElement("td");var td1=document.createElement("td");var td2=document.createElement("td");
        var a = document.createElement("a");a.href="#";a.text=jsondata[i]['bookName'];a.id=jsondata[i]['bookUrl'];a.onclick = function() { AccessBody(this) };td.appendChild(a);
        var a1 = document.createElement('a');a1.href="#";a1.text=jsondata[i+1]['bookName'];a1.id=jsondata[i+1]['bookUrl'];a1.onclick = function() { AccessBody(this) };td1.appendChild(a1);
        var a2 = document.createElement('a');a2.href="#";a2.text=jsondata[i+2]['bookName'];a2.id=jsondata[i+2]['bookUrl'];a2.onclick = function() { AccessBody(this) };td2.appendChild(a2);
        tr.appendChild(td);tr.appendChild(td1);tr.appendChild(td2);
        tableId.appendChild(tr);
    }
}


function AccessBody(column) {
    var bookUrl = column.id;
    var b = window.location.host;
    window.location.href="http://"+b+"/Personal_resume/contentpage/?"+bookUrl+"&"+column.text;
}
