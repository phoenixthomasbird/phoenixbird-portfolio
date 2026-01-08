# Backend Setup Guide

This website includes two backend options for the contact form:

## Option 1: PHP Backend (Recommended for most hosting)

### Setup:
1. The file `contact-handler.php` is already included
2. Upload it to your web server alongside `index.html`
3. Ensure your hosting supports PHP mail() function
4. The form is already configured to use this endpoint

### Testing:
```bash
# Test locally with PHP's built-in server
php -S localhost:8080
```

### Notes:
- Most shared hosting (like cPanel) supports PHP out of the box
- No additional dependencies required
- Includes spam prevention (honeypot) and rate limiting via IP tracking

---

## Option 2: Node.js Backend (For custom servers)

### Prerequisites:
```bash
npm install express cors body-parser nodemailer dotenv
```

### Setup:
1. Create a `.env` file in the root directory:
```
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
PORT=3000
```

2. For Gmail, enable "App Passwords":
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Generate a password for "Mail"

3. Update the form endpoint in `index.html` line 389:
```javascript
const response = await fetch('/api/contact', {
```

4. Start the server:
```bash
node contact-handler.js
```

### Notes:
- Includes rate limiting (5 requests per hour per IP)
- More flexible for customization
- Requires Node.js hosting or VPS

---

## Security Features

Both implementations include:
- ✅ Email validation
- ✅ Input sanitization
- ✅ Word count validation (200 words max)
- ✅ Honeypot spam prevention
- ✅ Security headers (X-Frame-Options, X-Content-Type-Options)
- ✅ CORS configuration
- ✅ XSS protection

---

## Fallback Option

If you prefer not to set up a backend, you can temporarily revert to the mailto: method:

In `index.html`, change line 250 to:
```html
<form class="contact-form" action="mailto:phoenixthomasbird@gmail.com" method="post" enctype="text/plain">
```

And remove or comment out the JavaScript form submission handler (lines 363-418).

**Note:** The mailto: method is not recommended for production as it:
- Opens the user's email client (poor UX)
- Doesn't work on mobile devices reliably
- Has no validation or spam prevention
- Doesn't provide feedback to the user

---

## Troubleshooting

### PHP Issues:
- Check if `mail()` function is enabled: `php -i | grep mail`
- Verify email is sent: Check spam folder
- Enable error logging in PHP to debug issues

### Node.js Issues:
- Check `.env` file is configured correctly
- Verify port 3000 is not in use: `lsof -i :3000`
- Check Gmail App Password is correct
- Review console logs for detailed error messages

### Testing:
Submit the form and check:
1. Browser console for any JavaScript errors
2. Network tab for the API request/response
3. Your email inbox (and spam folder)

---

## Production Deployment

### For PHP:
1. Upload all files via FTP or cPanel File Manager
2. Ensure proper file permissions (644 for PHP files)
3. Test the contact form on the live site

### For Node.js:
1. Use PM2 to keep the server running:
```bash
npm install -g pm2
pm2 start contact-handler.js --name contact-form
pm2 save
pm2 startup
```

2. Configure nginx reverse proxy (if needed):
```nginx
location /api {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

---

## Support

If you encounter issues, check:
- Server error logs
- Browser console (F12)
- Network requests in Developer Tools

For questions about implementation, refer to the inline comments in the handler files.
