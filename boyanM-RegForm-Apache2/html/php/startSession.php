<?php

session_start();

$user = $_GET["user"];
$_SESSION["user"] = $user;
$_SESSION["login"] = True;
$_SESSION["active"] = $_SERVER['REQUEST_TIME'];
print_r($_SESSION);

header("Location: http://test.com/main.php");

?>