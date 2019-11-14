<?php
	session_start();
		if(!(isset($_SESSION['login']))){
			header("Location: http://test.com/login.html");
		}

		else{
			
			if(isset($_SESSION['active']) && $_SERVER['REQUEST_TIME'] - $_SESSION['active'] <$_SESSION['user_timeout']) {

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