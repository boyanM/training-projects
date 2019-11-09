<?php

session_start();

$user = $_GET["user"];
$_SESSION["user"] = $user;
$_SESSION["login"] = True;
$_SESSION["admin"] = True;


header("Location: http://test.com/search.php");

?>