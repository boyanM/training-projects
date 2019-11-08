function editAcc(){
	var fields = document.getElementsByClassName("acc_field");
	for(var i = 0 ; i < fields.length; i++){
		fields[i].disabled = false;
	}
	button = document.getElementById("edit");
	button.style.display="none";

	save_btn = document.getElementById("save_btn");
	save_btn.style.display="block";

	pass_repeat_label = document.getElementById("psw_repeat_label")
	pass_repeat_label.style.display="inline";

	pass_repeat = document.getElementById("psw_repeat")
	pass_repeat.style.display = "block"

	var myInput = document.getElementById("psw");
	var letter = document.getElementById("letter");
	var capital = document.getElementById("capital");
	var number = document.getElementById("number");
	var length = document.getElementById("length");
	
	// When the user clicks on the password field, show the message box
	myInput.onfocus = function() {
	  document.getElementById("message").style.display = "block";
	}
	
	// When the user clicks outside of the password field, hide the message box
	myInput.onblur = function() {
	  document.getElementById("message").style.display = "none";
	}
	
	// When the user starts to type something inside the password field
	myInput.onkeyup = function() {
	  // Validate lowercase letters
	  var lowerCaseLetters = /[a-z]/g;
	  if(myInput.value.match(lowerCaseLetters)) {  
	    letter.classList.remove("invalid");
	    letter.classList.add("valid");
	  } else {
	    letter.classList.remove("valid");
	    letter.classList.add("invalid");
	  }
	  
	  // Validate capital letters
	  var upperCaseLetters = /[A-Z]/g;
	  if(myInput.value.match(upperCaseLetters)) {  
	    capital.classList.remove("invalid");
	    capital.classList.add("valid");
	  } else {
	    capital.classList.remove("valid");
	    capital.classList.add("invalid");
	  }
	
	  // Validate numbers
	  var numbers = /[0-9]/g;
	  if(myInput.value.match(numbers)) {  
	    number.classList.remove("invalid");
	    number.classList.add("valid");
	  } else {
	    number.classList.remove("valid");
	    number.classList.add("invalid");
	  }
	  
	  // Validate length
	  if(myInput.value.length >= 8) {
	    length.classList.remove("invalid");
	    length.classList.add("valid");
	  } else {
	    length.classList.remove("valid");
	    length.classList.add("invalid");
	  }
	}
}

function validate(){
	
	pass_repeat_label = document.getElementById("psw_repeat_label")
	pass_repeat_label.style.display = "none";

	pass_repeat = document.getElementById("psw_repeat")
	pass_repeat.style.display = "none"

	var fields = document.getElementsByClassName("acc_field");
	for(var i = 0 ; i < fields.length; i++){
		fields[i].disabled = true;
	}

	save_btn = document.getElementById("save_btn");
	save_btn.style.display="none";

	button = document.getElementById("edit");
	button.style.display="block";
}