<?php
	session_start();
?>

<!DOCTYPE html>
<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="http://test.com/main.css">
	</head>
	<body>
	<ul>
	  <li><a class="active" href="http://test.com/php/check.php?goto=main.php">Home</a></li>
	  <li>
	  	<a href="http://test.com/php/check.php?goto=account.php">Account</a>
	  </li>
	  <li><a href="#contact">Contact</a></li>
	  <li><a href="#about">About</a></li>
	</ul>


	<link rel="stylesheet" type="text/css" href="../style1.css">
	<script type="text/javascript" src="http://test.com/js/editacc.js"></script>
	<script type="text/javascript" src="http://test.com/js/showhint.js"></script>
	
		<p id="open">Welcome to your account</p>
	<br>
	<hr>
	
		<form name="edit_acc" method="POST"
		 action="http://test.com/cgi-bin/accfill.py?acc=%s">
			<label>Username</label>
			<input type="text" class="acc_field" name="username" value=%s disabled required>
			
			<label>Password</label>
			<input type="password" class="acc_field" id="psw" name="psw" disabled>
			 	
			 	<div id="message">
				  <h3>Password must contain the following:</h3>
				  <p id="letter" class="invalid">A <b>lowercase</b> letter</p>
				  <p id="capital" class="invalid">A <b>capital (uppercase)</b> letter</p>
				  <p id="number" class="invalid">A <b>number</b></p>
				  <p id="length" class="invalid">Minimum <b>8 characters</b></p>
				</div>
	
			<label id="psw_repeat_label">Repeat Password</label>
			<input type="password" class="acc_field" id="psw_repeat" name="psw_repeat" disabled>
	
			<label>E-mail</label>
			<input type="text" class="acc_field" name="mail" value=%s disabled required>
			
			<label for="Country">Country</label>
	  		<input type="text" onkeyup="showHint(this.value)" value=%s name="country"
	  		 id="txtHint" class="acc_field" list="countries" disabled required>
	
			<label for="address">Address</label>
	  		<input type="text" onkeyup="hint(this.value)" name="address"
	  		 id="ekatteHint" class="acc_field" list="ekatte" value=%s disabled required>
	
			<label>Phone</label>
			<input type="text" class="acc_field" name="phone" value=%s disabled required>
		<hr>
	
	<button type="button" id="edit" onclick="editAcc()">Edit profile</button>
	<input type="submit" id="save_btn" value="Save">
	</form>
	</body>
	</html>
