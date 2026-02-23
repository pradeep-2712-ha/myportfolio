import { motion } from "framer-motion";
import type { PortfolioData } from "../types";
import Reveal from "./Reveal";

type CertificationsProps = {
  data: PortfolioData;
};

export default function Certifications({ data }: CertificationsProps) {
  return (
    <Reveal>
      <section id="certifications" className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="section-title">Certifications</h2>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          {data.certifications.map((cert, idx) => (
            <motion.article
              key={`${cert.name}-${cert.issuer}`}
              className="card"
              initial={{ opacity: 0, y: 18 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.4, delay: idx * 0.06 }}
            >
              <h3 className="text-lg font-semibold text-ink-900 dark:text-white">{cert.name}</h3>
              <p className="mt-2 text-sm text-ink-700 dark:text-ink-100">{cert.issuer}</p>
              {cert.year ? <p className="mt-1 text-xs text-ink-600 dark:text-ink-200">{cert.year}</p> : null}
            </motion.article>
          ))}
        </div>
      </section>
    </Reveal>
  );
}
