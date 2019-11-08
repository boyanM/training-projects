function showButton(divID,but1ID,btn2ID){

	var div = document.getElementById(divID);
	div.style.display = "block";

	var showbtn = document.getElementById(but1ID);
	showbtn.style.display = "none";

	var hidebtn = document.getElementById(btn2ID);
	hidebtn.style.display = "inline-block";
}

function hideButton(divID,btn1ID,btn2ID){

	var div = document.getElementById(divID);
	div.style.display = "none";

	var showbtn = document.getElementById(btn1ID);
	showbtn.style.display = "inline-block";

	var hidebtn = document.getElementById(btn2ID);
	hidebtn.style.display = "none";

}
