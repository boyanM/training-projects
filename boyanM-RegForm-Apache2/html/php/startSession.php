<?php

session_start();

$user = $_GET["user"];
$_SESSION["user"] = $user;
$_SESSION["login"] = True;
$_SESSION["active"] = $_SERVER['REQUEST_TIME'];

$dbconn = pg_connect("host=localhost dbname=wordpress user=wp_read password=1111")or die('Could not connect: ' . pg_last_error());
			$query = "select user_timeout from pass_auth;";
			$result = pg_query($query) or die('Query failed: ' . pg_last_error());
			$result = pg_fetch_assoc($result);
			$result = $result['user_timeout'];

$_SESSION['user_timeout'] = $result;


print_r($_SESSION);

header("Location: http://test.com/main.php");

?>