// Node.js/Express contact form handler
// To use: npm install express cors body-parser nodemailer dotenv

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const nodemailer = require('nodemailer');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
    origin: 'https://phoenixtbird.com',
    methods: ['POST']
}));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Security headers
app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    res.setHeader('X-Frame-Options', 'DENY');
    next();
});

// Configure email transporter (using Gmail as example)
// Create a .env file with:
// EMAIL_USER=your-email@gmail.com
// EMAIL_PASS=your-app-password
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASS
    }
});

// Rate limiting (simple in-memory implementation)
const rateLimit = new Map();
const RATE_LIMIT_WINDOW = 60 * 60 * 1000; // 1 hour
const MAX_REQUESTS = 5;

function checkRateLimit(ip) {
    const now = Date.now();
    const userRequests = rateLimit.get(ip) || [];
    const recentRequests = userRequests.filter(time => now - time < RATE_LIMIT_WINDOW);

    if (recentRequests.length >= MAX_REQUESTS) {
        return false;
    }

    recentRequests.push(now);
    rateLimit.set(ip, recentRequests);
    return true;
}

// Contact form endpoint
app.post('/api/contact', async (req, res) => {
    const ip = req.ip || req.connection.remoteAddress;

    // Rate limiting
    if (!checkRateLimit(ip)) {
        return res.status(429).json({
            success: false,
            message: 'Too many requests. Please try again later.'
        });
    }

    const { email, message, website } = req.body;

    // Honeypot check
    if (website) {
        // Bot detected, fail silently
        return res.status(200).json({
            success: true,
            message: 'Message sent successfully'
        });
    }

    // Validation
    const errors = [];

    if (!email || !isValidEmail(email)) {
        errors.push('Valid email address is required');
    }

    if (!message || message.trim().length === 0) {
        errors.push('Message is required');
    }

    // Word count validation
    const wordCount = message.trim().split(/\s+/).length;
    if (wordCount > 200) {
        errors.push('Message must be 200 words or less');
    }

    if (errors.length > 0) {
        return res.status(400).json({
            success: false,
            errors
        });
    }

    // Sanitize input
    const sanitizedEmail = email.trim();
    const sanitizedMessage = message.trim();

    // Email options
    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: 'phoenixthomasbird@gmail.com',
        replyTo: sanitizedEmail,
        subject: 'New Contact Form Submission - phoenixtbird.com',
        text: `New contact form submission\n\nFrom: ${sanitizedEmail}\n\nMessage:\n${sanitizedMessage}\n\n---\nSent: ${new Date().toISOString()}\nIP: ${ip}`
    };

    try {
        await transporter.sendMail(mailOptions);
        res.status(200).json({
            success: true,
            message: 'Message sent successfully'
        });
    } catch (error) {
        console.error('Email send error:', error);
        res.status(500).json({
            success: false,
            message: 'Failed to send message. Please try again later.'
        });
    }
});

// Helper function
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Health check endpoint
app.get('/health', (req, res) => {
    res.status(200).json({ status: 'OK' });
});

app.listen(PORT, () => {
    console.log(`Contact form server running on port ${PORT}`);
});

module.exports = app;
