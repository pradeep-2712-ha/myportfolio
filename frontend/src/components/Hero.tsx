import { motion } from "framer-motion";
import type { PortfolioData } from "../types";

type HeroProps = {
  data: PortfolioData;
};

export default function Hero({ data }: HeroProps) {
  return (
    <section id="home" className="relative overflow-hidden px-6 pt-20 pb-24">
      <div className="mx-auto max-w-6xl">
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.45 }}
          className="font-semibold uppercase tracking-[0.2em] text-accent-600"
        >
          Full-Stack Engineer
        </motion.p>
        <motion.h1
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.05 }}
          className="font-heading mt-4 max-w-3xl text-4xl font-bold leading-tight text-ink-900 md:text-6xl dark:text-white"
        >
          {data.name}
          <span className="block text-ink-600 dark:text-ink-100">{data.title}</span>
        </motion.h1>
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.55, delay: 0.1 }}
          className="mt-6 max-w-2xl text-lg text-ink-700 dark:text-ink-100"
        >
          {data.tagline}
        </motion.p>
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          whileInView={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.15 }}
          className="mt-8 flex flex-wrap gap-3"
        >
          <a
            href="/resume.pdf"
            download
            className="rounded-full bg-accent-500 px-6 py-3 text-sm font-semibold text-white transition hover:bg-accent-600"
          >
            Download Resume
          </a>
          <a
            href="#contact"
            className="rounded-full border border-ink-300 px-6 py-3 text-sm font-semibold text-ink-700 transition hover:bg-ink-100 dark:border-ink-500 dark:text-ink-100 dark:hover:bg-ink-800"
          >
            Contact Me
          </a>
        </motion.div>
      </div>
      <div className="pointer-events-none absolute -top-24 right-0 h-80 w-80 rounded-full bg-accent-400/30 blur-3xl" />
      <div className="pointer-events-none absolute bottom-0 left-0 h-80 w-80 rounded-full bg-ink-400/20 blur-3xl" />
    </section>
  );
}
