<?php

	session_start();
		if(isset($_SESSION['active']) && $_SERVER['REQUEST_TIME'] - $_SESSION['active'] < $_SESSION['user_timeout']){

		$user = $_SESSION['user'];
		$login = $_SESSION['login'];
		$timeout = $_SESSION['user_timeout'];
		
		session_unset();
		session_destroy();
		session_start();

		$_SESSION["active"] = $_SERVER['REQUEST_TIME'];

		$_SESSION["user"] = $user;
		$_SESSION["login"] = $login;
		$_SESSION['user_timeout'] = $timeout;
	}

	else{
		session_unset();
		session_destroy();
		header("Location: https://test.com/login.html");
	}


	$dbconn = pg_connect("host=localhost dbname=wordpress user=wpuser password=password")or die('Could not connect: ' . pg_last_error());
			$query = "select c.username,c.email,co.country,c.phone from customers c join countries co on(c.country_id = co.id and c.username='$_SESSION[user]');";
			$result = pg_query($query) or die('Query failed: ' . pg_last_error());
			$result = pg_fetch_assoc($result);
	
	if(isset($_POST["username"]) && $_POST["username"] != $result['username']){
		$new_user = pg_escape_string($_POST["username"]);
		$update = "update customers set username='$new_user'
		 where username = '$result[username]';";
		pg_query($dbconn,$update) or die('Query failed: ' . pg_last_error());
    	$_SESSION['user'] = $new_user; 
	}

/*
	if(isset($_POST["psw"]) && isset($_POST["psw_repeat"])
	 && $_POST["psw"]==$_POST["psw_repeat"]){
		$new_psw = $_POST["psw"];
*/
	if(isset($_POST["mail"]) && $_POST["mail"] != $result['email']){
		$new_mail = pg_escape_string($_POST["mail"]);
		$update = "update customers set email='$new_mail'
		where email = '$result[email]';";
		pg_query($dbconn,$update) or die('Query failed: ' . pg_last_error());


	}

	if(isset($_POST["country"]) && $_POST["country"] != $result['country'] ){
		$new_country = pg_escape_string($_POST["country"]);
		$update = "update customers set country_id=(select id from countries where country='$new_country') where username = '$_SESSION[user]';";
		pg_query($dbconn,$update) or die('Query failed: ' . pg_last_error());

	}

	if(isset($_POST["phone"]) && $_POST["phone"] != $result['phone'] ){
		$new_phone = pg_escape_string($_POST["phone"]);
		$update = "update customers set phone ='$new_phone' where username = '$_SESSION[user]';";
		pg_query($dbconn,$update) or die('Query failed: ' . pg_last_error());
	}

	$query = "select c.username,c.email,co.country,c.phone from customers c join countries co on(c.country_id = co.id and c.username='$_SESSION[user]');";
	$result = pg_query($query) or die('Query failed: ' . pg_last_error());
	$result = pg_fetch_assoc($result);
	pg_close($dbconn);
	print_r($_SESSION)

?>

<!DOCTYPE html>
<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="https://test.com/main.css">
	</head>
	<body>
	<ul>
	  <li><a class="active" href="https://test.com/php/check.php?goto=main.php">Home</a></li>
	  <li>
	  	<a href="https://test.com/php/check.php?goto=account.php">Account</a>
	  </li>
	  <li><a href="#contact">Contact</a></li>
	  <li><a href="https://test.com/php/logout.php">Logout</a></li>
	</ul>


	<link rel="stylesheet" type="text/css" href="../style1.css">
	<script type="text/javascript" src="https://test.com/js/editacc.js"></script>
	<script type="text/javascript" src="https://test.com/js/showhint.js"></script>
	
		<p id="open">Welcome to your account</p>
	<br>
	<hr>
	
		<form name="edit_acc" method="POST"
		 action="https://test.com/account.php">
			<label>Username</label>
			<input type="text" class="acc_field" name="username" value='<?php echo $result['username'] ?>' disabled required>
			
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
			<input type="text" class="acc_field" name="mail"
			value='<?php echo $result['email'] ?>' disabled required>
			
			<label for="Country">Country</label>
	  		<input type="text" onkeyup="showHint(this.value)" name="country"
	  		 id="txtHint" class="acc_field" list="countries"
	  		 value='<?php echo $result['country'] ?>' disabled required>
	
			<label>Phone</label>
			<input type="text" class="acc_field" name="phone" 
			value='<?php echo $result['phone'] ?>' disabled required>
		<hr>
	
	<button type="button" id="edit" onclick="editAcc()">Edit profile</button>
	<input type="submit" id="save_btn" value="Save">
	</form>
	</body>
	</html>
