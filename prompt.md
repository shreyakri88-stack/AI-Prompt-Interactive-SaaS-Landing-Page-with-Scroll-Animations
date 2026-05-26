# Full-Stack Animated Portfolio Website

## Context and Role

As a Frontend Developer focused on building cutting-edge web applications, your task is to develop a performance-efficient personal website portfolio. The website should utilize **Framer Motion** to create captivating, responsive animations with story-like content driven by scrolling interactions.

The portfolio should present projects, skills, and experience in a narrative-based format that keeps users engaged throughout the browsing experience.

Additionally, the portfolio must include a fully functional contact system capable of collecting user information and sending an email notification to the website owner.

---

# Objective

Develop a complete full-stack portfolio website that:

- Implements scroll-based storytelling animations using Framer Motion
- Provides a modern, responsive UI with smooth transitions
- Includes a “Get in Touch” button that opens a contact form modal
- Logs user submissions securely
- Triggers an email notification to the portfolio owner with submitted details

---

# UI and Animation Requirements

## Scroll-Based Storytelling

Implement scroll-triggered animations using Framer Motion.

### Required Animation Features

- Parallax scrolling effects
- Fade-in animations
- Staggered transitions
- Sequential section animations
- Smooth storytelling flow between sections

### Portfolio Sections

The storytelling experience should smoothly transition between:

- Hero Section
- About Section
- Skills Section
- Projects Section
- Contact Section

### Performance Requirements

Ensure animations:

- Avoid layout thrashing
- Use GPU-friendly properties such as:
  - `transform`
  - `opacity`
- Do not negatively impact scroll performance

---

# Layout Requirements

The portfolio must include:

## Hero Section

- Animated introduction
- Engaging headline animations
- Smooth call-to-action interactions

## About Section

- Animated text reveal
- Scroll-based storytelling transitions

## Skills Section

- Animated progress indicators
- Motion-enhanced skill cards

## Projects Section

- Hover interactions
- Framer Motion transitions
- Interactive project showcase

## Call-to-Action Section

- “Get in Touch” button
- Animated hover and click effects

---

# Responsive Design Requirements

The website must be:

- Fully responsive- Layout adapts automatically to all screen sizes.
- Optimized for:
  - Mobile- UI should function properly on smartphones.
  - Tablet- Content spacing and scaling should suit tablets.
  - Desktop - Large-screen layouts should remain visually balanced.
- Accessible using:
  - Semantic HTML - Proper HTML structure improves accessibility and SEO.
  - Keyboard navigation support - Users should navigate without a mouse.
- Performance optimized - Site should remain lightweight and fast.

---

# Contact System Requirements

## Modal Behavior

Clicking the “Get in Touch” button must:

- Open a modal contact form
- Animate modal entry and exit using Framer Motion
- Prevent background scrolling
- Maintain accessibility standards

---

# Contact Form Fields

The modal form must contain:

| Field         | Requirement |
|----------------|-------------|
| Name           | Required |
| Email          | Required + Validated |
| Phone Number   | Required + Validated |
| Message        | Optional |

---

# Validation Requirements

Implement client-side validation with:

- Proper error messages
- Email format validation
- Phone number validation
- Prevention of invalid submissions
- Accessible validation feedback

---

# Backend Requirements

Create a backend API that:

- Handles form submissions securely
- Logs submissions safely
- Sends email notifications to the portfolio owner
- Returns structured JSON responses

---

# Email Notification Requirements

The email notification must include:

- Name
- Email
- Phone Number
- Message
- Submission Timestamp

Use:

- Nodemailer
- SMTP or transactional email service
- Environment variables for credential security

---

# Security Requirements

Sanitize all user inputs to prevent:

- XSS attacks-Removes malicious code from user inputs.
- Injection attacks - Prevents malicious database or server commands.
- Spam submissions - Reduces fake or automated submissions.
Implement:

- Input sanitization - Removes malicious code from user inputs.
- Rate limiting or CAPTCHA - Restricts repeated requests from users.
- Proper validation - Ensures all incoming data is safe and correctly formatted.

---

# API Response Format

## Success Response

```json
{
  "success": true,
  "message": "Message sent successfully"
}
```

## Error Response

```json
{
  "success": false,
  "error": "Validation failed"
}
```

---

# Technology Stack

## Frontend

- React or Next.js-JavaScript library for building UI components.
- Framer Motion-Animation library for React applications.
- Tailwind CSS-Utility-first CSS framework for fast UI development.

## Backend

- Node.js + Express OR Next.js API Routes
- Nodemailer-Library for sending emails from Node.js applications.
- dotenv-Loads environment variables securely from .env files.

## Optional Database

- MongoDB- NoSQL database for flexible document storage.
- PostgreSQL- Relational SQL database for structured data storage.

---

# Performance Requirements

Optimize the application for:

- Fast loading- Website should render quickly.
- Smooth animations- Motion effects should not lag or stutter.
- Bundle size reduction- Minimize unnecessary JavaScript and assets.
- Lazy loading- Load components or images only when needed.
- SEO optimization- Improve visibility on search engines.
- Accessibility compliance- Ensure usability for all users including disabled users.

---

# Expected Output

The final project should include:

- Smooth animated storytelling experience-Website should feel immersive and cinematic.
- Responsive portfolio UI-Interface should adapt cleanly to all devices.
- Functional animated contact modal-Popup form must work completely.
- Secure backend integration-APIs should safely process user data.
- Email notification system-Owner receives submission alerts automatically.
- Graceful error handling-Errors should be managed without breaking UX.
- Deployment-ready architecture-Project should be structured for real hosting environments.
- Documentation for setup and environment variables-Setup instructions should explain secure credential configuration.
