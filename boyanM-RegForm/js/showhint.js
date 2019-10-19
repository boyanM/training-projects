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
    xmlhttp.open("GET", "http://127.0.0.1:8000/cgi-bin/showhint.py?q=" + str, true);
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
          document.getElementById("ekatteHint").innerHTML = this.responseText;
        }
      };
      xmlhttp.open("GET", "http://127.0.0.1:8000/cgi-bin/showhint_ekatte.py?q=" + str, true);
      xmlhttp.send();
    }
  }
}