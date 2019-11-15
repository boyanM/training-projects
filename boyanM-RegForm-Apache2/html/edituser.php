<?php
	session_start();

	if(!isset($_SESSION['login']) && !isset($_SESSION['admin'])
	 && $_SESSION['admin'] != True && !isset($_GET['edit'])){
		session_unset();
		session_destroy();
		header("Location: http://test.com/admin.html");
	}

	print_r($_SESSION);

	$dbconn = pg_connect("host=localhost dbname=wordpress user=wpuser password=password")or die('Could not connect: ' . pg_last_error());

	$query = "select cu.*,c.country from customers cu join countries c on(cu.country_id=c.id and cu.id='$_GET[edit]');";

	$result = pg_query($dbconn,$query) or die('Query failed: ' . pg_last_error());
?>

<!DOCTYPE html>
<html lang="bg">

<head>
<meta charset=utf-8>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="http://test.com/search.css">
</head>
<body>
<?php
	echo "<br><br>
	<form name=\"reg_form\" method=\"POST\" action=\"http://test.com/edituser.php\">";
	while($row = pg_fetch_assoc($result)){
		foreach ($row as $key => $value) {
			echo "<label for=\"$key\"><b>$key</b></label>
			<input type=\"text\" name=\"$key\" value=\"$value\">
			<br>";
		}
	}
    echo "<br> <button type=\"submit\" class=\"del_btn\">Save</button>";
	echo "</form>";
?>
</body>
</html>