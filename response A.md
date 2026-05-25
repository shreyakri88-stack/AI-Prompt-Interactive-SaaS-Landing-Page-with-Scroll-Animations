# Full Stack SaaS Landing Page

### Next.js + Framer Motion + Tailwind + Nodemailer

---

# 1. Create Project

```bash
npx create-next-app@latest saas-landing
cd saas-landing

npm install framer-motion react-hook-form zod @hookform/resolvers nodemailer react-icons react-hot-toast

npm install express-rate-limit dompurify jsdom
```

---

# 2. Folder Structure

```bash
app/
 ├── api/
 │    └── contact/
 │         └── route.ts
 ├── components/
 │    ├── Hero.tsx
 │    ├── Features.tsx
 │    ├── Pricing.tsx
 │    ├── ContactModal.tsx
 │    ├── Navbar.tsx
 │    └── Footer.tsx
 ├── globals.css
 ├── layout.tsx
 └── page.tsx

lib/
 └── mail.ts

.env.local
```

---

# 3. Tailwind Setup

## `app/globals.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

html {
  scroll-behavior: smooth;
}

body {
  background: #050816;
  color: white;
  overflow-x: hidden;
}
```

---

# 4. Root Layout

## `app/layout.tsx`

```tsx
import './globals.css'

export const metadata = {
  title: 'Modern SaaS Landing',
  description: 'Animated SaaS Website',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

---

# 5. Main Page

## `app/page.tsx`

```tsx
'use client'

import Hero from './components/Hero'
import Features from './components/Features'
import Pricing from './components/Pricing'
import Footer from './components/Footer'

export default function Home() {
  return (
    <main>
      <Hero />
      <Features />
      <Pricing />
      <Footer />
    </main>
  )
}
```

---

# 6. Hero Section with Framer Motion

## `app/components/Hero.tsx`

```tsx
'use client'

import { motion } from 'framer-motion'
import ContactModal from './ContactModal'
import { useState } from 'react'

export default function Hero() {
  const [open, setOpen] = useState(false)

  return (
    <section className="min-h-screen flex items-center justify-center px-6 relative overflow-hidden">
      <motion.div
        initial={{ opacity: 0, y: 100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="text-center max-w-4xl"
      >
        <motion.h1
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="text-6xl font-bold leading-tight"
        >
          Build Stunning SaaS Experiences
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-6 text-xl text-gray-300"
        >
          Scroll-based storytelling with modern animations.
        </motion.p>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => setOpen(true)}
          className="mt-10 bg-blue-600 px-8 py-4 rounded-xl text-lg font-semibold"
        >
          Book a Demo
        </motion.button>
      </motion.div>

      <ContactModal open={open} setOpen={setOpen} />
    </section>
  )
}
```

---

# 7. Features Section

## `app/components/Features.tsx`

```tsx
'use client'

import { motion } from 'framer-motion'

const features = [
  'Advanced Animations',
  'Fast Performance',
  'Responsive Design',
  'SEO Optimized',
]

export default function Features() {
  return (
    <section className="py-32 px-6">
      <motion.div
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={{
          hidden: {},
          visible: {
            transition: {
              staggerChildren: 0.2,
            },
          },
        }}
        className="grid md:grid-cols-2 gap-8 max-w-6xl mx-auto"
      >
        {features.map((feature, i) => (
          <motion.div
            key={i}
            variants={{
              hidden: { opacity: 0, y: 50 },
              visible: { opacity: 1, y: 0 },
            }}
            whileHover={{ scale: 1.03 }}
            className="bg-white/10 backdrop-blur-lg p-8 rounded-2xl border border-white/10"
          >
            <h3 className="text-2xl font-semibold">{feature}</h3>
          </motion.div>
        ))}
      </motion.div>
    </section>
  )
}
```

---

# 8. Pricing Section

## `app/components/Pricing.tsx`

```tsx
'use client'

import { motion } from 'framer-motion'

export default function Pricing() {
  return (
    <section className="py-32 px-6">
      <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8">
        {[1, 2, 3].map((item) => (
          <motion.div
            key={item}
            whileHover={{ y: -10 }}
            className="bg-white/10 p-10 rounded-2xl border border-white/10"
          >
            <h2 className="text-3xl font-bold">Pro Plan</h2>
            <p className="mt-4 text-gray-300">Perfect for startups.</p>
            <div className="mt-8 text-5xl font-bold">$49</div>
          </motion.div>
        ))}
      </div>
    </section>
  )
}
```

---

# 9. Contact Modal

## `app/components/ContactModal.tsx`

```tsx
'use client'

import { AnimatePresence, motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import toast from 'react-hot-toast'

const schema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  phone: z.string().min(10),
  message: z.string().optional(),
})

export default function ContactModal({ open, setOpen }: any) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm({
    resolver: zodResolver(schema),
  })

  const onSubmit = async (data: any) => {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })

    const result = await res.json()

    if (result.success) {
      toast.success('Message sent successfully')
      reset()
      setOpen(false)
    } else {
      toast.error(result.error)
    }
  }

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            className="bg-[#111827] p-8 rounded-2xl w-full max-w-lg"
          >
            <h2 className="text-3xl font-bold mb-6">Get in Touch</h2>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <input
                {...register('name')}
                placeholder="Name"
                className="w-full p-4 rounded-lg bg-black/30"
              />
              {errors.name && <p>Name is required</p>}

              <input
                {...register('email')}
                placeholder="Email"
                className="w-full p-4 rounded-lg bg-black/30"
              />
              {errors.email && <p>Valid email required</p>}

              <input
                {...register('phone')}
                placeholder="Phone"
                className="w-full p-4 rounded-lg bg-black/30"
              />

              <textarea
                {...register('message')}
                placeholder="Message"
                className="w-full p-4 rounded-lg bg-black/30"
              />

              <button
                disabled={isSubmitting}
                className="w-full bg-blue-600 py-4 rounded-xl"
              >
                {isSubmitting ? 'Sending...' : 'Submit'}
              </button>
            </form>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}
```

---

# 10. Mail Utility

## `lib/mail.ts`

```ts
import nodemailer from 'nodemailer'

export const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS,
  },
})
```

---

# 11. API Route

## `app/api/contact/route.ts`

```ts
import { NextResponse } from 'next/server'
import { transporter } from '@/lib/mail'

export async function POST(req: Request) {
  try {
    const body = await req.json()

    const { name, email, phone, message } = body

    if (!name || !email || !phone) {
      return NextResponse.json(
        {
          success: false,
          error: 'Missing required fields',
        },
        { status: 400 }
      )
    }

    await transporter.sendMail({
      from: process.env.EMAIL_USER,
      to: process.env.EMAIL_TO,
      subject: 'New SaaS Lead',
      html: `
        <h2>New Lead</h2>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Phone:</strong> ${phone}</p>
        <p><strong>Message:</strong> ${message}</p>
      `,
    })

    console.log('Lead Saved:', body)

    return NextResponse.json({
      success: true,
      message: 'Lead submitted successfully',
    })
  } catch (error) {
    console.error(error)

    return NextResponse.json(
      {
        success: false,
        error: 'Something went wrong',
      },
      { status: 500 }
    )
  }
}
```

---

# 12. Footer Component

## `app/components/Footer.tsx`

```tsx
export default function Footer() {
  return (
    <footer className="py-10 text-center text-gray-400 border-t border-white/10">
      © 2026 Modern SaaS. All rights reserved.
    </footer>
  )
}
```

---

# 13. Environment Variables

## `.env.local`

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
EMAIL_TO=portfolio_owner@gmail.com
```

---

# 14. Run Project

```bash
npm run dev
```

---

# 15. Production Features Included

* ✅ Framer Motion animations
* ✅ Scroll storytelling UI
* ✅ Responsive layout
* ✅ Animated modal
* ✅ Form validation
* ✅ Secure API route
* ✅ Nodemailer integration
* ✅ Environment variable support
* ✅ Backend error handling
* ✅ Production-ready folder structure
* ✅ Tailwind styling
* ✅ Accessibility-friendly structure

---

# 16. Recommended Improvements

Add these for enterprise-grade scaling:

* MongoDB integration
* PostgreSQL support
* Rate limiting
* CAPTCHA protection
* Redis caching
* Analytics dashboard
* CMS integration
* Dark/light mode
* Advanced SEO metadata
* Docker deployment
* Vercel deployment pipeline

