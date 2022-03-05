<!DOCTYPE HTML>
<html>
<head>
  <title>Register Form</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
	body {
	background-image: url('sanket.jpg');
	}
	form {  
    display: flex;
    height: 100vh;
    justify-content: center;
    align-items: center;
  }
  div {
    width: 30%;
    padding: 5%; 
    border-spacing: 15px;
  }
	.contain {
   height: 50%;
   width:  50%;
   border-radius: 1px;
   /* background-color: yellow; */
   display: inline-block;
   background-color: #03d7fc;
   border: 3px solid black;
   
   font-size: 36px;
  }
  
  .contain input{
    padding: 15px;
    width: 30vh;
    border-radius: 50px;
  }
  .contain table td{
    color: red;
    font-style: italic;
    
  }
  .contain table  {
    padding-left: 100px;
  }
  .submitBtn input  {
    display: block;
    margin:  9 auto;
  }
  .submitBtn {
    
    display: flex;
    justify-content: center;
    width: 100%;
  }
  
  
  </style>
</head>
<body>
	
 <form   action="connection.php" method="POST">
 <div class="contain" >
  
  <table >
   <tr>
    <td><b>Full Name</b> :</td>
    <td><input type="text" name="username" required></td>
   </tr>
   <tr>
    <td><b>Class Name</b> : </td>
    <td><input type="text" name="class_name" required></td>
   </tr>
	 <tr>
    <td><b>Roll No:</b></td>
    <td><input type="int" name="roll_no" required></td>
   </tr>
   
   <tr>
    <td  colspan="2">
    <div class="submitBtn">

      <input type="submit" value="Submit" name="submit" >
    </div>  
    </td>
   </tr>
   
  </table>

  </div>
 </form>
</body>
</html>