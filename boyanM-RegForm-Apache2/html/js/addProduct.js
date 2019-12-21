function addProduct(customer_id,product_id){
  if (customer_id == 0 && product_id == 0) {
    document.getElementById("message").innerHTML = "";
    return;
  } else {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        document.getElementById("message").innerHTML = this.responseText;
      }
    };
    xmlhttp.open("GET",
     "https://test.com/cgi-bin/addProduct.py?customer_id="
        + customer_id
          + "&product_id=" + product_id, true);
    xmlhttp.send();
  }
}
