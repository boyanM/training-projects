<?php

session_start();

$user = $_GET["user"];
$_SESSION["user"] = $user;
$_SESSION["login"] = True;
$_SESSION["active"] = $_SERVER['REQUEST_TIME'];

$dbconn = pg_connect("host=localhost dbname=wordpress user=wp_read password=1111")or die('Could not connect: ' . pg_last_error());
			$query = "select user_timeout,auto_logout from pass_auth;";
			$result = pg_query($query) or die('Query failed: ' . pg_last_error());
			$result = pg_fetch_assoc($result);

$_SESSION['user_timeout'] = $result['user_timeout'];
$_SESSION['auto_logout'] = $_SERVER['REQUEST_TIME'] + $result['auto_logout'];

print_r($_SESSION);

header("Location: https://test.com/main.php");

?>