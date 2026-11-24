from html import escape

ARTICLES = [
  ('before-you-increase-the-budget','Acquisition','Before you increase the budget, inspect the journey.','journey'),
  ('a-clear-brief','Leadership','A clear brief is a leadership decision.','brief'),
  ('ai-and-judgment','AI and judgment','Where AI improves marketing, and where judgment matters.','ai'),
]

VISUALS = {
    'journey': ('thinking-acquisition.webp', 'Illustrated path from search intent through campaign creative, a landing page and form to a human handoff', 1786, 881),
    'brief': ('thinking-brief-illustration.webp', 'A blank brief connecting the objective, audience, evidence and approval', 1536, 1024),
    'ai': ('thinking-ai-judgment.webp', 'Source material passes through AI assistance to a human verification and approval decision', 1740, 904),
}

def visual(kind):
    file, alt, width, height = VISUALS[kind]
    return f'<div class="decision-image"><img src="/assets/{file}" alt="{escape(alt)}" width="{width}" height="{height}" loading="lazy" decoding="async"></div>'

def thinking_cards():
    return ''.join(f'<a class="decision-card" href="/thinking/{slug}/">{visual(kind)}<div class="decision-meta"><span>{escape(cat)}</span><h3>{escape(title)}</h3><strong>Read the note <span aria-hidden="true">↗</span></strong></div></a>' for slug,cat,title,kind in ARTICLES)
