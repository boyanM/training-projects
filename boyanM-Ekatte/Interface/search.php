<?php

$db = pg_connect("host=127.0.0.1 port=5432 dbname=ekatte user=ekatte_user password=Parola42");
$result = pg_query($db, "select s.ekatte_id as ekatte_id, s.name as name,t.township_id as township, a.area_id as area from settlements as s,townships as t,areas as a where s.name='$_POST[settlement]' and t.township_id=s.township_id and t.area_id = a.area_id;");

	echo $test;
echo "<link rel='stylesheet' type='text/css' href='search.css'>";

$check = pg_fetch_assoc($result);

if(empty($check))
{
 echo "No information in database for this settlement";
}
else
{
echo "<table>
  <tr>
    <th>Ekatte</th>
    <th>Name</th>
    <th>Township</th>
    <th>Area</th>
  </tr>";

echo "
	<tr>
		<td>$check[ekatte_id]</td>
		<td>$check[name]</td>
		<td>$check[township]</td>
		<td>$check[area]</td>

	</tr>";

while ($row = pg_fetch_assoc($result))
{
echo"
	<tr>
		<td>$row[ekatte_id]</td>
		<td>$row[name]</td>
		<td>$row[township]</td>
		<td>$row[area]</td>

	</tr>";
}
echo "</table>";



}



?>
