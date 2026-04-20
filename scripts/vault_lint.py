#!/usr/bin/env python3
"""
Vault-Lint — Wikilink-Health-Check fuer /root/obsidian_vault.
Teil vom `vault-ingest`-Skill, Operation `lint`.

Handelt folgende Obsidian-Syntax korrekt:
- Aliases via `|` und `\\|` (Escape in Markdown-Tables)
- Optionales `.md`-Suffix im Link-Target
- `#section` Anchors
- Relative Pfade mit `../`
- Embeds (`![[file.png]]`) via Non-MD-Asset-Indexing

Exit Codes:
  0 = clean (0 dead links, 0 stale)
  1 = dead links present
"""
import re, pathlib, sys, datetime
from collections import defaultdict

VAULT = pathlib.Path("/root/obsidian_vault")
PLACEHOLDERS = {"Wikilinks", "page-name", "file",
                "raw/source-file-name", "page-a", "page-b", "raw/<file>"}
STALE_DAYS = 30
SKIP_ORPHAN_DIRS = ("00 Wiki/", "05 Daily Notes/", "06 Archiv/")

def build_index():
    paths = {}
    basenames = defaultdict(list)
    for p in VAULT.rglob("*.md"):
        rel = str(p.relative_to(VAULT)).replace(".md", "")
        paths[rel] = p
        basenames[p.stem].append(p)
    for p in VAULT.rglob("*"):
        if p.is_file() and p.suffix != ".md":
            rel = str(p.relative_to(VAULT))
            paths[rel] = p
            basenames[p.name].append(p)
            basenames[p.stem].append(p)
    return paths, basenames

LINK_PAT = re.compile(r"\[\[([^\[\]\n]+?)\]\]")

def extract_target(raw):
    s = raw
    for sep in ("\\|", "|", "#"):
        if sep in s:
            s = s.split(sep, 1)[0]
    s = s.strip()
    if s.endswith(".md"):
        s = s[:-3]
    return s

def resolve(tgt, paths, basenames, src_path):
    if tgt in paths:
        return paths[tgt]
    if tgt in basenames and basenames[tgt]:
        return basenames[tgt][0]
    if tgt.startswith("../"):
        try:
            tp = (src_path.parent / (tgt + ".md")).resolve()
            rel = str(tp.relative_to(VAULT)).replace(".md", "")
            if rel in paths:
                return paths[rel]
        except Exception:
            pass
    return None

def main():
    paths, basenames = build_index()
    dead_per_file = defaultdict(list)
    inbound = defaultdict(set)
    total_links = 0

    for p in VAULT.rglob("*.md"):
        try:
            c = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for m in LINK_PAT.finditer(c):
            tgt = extract_target(m.group(1).strip())
            if not tgt or tgt in PLACEHOLDERS:
                continue
            total_links += 1
            r = resolve(tgt, paths, basenames, p)
            rel = str(p.relative_to(VAULT))
            if r:
                key = r.stem if r.suffix == ".md" else r.name
                inbound[key].add(rel)
            else:
                dead_per_file[rel].append(tgt)

    orphans = defaultdict(list)
    for p in VAULT.rglob("*.md"):
        rel = str(p.relative_to(VAULT))
        if any(rel.startswith(s) for s in SKIP_ORPHAN_DIRS):
            continue
        if not inbound.get(p.stem):
            orphans[rel.split("/")[0]].append(rel)

    today = datetime.date.today()
    stale = []
    for p in (VAULT / "00 Wiki").glob("*.md"):
        c = p.read_text(encoding="utf-8")
        m = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", c, re.MULTILINE)
        if m:
            age = (today - datetime.date.fromisoformat(m.group(1))).days
            if age > STALE_DAYS:
                stale.append((p.name, age))

    total_dead = sum(len(v) for v in dead_per_file.values())
    total_orphans = sum(len(v) for v in orphans.values())

    print(f"Vault-Lint — {today}")
    print(f"Total wikilinks: {total_links}")
    print(f"Dead links:      {total_dead} ({100*total_dead/max(total_links,1):.1f}%)")
    print(f"PARA-Orphans:    {total_orphans}")
    print(f"Stale Wiki:      {len(stale)}")

    if dead_per_file:
        print("\nDead links:")
        for f in sorted(dead_per_file):
            for t in dead_per_file[f]:
                print(f"  [{f}] → [[{t}]]")

    if orphans:
        print("\nOrphans per dir:")
        for d in sorted(orphans, key=lambda x: -len(orphans[x])):
            print(f"  {d}: {len(orphans[d])}")

    sys.exit(1 if total_dead > 0 else 0)

if __name__ == "__main__":
    main()
