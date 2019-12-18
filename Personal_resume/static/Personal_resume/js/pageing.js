
window.onload = function(){
    var xhr=new XMLHttpRequest();
    xhr.open('GET', "http://127.0.0.1:8000/GetPageDate/", true);
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
};


function createTable(jsondata){var tableId = document.getElementById('tablebox');var trth=document.createElement("tr");var th=document.createElement("th");var th1=document.createElement("th");var th2=document.createElement("th");var th3=document.createElement("th");var th4=document.createElement("th");var th5=document.createElement("th");th.innerHTML="用户名";th1.innerHTML="密码";th2.innerHTML="年龄";th3.innerHTML="性别";th4.innerHTML="民族";th5.innerHTML="id";trth.appendChild(th);trth.appendChild(th1);trth.appendChild(th2);trth.appendChild(th3);trth.appendChild(th4);trth.appendChild(th5);tableId.appendChild(trth);for (i = 0; i < jsondata.length; i++){var tr=document.createElement("tr");var td=document.createElement("td");var td1=document.createElement("td");var td2=document.createElement("td");var td3=document.createElement("td");var td4=document.createElement("td");var td5=document.createElement("td");td.innerHTML=jsondata[i]['username'];td1.innerHTML=jsondata[i]['passworld'];td2.innerHTML=jsondata[i]['sex'];td3.innerHTML=jsondata[i]['age'];td4.innerHTML=jsondata[i]['nation'];td5.innerHTML=jsondata[i]['id'];tr.appendChild(td);tr.appendChild(td1);tr.appendChild(td2);tr.appendChild(td3);tr.appendChild(td4);tr.appendChild(td5);tableId.appendChild(tr);}}


function deltr(){var tb = document.getElementById('tablebox');var rowNum=tb.rows.length;for (i=0;i<rowNum;i++) {tb.deleteRow(i);rowNum=rowNum-1;i=i-1;}}


function transferpage(page) {
    var xhr=new XMLHttpRequest();
    xhr.open('post', "http://127.0.0.1:8000/pageination/", true);
    xhr.setRequestHeader('content-type','application/x-www-form-urlencoded');
    var a = "page="+String(page);
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






















