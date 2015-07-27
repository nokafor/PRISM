<?php
// Check for empty fields
if(empty($_POST['name'])  		||
   empty($_POST['email']) 		||
   empty($_POST['organization']) 		||
   empty($_POST['message'])	||
   !filter_var($_POST['email'],FILTER_VALIDATE_EMAIL))
   {
	echo "No arguments Provided!";
	return false;
   }
	
$name = $_POST['name'];
$email_address = $_POST['email'];
$organization = $_POST['organization'];
$message = $_POST['message'];
	
require("/PHPMailer/PHPMailerAutoload.php");
$mail = new PHPMailer();

// set mailer to use SMTP
$mail->IsSMTP();

// As this email.php script lives on the same server as our email server
// we are setting the HOST to localhost
$mail->Host = "localhost";  // specify main and backup server

$mail->SMTPAuth = true;     // turn on SMTP authentication

// When sending email using PHPMailer, you need to send from a valid email address
// In this case, we setup a test email account with the following credentials:
// email: send_from_PHPMailer@bradm.inmotiontesting.com
// pass: password
$mail->Username = "send_from_PHPMailer@bradm.inmotiontesting.com";  // SMTP username
$mail->Password = "password"; // SMTP password

$mail->From = $email;

// below we want to set the email address we will be sending our email to.
$mail->AddAddress("nokafor@princeton.edu", "Sylvia Okafor");

// set word wrap to 50 characters
$mail->WordWrap = 50;
// set email format to HTML
$mail->IsHTML(true);

$mail->Subject = "PRISM Feedback Form Submitted By:  $name";

$email_body = "You have received a new message from your website contact form.\n\n"."Here are the details:\n\nName: $name\n\nEmail: $email_address\n\nOrganization: $organization\n\nMessage:\n$message";

$mail->Body    = $email_body;
$mail->AltBody = $email_body;

if(!$mail->Send())
{
   echo "Message could not be sent. <p>";
   echo "Mailer Error: " . $mail->ErrorInfo;
   exit;
}

echo "Message has been sent";

return true;			
?>