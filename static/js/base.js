var res;
//create a list of cuisines under browse-cuisine menu
function create_list(res){
    var ul_list = document.getElementById("cuisine");
    for(i=0;i<res.length;i++){
        var li = document.createElement("li");
        var a = document.createElement("a");
        console.log(res[i])
        a.href="/breakingbread/browse/cuisine/"+res[i].toLowerCase()+"/";
        a.innerHTML=res[i];
        li.appendChild(a);
        ul_list.appendChild(li);
            
    }
        
}

function initialize(){
    var xhttp=new XMLHttpRequest();
    xhttp.onreadystatechange=function(){
            
        if(this.readyState==4 && this.status==200){
            res = JSON.parse(this.response) ;
            create_list(res["cuisines"]);
                
        }
        else{
            console.log(this.readyState);
            console.log(this.status);
        }
    };
    xhttp.open("GET","/breakingbread/cuisine",true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send();
        
}
window.onload=initialize();

