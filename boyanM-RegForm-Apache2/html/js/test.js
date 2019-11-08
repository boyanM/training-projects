function test(){
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("txtHint").innerHTML = this.responseText;
    }
  };
  xmlhttp.open("GET", "http://test.com/cgi-bin/test2.py", true);
  xmlhttp.send();

}