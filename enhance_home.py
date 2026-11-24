from pathlib import Path
from PIL import Image
from html import escape

root = Path(__file__).parent
path = root / 'homepage.html'
html = path.read_text()

chapters = [
    dict(name='Minimalance', kind='BRAND LAUNCH', deck='Architect and designer feedback shaped the positioning, sales training and launch of a furniture brand.', proof='₹5 crore', detail='first-year revenue', slug='minimalance', media=[('minimalance-launch.webp','Minimalance furniture launch space','Launch / environment'),('catalogue-leman.webp','Leman chair from the Minimalance catalogue','Product / catalogue')], tone='#1c1b16'),
    dict(name='Incuse Digital', kind='COMMERCIAL ANALYTICS', deck='SQL revealed which industrial buyers placed orders and informed a new focus on maintenance teams.', proof='20% → 26%', detail='qualified leads that became orders during the pilot', slug='incuse', media=[('incuse-logo-drive.png','Incuse Digital logo and brand material','Brand / system'),('incuse-gisec-exhibition.png','Incuse GISEC exhibition campaign','Campaign / event')], tone='#181a1b'),
    dict(name='REMIC', kind='ACQUISITION + CAMPAIGN', deck='Audience research, campaign creative, Search and Performance Max, then the conversion path.', proof='2,260', detail='tracked conversions at $35 CPA', slug='remic', media=[('remic-pmax.jpg','REMIC paid acquisition campaign material','Paid acquisition / Performance Max'),('remic-course-ad.webp','REMIC Mortgage Agent course ad','Course acquisition / paid')], tone='#111410'),
    dict(name='Xipster', kind='B2B SAAS + DEMAND', deck='Search, paid media, email and social supported demand generation for a B2B payments product.', proof='+28%', detail='B2B lead generation', slug='xipster', media=[('xipster-bull-campaign.png','Xipster campaign creative','Product / campaign'),('xipster-get-paid-campaign.png','Xipster Get Paid campaign creative','Payments / message')], tone='#152021'),
    dict(name='Camfire Media', kind='PORTFOLIO LEADERSHIP', deck='Portfolio strategy and campaign delivery across eight brands, a seven-person team and a C$2.6M managed marketing budget.', proof='$7.2M', detail='pipeline influenced across the client portfolio', slug='camfire', tone='#171917'),
    dict(name='Nett Technologies', kind='INDUSTRIAL B2B + CRM', deck='CRM evaluation and a proposed lead-management path from inquiry through post-sale follow-up.', proof='CRM', detail='evaluation and lead-qualification deliverables', slug='nett-technologies', media=[('nett-lead-funnel.png','Nett Technologies proposed lead-management funnel','Lead flow / proposal'),('nett-brand-banner.gif','Nett Technologies brand banner','Industrial / brand context')], tone='#142029'),
    dict(name='Bhatt Bros × ALEA', kind='B2B PARTNERSHIP', deck='Product and exhibition communications introduced the Indo-Italian textile machinery partnership.', proof='39', detail='client inquiries from nine countries', slug='bhatt-bros-alea', media=[('bhatt-exhibition-4.webp','Bhatt Bros textile machinery exhibition','Exhibition / presence'),('bhatt-exhibition-1.webp','Bhatt Bros machinery display','Product / floor')], tone='#1a1c17'),
    dict(name='SoalTech', kind='HEALTH-TECH + PRODUCT', deck='Competitor research and positioning carried into a clinic-and-patient application.', proof='9 months', detail='brand and product engagement', slug='soaltech', media=[('soaltech-healthcare-ui.png','SoalTech healthcare application screens','Product / application'),('soaltech-brand-kit.webp','SoalTech brand kit','Brand / guidance')], tone='#14201e'),
    dict(name='AutoReel', kind='AUDIT + FUNNEL DESIGN', deck='A proposed 90-day acquisition and activation roadmap, from discovery through export and upgrade.', proof='90 days', detail='proposed strategy, not implemented', slug='autoreel', media=[('autoreel-activation.jpg','AutoReel activation path slide','Activation / audit'),('autoreel-90-day-plan.jpg','AutoReel 90-day growth plan slide','Roadmap / proposal')], tone='#151b1b'),
]

def figure(item, cls):
    name, alt, caption = item
    w,h = Image.open(root / 'dist' / 'assets' / name).size
    return f'<figure class="artifact {cls}"><img src="/assets/{name}" alt="{escape(alt)}" width="{w}" height="{h}" loading="lazy"><figcaption>{escape(caption)}</figcaption></figure>'

rendered=[]
for i,c in enumerate(chapters):
    if c.get('media'):
        visual=f'<div class="scene-art scene-art-{c["slug"]}">{figure(c["media"][0],"primary")}{figure(c["media"][1],"secondary")}</div>'
    else:
        visual='''<div class="scene-art scene-art-camfire"><div class="portfolio-board" aria-label="Camfire portfolio scope and outcomes"><span>CAMFIRE MEDIA / PORTFOLIO VIEW</span><strong>Eight brands.<br>One portfolio.</strong><div><span>7 people</span><span>C$2.6M managed marketing budget</span><span>Paid · CRM · Content</span></div><small>Scope and outcomes / not campaign artwork</small></div></div>'''
    proof_class=' word-proof' if c['slug'] in ('soaltech','autoreel','incuse','minimalance') else ''
    rendered.append(f'''<article class="chapter {'active' if i==0 else ''}" data-scene-index="{i}" style="--scene:{c['tone']};--scene-accent:#ff8d62" {'inert' if i else ''} aria-hidden="{'true' if i else 'false'}"><div class="scene-copy"><span class="scene-label">{i+1:02d} / {c['kind']}</span><h2>{escape(c['name'])}<span class="scene-dot">.</span></h2><p class="scene-deck">{escape(c['deck'])}</p><p class="scene-proof{proof_class}"><strong>{escape(c['proof'])}</strong><span>{escape(c['detail'])}</span></p><a class="scene-link" href="/work/{c['slug']}/">Explore the case <span aria-hidden="true">↗</span></a></div>{visual}</article>''')

controls=''.join(f'<button type="button" data-jump="{i}" class="{"active" if i==0 else ""}" aria-label="Show {escape(c["name"])}" {"aria-current=\"true\"" if i==0 else ""}></button>' for i,c in enumerate(chapters))
section=f'''<section class="theatre" id="selected" aria-label="Nine projects in motion" style="--chapter-count:{len(chapters)}"><div class="theatre-pin"><div class="theatre-head"><span>SELECTED WORK / NINE PROJECTS</span><span data-chapter-number>01 / 09</span><a class="theatre-skip" href="#approach">Skip showcase ↓</a></div><div class="theatre-stage" data-theatre>{''.join(rendered)}</div><div class="theatre-foot"><span>Scroll or choose a project</span><div class="theatre-nav" aria-label="Jump to project">{controls}</div><span class="theatre-progress" aria-hidden="true"><i></i></span></div></div><div class="theatre-steps" aria-hidden="true">{''.join('<div></div>' for _ in chapters)}</div></section>'''
start=html.index('<section class="theatre"')
end=html.index('</section>',start)+len('</section>')
html=html[:start]+section+html[end:]
html=html.replace('<section class="work wrap" aria-labelledby="work-h">','<section class="work wrap" id="project-index" aria-labelledby="work-h">')
html=html.replace('Explore all work</h2>','Project index</h2>')
html=html.replace('Commercial work with the decision behind it and the result after it.','Jump directly to a case or browse the full set of project material.')
html=html.replace('data-preview="/assets/incuse-logo-drive.png"','data-preview="/assets/incuse-workflow.webp"').replace('data-preview="/assets/xipster-bull-campaign.png"','data-preview="/assets/xipster-campaign.webp"').replace('data-preview="/assets/soaltech-healthcare-ui.png"','data-preview="/assets/soaltech-app.png"')
path.write_text(html)
print('Updated nine selected-work chapters.')
