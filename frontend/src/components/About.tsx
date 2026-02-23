import type { PortfolioData } from "../types";
import Reveal from "./Reveal";

type AboutProps = {
  data: PortfolioData;
};

export default function About({ data }: AboutProps) {
  return (
    <Reveal>
      <section id="about" className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="section-title">About</h2>
        <p className="section-copy">{data.about}</p>
        <div className="mt-6 flex flex-wrap gap-4 text-sm">
          <span className="pill">{data.location}</span>
          <span className="pill">{data.contact_email}</span>
          <span className="pill">{data.phone}</span>
        </div>
      </section>
    </Reveal>
  );
}
