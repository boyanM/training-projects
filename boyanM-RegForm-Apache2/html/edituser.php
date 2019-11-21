<?php
	session_start();

	if(!isset($_SESSION['login']) && !isset($_SESSION['admin'])
	 && !isset($_GET['edit'])){
		session_unset();
		session_destroy();
		header("Location: https://test.com/admin.html");
	}


	$dbconn = pg_connect("host=localhost dbname=wordpress user=wpuser password=password")or die('Could not connect: ' . pg_last_error());

	if(!empty($_POST)){
		foreach($_POST as $key=>$value){
		 	try{
		 		if($key == 'country'){
		 			$update = "update customers set country_id=(select id from countries where country='$value') where id=$_GET[edit] ;";
		 		}

		 		else{	
		 			$update = "update customers set $key='$value' where id=$_GET[edit];";
		 		}
		 		$check = pg_query($dbconn,$update);
		  		if(!$check){
		  			throw new Exception("Error while updating the database");
		  			
		  		}

			}
			catch(Exception $e){
			$error = "";

			switch ($key) {
					case "email":
						$error .= "Already user with that email<br>";
						break;
					
					case "username":
						$error .= "Already user with that username<br>";
						break;
					
					case "country":
						$error .= "Already user with that email<br>";
						break;
					default:
       					 $error .= "Error updating $key!";

				}
			}
		}
	}

	$query = "select cu.*,c.country from customers cu join countries c on(cu.country_id=c.id and cu.id='$_GET[edit]');";

	$result = pg_query($dbconn,$query) or die('Query failed: ' . pg_last_error());
?>

<!DOCTYPE html>
<html lang="bg">

<head>
<meta charset=utf-8>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="https://test.com/search.css">
</head>
<body>
	
<?php
		if(isset($error)){
			echo "<div id=\"error\">
				<p>$error</p>
			</div>";
		}
		elseif(!(isset($error)) && !(empty($_POST))){
			echo "<div id=\"succesful_save\">
				<p>Succesful update</p>
			</div>";
		}
?>			
<a href="https://test.com/useracc.php" class="add_btn">GO BACK</a>
<?php
	echo "<br><br>
	<form name=\"edit_form\" method=\"POST\"
	 action=\"https://test.com/edituser.php?edit=$_GET[edit]\">";
	$counter=0;
	while($row = pg_fetch_assoc($result)){
		foreach ($row as $key => $value) {
			if($counter >=9 && $counter <= 18 || $counter == 2 || $counter == 5){
				echo "<label for=\"$key\"><b>$key</b></label>
				<input type=\"text\" name=\"$key\" value=\"$value\" disabled>
				<br>";	
			}
			else{
				echo "<label for=\"$key\"><b>$key</b></label>
				<input type=\"text\" name=\"$key\" value=\"$value\">
				<br>";
			}
			$counter++;
		}

	}
    echo "<br> <button type=\"submit\" class=\"del_btn\">Save</button>";
	echo "</form>";
?>
</body>
</html>