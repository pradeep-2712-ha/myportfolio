import sqlite3
import re

from app.models.schemas import CertificationOut, EducationOut, ExperienceOut, PortfolioOut, ProjectOut, SkillOut


def get_portfolio_data(db: sqlite3.Connection) -> PortfolioOut:
    portfolio = db.execute("SELECT * FROM portfolio ORDER BY id LIMIT 1").fetchone()
    if not portfolio:
        raise ValueError("Portfolio data not found. Run seed.py first.")

    portfolio_id = int(portfolio["id"])
    skills_rows = db.execute(
        "SELECT name, level, category FROM skills WHERE portfolio_id = ? ORDER BY id",
        (portfolio_id,)
    ).fetchall()
    projects_rows = db.execute(
        "SELECT id, title, summary, stack_csv, link FROM projects WHERE portfolio_id = ? ORDER BY id",
        (portfolio_id,)
    ).fetchall()
    experience_rows = db.execute(
        "SELECT id, role, company, period, highlights_csv FROM experience WHERE portfolio_id = ? ORDER BY id",
        (portfolio_id,)
    ).fetchall()
    education_rows = db.execute(
        "SELECT degree, institution, year FROM education WHERE portfolio_id = ? ORDER BY id",
        (portfolio_id,)
    ).fetchall()
    certification_rows = db.execute(
        "SELECT name, issuer, year FROM certifications WHERE portfolio_id = ? ORDER BY id",
        (portfolio_id,)
    ).fetchall()

    return PortfolioOut(
        name=portfolio["name"],
        title=portfolio["title"],
        tagline=portfolio["tagline"],
        about=portfolio["about"],
        contact_email=portfolio["contact_email"],
        phone=portfolio["phone"],
        location=portfolio["location"],
        linkedin_url=portfolio["linkedin_url"],
        github_url=portfolio["github_url"],
        skills=[SkillOut(name=s["name"], level=s["level"], category=s["category"]) for s in skills_rows],
        projects=[
            ProjectOut(
                id=int(p["id"]),
                title=p["title"],
                summary=p["summary"],
                stack=[t.strip() for t in p["stack_csv"].split(",") if t.strip()],
                link=p["link"]
            )
            for p in projects_rows
        ],
        experience=[
            ExperienceOut(
                id=int(e["id"]),
                role=e["role"],
                company=e["company"],
                period=e["period"],
                highlights=[h.strip() for h in e["highlights_csv"].split("||") if h.strip()]
            )
            for e in experience_rows
        ],
        education=[
            EducationOut(degree=e["degree"], institution=e["institution"], year=e["year"]) for e in education_rows
        ],
        certifications=[
            CertificationOut(name=c["name"], issuer=c["issuer"], year=c["year"]) for c in certification_rows
        ]
    )


def build_context_blob(data: PortfolioOut) -> str:
    return (
        f"Name: {data.name}\n"
        f"Title: {data.title}\n"
        f"Tagline: {data.tagline}\n"
        f"About: {data.about}\n"
        f"Contact: {data.contact_email}, {data.phone}, {data.location}\n"
        f"Links: LinkedIn {data.linkedin_url}, GitHub {data.github_url}\n\n"
        f"Skills:\n"
        + "\n".join([f"- {s.name} ({s.level}, {s.category})" for s in data.skills])
        + "\n\nProjects:\n"
        + "\n".join([f"- {p.title}: {p.summary} | Stack: {', '.join(p.stack)} | Link: {p.link}" for p in data.projects])
        + "\n\nExperience:\n"
        + "\n".join(
            [f"- {e.role} at {e.company} ({e.period}) | Highlights: {'; '.join(e.highlights)}" for e in data.experience]
        )
        + "\n\nEducation:\n"
        + "\n".join([f"- {e.degree}, {e.institution} ({e.year})" for e in data.education])
        + "\n\nCertifications:\n"
        + "\n".join([f"- {c.name} ({c.issuer})" for c in data.certifications])
    )


def generate_local_answer(message: str, data: PortfolioOut) -> str:
    q = message.lower()

    if "skill" in q or "tech" in q:
        skill_lines = [f"- {s.name} ({s.level})" for s in data.skills]
        return "Here are the key skills from this portfolio:\n" + "\n".join(skill_lines)

    if "project" in q:
        project_lines = [f"- {p.title}: {p.summary}" for p in data.projects]
        return "Here are the projects listed in this portfolio:\n" + "\n".join(project_lines)

    if "experience" in q or "work" in q:
        exp_lines = [f"- {e.role} at {e.company} ({e.period})" for e in data.experience]
        return "Here is the work experience in this portfolio:\n" + "\n".join(exp_lines)

    if "education" in q or "degree" in q or "university" in q:
        edu_lines = [f"- {e.degree}, {e.institution} ({e.year})" for e in data.education]
        return "Here is the education information:\n" + "\n".join(edu_lines)

    if "contact" in q or "email" in q:
        return (
            f"Contact: {data.contact_email} | {data.phone}\n"
            f"LinkedIn: {data.linkedin_url}\n"
            f"GitHub: {data.github_url}"
        )

    if "certification" in q or "certificate" in q:
        cert_lines = [f"- {c.name} ({c.issuer})" for c in data.certifications]
        return "Here are the certifications listed in this portfolio:\n" + "\n".join(cert_lines)

    return (
        f"{data.name} is a {data.title}. "
        "Ask about skills, projects, experience, education, or contact."
    )


def try_apply_mutation(db: sqlite3.Connection, message: str) -> str | None:
    text = message.strip()
    lowered = text.lower()
    fields = _parse_fields(text)

    if lowered in {"add", "add it", "add this"}:
        return (
            "Tell me what to add. Examples: "
            "add skill name=React level=Advanced category=Frontend, "
            "add project title=Portfolio summary=Personal site stack=React,FastAPI, "
            "add experience role=Engineer company=Acme period=2024-Present."
        )

    if lowered.startswith("add skill:") or ("add" in lowered and "skill" in lowered):
        name = fields.get("name") or _extract_skill_name(text)
        level = fields.get("level", "Intermediate")
        category = fields.get("category", "General")
        if not name:
            return (
                "Use: add skill name=React level=Advanced category=Frontend "
                "or simple: add skill React"
            )
        portfolio_id = _get_portfolio_id(db)
        db.execute(
            "INSERT INTO skills (name, level, category, portfolio_id) VALUES (?, ?, ?, ?)",
            (name, level, category, portfolio_id)
        )
        db.commit()
        return f"Added skill: {name} ({level}, {category})."

    if lowered.startswith("add project:") or ("add" in lowered and "project" in lowered):
        title = fields.get("title") or _extract_project_title(text)
        summary = fields.get("summary", "Added via AI assistant.")
        stack = fields.get("stack", "")
        link = fields.get("link", "https://github.com/example/project")
        if not title or not summary:
            return (
                "Use: add project title=My App summary=What it does stack=React,TypeScript link=https://... "
                "or simple: add project My App"
            )
        portfolio_id = _get_portfolio_id(db)
        db.execute(
            "INSERT INTO projects (title, summary, stack_csv, link, portfolio_id) VALUES (?, ?, ?, ?, ?)",
            (title, summary, stack, link, portfolio_id)
        )
        db.commit()
        return f"Added project: {title}."

    if (
        lowered.startswith("add experience:")
        or "add exp" in lowered
        or ("add" in lowered and "experience" in lowered)
    ):
        role = fields.get("role")
        company = fields.get("company")
        period = fields.get("period")
        highlights = fields.get("highlights", "")
        if not role or not company or not period:
            return (
                "Use format: add experience: role=Senior Engineer | company=Acme | period=2024-Present | "
                "highlights=Built X; Improved Y"
            )
        highlights_csv = "||".join([h.strip() for h in highlights.split(";") if h.strip()])
        portfolio_id = _get_portfolio_id(db)
        db.execute(
            "INSERT INTO experience (role, company, period, highlights_csv, portfolio_id) VALUES (?, ?, ?, ?, ?)",
            (role, company, period, highlights_csv, portfolio_id)
        )
        db.commit()
        return f"Added experience: {role} at {company} ({period})."

    return None


def _parse_fields(raw: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    keys = "name|level|category|title|summary|stack|link|role|company|period|highlights"
    for match in re.finditer(rf"\b({keys})\b\s*[:=]\s*(.*?)(?=\s+\b({keys})\b\s*[:=]|$)", raw, re.IGNORECASE):
        key = match.group(1).strip().lower()
        value = match.group(2).strip().strip("|").strip(",")
        if value:
            fields[key] = value
    return fields


def _split_pair(token: str) -> tuple[str, str]:
    for sep in ("=", ":"):
        if sep in token:
            left, right = token.split(sep, 1)
            return left.strip(), right.strip()
    return "", ""


def _extract_skill_name(text: str) -> str | None:
    match = re.search(r"add(?:\s+my)?\s+skill\s+(.+)$", text, flags=re.IGNORECASE)
    if not match:
        return None
    value = match.group(1).strip()
    if "=" in value or ":" in value:
        return None
    return value


def _extract_project_title(text: str) -> str | None:
    match = re.search(r"add(?:\s+my)?\s+project\s+(.+)$", text, flags=re.IGNORECASE)
    if not match:
        return None
    value = match.group(1).strip()
    if "=" in value or ":" in value:
        return None
    return value


def _get_portfolio_id(db: sqlite3.Connection) -> int:
    row = db.execute("SELECT id FROM portfolio ORDER BY id LIMIT 1").fetchone()
    if not row:
        raise ValueError("Portfolio data not found. Run seed.py first.")
    return int(row["id"])
