<?php
session_start();

if(!isset($_SESSION['login']) && !isset($_SESSION['admin']) && $_SESSION['admin'] != True){
	session_unset();
	session_destroy();
	header("Location: http://test.com/admin.html");
}

print_r($_SESSION);

?>

<!DOCTYPE html>

<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="http://test.com/search.css">
	</head>
	<body>
		<ul>
		  <li><a class="active"
		   href="http://test.com/useracc.php">User Accounts</a></li>
		  <li>
		  	<a href="http://test.com/php/check.php?goto=account.php">Password Configuration</a>
		  </li>
		  <li><a href="#contact">User Timeout</a></li>
		  <li><a href="#about">To Be Continued...</a></li>
		</ul>
	</body>
</html>			