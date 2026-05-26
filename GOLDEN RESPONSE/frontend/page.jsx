
'use client'
import { motion } from 'framer-motion'

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center">
      <motion.h1
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="text-6xl font-bold"
      >
        AI Prompt Interactive
      </motion.h1>
    </main>
  )
}
