import { motion } from "framer-motion";
import { useMemo, useState } from "react";
import type { PortfolioData, Skill } from "../types";
import Reveal from "./Reveal";

type SkillsProps = {
  data: PortfolioData;
};

const levelScore: Record<string, number> = {
  Advanced: 90,
  Intermediate: 70,
  Beginner: 45
};

const skillScoreOverrides: Record<string, number> = {
  C: 100,
  "C lang": 100,
  Java: 100,
  "Machine Learning": 100,
  "Machine Learning (Basics)": 100,
  Python: 90,
  JavaScript: 90,
  ReactJS: 90,
  "Node.js": 90
};

function normalize(value: string): string {
  return value.trim().toLowerCase();
}

function scoreFor(level: string): number {
  return levelScore[level] ?? 60;
}

function scoreForSkill(skill: Skill): number {
  return skillScoreOverrides[skill.name] ?? scoreFor(skill.level);
}

export default function Skills({ data }: SkillsProps) {
  const [activeCategory, setActiveCategory] = useState<string>("All");
  const [query, setQuery] = useState("");

  const categories = useMemo(() => {
    const set = new Set(data.skills.map((skill) => skill.category));
    return ["All", ...Array.from(set)];
  }, [data.skills]);

  const visibleSkills = useMemo(() => {
    const search = normalize(query);
    return data.skills.filter((skill) => {
      const categoryMatch = activeCategory === "All" || skill.category === activeCategory;
      const textMatch =
        !search || normalize(skill.name).includes(search) || normalize(skill.category).includes(search);
      return categoryMatch && textMatch;
    });
  }, [data.skills, activeCategory, query]);

  const grouped = useMemo(() => {
    const map = new Map<string, Skill[]>();
    for (const skill of visibleSkills) {
      const arr = map.get(skill.category) ?? [];
      arr.push(skill);
      map.set(skill.category, arr);
    }
    return Array.from(map.entries());
  }, [visibleSkills]);

  return (
    <Reveal>
      <section id="skills" className="mx-auto max-w-6xl px-6 py-14">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 className="section-title">Skills</h2>
            <p className="section-copy mt-2 max-w-2xl">
              Explore skills by category and level. This layout makes it easy for recruiters to scan strengths quickly.
            </p>
          </div>
          <div className="rounded-2xl border border-ink-200 bg-white/75 px-4 py-3 text-sm dark:border-ink-600 dark:bg-ink-800/70">
            <p className="text-ink-700 dark:text-ink-100">
              Showing <span className="font-bold text-accent-600">{visibleSkills.length}</span> of{" "}
              <span className="font-bold">{data.skills.length}</span> skills
            </p>
          </div>
        </div>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          {categories.map((category) => (
            <button
              key={category}
              type="button"
              onClick={() => setActiveCategory(category)}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                category === activeCategory
                  ? "bg-accent-500 text-white"
                  : "border border-ink-300 text-ink-700 hover:bg-ink-100 dark:border-ink-500 dark:text-ink-100 dark:hover:bg-ink-800"
              }`}
            >
              {category}
            </button>
          ))}
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search skill..."
            className="ml-auto w-full max-w-xs rounded-full border border-ink-300 bg-white px-4 py-2 text-sm outline-none focus:border-accent-500 dark:border-ink-500 dark:bg-ink-900 dark:text-ink-100"
          />
        </div>

        <div className="mt-8 space-y-8">
          {grouped.map(([category, skills], sectionIdx) => (
            <div key={category}>
              <h3 className="text-lg font-semibold text-ink-800 dark:text-ink-100">{category}</h3>
              <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {skills.map((skill, idx) => (
                  <motion.article
                    key={`${category}-${skill.name}`}
                    className="card"
                    initial={{ opacity: 0, y: 14 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, amount: 0.2 }}
                    transition={{ duration: 0.35, delay: sectionIdx * 0.05 + idx * 0.03 }}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <h4 className="text-base font-semibold text-ink-900 dark:text-white">{skill.name}</h4>
                      <span className="rounded-full bg-accent-500/10 px-3 py-1 text-xs font-semibold text-accent-600">
                        {skill.level}
                      </span>
                    </div>
                    <div className="mt-4 h-2 w-full rounded-full bg-ink-100 dark:bg-ink-700">
                      <motion.div
                        className="h-2 rounded-full bg-accent-500"
                        initial={{ width: 0 }}
                        whileInView={{ width: `${scoreForSkill(skill)}%` }}
                        viewport={{ once: true, amount: 0.4 }}
                        transition={{ duration: 0.7, delay: 0.1 }}
                      />
                    </div>
                    <p className="mt-2 text-xs text-ink-600 dark:text-ink-200">
                      {scoreForSkill(skill)}% proficiency
                    </p>
                  </motion.article>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>
    </Reveal>
  );
}
