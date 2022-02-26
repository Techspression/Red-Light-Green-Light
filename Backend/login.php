<! DOCTYPE html>
	<html lang="en">

	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>Login Page </title>
		<link rel="stylesheet" href="style_2.css">
		<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
		<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
		<style>
			* {
				margin: 0;
				padding: 0;
				box-sizing: border-box;
			}

			.btn {
				display: inline-block;
				background: #FF4300;
				color: #fff;
				padding: 8px 30px;
				margin: 30px 0;
				border-radius: 30px;
				transition: background 0.5s;
			}

			.btn:hover {
				background: #563434;
			}

			/*-------- footer ---------*/

			.footer {
				background: #000;
				color: #8a8a8a;
				font-size: 14px;
				padding: 60px 0 20px;
			}

			.footer p {
				color: #8a8a8a;
			}

			.footer h3 {
				color: #fff;
				margin-bottom: 20px;
			}

			.footer-col-1,
			.footer-col-2,
			.footer-col-3,
			.footer-col-4 {
				min-width: 250px;
				margin-bottom: 20px;
			}

			.footer-col-1 {
				flex-basis: 30%;
			}

			.footer-col-2 {
				flex: 1;
				text-align: center;
			}

			.footer-col-2 img {
				width: 180px;
				margin-bottom: 20px;
			}

			.footer-col-3,
			.footer-col-4 {
				flex-basis: 12%;
				text-align: center;
			}

			ul {
				list-style-type: none;
			}

			.app-logo {
				margin-top: 20px;
			}

			.app-logo img {
				width: 140px;
			}

			.footer hr {
				border: none;
				background: #b5b5b5;
				height: 1px;
				margin: 20px 0;
			}

			.copyright {
				text-align: center;
			}

			.menu-icon {
				width: 28px;
				margin-left: 20px;
				display: none;
			}

			/*------ media query for menu -- */

			@media only screen and (max-width: 800px) {

				nav ul {
					position: absolute;
					top: 70px;
					left: 0;
					background: #333;
					width: 100%;
					overflow: hidden;
					transition: max-height 0.5s;
				}

				nav ul li {
					display: block;
					margin-right: 50px;
					margin-top: 10px;
					margin-bottom: 10px;
				}

				nav ul li a {
					color: #fff;
				}

				.menu-icon {
					display: block;
					cursor: pointer;
				}
			}




			/*------ account-page--*/

			.account-page {
				padding: 50px 0;
				background: radial-gradient(#fff, #00FFF3);
			}

			.form-container {
				background: #fff;
				width: 300px;
				height: 400px;
				position: relative;
				text-align: center;
				padding: 20px 0;
				margin: auto;
				box-shadow: 0 0 20px 0px rgba(0, 0, 0, 0.1);
				overflow: hidden;
			}

			.form-container span {
				font-weight: bold;
				padding: 0 10px;
				color: #555;
				cursor: pointer;
				width: 100px;
				display: inline-block;
			}

			.form-btn {
				display: inline-block;
			}

			.form-container form {
				max-width: 300px;
				padding: 0 20px;
				position: absolute;
				top: 130px;
				transition: transform 1s;
			}

			form input {
				width: 100%;
				height: 30px;
				margin: 10px 0;
				padding: 0 10px;
				border: 1px solid #ccc;
			}

			form .btn {
				width: 100%;
				border: none;
				cursor: pointer;
				margin: 10px 0;
			}

			form .btn:focus {
				outline: none;
			}

			#LoginForm {
				left: -300px;
			}

			.form {
				position: absolute;
				top:-25px
			}

			#hide1 {
				display: none;
			}
            #reg_hide1{
				display: none;
			}
			#RegForm {
				left: 0;
				top: 106px;
			}

			form a {
				font-size: 12px;
			}

			#Indicator {
				width: 100px;
				border: none;
				background: #ff523b;
				height: 3px;
				margin-top: 8px;
				transform: translateX(100px);
				transition: transform;}
				/*--media query for less than 600 screen size--*/


				@media only screen and (max-width: 600px) {
					.row {
						text-align: center;
					}

					.col-2,
					.col-3,
					.col-4 {
						flex-basis: 100%;
					}

					.single-product .row {
						text-align: left;
					}

					.single-product .col-2 {
						padding: 20px 0;
					}

					.single-product h1 {
						font-size: 26px;
						line-height: 32px;
					}

					.cart-info p {
						display: none;
					}
				}

				@media screen and (max-width: 650px) {
					.column {
						width: 100%;
						display: block;
					}
				}
		</style>
	</head>

	<body>

		<!----- account-page----->
		<div class="account-page">
			<div class="container">
				<div class="row">


					<div class="col-2">
						<div class="form-container">
							<div class="form-btn">
								<span onclick="login()">Login</span>
								<span onclick="register()">Register</span>
								<hr id="Indicator">
								</hr>
							</div>
							<div class="form">
								<form id="LoginForm" action = "authentication.php" onsubmit = "return validation()" method = "POST">
									<div>
										<input type="text" placeholder="Username" name="user" id="user">
									</div>
									<div style="display: flex;">
										<input type="password" placeholder="Password" id="myLogInput" name="pass">
										<span class="eye" onclick="myLogFunction()" style="height: 30px; margin: 10px 0px; padding: 5px; border: 1px solid #ccc; ">
											<i id="hide1" class="fa fa-eye"></i>
											<i id="hide2" class="fa fa-eye-slash"></i>
										</span>
									</div>
									<button type="submit" class="btn" id="btn" value="Login">Login</button>
									<a href="">Forgot password</a>
								</form>
							</div>
							<form id="RegForm" >
								<input type="text" placeholder="Username">
								<input type="email" placeholder="Email">
								<div style="display: flex;">
										<input type="password" placeholder="Password" id="myRegInput">
										<span class="eye" onclick="myRegFunction()" style="height: 30px; margin: 10px 0px; padding: 5px; border: 1px solid #ccc; ">
											<i id="reg_hide1" class="fa fa-eye"></i>
											<i id="reg_hide2" class="fa fa-eye-slash"></i>
										</span>
									</div>
								<button type="submit" class="btn">Register</button>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
		<!---------- footer ------->
		<div class="footer">
			<div class="container">
				<div class="row">
					<div class="footer-col-1">
						<h3>Download Our App</h3>
						<p>Download App for android and ios mobile phone.</p>



						<div class="footer-col-4">
							<h3>Follow us</h3>
							<ul>
								<li>Facebook</li>
								<li>Twitter</li>
								<li>Instagram</li>
								<li>YouTube</li>
							</ul>
						</div>
					</div>
					<hr>
					<p class="copyright">Copyright 2021 _.itz_sanket.003_</p>
				</div>
			</div>
			<!------- js for toggle menu -------->
			<script>
				var MenuItems = document.getElementById("MenuItems");

				MenuItems.style.maxHeight = "0px";

				function menutoggle() {
					if (MenuItems.style.maxHeight == "0px") {
						MenuItems.style.maxHeight = "200px";
					} else {
						MenuItems.style.maxHeight = "0px";
					}
				}
			</script>
			<!----------- js for toggle ---------->
			<script>
				var LoginForm = document.getElementById("LoginForm");
				var RegForm = document.getElementById("RegForm");
				var Indicator = document.getElementById("Indicator");

				function register() {
					RegForm.style.transform = "translateX(0px)";
					LoginForm.style.transform = "translateX(0px)";
					Indicator.style.transform = "translateX(100px)";
				}

				function login() {
					RegForm.style.transform = "translateX(300px)";
					LoginForm.style.transform = "translateX(300px)";
					Indicator.style.transform = "translateX(0px)";
				}
			</script>
			<script>
				function myLogFunction() {
					var x = document.getElementById("myLogInput");
					var y = document.getElementById("hide1");
					var z = document.getElementById("hide2");

					if (x.type === 'password') {
						x.type = "text";
						y.style.display = "block";
						z.style.display = "none";
					} else {
						x.type = "password";
						y.style.display = "none";
						z.style.display = "block";
					}
				}
				function myRegFunction() {
					var x = document.getElementById("myRegInput");
					var y = document.getElementById("reg_hide1");
					var z = document.getElementById("reg_hide2");

					if (x.type === 'password') {
						x.type = "text";
						y.style.display = "block";
						z.style.display = "none";
					} else {
						x.type = "password";
						y.style.display = "none";
						z.style.display = "block";
					}
				}
				function validation()  
            {  
                var id=document.f1.user.value;  
                var ps=document.f1.pass.value;  
                if(id.length=="" && ps.length=="") {  
                    alert("User Name and Password fields are empty");  
                    return false;  
                }  
                else  
                {  
                    if(id.length=="") {  
                        alert("User Name is empty");  
                        return false;  
                    }   
                    if (ps.length=="") {  
                    alert("Password field is empty");  
                    return false;  
                    }  
                }                             
            }  
			</script>
	</body>

	</html>