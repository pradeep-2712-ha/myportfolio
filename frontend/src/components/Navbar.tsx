type NavbarProps = {
  brand: string;
  darkMode: boolean;
  onToggleTheme: () => void;
};

export default function Navbar({ brand, darkMode, onToggleTheme }: NavbarProps) {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-white/70 backdrop-blur-lg dark:bg-ink-900/75">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-6 py-4">
        <a href="#home" className="font-heading text-lg font-semibold tracking-wide text-ink-800 dark:text-white">
          {brand}
        </a>
        <nav className="order-3 flex w-full gap-5 overflow-x-auto pb-1 text-sm font-semibold text-ink-700 md:order-2 md:w-auto md:pb-0 dark:text-ink-100">
          <a href="#about" className="hover:text-accent-500">About</a>
          <a href="#skills" className="hover:text-accent-500">Skills</a>
          <a href="#projects" className="hover:text-accent-500">Projects</a>
          <a href="#experience" className="hover:text-accent-500">Experience</a>
          <a href="#certifications" className="hover:text-accent-500">Certifications</a>
          <a href="#contact" className="hover:text-accent-500">Contact</a>
        </nav>
        <button
          type="button"
          aria-label="Toggle theme"
          onClick={onToggleTheme}
          className="order-2 rounded-full border border-ink-300 px-4 py-2 text-sm font-medium text-ink-700 transition hover:bg-ink-100 md:order-3 dark:border-ink-500 dark:text-ink-100 dark:hover:bg-ink-800"
        >
          {darkMode ? "Light" : "Dark"}
        </button>
      </div>
    </header>
  );
}
