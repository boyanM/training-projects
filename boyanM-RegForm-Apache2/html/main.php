<?php
	session_start();

	if(isset($_SESSION['active']) && $_SERVER['REQUEST_TIME'] - $_SESSION['active'] < $_SESSION['user_timeout'] && $_SERVER['REQUEST_TIME'] < $_SESSION['auto_logout']) {

		$user = $_SESSION['user'];
		$login = $_SESSION['login'];
		$timeout = $_SESSION['user_timeout'];
		$auto_logout = $_SESSION['auto_logout'];

		session_unset();
		session_destroy();
		session_start();

		$_SESSION['user'] = $user;
		$_SESSION['login'] = $login;
		$_SESSION['active'] = $_SERVER['REQUEST_TIME'];
		$_SESSION['user_timeout'] = $timeout;
		$_SESSION['auto_logout'] = $auto_logout;
	}

	else{
		session_unset();
		session_destroy();
		header("Location: https://test.com/login.html");
	}

	print_r($_SESSION);
	
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
	  <li><a class="active" href="#home">Home</a></li>
	  <li>
	  	<a href="https://test.com/php/check.php?goto=account.php">Account</a>
	  </li>
	  <li><a href="#contact">Contact</a></li>
	  <li><a href="https://test.com/php/logout.php">Logout</a></li>
	  <li class="menu_right"><a href="https://test.com/php/logout.php">Cart</a></li>

	</ul>

</body>
</html>