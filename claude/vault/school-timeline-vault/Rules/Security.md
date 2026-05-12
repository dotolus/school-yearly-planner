---
title: Security Rules
tags:
  - rules
  - security
  - project/school-timeline
---

# Security Rules

> [!note]
> This is a static front-end project with no server, no auth, and no user-submitted data. Security concerns are minimal but still worth documenting.

## Rules

- All data files (`data/*.js`) are static and version-controlled — never include personal student data, passwords, or credentials
- No external scripts or CDN dependencies — everything runs from local files to avoid supply-chain risk
- If the project is later extended with a backend, apply standard OWASP rules: validate all inputs, parameterize queries, sanitize HTML output
- Do not use `innerHTML` with untrusted user input; currently all HTML strings in `details` fields come from the controlled data files only
