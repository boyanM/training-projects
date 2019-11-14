<?php
session_start();

if(!isset($_SESSION['login']) && !isset($_SESSION['admin']) && $_SESSION['admin'] != True){
	session_unset();
	session_destroy();
	header("Location: http://test.com/admin.html");
}

print_r($_SESSION);

$dbconn = pg_connect("host=localhost dbname=wordpress user=wp_read password=1111")or die('Could not connect: ' . pg_last_error());

$query = "select cu.*,c.country from customers cu join countries c on(cu.country_id=c.id);";

$result = pg_query($query) or die('Query failed: ' . pg_last_error());
$result = pg_fetch_assoc($result);
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
		  <li><a class="active"
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

				for($i = 0; $i < count(array_keys($result));$i++){
						$key = array_keys($result)[$i];
						echo "<th>$key</th>";
				}
						 	
			echo "</tr>";

			foreach ($result as $key => $value) {
				echo $value;
			}
			print_r($result);
			echo"
			</table>";
			?>
		</div>	


	</body>
</html>	