#!/usr/bin/env python3
"""Build the portfolio's HTML pages from data/*.json.

Run from the site root:   python tools/build.py

The generated pages are ordinary, complete HTML (they work with no JavaScript
and no server). Edit the wording in data/*.json (journeys, packet steps, tips,
work, projects, certificates, tools) or the page text below, then run this again.
If you prefer to hand-edit the .html files instead, simply never run this script.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "data").glob("*.json")}

SITE = {
    "name": "Joseph S. Callos",
    "email": "callosjoseph818@gmail.com",
    "linkedin": "https://www.linkedin.com/in/joseph-callos-329b153b8",
    "facebook": "https://www.facebook.com/joseph.callos.8",
    "github": "https://github.com/otep808",
    "discord": "https://discordapp.com/users/1163857497963102219",
    "first_site": "https://otep808.github.io/portfolio/",
    "arcade": "https://otep808.github.io/portfolio/games.html",
}

ICONS = {
    "chat": "M21 11.5a8.5 8.5 0 0 1-8.5 8.5c-1.5 0-3-.4-4.2-1L3 20l1.2-5.3A8.5 8.5 0 1 1 21 11.5z",
    "phone": "M7 2h10a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1z M11 18h2",
    "router": "M3 14h18v6H3z M7 17h.01 M11 17h.01 M8 14l-2-4 M16 14l2-4 M12 14V8",
    "wifi": "M2.5 9a15 15 0 0 1 19 0 M5.5 12.5a10.5 10.5 0 0 1 13 0 M8.6 16a6 6 0 0 1 6.8 0 M12 19.5h.01",
    "globe": "M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18z M3 12h18 M12 3c2.5 2.6 3.9 5.7 3.9 9S14.5 18.4 12 21c-2.5-2.6-3.9-5.7-3.9-9S9.5 5.6 12 3z",
    "server": "M3 4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z M3 16a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z M7 6h.01 M7 18h.01",
    "laptop": "M4 5h16v10H4z M2 19h20",
    "search": "M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16z M21 21l-4.3-4.3",
    "card": "M2 5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z M2 10h20",
    "bank": "M3 21h18 M4 18h16 M6 18v-7 M10 18v-7 M14 18v-7 M18 18v-7 M12 3l9 5H3z",
    "lock": "M5 11h14a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z M8 11V7a4 4 0 0 1 8 0v4",
    "check": "M20 6L9 17l-5-5",
    "folder": "M3 5a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
    "cloud": "M17.5 18a4.5 4.5 0 0 0 .9-8.8A7 7 0 0 0 4.7 11 3.8 3.8 0 0 0 6 18z",
    "upload": "M12 15V3 M7 8l5-5 5 5 M4 21h16",
    "download": "M12 3v12 M7 10l5 5 5-5 M4 21h16",
    "shield": "M12 22s8-3.6 8-10V5l-8-3-8 3v7c0 6.4 8 10 8 10z M9 11.5l2 2 4-4.5",
    "alert": "M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z M12 9v4 M12 17h.01",
    "bulb": "M9 18h6 M10 21h4 M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z",
    "arrow-right": "M5 12h14 M13 6l6 6-6 6",
    "arrow-left": "M19 12H5 M11 6l-6 6 6 6",
    "refresh": "M3 12a9 9 0 0 1 15.5-6.2L21 8 M21 3v5h-5 M21 12a9 9 0 0 1-15.5 6.2L3 16 M3 21v-5h5",
    "play": "M7 4l13 8-13 8z",
    "pause": "M8 4v16 M16 4v16",
    "sun": "M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M12 2v2 M12 20v2 M4.9 4.9l1.4 1.4 M17.7 17.7l1.4 1.4 M2 12h2 M20 12h2 M4.9 19.1l1.4-1.4 M17.7 6.3l1.4-1.4",
    "moon": "M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z",
    "menu": "M4 7h16 M4 12h16 M4 17h16",
    "x": "M6 6l12 12 M18 6L6 18",
    "mail": "M3 5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z M3 6l9 7 9-7",
    "file": "M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z M14 3v5h5 M9 13h6 M9 17h6",
    "copy": "M9 9h11v11H9z M5 15V5a1 1 0 0 1 1-1h10",
}

NAV = [("index", "Home"), ("journeys", "Journeys"), ("projects", "My work"), ("skills", "Skills"),
       ("learn", "Learn"), ("about", "About"), ("contact", "Contact")]

e = html.escape


def sprite():
    s = "".join('<symbol id="i-%s" viewBox="0 0 24 24"><path d="%s"/></symbol>' % (k, v) for k, v in ICONS.items())
    return '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">%s</svg>' % s


def ico(name, cls="ico"):
    return '<svg class="%s" aria-hidden="true"><use href="#i-%s"/></svg>' % (cls, name)


def plain(s):
    """Typographic tidy: the data keeps ' · ' separators; show commas instead."""
    return s.replace(" · ", ", ")


# ---------------------------------------------------------------- layout
def page(slug, title, desc, body, extra_head=""):
    nav = "".join('<a href="%s.html"%s>%s</a>' % (s, ' aria-current="page"' if s == slug else "", l) for s, l in NAV)
    drawer = "".join('<a href="%s.html"%s>%s</a>' % (s, ' aria-current="page"' if s == slug else "", l) for s, l in NAV)
    full = ("Joseph S. Callos | How it works around you" if slug == "index" else "%s | Joseph S. Callos" % title)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(full)s</title>
<meta name="description" content="%(desc)s">
<meta name="color-scheme" content="light dark">
<meta name="theme-color" content="#0f1a2a">
<meta property="og:title" content="%(full)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&amp;family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
<script>(function(){var d=document.documentElement;d.classList.add('js');try{var t=localStorage.getItem('otep2_theme');if(t)d.setAttribute('data-theme',t)}catch(e){}})();</script>
%(extra_head)s</head>
<body>
%(sprite)s
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="brand" href="index.html" aria-label="Joseph S. Callos, home">
      <span class="brand-mark" aria-hidden="true">J</span>
      <span class="brand-text"><b>Joseph S. Callos</b><span>How it works around you</span></span>
    </a>
    <nav class="nav" aria-label="Main">%(nav)s</nav>
    <div class="head-tools">
      <span class="clock" id="clock" title="Philippine time" aria-hidden="true"></span>
      <button class="icon-btn theme-btn js-only" type="button" aria-label="Switch colour theme">%(sun)s%(moon)s</button>
      <button class="icon-btn menu-btn js-only" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">%(menu)s%(x)s</button>
    </div>
  </div>
  <nav class="drawer" id="drawer" aria-label="Mobile"><div class="wrap">%(drawer)s</div></nav>
</header>
<main id="main">
%(body)s
</main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div>
      <h2>Joseph S. Callos</h2>
      <p>BS Information Technology student at Pamantasan ng Lungsod ng Valenzuela. I explain everyday technology, then show how I make it safer, faster and more reliable.</p>
      <p class="small">Plain HTML, CSS and JavaScript. It works without JavaScript, and respects reduced-motion settings.</p>
    </div>
    <div><h2>Pages</h2><ul>%(foot_nav)s</ul></div>
    <div><h2>Find me</h2><ul>
      <li><a href="mailto:%(email)s">Email</a></li>
      <li><a href="%(linkedin)s" target="_blank" rel="noopener">LinkedIn</a></li>
      <li><a href="%(github)s" target="_blank" rel="noopener">GitHub</a></li>
      <li><a href="%(arcade)s" target="_blank" rel="noopener">Game arcade (first portfolio)</a></li>
    </ul></div>
  </div>
</footer>
%(gsap)s<script src="javascript/main.js" defer></script>
</body>
</html>
""" % dict(full=e(full), desc=e(desc), extra_head=extra_head, sprite=sprite(), nav=nav, drawer=drawer,
           gsap=('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>\n'
                 '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>\n') if slug == "projects" else "",
           sun=ico("sun", "ico sun"), moon=ico("moon", "ico moon"), menu=ico("menu", "ico open"), x=ico("x", "ico close"),
           body=body, foot_nav="".join('<li><a href="%s.html">%s</a></li>' % (s, l) for s, l in NAV), **SITE)


def page_head(title, lede, crumb=None):
    return """<div class="page-head"><div class="wrap">
  <h1>%s</h1>
  <p>%s</p>
</div></div>""" % (title, lede)


def tech_toggle(label="Detail level"):
    return ('<div class="seg js-only" role="group" aria-label="%s">'
            '<button type="button" data-tech="off" aria-pressed="true">Plain language</button>'
            '<button type="button" data-tech="on" aria-pressed="false">Technical details</button></div>') % label


def cta(title="Need a hand with the tech around you?", text="I am open to internships, collaborations and IT support questions, especially where explaining things clearly matters as much as fixing them."):
    return """<div class="section"><div class="wrap"><div class="cta">
  <h2>%s</h2>
  <p>%s</p>
  <div class="hero-actions" style="margin:0">
    <a class="btn btn-primary" href="contact.html">Send me a message</a>
    <a class="btn btn-line" href="files/resume.pdf" target="_blank" rel="noopener">Read my résumé (PDF)</a>
  </div>
</div></div></div>""" % (title, text)


# ---------------------------------------------------------------- components
def route(nodes, color, numbered=False, i=0, all_done=False):
    n = len(nodes)
    out = ['<ol class="route" style="--n:%d;--i:%d;--line:var(--c-%s)">' % (n, (n - 1) if all_done else i, color)]
    for k, nd in enumerate(nodes):
        name = nd["name"]
        sub = nd["sub"]
        cls = "station" + (" done" if all_done else (" now" if k == 0 else ""))
        dot = ('<span class="st-dot num">%d</span>' % (k + 1)) if numbered else '<span class="st-dot">%s</span>' % ico(nd.get("icon", "check"))
        out.append('<li class="%s">%s<span class="st-txt"><b>%s</b><small>%s</small></span></li>' % (cls, dot, e(name), e(sub)))
    out.append("</ol>")
    return "".join(out)


def packet_widget(autorun=False, heading="h2"):
    scns = []
    for k, s in enumerate(DATA["packet"]):
        steps = "".join('<li><strong>%s</strong> <span class="plain">%s</span> <span class="tech">%s</span></li>' % (e(x["title"]), e(x["plain"]), e(x["tech"])) for x in s["steps"])
        scns.append('<section class="packet-scn" id="pk-%s" data-label="%s" data-icon="%s" data-color="%s" data-route="%s" aria-label="%s">'
                    '<h3>%s</h3>%s<ol class="steps-list">%s</ol></section>' % (
                        s["id"], e(s["label"]), s["icon"], s["color"], e(s["route"]), e(s["label"]), e(s["label"]), route(s["nodes"], s["color"]), steps))
    return """<div class="packet" data-packet%s>
  <div class="packet-top">
    <div><%s>Follow the packet</%s>
    <p>Everything you send is cut into small pieces called packets. Pick something you do every day and ride one.</p></div>
    %s
  </div>
  <div class="tabs js-only" role="tablist" aria-label="What are you sending?"></div>
  %s
  <div class="step-card js-only" aria-live="polite">
    <div class="step-meta"><span class="step-count"></span><span class="step-route"></span></div>
    <h4></h4><p class="plain"></p><p class="tech"></p>
  </div>
  <div class="controls js-only">
    <button class="icon-btn" type="button" data-prev aria-label="Previous step">%s</button>
    <button class="btn btn-primary" type="button" data-play aria-pressed="false">%s<span>Play journey</span></button>
    <button class="icon-btn" type="button" data-next aria-label="Next step">%s</button>
    <div class="bar" aria-hidden="true"><i></i></div>
  </div>
</div>""" % (" data-autorun" if autorun else "", heading, heading, tech_toggle(), "".join(scns), ico("arrow-left"), ico("play"), ico("arrow-right"))


def picks(base=""):
    out = ['<div class="picker" role="tablist" aria-label="Everyday journeys">']
    for j in DATA["journeys"]:
        out.append('<a class="pick" role="tab" aria-selected="false" href="%s#journey-%s" style="--line:var(--c-%s)"><span class="bullet">%s</span>'
                   '<span><b>%s</b><span class="s">%s</span><span class="t">About %d min</span></span></a>' % (
                       base, j["id"], j["color"], ico(j["icon"]), e(j["title"]), e(j["short"]), j["minutes"]))
    out.append("</div>")
    return "".join(out)


def journey(j):
    wrong = "".join("<li>%s<span>%s</span></li>" % (ico("alert"), e(w)) for w in j["wrong"])
    return """<article class="journey" id="journey-%(id)s" style="--line:var(--c-%(color)s)" aria-labelledby="jt-%(id)s">
  <div class="journey-in">
    <div class="j-top"><h3 id="jt-%(id)s">%(title)s</h3><span class="j-count js-only" aria-live="polite"></span></div>
    <div class="segbar js-only" role="group" aria-label="Steps"></div>
    <section class="jstep" data-name="The situation"><h4>The situation</h4><p class="big">%(situation)s</p>%(route)s</section>
    <section class="jstep" data-name="In simple terms"><h4>In simple terms</h4><p class="body">%(simple)s</p><p class="tech-note"><b>For the curious:</b> %(tech)s</p></section>
    <section class="jstep" data-name="What can go wrong"><h4>What can go wrong</h4><ul>%(wrong)s</ul></section>
    <section class="jstep" data-name="How I help"><h4>How I help</h4><div class="help-box"><p style="margin:0">%(help)s</p></div></section>
    <section class="jstep" data-name="Try this today"><h4>Try this today</h4><div class="callout"><b>One small thing to do</b>%(tryit)s</div></section>
    <div class="j-nav js-only">
      <button class="btn btn-line" type="button" data-back>%(left)s<span>Back</span></button>
      <button class="btn btn-primary" type="button" data-fwd><span>Next</span>%(right)s</button>
    </div>
  </div>
</article>""" % dict(j, title=e(j["title"]), situation=e(j["situation"]), simple=e(j["simple"]), tech=e(j["tech"]), wrong=wrong,
                     help=e(j["help"]), tryit=e(j["tryit"]), route=route(j["flow"], j["color"], numbered=True, all_done=True),
                     left=ico("arrow-left"), right=ico("arrow-right"))


def work_card(w):
    tags = "".join("<li>%s</li>" % e(t) for t in w["tags"])
    return """<article class="work-card" style="--line:var(--c-%s)">
  <div class="work-top"><span class="bullet" aria-hidden="true"></span><h3>%s</h3></div>
  <div class="work-top" style="padding-top:12px"><ul class="tags">%s</ul></div>
  <div class="work-body">
    <div><h4>The situation</h4><p>%s</p></div>
    <div><h4>What I built or fixed</h4><p>%s</p></div>
    <div><h4>Why it mattered</h4><p>%s</p><span class="win">%s%s</span></div>
  </div>
  <details class="more"><summary>Show technical details</summary><div class="inner"><p>%s</p></div></details>
</article>""" % (w["color"], e(w["title"]), tags, e(w["situation"]), e(w["built"]), e(w["result"]), ico("check"), e(w["highlight"]), w["tech"])


def card(p, cert=False):
    kind = e(plain(p["kind"]))
    if cert:
        if p["image"]:
            thumb = '<a href="%s" target="_blank" rel="noopener" aria-label="Open certificate: %s"><img src="%s" alt="Certificate: %s" loading="lazy"></a>' % (p["file"], e(p["title"]), p["image"], e(p["title"]))
        else:
            thumb = '<div class="pdf-thumb" aria-hidden="true">%s</div>' % ico("file")
        link = '<a href="%s" target="_blank" rel="noopener">View certificate%s</a>' % (p["file"], " (PDF)" if p["file"].endswith(".pdf") else "")
        return '<article class="card cert">%s<div class="card-body"><span class="kind">%s</span><h3>%s</h3><p>%s</p>%s</div></article>' % (thumb, kind, e(p["title"]), e(p["text"]), link)
    return ('<article class="poster" data-tags="%s"><div class="poster-img"><img src="%s" alt="%s" loading="lazy"></div><div class="card-body"><span class="kind">%s</span><h3>%s</h3><p>%s</p>'
            '<a href="%s" target="_blank" rel="noopener">%s</a></div></article>') % (
        " ".join(p["tags"]), p["image"], e(p["alt"]), kind, e(p["title"]), e(p["text"]), e(p["link"]), e(p["label"]))


def reel(heading="h2", here=False):
    return """<div class="reel">
  <div><%(h)s>Watch the work in action</%(h)s>
  <p class="muted" style="margin-top:12px">A 55-second reel of my projects: EkSpyRy, The Future Times, CineReel and more. It is the quickest way to see what I build before you read the details.</p>
  <p class="small muted">%(note)s</p></div>
  <video controls preload="none" poster="images/demo-reel-poster.jpg" aria-label="Demo reel of Joseph's projects, 55 seconds">
    <source src="files/demo-reel.mp4" type="video/mp4">
    Your browser cannot play this video. <a href="files/demo-reel.mp4">Download the demo reel (MP4)</a>.
  </video>
</div>""" % dict(h=heading, note=("Captions are not available yet. All 17 projects are listed below." if here else 'Captions are not available yet. All 17 projects are on the <a href="projects.html#archive">My work</a> page.'))


def tips_panel():
    items = "".join('<li><h3>%s</h3><p class="why">%s</p><p class="act">%s</p></li>' % (e(t["title"]), e(t["why"]), e(t["action"])) for t in DATA["tips"])
    return """<div data-tips><div class="tip-panel">
  <ol class="tip-list tip-static" style="padding-left:1.2em;margin:0">%s</ol>
</div></div>""" % items


# ---------------------------------------------------------------- pages
def build_index():
    work = "".join(
        '<li><a class="pick" style="--line:var(--c-%s)" href="projects.html#%s"><span class="bullet" aria-hidden="true">%s</span><span><b>%s</b><span class="s">%s</span><span class="t">%s</span></span></a></li>' % (
            w["color"], w["id"], ico("check"), e(w["title"]), e(w["situation"].split(". ")[0] + "."), e(w["highlight"])) for w in DATA["work"])
    learn = [
        ("globe", "How everyday things travel", "A message, a web page, a payment and a file all move as small packets. You will see each step, with no jargon."),
        ("alert", "What can go wrong", "Slow Wi-Fi, lost files, copycat checkout pages. You will learn to spot the cause in minutes."),
        ("bulb", "One thing to try today", "Every journey ends with a small action, such as turning on updates or backing up a folder."),
    ]
    learn_html = "".join('<li><span class="bullet" aria-hidden="true" style="--line:var(--ink)">%s</span><div><h3>%s</h3><p class="muted" style="margin:6px 0 0">%s</p></div></li>' % (ico(i), t, d) for i, t, d in learn)
    body = """
<section class="hero"><div class="wrap hero-grid">
  <div>
    <h1>Let me help you understand the technology you already use.</h1>
    <p class="lede">And show you how I make it safer, faster and more reliable.</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="journeys.html">Explore everyday tech</a>
      <a class="btn btn-line" href="projects.html">See my work</a>
      <a class="btn btn-line" href="learn.html">Get practical tips</a>
    </div>
    <p class="hero-note"><img src="images/joseph-profile.jpg" alt="Joseph S. Callos" width="56" height="56"><span>I am Joseph, a BSIT student at PLV in Valenzuela City. You do not need to know anything about IT to follow along.</span></p>
  </div>
  %(packet)s
</div></section>

<section class="section tint" aria-labelledby="learn-h"><div class="wrap">
  <div class="section-head"><h2 id="learn-h">What you will learn here</h2></div>
  <ul class="can" style="list-style:none;padding:0;margin:0;grid-template-columns:repeat(auto-fit,minmax(min(100%%,280px),1fr))">%(learn)s</ul>
</div></section>
<style>.can li{display:flex;gap:16px;align-items:flex-start;border-top:3px solid var(--ink);padding-top:16px}.can li h3{font-size:1.15rem}</style>

<section class="section" id="journeys"><div class="wrap">
  <div class="section-head"><h2>Start with a moment you recognise</h2><p>Six short journeys. Each one takes a minute or two and ends with something you can do today.</p></div>
  %(picks)s
  <p style="margin-top:20px"><a class="btn btn-line" href="journeys.html">Open all journeys</a></p>
</div></section>

<section class="section tint" id="work"><div class="wrap">
  <div class="section-head"><h2>My work, translated</h2><p>Each project starts with the everyday problem it solves. Recruiters can open the technical details on every one.</p></div>
  <ul class="picker" style="list-style:none;padding:0;margin:0">%(work)s</ul>
  <p style="margin-top:20px"><a class="btn btn-line" href="projects.html">See all my work</a></p>
</div></section>

<section class="section" id="reel"><div class="wrap">%(reel)s</div></section>

<section class="section tint" id="tips"><div class="wrap">
  %(tips)s
  <p style="margin-top:18px"><a class="btn btn-line" href="learn.html">See all the tips</a></p>
</div></section>
%(cta)s
""" % dict(packet=packet_widget(autorun=True), learn=learn_html, picks=picks("journeys.html"), work=work, reel=reel(), tips=tips_panel(), cta=cta())
    return page("index", "Home", "Joseph S. Callos, BSIT student at PLV. A portfolio that explains the technology you already use and shows how I make it safer, faster and more reliable.", body)


def build_journeys():
    body = page_head("Everyday tech journeys", "Choose a situation you recognise. You get a simple explanation, what can go wrong, how I help, and one thing to try today.") + """
<section class="section" data-journeys><div class="wrap">
  <div class="section-head" style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;justify-content:space-between;max-width:none">
    <h2 style="font-size:1.4rem">Pick a journey</h2>%s
  </div>
  %s
  <div style="margin-top:24px">%s</div>
</div></section>
%s""" % (tech_toggle(), picks(), "".join(journey(j) for j in DATA["journeys"]), cta("Want this explained for your home or office?", "I can look at your Wi-Fi, backups or accounts and tell you what to fix first, in plain language."))
    return page("journeys", "Everyday tech journeys", "Six short interactive journeys: sending a message, opening a website, slow Wi-Fi, online payments, lost files and suspicious messages.", body)


def build_projects():
    work = "".join('<div id="%s" style="scroll-margin-top:90px">%s</div>' % (w["id"], work_card(w)) for w in DATA["work"])
    chips = [("all", "All"), ("python", "Python"), ("web", "Web"), ("design", "Design and Figma"), ("research", "Research"), ("media", "Media"), ("group", "Group work"), ("solo", "Solo work")]
    chip_html = "".join('<button type="button" class="chip" data-filter="%s" aria-pressed="%s">%s</button>' % (k, "true" if k == "all" else "false", l) for k, l in chips)
    cards = "".join(card(p) for p in DATA["projects"])
    body = page_head("My work, translated", "Every project starts with the everyday situation it solves, then what I built or fixed, why it mattered and the result. Open the technical details if you want the stack.") + """
<section class="section"><div class="wrap">
  <div class="section-head" style="display:flex;gap:16px;flex-wrap:wrap;align-items:center;justify-content:space-between;max-width:none"><h2>Recent systems</h2>%s</div>
  <div class="work">%s</div>
</div></section>
<section class="section tint" id="reel"><div class="wrap">%s</div></section>
<section class="section" id="archive" data-filter-wrap><div class="wrap">
  <div class="section-head"><h2>The full archive: 17 projects</h2><p>From my first portfolio: coursework and group projects at PLV, each in one plain sentence. Keep scrolling: the posters pin in place and slide sideways &mdash; hover one to bring it forward.</p></div>
  <div class="filters js-only" role="group" aria-label="Filter projects">%s</div>
  <p class="count" data-count aria-live="polite">Showing 17 of 17 projects</p>
</div>
<section id="posters" class="posters" aria-label="All 17 projects as posters. Scroll to move through them.">
  <div class="posters-track">%s</div>
</section>
<div class="wrap">
  <p style="margin-top:28px" class="muted">Looking for the games? My first portfolio has a 17-game arcade with leaderboards: <a href="%s" target="_blank" rel="noopener">play the arcade</a>.</p>
</div></section>
%s""" % (tech_toggle(), work, reel(here=True), chip_html, cards, SITE["arcade"], cta("Have a project in mind?", "Tell me what you are trying to fix or build. I will reply within a day."))
    return page("projects", "My work", "Three recent systems and 17 projects from PLV, each explained in plain language first, with technical details for recruiters.", body)


def build_skills():
    can = [
        ("wifi", "Networks and Wi-Fi", "I set up and troubleshoot simulated enterprise networks in Cisco Packet Tracer: routers, switches and diagnosing why a connection is slow."),
        ("website", "Websites and web apps", "HTML5, CSS3, JavaScript and PHP. I build pages that are quick to load, easy to read and work on ordinary phones."),
        ("files", "Databases and records", "SQL, MySQL and SQLite. I design systems that keep a reliable record, like orders, tickets and stock levels."),
        ("message", "Design and prototypes", "Figma, Canva and Photoshop. I turn an idea into a clickable prototype people can try before anything is built."),
        ("payment", "Python and automation", "Desktop tools, data structures and small automations, from a food-expiry tracker to a maths board game."),
        ("scam", "Safer habits", "Seminars and courses in cybersecurity and critical infrastructure protection. I teach the pause-and-verify habit."),
    ]
    can_html = "".join('<article style="--line:var(--c-%s)"><h3>%s</h3><p>%s</p></article>' % (c, t, d) for c, t, d in [(a[0], a[1], a[2]) if False else (a[0], a[1], a[2]) for a in can])
    tools = "".join('<li><img src="%s" alt="" width="26" height="26" loading="lazy">%s</li>' % (t["image"], e(t["name"])) for t in DATA["tools"])
    certs = "".join(card(c, cert=True) for c in DATA["certs"])
    body = page_head("Skills, in plain words", "What I can do for you, the tools I use, and the 11 certificates and seminars behind them.") + """
<section class="section"><div class="wrap">
  <div class="section-head"><h2>What I can help with</h2></div>
  <div class="can">%s</div>
</div></section>
<section class="section tint"><div class="wrap">
  <div class="section-head"><h2>Tools I work with</h2></div>
  <ul class="tool-row">%s</ul>
</div></section>
<section class="section" id="credentials"><div class="wrap">
  <div class="section-head"><h2>Certificates and seminars</h2><p>Open any certificate to see it in full.</p></div>
  <div class="grid">%s</div>
</div></section>
%s""" % (can_html, tools, certs, cta())
    return page("skills", "Skills", "Skills, tools, certificates and seminars of Joseph S. Callos: networking, web development, databases, design, Python and cybersecurity.", body)


def build_learn():
    items = "".join(
        '<li><label class="check"><input type="checkbox" value="%d"><div><b>%s</b><span>%s</span></div></label></li>' % (i, e(t["title"]), e(t["action"])) for i, t in enumerate(DATA["tips"]))
    body = page_head("Learn one thing", "Short, practical tips. Each one is a sentence of explanation and one clear action. Do one today, tick it off, come back for another.") + """
<section class="section"><div class="wrap">
  %s
</div></section>
<section class="section tint"><div class="wrap">
  <div class="section-head"><h2>Your checklist</h2><p>Ticks are saved in this browser only. Nothing is sent anywhere.</p></div>
  <p class="progress-note js-only" data-progress></p>
  <ul class="checklist" data-checklist>%s</ul>
</div></section>
%s""" % (tips_panel(), items, cta("Stuck on one of these?", "Send me a message and I will walk you through it."))
    return page("learn", "Learn one thing", "Practical everyday tech tips: turn on updates, use a password manager, enable two-factor authentication, back up your files.", body)


def build_about():
    body = page_head("Meet Joseph", "A second-year BSIT student from Valenzuela who builds things from scratch and explains technical ideas by comparing them to things you already know.") + """
<section class="section"><div class="wrap about-grid">
  <figure class="portrait" style="margin:0"><img src="images/joseph-photo.jpg" alt="Joseph S. Callos outdoors" loading="lazy"></figure>
  <div>
    <h2>Motivated by a simple motto: time is gold</h2>
    <p style="margin-top:14px">Every second spent on something should bring value, to yourself or to others. I build web systems that are clean, design interfaces that feel obvious, and solve problems one step at a time. I work well alone or in a team, and I like practical teaching: show it, then let the person try.</p>
    <p>Outside class I play acoustic guitar (rock, country and folk, with a soft spot for The Beatles and Jim Croce), play badminton, collect building blocks, and look after three cats and two dogs.</p>
    <dl class="facts">
      <div><dt>Full name</dt><dd>Joseph S. Callos</dd></div>
      <div><dt>Program</dt><dd>BS Information Technology</dd></div>
      <div><dt>School</dt><dd>Pamantasan ng Lungsod ng Valenzuela</dd></div>
      <div><dt>Year level</dt><dd>2nd year</dd></div>
      <div><dt>Based in</dt><dd>Valenzuela City, Philippines</dd></div>
      <div><dt>Open to</dt><dd>Internships and collaborations</dd></div>
    </dl>
  </div>
</div></section>
<section class="section tint"><div class="wrap about-grid" style="grid-template-columns:none">
  <div class="section-head"><h2>Where I have been</h2></div>
  <ol class="timeline" style="max-width:62ch">
    <li><b>2026: Cloud computing seminar</b><span>Seminars and Colloquia at PLV.</span></li>
    <li><b>2024 to now: BS Information Technology</b><span>Pamantasan ng Lungsod ng Valenzuela. Web systems, networking, databases, data structures and multimedia.</span></li>
    <li><b>2023: Senior high school graduate</b><span>ICT and TVL track. First certificates in SQL, networking and HTML with CSS.</span></li>
  </ol>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2>How I work</h2></div>
  <div class="values">
    <article class="can" style="display:block"><div style="--line:var(--c-message)"><h3>Collaboration</h3><p class="muted" style="margin:6px 0 0">I take on the technical build and the documentation in group projects, and I settle disagreements in open discussion.</p></div></article>
    <article class="can" style="display:block"><div style="--line:var(--c-website)"><h3>Clarity</h3><p class="muted" style="margin:6px 0 0">I explain technical ideas with something you already know, so you can decide for yourself.</p></div></article>
    <article class="can" style="display:block"><div style="--line:var(--c-wifi)"><h3>Creativity</h3><p class="muted" style="margin:6px 0 0">My best fixes come from improvising, at 3 am if needed, with no Stack Overflow in sight.</p></div></article>
  </div>
</div></section>
%s""" % cta()
    return page("about", "About", "About Joseph S. Callos: BSIT student at PLV in Valenzuela City, his background, interests and how he works.", body)


def build_contact():
    body = page_head("Contact", "Collaboration, a job or internship, or help with technology. Pick what fits, write a few lines, and I will reply within 24 hours.") + """
<section class="section"><div class="wrap contact-grid">
  <div>
    <form data-contact data-email="%(email)s" action="mailto:%(email)s" method="post" enctype="text/plain" novalidate>
      <fieldset class="ask"><legend>What is this about?</legend>
        <div class="ask-opts">
          <label><input type="radio" name="kind" value="Collaboration" checked> Collaboration</label>
          <label><input type="radio" name="kind" value="Job or internship"> Job or internship</label>
          <label><input type="radio" name="kind" value="IT support"> IT support</label>
        </div>
      </fieldset>
      <div class="field"><label for="c-name">Your name</label><input type="text" id="c-name" name="name" autocomplete="name" required><span class="err" role="alert">Enter your name so I know who to reply to.</span></div>
      <div class="field"><label for="c-email">Your email</label><input type="email" id="c-email" name="email" autocomplete="email" required><span class="err" role="alert">Enter a valid email address, like name@example.com.</span></div>
      <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" maxlength="1000" required></textarea><span class="err" role="alert">Write at least 10 characters so I can understand what you need.</span></div>
      <div class="form-actions">
        <button class="btn btn-primary" type="submit">Open email draft</button>
        <button class="btn btn-line js-only" type="button" data-copy="%(email)s">%(copy)s<span>Copy my email</span></button>
      </div>
      <p class="small muted" style="margin-top:14px">This opens a draft in your email app. Nothing is stored on this site.</p>
    </form>
  </div>
  <div>
    <h2 style="font-size:1.4rem;margin-bottom:14px">Or reach me directly</h2>
    <ul class="contact-list">
      <li><a href="mailto:%(email)s"><b>Email</b><span>%(email)s</span></a></li>
      <li><a href="%(linkedin)s" target="_blank" rel="noopener"><b>LinkedIn</b><span>linkedin.com/in/joseph-callos-329b153b8</span></a></li>
      <li><a href="%(github)s" target="_blank" rel="noopener"><b>GitHub</b><span>github.com/otep808</span></a></li>
      <li><a href="%(facebook)s" target="_blank" rel="noopener"><b>Facebook</b><span>facebook.com/joseph.callos.8</span></a></li>
      <li><a href="%(discord)s" target="_blank" rel="noopener"><b>Discord</b><span>Otep Codes</span></a></li>
      <li><a href="files/resume.pdf" target="_blank" rel="noopener"><b>Résumé (PDF)</b><span>Education, projects, certificates and references</span></a></li>
    </ul>
    <p class="small muted" style="margin-top:16px">Based in Valenzuela City, Metro Manila. Afternoons and evenings (Philippine time) work best. Preferred contact: email or Facebook.</p>
  </div>
</div></section>
""" % dict(SITE, copy=ico("copy"))
    return page("contact", "Contact", "Contact Joseph S. Callos for collaboration, internships or IT support questions. Replies within 24 hours.", body)


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#0f1a2a"/>'
           '<text x="32" y="45" text-anchor="middle" font-family="Arial,sans-serif" font-weight="800" font-size="38" fill="#fff">J</text>'
           '<circle cx="51" cy="51" r="8" fill="#ff5a1f" stroke="#0f1a2a" stroke-width="3"/></svg>')


def main():
    (ROOT / "images").mkdir(exist_ok=True)
    (ROOT / "images" / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    pages = {"index": build_index, "journeys": build_journeys, "projects": build_projects, "skills": build_skills,
             "learn": build_learn, "about": build_about, "contact": build_contact}
    for name, fn in pages.items():
        (ROOT / (name + ".html")).write_text(fn(), encoding="utf-8")
        print("  built %s.html" % name)


if __name__ == "__main__":
    main()
