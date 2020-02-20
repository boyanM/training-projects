function priceLoader(quantity,price,basket_id){
  // session_id 
  if (quantity == 0 || quantity === undefined) {
    document.getElementById("price"+basket_id).innerHTML = "Price: ";
    return;
  } else {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        price_index = this.responseText.search("\\|");
        document.getElementById("price"+basket_id).innerHTML =
         this.responseText.slice(0,price_index);
        
        document.getElementById("total").innerHTML =
         this.responseText.slice(price_index+1)

        document.getElementById("total_h").value =
         this.responseText.slice(price_index+8,-1)  
      }
    };
    xmlhttp.open("GET",
     "https://test.com/cgi-bin/priceLoader.py?basket_id="
        + basket_id
          + "&quantity=" + quantity, true);
    xmlhttp.send();
  }
}
