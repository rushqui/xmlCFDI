<?php

require("phpmailer/PHPMailerAutoload.php");


$mail = new PHPMailer();

// set mailer to use SMTP
$mail->IsSMTP();
 
// As this email.php script lives on the same server as our email server
// we are setting the HOST to localhost
$mail->Host = "vm6.digitalserver.org";  // specify main and backup server
 
$mail->SMTPAuth = true;     // turn on SMTP authentication
// When sending email using PHPMailer, you need to send from a valid email address
// In this case, we setup a test email account with the following credentials:
// email: send_from_PHPMailer@bradm.inmotiontesting.com
// pass: password
$mail->Username = "ivancrupiicsa@hotmail.com";  // SMTP username
$mail->Password = "CARA900719HDFLML"; // SMTP password
// set email format to HTML

if( $_SERVER['REQUEST_METHOD'] == 'POST' ) {
    if( $_POST['frm-name'] != '' AND $_POST['frm-email'] != '' AND $_POST['frm-message'] != '' ) {

        $name = $_POST['frm-name'];
        $email = $_POST['frm-email'];
        $phone = $_POST['frm-phone'];
        $message = $_POST['frm-message'];

        $subject = 'Nuevo mensaje en ecdiciem.com';

        $botcheck = $_POST['frm-botcheck'];

		$toemail = 'ivancrupiicsa@hotmail.com'; // Your Email Address
        $toname = 'Avisos Jonathan'; // Your Name

        if( $botcheck == '' ) {

            $mail->SetFrom( $email , $name ); 
            $mail->AddAddress( $toemail , $toname );
            $mail->AddCC( $email , $name );
            $mail->AddBCC( "avisos.ivancrupiicsa@hotmail.com" , $name );
            $mail->Subject = "Mensaje nuevo en manumaps.com";

            $name = isset($name) ? "Nombre: $name<br><br>" : '';
            $email = isset($email) ? "Email: $email<br><br>" : '';
            $phone = isset($phone) ? "Teléfono: $phone<br><br>" : ''; 
            $message = isset($message) ? "Mensaje: <br>$message<br><br>" : '';

            $referrer = $_SERVER['HTTP_REFERER'] ? '<br><br><br>Este correo fue enviado por: ' . $_SERVER['HTTP_REFERER'] : '';

            $body = "$name $email $phone $message $referrer";

            $mail->MsgHTML( $body );
			
			$mail->IsHTML(true);
			$mail->CharSet = 'UTF-8';
            $sendEmail = $mail->Send();

            if( $sendEmail == true ):
                echo '<strong>Gracias por contactarnos! </strong> tu mensaje ha sido recibido y a la brevedad nos pondremos en contacto contigo.';
            else:
                echo 'El correo <strong>no </strong> se envió debido a un error inesperado. Por favor intente más tarde.<br /><br /><strong>Razón:</strong><br />' . $mail->ErrorInfo . '';
            endif;
        } else {
            echo 'Bot <strong>Detected</strong>.!';
        }
    } else {
        echo 'Por favor <strong>llene</strong> todos los campos e intente de nuevo.';
    }
} else {
    echo ' <strong>Ocurrió un error</strong>. Disculpe las molestias, intente más tarde.';
}


 
?>