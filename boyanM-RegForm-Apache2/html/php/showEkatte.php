<?php
include "connToEkatte.php";

$param = $_GET['q'];

$array = array();

$query = "select s.id id,s.name sname,a.name aname
			 from settlements as s,townships as t,areas as a
	 			where lower(s.name) like concat(lower('$param'),'%')
	 and s.township_id = t.id and t.area_id=a.id limit 5;";

$result = pg_query($query) or die('Query failed: ' . pg_last_error());

while($row = pg_fetch_assoc($result)){
    $id = $row['id'];
    $username = $row['sname'];
    $name = $row['aname'];

    $array[] = array("id" => $id,
            "sname" => $username,
            "aname" => $name);

}
echo json_encode($array);
?>

