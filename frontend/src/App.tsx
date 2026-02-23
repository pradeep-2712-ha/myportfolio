import { useEffect, useState } from "react";
import { getPortfolioData } from "./api/client";
import type { PortfolioData } from "./types";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import About from "./components/About";
import Skills from "./components/Skills";
import Projects from "./components/Projects";
import Experience from "./components/Experience";
import Certifications from "./components/Certifications";
import Contact from "./components/Contact";
import ChatWidget from "./components/ChatWidget";

export default function App() {
  const [data, setData] = useState<PortfolioData | null>(null);
  const [loading, setLoading] = useState(true);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    void (async () => {
      try {
        const result = await getPortfolioData();
        setData(result);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  useEffect(() => {
    if (darkMode) document.documentElement.classList.add("dark");
    else document.documentElement.classList.remove("dark");
  }, [darkMode]);

  if (loading) {
    return <main className="grid min-h-screen place-items-center text-ink-700">Loading portfolio...</main>;
  }

  if (!data) {
    return <main className="grid min-h-screen place-items-center text-red-600">Unable to load portfolio.</main>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-ink-50 via-white to-ink-100 text-ink-800 transition dark:from-ink-900 dark:via-ink-800 dark:to-ink-900 dark:text-ink-100">
      <Navbar
        brand="Pradeepsai"
        darkMode={darkMode}
        onToggleTheme={() => setDarkMode((prev) => !prev)}
      />
      <Hero data={data} />
      <About data={data} />
      <Skills data={data} />
      <Projects data={data} />
      <Experience data={data} />
      <Certifications data={data} />
      <Contact data={data} />
      <ChatWidget />
    </div>
  );
}
