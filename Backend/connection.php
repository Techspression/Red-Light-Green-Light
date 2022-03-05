<?php
    $host = "localhost";
	$user="root";
	$password="";
	$dbName="mydatabase";
	
	$conn =mysqli_connect($host,$user,$password,$dbName);
	
	$username =$_POST["username"];
	$class = $_POST["class_name"];
	$roll = $_POST["roll_no"];
	if ($conn){
	echo "connected";
	}
	else {
	 die("Eror : " .mysqli_connect_error());
	}

	$sql="INSERT INTO `player_info`(`username`, `Class_name`, `roll_no`) VALUES ('$username','$class',$roll)";
	
	$result=mysqli_query($conn,$sql);
	if($result){
	echo "inserted";}
	else {
	echo "not inserted";}
?>