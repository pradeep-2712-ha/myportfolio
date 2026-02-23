import { motion } from "framer-motion";
import type { PortfolioData } from "../types";
import Reveal from "./Reveal";

type ExperienceProps = {
  data: PortfolioData;
};

export default function Experience({ data }: ExperienceProps) {
  return (
    <Reveal>
      <section id="experience" className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="section-title">Experience</h2>
        <div className="mt-8 space-y-6 border-l-2 border-accent-500/50 pl-6">
          {data.experience.map((job, idx) => (
            <motion.article
              key={job.id}
              className="relative"
              initial={{ opacity: 0, x: -18 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, amount: 0.25 }}
              transition={{ duration: 0.45, delay: idx * 0.08 }}
            >
              <span className="absolute -left-[34px] top-2 h-3 w-3 rounded-full bg-accent-500" />
              <h3 className="text-xl font-semibold text-ink-900 dark:text-white">
                {job.role} - {job.company}
              </h3>
              <p className="mt-1 text-sm text-ink-600 dark:text-ink-100">{job.period}</p>
              <ul className="mt-3 space-y-2 text-sm text-ink-700 dark:text-ink-100">
                {job.highlights.map((h) => (
                  <li key={h}>- {h}</li>
                ))}
              </ul>
            </motion.article>
          ))}
        </div>
      </section>
    </Reveal>
  );
}

