<?php
session_start();

if(!isset($_SESSION['login']) && !isset($_SESSION['admin']) && $_SESSION['admin'] != True){
	session_unset();
	session_destroy();
	header("Location: http://test.com/admin.html");
}

print_r($_SESSION);

$dbconn = pg_connect("host=localhost dbname=wordpress user=wpuser password=password")or die('Could not connect: ' . pg_last_error());

if(isset($_GET['del'])){
	$delete = "update customers set inactive=true where id=$_GET[del];";
	pg_query($dbconn,$delete) or die('Query failed: ' . pg_last_error());
	header("Location: http://test.com/useracc.php");
}

$query = "select cu.id,cu.email,cu.username,cu.inactive,cu.country_id,c.country from customers cu join countries c on(cu.country_id=c.id);";

$result = pg_query($dbconn,$query) or die('Query failed: ' . pg_last_error());
$col_name = pg_fetch_assoc($result);
?>

<!DOCTYPE html>

<html lang="bg">
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" type="text/css" href="http://test.com/search.css">
	</head>
	<body>
		<ul>
		  <li><a
		   href="http://test.com/useracc.php">User Accounts</a></li>
		  <li>
		  	<a href="http://test.com/php/check.php?goto=account.php">Password Configuration</a>
		  </li>
		  <li><a href="#contact">User Timeout</a></li>
		  <li><a href="#about">To Be Continued...</a></li>
		</ul>
		
		<div class="user_accounts">
<?php
		echo "<table>
		<tr>";

		for($i = 0; $i < count(array_keys($col_name));$i++){
			$key = array_keys($col_name)[$i];
			echo "<th>$key</th>";
		}
		echo "<th>Action</th>";			 	
		echo "</tr>";
		
		echo"<tr>";
		if($col_name['inactive'] == 'f'){
			foreach ($col_name as $key => $value) {
					echo "<td>$value</td>";
			}
			echo"<td>
					<a href=\"useracc.php?del=$col_name[id]\" class=\"del_btn\">Delete</a>
					<a href=\"edituser.php?edit=$col_name[id]\" class=\"edit_btn\">Edit</a>
				</td>";
			echo "</tr>";
		}

		while($row = pg_fetch_assoc($result)){
			
			echo "<tr>";
			foreach ($row as $key => $value) {
				if($row['inactive'] == 'f'){
					echo "<td>$value</td>";
					if($key == 'country'){
					echo"<td>
							<a href=\"useracc.php?del=$row[id]\" class=\"del_btn\">Delete</a>
							<a href=\"edituser.php?edit=$row[id]\"; class=\"edit_btn\" >Edit</a>
				
						</td>";
					}
				}
			}

			echo "</tr>";
		}
		echo"</table>";
		pg_close($dbconn);
?>
		</div>	


	</body>
</html>	