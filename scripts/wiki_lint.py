#!/usr/bin/env python3
"""wiki_lint.py — Karpathy-LLM-Wiki Lint-Tool für /root/obsidian_vault/00 Wiki/.

Usage: python3 scripts/wiki_lint.py

Checks:
  - Dead Wikilinks (targets that don't resolve to any *.md in the vault)
  - Orphans (wiki pages with zero incoming links from other wiki pages)
  - Stale pages (frontmatter 'updated:' > 30 days old)

Strips inline code spans (backticks) before link extraction to avoid flagging
documentation-examples like `[[Wikilinks]]` as dead.
"""
import re
import datetime
from pathlib import Path

VAULT = Path("/root/obsidian_vault")
WIKI = VAULT / "00 Wiki"
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
CODE_RE = re.compile(r"`[^`]*`")
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
UPDATED_RE = re.compile(r"^updated:\s*(\S+)", re.MULTILINE)

def extract_links(text: str):
    text = FENCE_RE.sub("", text)
    text = CODE_RE.sub("", text)
    return [m.group(1).strip() for m in LINK_RE.finditer(text)]

def main():
    wiki_pages = {p.stem for p in WIKI.glob("*.md")}
    vault_stems = {md.stem for md in VAULT.rglob("*.md")}
    vault_rels = {md.relative_to(VAULT).as_posix()[:-3] for md in VAULT.rglob("*.md")}

    all_links = []
    for p in WIKI.glob("*.md"):
        for target in extract_links(p.read_text()):
            all_links.append((p.name, target))

    dead = []
    for src, target in sorted(set(all_links)):
        hit = target in vault_rels if '/' in target else target in vault_stems
        if not hit:
            dead.append((src, target))

    incoming = {s: 0 for s in wiki_pages}
    for src, target in all_links:
        stem = target.split('/')[-1]
        if stem in incoming and src != f"{stem}.md" and src != "index.md":
            incoming[stem] += 1
    orphans = sorted(p for p, c in incoming.items() if c == 0 and p not in ("index", "log"))

    today = datetime.date.today()
    stale = []
    for p in WIKI.glob("*.md"):
        m = UPDATED_RE.search(p.read_text())
        if m:
            try:
                d = datetime.date.fromisoformat(m.group(1))
                age = (today - d).days
                if age > 30:
                    stale.append((p.stem, age))
            except ValueError:
                pass

    print(f"=== WIKI LINT {today} ===")
    print(f"pages={len(wiki_pages)}  links={len(all_links)}  dead={len(dead)}  orphans={len(orphans)}  stale={len(stale)}")
    if dead:
        print("\nDEAD LINKS:")
        for src, target in dead:
            print(f"  [{src}] -> {target!r}")
    if orphans:
        print("\nORPHANS:")
        for p in orphans:
            print(f"  {p}")
    if stale:
        print("\nSTALE (>30d):")
        for p, age in stale:
            print(f"  {p} ({age}d)")
    return 1 if (dead or orphans) else 0

if __name__ == "__main__":
    raise SystemExit(main())
