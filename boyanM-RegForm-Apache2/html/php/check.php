<?php
	session_start();
		if(!(isset($_SESSION['login']))){
			header("Location: https://test.com/login.html");
		}

		else{
			
			if(isset($_SESSION['active']) && $_SERVER['REQUEST_TIME'] - $_SESSION['active'] <$_SESSION['user_timeout']) {

				$goto = $_GET['goto'];
				$_SESSION["active"] = $_SERVER['REQUEST_TIME'];
				header("Location: https://test.com/$goto");
			}
			
			else{
				session_unset();
				session_destroy();
				header("Location: https://test.com/login.html");
			}
	}
	
	
	print_r($_SESSION);
	?>