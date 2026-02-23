import type { PortfolioData } from "../types";
import Reveal from "./Reveal";

type ContactProps = {
  data: PortfolioData;
};

export default function Contact({ data }: ContactProps) {
  return (
    <Reveal>
      <section id="contact" className="mx-auto max-w-6xl px-6 py-14">
        <div className="card flex flex-col items-start justify-between gap-6 md:flex-row md:items-center">
          <div>
            <h2 className="section-title !mt-0">Contact</h2>
            <p className="section-copy mt-3">Open to internships, full-time opportunities, and AI/ML collaborations.</p>
            <div className="mt-4 flex flex-wrap gap-3 text-sm">
              <a href={data.linkedin_url} target="_blank" rel="noreferrer" className="tag">
                LinkedIn
              </a>
              <a href={data.github_url} target="_blank" rel="noreferrer" className="tag">
                GitHub
              </a>
              <a href={`tel:${data.phone.replace(/\s/g, "")}`} className="tag">
                {data.phone}
              </a>
            </div>
          </div>
          <a
            href={`mailto:${data.contact_email}`}
            className="rounded-full bg-accent-500 px-6 py-3 font-semibold text-white transition hover:bg-accent-600"
          >
            {data.contact_email}
          </a>
        </div>
      </section>
    </Reveal>
  );
}
