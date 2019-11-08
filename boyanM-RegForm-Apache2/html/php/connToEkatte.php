<?php
    $dbconn = pg_connect("host=localhost dbname=ekatte user=ekatte_read password=1111")or die('Could not connect: ' . pg_last_error());

?>