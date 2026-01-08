<?php
// Contact form handler with security measures
header('Content-Type: application/json');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit;
}

// CORS settings (adjust domain as needed)
$allowed_origin = 'https://phoenixtbird.com';
if (isset($_SERVER['HTTP_ORIGIN']) && $_SERVER['HTTP_ORIGIN'] === $allowed_origin) {
    header("Access-Control-Allow-Origin: $allowed_origin");
}

// Get POST data
$email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
$message = htmlspecialchars(trim($_POST['message'] ?? ''), ENT_QUOTES, 'UTF-8');

// Honeypot field (add this hidden field to your form)
$honeypot = $_POST['website'] ?? '';

// Validation
$errors = [];

if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Valid email address is required';
}

if (empty($message)) {
    $errors[] = 'Message is required';
}

// Word count validation
$wordCount = str_word_count($message);
if ($wordCount > 200) {
    $errors[] = 'Message must be 200 words or less';
}

// Honeypot check
if (!empty($honeypot)) {
    // Likely a bot, fail silently
    http_response_code(200);
    echo json_encode(['success' => true, 'message' => 'Message sent successfully']);
    exit;
}

// If validation fails
if (!empty($errors)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'errors' => $errors]);
    exit;
}

// Email configuration
$to = 'phoenixthomasbird@gmail.com';
$subject = 'New Contact Form Submission - phoenixtbird.com';
$headers = [
    'From: noreply@phoenixtbird.com',
    'Reply-To: ' . $email,
    'X-Mailer: PHP/' . phpversion(),
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8'
];

$emailBody = "New contact form submission\n\n";
$emailBody .= "From: $email\n\n";
$emailBody .= "Message:\n$message\n\n";
$emailBody .= "---\n";
$emailBody .= "Sent: " . date('Y-m-d H:i:s') . "\n";
$emailBody .= "IP: " . ($_SERVER['REMOTE_ADDR'] ?? 'Unknown') . "\n";

// Send email
$success = mail($to, $subject, $emailBody, implode("\r\n", $headers));

if ($success) {
    http_response_code(200);
    echo json_encode(['success' => true, 'message' => 'Message sent successfully']);
} else {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Failed to send message. Please try again later.']);
}
?>
