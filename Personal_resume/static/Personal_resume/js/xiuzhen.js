window.onload = function(){
    deltr();
    getAllBook();
    bookcraw();
};



function bookcraw() {
    var xhr=new XMLHttpRequest();
    var a = window.location.host;
    xhr.open('GET', "http://"+a+"/Personal_resume/BookCraw/?channel=2", true);
    xhr.send();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 || xhr.readyState==200){
            if(xhr.status==200 || xhr.status==304){
                console.log(xhr.responseText)
            }
        }
    }
}



function getAllBook() {
    var xhr=new XMLHttpRequest();
    var a = window.location.host;
    xhr.open('GET', "http://"+a+"/Personal_resume/Get_catalogue/?channel=2", true);
    xhr.send();
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4 || xhr.readyState==200){
            if(xhr.status==200 || xhr.status==304){
                deltr();JsonDate = eval(xhr.responseText);
                createTable(JsonDate[0]['DateList']);
                new myPagination({
                    id: 'pagination',
                    curPage:1, //初始页码
                    pageAmount: 50,  //每页多少条
                    dataTotal: JsonDate[0]['autoNum'], //总共多少条数据
                    pageTotal: Math.ceil(parseInt(JsonDate[0]['autoNum'], 10)/50), //总页数
                    pageSize: 5, //可选,分页个数
                    showPageTotalFlag:true, //是否显示数据统计
                    showSkipInputFlag:true, //是否支持跳转
                    getPage: function (page) {
                        transferpage(page)
                    }
                });
            }
        }
    }
}


function transferpage(page) {
    var xhr=new XMLHttpRequest();
    var b = window.location.host;
    xhr.open('post', "http://"+b+"/Personal_resume/pageination/", true);
    xhr.setRequestHeader('content-type','application/x-www-form-urlencoded');
    var a = "page="+String(page)+"&channel=1";
    xhr.send(a);
    xhr.onreadystatechange=function(){
        if(xhr.readyState==4){
            if(xhr.status==200){
                JsonDate = eval(xhr.responseText);
                deltr();
                createTable(JsonDate[0]['DateList'])
            }
        }
    }
}



function createTable(jsondata){
    var tableId = document.getElementById('tablebox');
    var trth=document.createElement("tr");
    var th=document.createElement("th");var th1=document.createElement("th");var th2=document.createElement("th");var th3=document.createElement("th");
    th.innerHTML="小说名称";th1.innerHTML="最新章节";th2.innerHTML="更新时间";th3.innerHTML="作者";
    trth.appendChild(th);trth.appendChild(th1);trth.appendChild(th2);trth.appendChild(th3);
    tableId.appendChild(trth);
    for (i = 0; i < jsondata.length; i++){
        var tr=document.createElement("tr");
        var td=document.createElement("td");var td1=document.createElement("td");var td2=document.createElement("td");var td3=document.createElement("td");
        var a = document.createElement("a");a.href="#";a.text=jsondata[i]['bookName'];a.id=jsondata[i]['bookUrl'];a.onclick = function() { stopskip(this) };td.appendChild(a);
        var a1 = document.createElement('a');a1.href=jsondata[i]['ChapterUrl'];a1.text=jsondata[i]['latestChapter'];td1.appendChild(a1);
        td2.innerHTML=jsondata[i]['update'];
        td3.innerHTML=jsondata[i]['author'];
        tr.appendChild(td);tr.appendChild(td1);tr.appendChild(td2);tr.appendChild(td3);
        tableId.appendChild(tr);
    }
}


function deltr(){
    var tb = document.getElementById('tablebox');
    var rowNum=tb.rows.length;
    for (i=0;i<rowNum;i++) {
        tb.deleteRow(i);
        rowNum=rowNum-1;
        i=i-1;
    }
}



function stopskip(column) {
    var bookUrl = column.id;
    var a = window.location.host;
    window.location.href="http://"+a+"/Personal_resume/cataloguepage/?"+bookUrl.substring(21)+"&"+column.text;
}







