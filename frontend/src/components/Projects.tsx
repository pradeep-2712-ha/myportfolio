import { motion } from "framer-motion";
import type { PortfolioData } from "../types";
import Reveal from "./Reveal";

type ProjectsProps = {
  data: PortfolioData;
};

export default function Projects({ data }: ProjectsProps) {
  return (
    <Reveal>
      <section id="projects" className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="section-title">Projects</h2>
        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          {data.projects.map((project, idx) => (
            <motion.article
              key={project.id}
              className="card"
              initial={{ opacity: 0, y: 24 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.2 }}
              transition={{ duration: 0.45, delay: idx * 0.07 }}
            >
              <h3 className="text-xl font-semibold text-ink-900 dark:text-white">{project.title}</h3>
              <p className="mt-3 text-sm leading-6 text-ink-700 dark:text-ink-100">{project.summary}</p>
              <div className="mt-4 flex flex-wrap gap-2">
                {project.stack.map((tech) => (
                  <span key={tech} className="tag">
                    {tech}
                  </span>
                ))}
              </div>
              <a href={project.link} className="mt-5 inline-flex text-sm font-semibold text-accent-600 hover:underline">
                View Project
              </a>
            </motion.article>
          ))}
        </div>
      </section>
    </Reveal>
  );
}
