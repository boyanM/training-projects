<?php
	session_start();

	if(isset($_SESSION['active']) && $_SERVER['REQUEST_TIME'] - $_SESSION['active'] < $_SESSION['user_timeout']){

		$user = $_SESSION['user'];
		$login = $_SESSION['login'];
		$timeout = $_SESSION['user_timeout'];
		
		session_unset();
		session_destroy();
		session_start();

		$_SESSION['user'] = $user;
		$_SESSION['login'] = $login;
		$_SESSION['active'] = $_SERVER['REQUEST_TIME'];
		$_SESSION['user_timeout'] = $timeout;
	}

	else{
		session_unset();
		session_destroy();
		header("Location: http://test.com/login.html");
	}

	print_r($_SESSION);
	
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
	  <li><a class="active" href="#home">Home</a></li>
	  <li>
	  	<a href="http://test.com/php/check.php?goto=account.php">Account</a>
	  </li>
	  <li><a href="#contact">Contact</a></li>
	  <li><a href="#about">About</a></li>
	</ul>

</body>
</html>