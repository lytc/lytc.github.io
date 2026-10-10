#!/usr/bin/env python3
"""Build a plain static portfolio. Standard library only."""
import html
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = json.loads((ROOT / 'content/work.json').read_text())
EVIDENCE = json.loads((ROOT / 'data/evidence.json').read_text())
ACTIVITY = json.loads((ROOT / 'data/activity.json').read_text())
CSS_VERSION = hashlib.sha256((ROOT / 'assets/site.css').read_bytes()).hexdigest()[:12]
e = html.escape


def page(title, description, body, path='/'):
    return f'''<!doctype html>
<html lang="en" id="top"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<link rel="canonical" href="https://lytc.github.io{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website"><meta property="og:url" content="https://lytc.github.io{path}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css?v={CSS_VERSION}">
</head><body><a class="skip-link" href="#main">Skip to content</a>
<header><a class="name" href="/">Ly Tran</a><nav aria-label="Main navigation"><a href="/#work">Work</a><a href="/#stack">Stack</a><a href="/activity.html">Numbers</a><a href="/working-together.html">Fit</a><a href="#contact">Contact</a></nav></header>
{body}
<footer id="contact"><h2>Contact</h2><p><a href="mailto:prtran@gmail.com">prtran@gmail.com</a> · <a href="tel:+84908204012">+84 908 204 012</a> · <a href="https://github.com/lytc">GitHub</a></p><p class="muted">Vietnam · Remote or Ho Chi Minh City</p><div class="footer-meta"><a href="/evidence.html">Sources & scope</a><span>Updated October 2026</span></div></footer>
</body></html>'''


def write(name, title, description, body):
    path = '/' if name == 'index.html' else '/' + name
    (ROOT / name).write_text(page(title, description, body, path))


def metric_rows():
    gh = ACTIVITY['github']
    ts = ACTIVITY['typescript_line_changes']
    rows = [
        ('PRs opened', f"{gh['pull_requests_opened']:,}", 'Across Digication repositories'),
        ('PRs merged', f"{gh['pull_requests_merged']:,}", 'Included in the opened PRs'),
        ('Others’ PRs reviewed', f"{gh['others_pull_requests_reviewed']:,}", 'Distinct PRs; self-authored excluded'),
        ('Non-merge commits', f"{ACTIVITY['product_history']['unique_non_merge_commits']:,}", 'Three product-history snapshots'),
        ('TypeScript lines added', f"{ts['added']:,}", 'Filtered diffs in two product repositories'),
        ('TypeScript lines removed', f"{ts['deleted']:,}", 'Same scope as lines added'),
    ]
    return ''.join(f'<tr><th scope="row">{label}</th><td class="number">{value}</td><td>{scope}</td></tr>' for label, value, scope in rows)


def fit_summary():
    return '''<div class="fit-summary"><div><h3>I may not be the right fit if…</h3><ul><li>Meetings are central to everyday work.</li><li>Technical decisions are imposed by rank.</li><li>The role is mainly people management.</li></ul></div><div><h3>Where I do my best work</h3><ul><li>Architecture, platforms, and developer tools.</li><li>Written communication and very few meetings.</li><li>An equal voice in decisions and shared responsibility.</li></ul></div></div>'''


def ai_period_table():
    data = ACTIVITY['ai_periods']
    periods = data['periods']
    labels = ['2011–23', '2024', '2025', '2026*']
    headers = ''.join(f'<th scope="col">{label}<small>{p["months"]:.1f} mo</small></th>' for label, p in zip(labels, periods))
    estimates = ''.join(f'<td class="number">{p["ai_use_estimate_percent"]}%</td>' if p['ai_use_estimate_percent'] is not None else '<td class="number">—</td>' for p in periods)
    rows = f'<tr><th scope="row">AI use (my estimate)</th>{estimates}</tr>'
    for label, key in [('PRs opened', 'prs_opened'), ('PRs opened / month', 'prs_opened_per_month'), ('PRs merged', 'prs_merged'), ('Others’ PRs reviewed', 'others_prs_reviewed'), ('Product commits', 'product_commits'), ('TypeScript lines added', 'typescript_added'), ('TypeScript lines removed', 'typescript_removed')]:
        cells = ''.join(f'<td class="number">{p[key]:,.1f}</td>' if key.endswith('per_month') else f'<td class="number">{p[key]:,}</td>' for p in periods)
        rows += f'<tr><th scope="row">{label}</th>{cells}</tr>'
    return f'''<section id="ai-periods"><h2>By period and AI use</h2><p>I estimate my AI use at 30% in 2024, 50% in 2025, and 90% in 2026. These are personal estimates, not measured percentages of AI-written code.</p><div class="table-wrap"><table class="period-table"><thead><tr><th scope="col">Activity</th>{headers}</tr></thead><tbody>{rows}</tbody></table></div><p class="note">*2026 runs to October 10. No AI-use estimate was given for before 2024. A PR reviewed in multiple periods appears in each of those periods.</p><p class="note">PRs include product and internal-tool work. Commits cover three product snapshots; TypeScript covers two. This is a record of activity, not a measurement of AI’s effect on productivity.</p><details><summary>Dates, monthly rates, and limits</summary><p>{e(data['method'])}</p><p>{e(data['monthly_rate'])}</p><p>{e(data['limits'])}</p></details></section>'''


def home():
    work = ''.join(f'<article class="work-row"><h3><a href="/work/{item["slug"]}.html">{e(item["title"])}</a></h3><p>{e(item["summary"])}</p></article>' for item in WORK)
    body = f'''<main id="main"><section class="intro"><h1>Ly Tran</h1><p class="lead">Senior engineer. TypeScript, products, and developer tools.</p><p id="journey">I’ve contributed to Digication since 2011, from learning applications and APIs to shared packages and infrastructure. My next focus is architecture, platforms, and improving how a team builds software.</p><p><a href="/working-together.html">Working together</a> · <a href="mailto:prtran@gmail.com">Email me</a></p></section>
<section id="work"><h2>Selected work</h2><p class="muted">Products and engineering work at Digication, built with colleagues.</p><div class="work-list">{work}</div></section>
<section id="stack"><h2>Stack</h2><dl class="stack-list"><dt>Preferred</dt><dd><strong>TypeScript · React · Node.js</strong></dd><dt>Frontend</dt><dd>Apollo Client, Material UI, Vite, rich-text editing, shared UI.</dd><dt>Backend</dt><dd>GraphQL, Apollo Server, TypeGraphQL, TypeORM, MySQL, Redis.</dd><dt>Infrastructure</dt><dd>AWS Lambda, SQS, S3, SST, CDK, Docker, pnpm, CI/CD.</dd><dt>AI & testing</dt><dd>AI SDKs, OpenAI, Anthropic, Google AI, Jest, React Testing Library.</dd><dt>Earlier work</dt><dd>JavaScript, PHP, and migration of legacy PHP/Ruby applications.</dd></dl><div id="approach"><h3>How I work with AI</h3><p>I use coding agents for much of my recent implementation. I review the changes, run checks, and remain responsible for what I submit.</p></div></section>
<section id="activity"><h2>Numbers</h2><p class="muted">Snapshot: October 10, 2026.</p><div class="table-wrap"><table><thead><tr><th scope="col">Activity</th><th scope="col">Count</th><th scope="col">Scope</th></tr></thead><tbody>{metric_rows()}</tbody></table></div><p class="note">Line counts are cumulative changes, not unique code written by hand. Repeated edits and AI-assisted work are included. These metrics have different scopes and should not be added together.</p><p><a href="/activity.html#ai-periods">Numbers by year and AI use</a></p></section>
<section id="fit"><h2>Working together</h2>{fit_summary()}<p>I prefer agreement backed by reasoning and evidence. If disagreement remains, decide by majority.</p><p><a href="/working-together.html">More about the role and team I’m looking for</a></p></section></main>'''
    write('index.html', 'Ly Tran — Senior Engineer', 'TypeScript, products, architecture, and developer tools. Selected work and contribution history.', body)


def case_pages():
    for item in WORK:
        points = ''.join(f'<li>{e(point)}</li>' for point in item['points'])
        links = ''.join(f'<li><a href="{e(link["url"])}">{e(link["label"])}</a></li>' for link in item['links'])
        body = f'''<main id="main"><div class="page-intro"><a href="/#work">← Selected work</a><h1>{e(item['title'])}</h1><p class="lead">{e(item['summary'])}</p><p class="muted">{e(item['role'])}<br>{e(item['period'])}</p></div><section><h2>My work</h2><ul class="work-points">{points}</ul><p>{e(item['scope'])}</p><p class="muted">{' · '.join(e(t) for t in item['tags'])}</p></section><section><h2>Evidence</h2><p>Checked against private implementation history and relevant work records in October 2026. Source code and internal records remain private. Public product pages describe capabilities; individual contributions are based on the private records.</p><ul>{links}</ul><p><a href="/evidence.html#method">Verification method</a></p></section></main>'''
        write(f'work/{item["slug"]}.html', item['title']+' — Ly Tran', item['summary'], body)


def activity_page():
    gh, history, ts = (ACTIVITY[key] for key in ['github', 'product_history', 'typescript_line_changes'])
    assert sum(r['commits'] for r in history['repositories']) == history['unique_non_merge_commits']
    assert sum(r['added'] for r in ts['repositories']) == ts['added']
    assert sum(r['deleted'] for r in ts['repositories']) == ts['deleted']
    repos = ''.join(f'<tr><th scope="row">{e(r["label"])}</th><td class="number">{r["commits"]:,}</td><td>{e(r["snapshot_tip_date"])}</td></tr>' for r in history['repositories'])
    lines = ''.join(f'<tr><th scope="row">{e(r["label"])}</th><td class="number">{r["added"]:,}</td><td class="number">{r["deleted"]:,}</td></tr>' for r in ts['repositories'])
    body = f'''<main id="main"><div class="page-intro"><h1>Numbers</h1><p>Contribution activity, counted October 10, 2026. These numbers describe volume, not quality or business impact.</p></div>{ai_period_table()}<section><h2>All periods</h2><div class="table-wrap"><table><thead><tr><th scope="col">Activity</th><th scope="col">Count</th><th scope="col">Scope</th></tr></thead><tbody>{metric_rows()}</tbody></table></div></section>
<section><h2>PRs and reviews</h2><p>{e(gh['scope'])}</p><p>Opened PRs include the merged PRs. Reviews count different PRs, not review events or comments. Self-authored PRs and unsent drafts are excluded.</p><details><summary>Calculation and limits</summary><p>{e(gh['method'])}</p><p>{e(gh['limits'])}</p><p><a href="https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests">GitHub search definitions</a></p></details></section>
<section id="code"><h2>Product commits</h2><p>Non-merge commits in three local snapshots of default-branch history. Only commits attributed to the exact author names “lytc” or “Ly Tran” are counted.</p><div class="table-wrap"><table><thead><tr><th scope="col">Area</th><th scope="col">Commits</th><th scope="col">Snapshot tip</th></tr></thead><tbody>{repos}</tbody></table></div><details><summary>Calculation and limits</summary><p>{e(history['method'])}</p><p>{e(history['limits'])}</p><p>The local snapshots were not refreshed during this measurement.</p></details></section>
<section><h2>TypeScript line changes</h2><p>Added and removed lines in filtered TypeScript diffs from two product repositories. Includes implementation, tests, and configuration.</p><div class="table-wrap"><table><thead><tr><th scope="col">Area</th><th scope="col">Added</th><th scope="col">Removed</th></tr></thead><tbody>{lines}</tbody></table></div><p>These are cumulative changes, not current source LOC or unique lines written by hand. Repeated edits, formatting, imported code, and AI-assisted work can be included.</p><details><summary>Filtering and verification</summary><p>{e(ts['method'])}</p><p>{e(ts['limits'])}</p><p><a href="https://git-scm.com/docs/git-log">Git diff statistics</a></p></details></section>
<section><h2>Source data</h2><p>The PR counts cover more repositories than the commit counts. The TypeScript filter is narrower again. Private records remain private.</p><p><a href="/data/activity.json">Aggregate counts and definitions (JSON)</a> · <a href="/evidence.html">Evidence</a></p></section></main>'''
    write('activity.html', 'Numbers — Ly Tran', 'PR, review, commit and TypeScript line-change counts with dates and methods.', body)


def working_together_page():
    body = '''<main id="main"><div class="page-intro"><h1>Working together</h1><p class="lead">I’m looking for an engineering role focused on architecture, platforms, and better development workflows.</p><p>Based in Vietnam. Open to remote work or a role in Ho Chi Minh City. I’m not looking to relocate internationally.</p></div>
<section><h2>I may not be the right fit if…</h2><ul class="work-points"><li><strong>Meetings are central to everyday work.</strong> I’m looking for a nearly meeting-free way of collaborating.</li><li><strong>Technical decisions are imposed by rank.</strong> I expect different opinions to get a fair hearing and be supported by reasoning and evidence.</li><li><strong>The role is mainly people management.</strong> I want to stay on the engineering track, while contributing technical guidance and support for colleagues.</li></ul></section>
<section><h2>Where I do my best work</h2><ul class="work-points"><li><strong>Architecture and platforms.</strong> Shared services, reusable packages, and tools that help the whole team build software.</li><li><strong>AI and automation.</strong> Practical tools for developing and reviewing software with AI.</li><li><strong>Very few meetings.</strong> I see little need for meetings to exchange information. I prefer written communication and time to focus.</li><li><strong>Equal voice and shared responsibility.</strong> Everyone should be able to question a decision and be responsible for the result.</li></ul></section>
<section><h2>How I want the team to decide</h2><p>Seek agreement first. Explain different opinions with a convincing argument and evidence. If disagreement remains, decide by majority.</p></section>
<section><h2>Get in touch</h2><p>Send me a short description of the role, the problem you’re working on, and how your team works.</p><p><a href="mailto:prtran@gmail.com">prtran@gmail.com</a></p></section></main>'''
    write('working-together.html', 'Working together — Ly Tran', 'The engineering role and team I am looking for.', body)


def evidence_page():
    products = ''.join(f'<li><a href="{e(s["url"])}">{e(s["name"])}</a></li>' for s in EVIDENCE['public_product_sources'])
    upstream = ''.join(f'<li><a href="{e(pr["url"])}">{e(pr["repository"])} #{pr["number"]}</a> — {e(pr["title"])} ({pr["merged_at"][:4]})</li>' for pr in EVIDENCE['selected_upstream'])
    body = f'''<main id="main"><div class="page-intro"><h1>Evidence</h1><p>Public product links and how the contributions were checked.</p></div><section><h2>Product links</h2><ul>{products}</ul><p class="note">These pages describe the products, not individual authorship.</p></section><section id="method"><h2>Verification</h2><div id="private-work"><p>Contribution descriptions were checked against private Git history, selected changes, package manifests, and relevant work records in October 2026.</p><p>The site distinguishes work I started, work I contributed to, and team achievements. Company code, private messages, customer data, and operational figures are not published here.</p><p>Experience dates come from attributable contributions: March 2011 for Digication, February 2016 for TypeScript, and August 2016 for React. Senior Engineer is my current title.</p><p>Much of my recent implementation is AI-assisted. Counts and tool adoption do not establish improvements in productivity, cost, or defect rates.</p></div><p><a href="/activity.html">Activity counts and methods</a> · <a href="/data/evidence.json">Source register (JSON)</a></p></section><section><details><summary>Earlier upstream contributions</summary><ul>{upstream}</ul><p class="note">Selected historical examples. Author and merged state checked October 10, 2026.</p></details></section></main>'''
    write('evidence.html', 'Evidence — Ly Tran', 'Public product sources and verification of individual contributions.', body)


def misc():
    write('404.html', 'Page not found — Ly Tran', 'Return to the portfolio.', '<main id="main"><div class="page-intro"><h1>Page not found</h1><p><a href="/">Return to the portfolio</a></p></div></main>')
    urls = ['/', '/evidence.html', '/activity.html', '/working-together.html'] + [f'/work/{i["slug"]}.html' for i in WORK]
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>https://lytc.github.io{p}</loc><lastmod>2026-10-10</lastmod></url>\n' for p in urls)+'</urlset>\n')
    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://lytc.github.io/sitemap.xml\n')


if __name__ == '__main__':
    home()
    case_pages()
    activity_page()
    working_together_page()
    evidence_page()
    misc()
    print('Built 12 static pages.')
