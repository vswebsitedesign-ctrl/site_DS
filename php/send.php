<?php
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /contact/');
    exit;
}

// Honeypot check
if (!empty($_POST['surname_leave_email'])) {
    header('Location: /thank-you/');
    exit;
}

$firstname = trim(strip_tags($_POST['firstname'] ?? ''));
$surname   = trim(strip_tags($_POST['surname'] ?? ''));
$phone     = trim(strip_tags($_POST['phone'] ?? ''));
$email     = trim(strip_tags($_POST['email'] ?? ''));
$postcode  = trim(strip_tags($_POST['postcode'] ?? ''));
$message   = trim(strip_tags($_POST['message'] ?? ''));
$clearance = isset($_POST['clearance']) ? implode(', ', array_map('strip_tags', $_POST['clearance'])) : 'Not specified';

if (empty($firstname) || empty($phone) || empty($postcode)) {
    header('Location: /contact/?error=missing');
    exit;
}

$to      = 'info@dandsclearances.co.uk';
$subject = "New Enquiry from $firstname $surname — $postcode";
$body    = "Name: $firstname $surname\n"
         . "Phone: $phone\n"
         . "Email: $email\n"
         . "Postcode: $postcode\n"
         . "Clearance Type: $clearance\n"
         . "Message: $message\n";

$headers = "From: noreply@dandsclearances.co.uk\r\n"
         . "Reply-To: $email\r\n"
         . "Content-Type: text/plain; charset=UTF-8\r\n";

mail($to, $subject, $body, $headers);

header('Location: /thank-you/');
exit;
