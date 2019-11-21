function showHint(str) {
  if (str.length == 0) {
    document.getElementById("txtHint").innerHTML = "";
    return;
  } else {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("txtHint").innerHTML = this.responseText;
      }
    };
    xmlhttp.open("GET", "https://test.com/cgi-bin/showhint.py?q=" + str, true);
    xmlhttp.send();
  }
}


function hint(str) {
    
    if (str.length == 0) {
      document.getElementById("ekatteHint").innerHTML = "";
      return;
    } else {
      if(document.getElementById("txtHint").value == "Bulgaria"){
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          response = JSON.parse(this.responseText)

        if (document.contains(document.getElementById("ekatte"))) {
            document.getElementById("ekatte").remove();
}
          var y = document.createElement("DATALIST");
          y.setAttribute("id", "ekatte");
          document.getElementById("ekatteHint").appendChild(y);

          var len = response.length;
          
          var dataList = document.getElementById('ekatte');

          for(var i = 0; i < len;i++){
            var option = document.createElement('option');
            option.value = "["+response[i].id+"] "+ response[i].sname;
            option.label = "обл. " + response[i].aname;
            dataList.appendChild(option);  
          }

          
        }
      };
      xmlhttp.open("GET", "https://test.com/php/showEkatte.php?q=" + str, true);
      xmlhttp.send();
    }
  }
}