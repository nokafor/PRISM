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

require 'vendor/autoload.php';
$sendgrid = new SendGrid('princetonism', 'PRISMfounder16');

$email_body = "You have received a new message from your website contact form.\n\n"."Here are the details:\n\nName: $name\n\nEmail: $email_address\n\nOrganization: $organization\n\nMessage:\n$message";

$message = new SendGrid\Email();
$message->addTo('nokafor@princeton.edu')->
          setFrom('nokafor@noreply.com')->
          setSubject("PRISM Feedback Form:  $name")->
          setText($email_body)->
          setHtml('<strong>Hello World!</strong>');
$response = $sendgrid->send($message);

return $response

// Create the email and send the message
// $to = 'nokafor@princeton.edu'; // Add your email address inbetween the '' replacing yourname@yourdomain.com - This is where the form will send a message to.
// $email_subject = "PRISM Feedback Form:  $name";
// $email_body = "You have received a new message from your website contact form.\n\n"."Here are the details:\n\nName: $name\n\nEmail: $email_address\n\nOrganization: $organization\n\nMessage:\n$message";
// $headers = "From: nokafor@princeton.edu\n"; // This is the email address the generated message will be from. We recommend using something like noreply@yourdomain.com.
// $headers .= "Reply-To: $email_address";	
// mail($to,$email_subject,$email_body,$headers);
// return true;			
?>