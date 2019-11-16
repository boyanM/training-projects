<?php	
	session_start();

	if(!isset($_SESSION['login']) && !isset($_SESSION['admin'])
	 && !isset($_GET['edit'])){
		session_unset();
		session_destroy();
		header("Location: http://test.com/admin.html");
	}

	$dbconn = pg_connect("host=localhost dbname=wordpress user=wpuser password=password")or die('Could not connect: ' . pg_last_error());

	if(!empty($_POST)){
		$values = "";
		foreach($_POST as $key=>$value){
			if($key == 'country'){
				$values .= "(select id from countries where country='$value'),";	
			}
			else{
				$values .= "'$value',"; 
			}
		}
		$values .= "'\$pbkdf2-sha256$29000$09o7J8S4F6K01lqrVcpZaw\$sbU70y1lYT70fJoHgIXxox2f7ng7Jj22wGf9OgzIs3o','t',now()";
		 	try{
	 			$insert = "insert into customers (email,username,name,lname,bday,gender,phone,country_id,password,confirmed,last_pass_change) VALUES($values);";

		 	$check = pg_query($dbconn,$insert);
		  	if(!$check){
		  		throw new Exception("Error while updating the database");
		  			
		  	}
		  }

			catch(Exception $e){
			$error = "Wrong filled fields !";

			}

			if(!(isset($error))){
			header("Location: http://test.com/useracc.php");
			}
		}

?>

<!DOCTYPE html>
<html lang="bg">

<head>
	<meta charset=utf-8>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="http://test.com/search.css">
</head>
<body>
<a href="http://test.com/useracc.php" class="add_btn">GO BACK</a>
<?php
		if(isset($error)){
			echo "<div id=\"error\">
				<p>$error</p>
			</div>";
		}
?>	
	<form name="new_user" method="POST" action="http://test.com/createuser.php">

				<label for="email"><b>E-mail</b></label>
				<input type="text" name="email" required>
				<br><label for="username"><b>Username</b></label>
				<input type="text" name="username" required>
				<br><label for="name"><b>Name</b></label>
				<input type="text" name="name" required>
				<br><label for="lname"><b>Last name</b></label>
				<input type="text" name="lname" required>
				<br><label for="bday"><b>Birthday</b></label>
				<input type="text" name="bday" required>
				<br><label for="gender"><b>Gender</b></label>
				<input type="text" name="gender" required>
				<br><label for="phone"><b>Phone</b></label>
				<input type="text" name="phone" required>
				<br><label for="country"><b>Country</b></label>
				<input type="text" name="country" required>
				<br><br> <button type="submit" class="del_btn">Save</button>
	</form>
</body>
</html>	