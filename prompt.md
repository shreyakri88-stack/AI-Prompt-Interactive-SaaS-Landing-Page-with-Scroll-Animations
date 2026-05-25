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

- Fully responsive
- Optimized for:
  - Mobile
  - Tablet
  - Desktop
- Accessible using:
  - Semantic HTML
  - ARIA labels
  - Keyboard navigation support
- Performance optimized

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

- XSS attacks
- Injection attacks
- Spam submissions

Implement:

- Input sanitization
- Rate limiting or CAPTCHA
- Proper validation

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

- React or Next.js
- Framer Motion
- Tailwind CSS

## Backend

- Node.js + Express OR Next.js API Routes
- Nodemailer
- dotenv

## Optional Database

- MongoDB
- PostgreSQL

---

# Performance Requirements

Optimize the application for:

- Fast loading
- Smooth animations
- Bundle size reduction
- Lazy loading
- SEO optimization
- Accessibility compliance

---

# Expected Output

The final project should include:

- Smooth animated storytelling experience
- Responsive portfolio UI
- Functional animated contact modal
- Secure backend integration
- Email notification system
- Graceful error handling
- Deployment-ready architecture
- Documentation for setup and environment variables
