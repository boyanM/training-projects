<?php
session_start();

if(!isset($_SESSION['login']) && !isset($_SESSION['admin']) && $_SESSION['admin'] != True){
	session_unset();
	session_destroy();
	header("Location: https://test.com/admin.html");
}

print_r($_SESSION);

$dbconn = pg_connect("host=localhost dbname=wordpress user=wpuser password=password")or die('Could not connect: ' . pg_last_error());

if(!empty($_POST)){
		$update="update pass_auth set 
		 user_timeout=$_POST[timer1]";

		$check = pg_query($dbconn,$update);
}

$query = "select user_timeout from pass_auth;";

$result = pg_query($dbconn,$query) or die('Query failed: ' . pg_last_error());
$table = pg_fetch_assoc($result);



?>


<!DOCTYPE html>

<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="https://test.com/search.css">
	</head>
	<body>
		<ul>
		  <li><a
		   href="https://test.com/useracc.php" class="active">User Accounts</a></li>
		  <li>
		  	<a href="https://test.com/pass_conf.php">Password Configuration</a>
		  </li>
		  <li><a href="https://test.com/timeout_conf.php">Timeout Configuration</a></li>
		</ul>

			<?php
				if(isset($check) && $check == false){
					echo "
					<div>
					Fail to update the settings
					</div>";

				}
				elseif(isset($check) && $check != false){
					echo "
					<div id=\"succesful_save\">
						Succesful update !
					</div>";
				}

			?>
		

		<div>
			<form name="timers" method="POST" action="https://test.com/timeout_conf.php">
				<label for="timer1"><b>User Timeout Time: </b></label>
				<input type="number" name="timer1" value="<?php echo $table['user_timeout'];?>" required>

				<br><br> <button type="submit" class="del_btn">Save</button>
		</div>

	</body>
</html>			
