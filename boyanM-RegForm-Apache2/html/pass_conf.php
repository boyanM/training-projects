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
		 pass_auth1_sec=$_POST[timer1]
		  ,pass_auth2_min=$_POST[timer2]
		   ,after_attempts=$_POST[timer3]
		    ,pass_exp=$_POST[timer4];";

		$check = pg_query($dbconn,$update); //or die('Query failed: ' . pg_last_error());

}



$query = "select pass_auth1_sec,pass_auth2_min,after_attempts,pass_exp from pass_auth;";

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
		  <li><a href="https://test.com/cgi-bin/rendering/references.py">All Orders</a></li>
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
			<form name="timers" method="POST" action="https://test.com/pass_conf.php">
				<label for="timer1"><b>After wrong attempt wait: </b></label>
				<input type="number" name="timer1" 
				value="<?php echo $table['pass_auth1_sec']; ?>" required>

				<br><label for="timer2"><b>After N wrong attempts wait: </b></label>
				<input type="number" name="timer2" 
				value="<?php echo $table['pass_auth2_min']; ?>" required>

				<br><label for="timer3"><b>After N attempts:</b></label>
				<input type="number" name="timer3" 
				value="<?php echo $table['after_attempts']; ?>" required>
				
				<br><label for="timer4"><b>Password Expires:</b></label>
				<input type="number" name="timer4" 
				value="<?php echo $table['pass_exp']; ?>" required>

				<br><br> <button type="submit" class="del_btn">Save</button>
		</div>

	</body>
</html>			
