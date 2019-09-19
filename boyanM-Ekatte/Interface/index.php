
<!DOCTYPE html>
<html lang="bg">
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="UTF-8">  
</head>
<body>

<link rel="stylesheet" type="text/css" href="search.css">

<h2>Search for a settlement</h2>

<form name="serach"  method="POST" accept-charset="utf-8" >
<input name="settlement" type="text" id="myInput" placeholder="Search for names.." title="Type in a name"/>
</form>

<?php


$db = pg_connect("host=127.0.0.1 port=5432 dbname=ekatte user=ekatte_user password=Parola42");

$countRows = pg_query($db, "select (select count(*) from settlements) as rows_settlement,(select count(*) from townships) as rows_townhips,(select count(*) from areas) as rows_areas;");

echo "<table>
  <tr>
    <th>Rows of Settlements Table</th>
    <th>Rows of Townships Table</th>
    <th>Rows of Area Table</th>
  </tr>";
$numberOfRows = pg_fetch_assoc($countRows);

echo "
	<tr>
		<td>$numberOfRows[rows_settlement]</td>
		<td>$numberOfRows[rows_townhips]</td>
		<td>$numberOfRows[rows_areas]</td>
		

	</tr>";
echo "</table><br><br>";

$string = $_POST['settlement'];

$result = pg_query($db, "select s.t_v_m as t_v_m, s.name as name,t.name as township, a.name as area
 from settlements as s,townships as t,areas as a 
	where LOWER(s.name) = LOWER('$string')
		and t.township_id=s.township_id 
		and t.area_id = a.area_id;");

	echo $test;

$check = pg_fetch_assoc($result);

if(empty($check))
{

}
else
{
$counter = 1;	
echo "<table>
  <tr>
    <th>Type</th>
    <th>Name</th>
    <th>Township</th>
    <th>Area</th>
  </tr>";

echo "
	<tr>
		<td>$check[t_v_m]</td>
		<td>$check[name]</td>
		<td>$check[township]</td>
		<td>$check[area]</td>

	</tr>";

while ($row = pg_fetch_assoc($result))
{
	$counter += 1;
echo"
	<tr>
		<td>$row[t_v_m]</td>
		<td>$row[name]</td>
		<td>$row[township]</td>
		<td>$row[area]</td>

	</tr>";
}
echo "</table><br>";
echo "There is(are) $counter row(s) with that name";

}
?>



</body>
</html>