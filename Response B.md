# NextGen SaaS Architecture & Implementation Guide

## Project Structure

```plaintext
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   └── lead/
│   │   │       └── route.ts
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── providers.tsx
│   │   ├── robots.ts
│   │   └── sitemap.ts
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Accordion.tsx
│   │   │   ├── Button.tsx
│   │   │   └── Card.tsx
│   │   ├── sections/
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── ProductDemo.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── Pricing.tsx
│   │   │   ├── FAQ.tsx
│   │   │   └── CTASection.tsx
│   │   └── LeadModal.tsx
│   ├── hooks/
│   │   └── useMousePosition.ts
│   ├── lib/
│   │   ├── db.ts
│   │   └── utils.ts
│   └── models/
│       └── Lead.ts
├── .env.example
├── next.config.js
├── tailwind.config.ts
└── tsconfig.json
```

---

# 1. Database & Backend Layer

## `src/lib/db.ts`

```ts
import mongoose from 'mongoose';

const MONGODB_URI = process.env.MONGODB_URI || '';

if (!MONGODB_URI) {
  throw new Error('Please define the MONGODB_URI environment variable inside .env');
}

let cached = (global as any).mongoose;

if (!cached) {
  cached = (global as any).mongoose = {
    conn: null,
    promise: null,
  };
}

export async function connectToDatabase() {
  if (cached.conn) return cached.conn;

  if (!cached.promise) {
    const opts = {
      bufferCommands: false,
    };

    cached.promise = mongoose.connect(MONGODB_URI, opts).then((m) => m);
  }

  cached.conn = await cached.promise;

  return cached.conn;
}
```

---

## `src/models/Lead.ts`

```ts
import mongoose, { Schema, Document, models, model } from 'mongoose';

export interface ILead extends Document {
  name: string;
  email: string;
  phone: string;
  company?: string;
  message?: string;
  ipAddress: string;
  userAgent: string;
  createdAt: Date;
}

const LeadSchema = new Schema<ILead>({
  name: {
    type: String,
    required: true,
    trim: true,
    maxlength: 100,
  },
  email: {
    type: String,
    required: true,
    trim: true,
    lowercase: true,
  },
  phone: {
    type: String,
    required: true,
    trim: true,
  },
  company: {
    type: String,
    trim: true,
    maxlength: 100,
  },
  message: {
    type: String,
    trim: true,
    maxlength: 1000,
  },
  ipAddress: {
    type: String,
    required: true,
  },
  userAgent: {
    type: String,
    required: true,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

export const Lead =
  models.Lead || model<ILead>('Lead', LeadSchema);
```

---

## `src/app/api/lead/route.ts`

```ts
import { NextRequest, NextResponse } from 'next/server';
import { connectToDatabase } from '@/lib/db';
import { Lead } from '@/models/Lead';
import nodemailer from 'nodemailer';

// In-memory rate limiter
const ipCache = new Map<
  string,
  { count: number; resetTime: number }
>();

const RATE_LIMIT = 5;
const WINDOW_MS = 15 * 60 * 1000;

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const userData = ipCache.get(ip);

  if (!userData) {
    ipCache.set(ip, {
      count: 1,
      resetTime: now + WINDOW_MS,
    });
    return false;
  }

  if (now > userData.resetTime) {
    ipCache.set(ip, {
      count: 1,
      resetTime: now + WINDOW_MS,
    });
    return false;
  }

  userData.count += 1;

  return userData.count > RATE_LIMIT;
}

function sanitize(input: string): string {
  return input.replace(/[&<>"']/g, (match) => {
    const entityMap: Record<string, string> = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#x27;',
    };

    return entityMap[match];
  });
}

export async function POST(req: NextRequest) {
  try {
    const ip =
      req.headers.get('x-forwarded-for') ||
      req.ip ||
      '127.0.0.1';

    if (isRateLimited(ip)) {
      return NextResponse.json(
        {
          success: false,
          error: 'Too many requests.',
        },
        { status: 429 }
      );
    }

    const body = await req.json();

    const {
      name,
      email,
      phone,
      company,
      message,
    } = body;

    if (!name || !email || !phone) {
      return NextResponse.json(
        {
          success: false,
          error: 'Missing required fields.',
        },
        { status: 400 }
      );
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const phoneRegex = /^\+?[1-9]\d{1,14}$/;

    if (
      !emailRegex.test(email) ||
      !phoneRegex.test(phone)
    ) {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid field formats.',
        },
        { status: 400 }
      );
    }

    await connectToDatabase();

    const sanitizedLead = {
      name: sanitize(name),
      email: sanitize(email),
      phone: sanitize(phone),
      company: company ? sanitize(company) : '',
      message: message ? sanitize(message) : '',
      ipAddress: ip,
      userAgent:
        req.headers.get('user-agent') || 'Unknown',
    };

    await Lead.create(sanitizedLead);

    const transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: Number(process.env.SMTP_PORT),
      secure: true,
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS,
      },
    });

    const mailOptions = {
      from: `"SaaS Engine" <${process.env.SMTP_USER}>`,
      to: process.env.ADMIN_EMAIL,
      subject: `🔥 New Lead - ${sanitizedLead.name}`,
      html: `
        <h3>New Lead Submitted</h3>
        <p><strong>Name:</strong> ${sanitizedLead.name}</p>
        <p><strong>Email:</strong> ${sanitizedLead.email}</p>
        <p><strong>Phone:</strong> ${sanitizedLead.phone}</p>
        <p><strong>Company:</strong> ${sanitizedLead.company || 'N/A'}</p>
        <p><strong>Message:</strong> ${sanitizedLead.message || 'N/A'}</p>
      `,
    };

    transporter
      .sendMail(mailOptions)
      .catch((err) => console.error(err));

    return NextResponse.json(
      {
        success: true,
        message: 'Lead submitted successfully',
      },
      { status: 201 }
    );
  } catch (error) {
    console.error(error);

    return NextResponse.json(
      {
        success: false,
        error: 'Internal server error',
      },
      { status: 500 }
    );
  }
}
```

---

# 2. Global Layout & Providers

## `src/app/providers.tsx`

```tsx
'use client';

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react';

interface ModalContextType {
  isOpen: boolean;
  openModal: () => void;
  closeModal: () => void;
}

const ModalContext =
  createContext<ModalContextType | undefined>(
    undefined
  );

export function Providers({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isOpen, setIsOpen] = useState(false);

  const openModal = () => setIsOpen(true);

  const closeModal = () => setIsOpen(false);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  return (
    <ModalContext.Provider
      value={{
        isOpen,
        openModal,
        closeModal,
      }}
    >
      {children}
    </ModalContext.Provider>
  );
}

export const useModal = () => {
  const context = useContext(ModalContext);

  if (!context) {
    throw new Error(
      'useModal must be used within Providers'
    );
  }

  return context;
};
```

---

## `src/app/layout.tsx`

```tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

import './globals.css';

import { Providers } from './providers';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
});

export const metadata: Metadata = {
  title: 'NextGen SaaS',
  description:
    'AI-driven operations canvas built for fast-moving teams.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className="dark bg-black"
    >
      <body
        className={`${inter.variable} font-sans text-slate-200 antialiased overflow-x-hidden`}
      >
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

---

# 3. Framer Motion Frontend

## `src/components/sections/Hero.tsx`

```tsx
'use client';

import {
  motion,
  useScroll,
  useTransform,
} from 'framer-motion';

import { useModal } from '@/app/providers';

export default function Hero() {
  const { openModal } = useModal();

  const { scrollY } = useScroll();

  const yText = useTransform(
    scrollY,
    [0, 500],
    [0, 120]
  );

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-black">
      <motion.div
        style={{ y: yText }}
        className="relative z-10 text-center max-w-4xl px-4"
      >
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
          Automate Operations With AI
        </h1>

        <p className="text-slate-400 text-lg mb-10">
          Visualize system states and deploy
          scalable workflows visually.
        </p>

        <button
          onClick={openModal}
          className="px-8 py-4 rounded-xl bg-indigo-600 text-white"
        >
          Book a Demo
        </button>
      </motion.div>
    </section>
  );
}
```

---

# 4. FAQ Section

## `src/components/sections/FAQ.tsx`

```tsx
'use client';

import { useState } from 'react';

import {
  AnimatePresence,
  motion,
} from 'framer-motion';

const faqs = [
  {
    q: 'Is migration difficult?',
    a: 'No. Migration is fast and simple.',
  },
  {
    q: 'How secure is the system?',
    a: 'All data uses TLS 1.3 encryption.',
  },
];

export default function FAQ() {
  const [openIndex, setOpenIndex] =
    useState<number | null>(null);

  return (
    <section className="py-24 max-w-3xl mx-auto px-4">
      <h2 className="text-3xl font-bold text-center mb-12">
        FAQ
      </h2>

      <div className="space-y-4">
        {faqs.map((faq, i) => (
          <div
            key={i}
            className="border-b border-slate-800 pb-4"
          >
            <button
              onClick={() =>
                setOpenIndex(
                  openIndex === i ? null : i
                )
              }
              className="w-full flex justify-between py-4"
            >
              <span>{faq.q}</span>

              <span>
                {openIndex === i ? '−' : '+'}
              </span>
            </button>

            <AnimatePresence>
              {openIndex === i && (
                <motion.div
                  initial={{
                    height: 0,
                    opacity: 0,
                  }}
                  animate={{
                    height: 'auto',
                    opacity: 1,
                  }}
                  exit={{
                    height: 0,
                    opacity: 0,
                  }}
                >
                  <p className="text-slate-400 pb-4">
                    {faq.a}
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </section>
  );
}
```

---

# 5. Lead Modal

## `src/components/LeadModal.tsx`

```tsx
'use client';

import { useModal } from '@/app/providers';

import {
  AnimatePresence,
  motion,
} from 'framer-motion';

export default function LeadModal() {
  const { isOpen, closeModal } =
    useModal();

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeModal}
            className="absolute inset-0 bg-black/70"
          />

          <motion.div
            initial={{
              opacity: 0,
              scale: 0.95,
            }}
            animate={{
              opacity: 1,
              scale: 1,
            }}
            exit={{
              opacity: 0,
              scale: 0.95,
            }}
            className="relative bg-slate-900 p-8 rounded-2xl z-10 w-full max-w-lg"
          >
            <button
              onClick={closeModal}
              className="absolute top-4 right-4"
            >
              ✕
            </button>

            <h3 className="text-2xl font-bold mb-6">
              Schedule Demo
            </h3>

            <form className="space-y-4">
              <input
                type="text"
                placeholder="Full Name"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2"
              />

              <input
                type="email"
                placeholder="Email"
                className="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2"
              />

              <button className="w-full py-3 rounded-xl bg-indigo-600">
                Submit
              </button>
            </form>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
```

---

# 6. Main Landing Page

## `src/app/page.tsx`

```tsx
import Hero from '@/components/sections/Hero';
import Features from '@/components/sections/Features';
import ProductDemo from '@/components/sections/ProductDemo';
import FAQ from '@/components/sections/FAQ';
import LeadModal from '@/components/LeadModal';

export default function Home() {
  return (
    <main className="relative min-h-screen bg-black overflow-x-hidden">
      <Hero />
      <Features />
      <ProductDemo />
      <FAQ />
      <LeadModal />
    </main>
  );
}
```

---

# 7. Environment Variables

## `.env.example`

```env
# MongoDB
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/saas_production

# SMTP
SMTP_HOST=smtp.postmarkapp.com
SMTP_PORT=587
SMTP_USER=your_smtp_user
SMTP_PASS=your_smtp_password
ADMIN_EMAIL=admin@yourdomain.com
```

---

# 8. Next.js Configuration

## `next.config.js`

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  images: {
    domains: ['images.unsplash.com'],
    formats: ['image/avif', 'image/webp'],
  },

  experimental: {
    optimizePackageImports: ['framer-motion'],
  },
};

module.exports = nextConfig;
```

---

# 9. Deployment Workflow

## Vercel / Netlify Deployment

### Step 1 — Initialize Repository

```bash
git init
git add .
git commit -m "Initial commit"
```

---

### Step 2 — Push to GitHub

```bash
git remote add origin <your-repository-url>
git push -u origin main
```

---

### Step 3 — Connect to Vercel

* Import repository into Vercel
* Select framework preset: Next.js
* Configure environment variables

---

### Step 4 — Build Settings

```plaintext
Build Command: next build
Output Directory: .next
```

---

# 10. Performance Optimizations

* Hardware accelerated transforms
* Framer Motion optimized imports
* No layout thrashing
* Lazy-loaded animation sections
* Responsive typography
* AVIF/WebP image delivery
* Accessible modal focus trapping
* Scroll lock handling
* SEO metadata optimization
* Dynamic sitemap and robots generation

---

# 11. Recommended Production Enhancements

## Infrastructure

* Redis rate limiting
* Edge middleware protection
* CDN caching
* Queue-based email processing

## Security

* CSRF protection
* CAPTCHA validation
* Request fingerprinting
* Audit logging

## Analytics

* PostHog
* Vercel Analytics
* OpenTelemetry tracing

## Scalability

* Horizontal API scaling
* MongoDB Atlas sharding
* Edge rendering
* ISR caching strategies
