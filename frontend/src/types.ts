export type Skill = {
  name: string;
  level: string;
  category: string;
};

export type Project = {
  id: number;
  title: string;
  summary: string;
  stack: string[];
  link: string;
};

export type Experience = {
  id: number;
  role: string;
  company: string;
  period: string;
  highlights: string[];
};

export type Education = {
  degree: string;
  institution: string;
  year: string;
};

export type Certification = {
  name: string;
  issuer: string;
  year: string;
};

export type PortfolioData = {
  name: string;
  title: string;
  tagline: string;
  about: string;
  contact_email: string;
  phone: string;
  location: string;
  linkedin_url: string;
  github_url: string;
  skills: Skill[];
  projects: Project[];
  experience: Experience[];
  education: Education[];
  certifications: Certification[];
};

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};
