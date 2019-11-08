<?php
	session_start();
		if(!(isset($_SESSION['login']))){
			header("Location: http://test.com/login.html");
		}

		else{
			$dbconn = pg_connect("host=localhost dbname=wordpress user=wp_read password=1111")or die('Could not connect: ' . pg_last_error());
			$query = "select user_timeout from pass_auth;";
			$result = pg_query($query) or die('Query failed: ' . pg_last_error());
			$result = pg_fetch_assoc($result);
			if(isset($_SESSION['active']) && $_SERVER['REQUEST_TIME'] - $_SESSION['active'] < $result['user_timeout']) {

				$goto = $_GET['goto'];
				$_SESSION["active"] = $_SERVER['REQUEST_TIME'];
				header("Location: http://test.com/$goto");
			}
			
			else{
				session_unset();
				session_destroy();
				header("Location: http://test.com/login.html");
			}
	}

	
	print_r($_SESSION);
	?>