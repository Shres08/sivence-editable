from pathlib import Path
from html import escape as esc
import json, shutil
from editorial_fragments import thinking_cards
from PIL import Image

ROOT = Path(__file__).parent
OUT = ROOT / 'dist'
ORIGIN = 'https://sivencestudio.com'
EMAIL = 'joshisreshta@gmail.com'
LINKEDIN = 'https://www.linkedin.com/in/sreshtajoshi/'
ROUTES = {}

# Muted lighting is selected from the existing project material. The brand accent
# remains Sivence orange; these colours sit behind images and never tint the work.
CASE_WASH = {
    'camfire':('#a5744d','#d29a63'),
    'remic':('#416ac1','#df8849'),
    'minimalance':('#9c8064','#bcb6a2'),
    'incuse':('#527e9b','#c48261'),
    'xipster':('#508c98','#d97e5c'),
    'nett-technologies':('#628a79','#b09b72'),
    'bhatt-bros-alea':('#aa7659','#c2a17a'),
    'soaltech':('#559a92','#92bab0'),
    'autoreel':('#6574a3','#9787ad'),
    'titanfile':('#678399','#b6a685'),
}
WORK_ORDER = ['minimalance','incuse','remic','xipster','camfire','nett-technologies','bhatt-bros-alea','soaltech','autoreel','titanfile']
LAB_WASH = {
    'paintings':('#8b9b75','#c29a75'),
    'healthcan':('#64a59a','#b0c9bf'),
    'before-every-yes':('#b97f69','#d6aa89'),
    'form-in-motion':('#6f85ae','#b0bfd3'),
    'marketing-intelligence':('#758f83','#b8b69a'),
    'connected-care':('#6fa3a0','#a8c1b8'),
    'creative-reel':('#9c778b','#c49c7e'),
    'radhe-dhokla':('#b8835c','#d2ad77'),
    'aritzia':('#a08a89','#c4a9a0'),
}
ARTICLE_WASH = {
    'before-you-increase-the-budget':('#577eae','#c69b71'),
    'a-clear-brief':('#9c9078','#c6a786'),
    'ai-and-judgment':('#788d8a','#a6b3a6'),
}

def ambient_attributes(path):
    parts=path.strip('/').split('/')
    if parts[0]=='work' and len(parts)>1 and parts[1] in CASE_WASH:
        family,slug,colors='case',parts[1],CASE_WASH[parts[1]]
    elif parts[0]=='work':
        family,slug,colors='work','index',CASE_WASH['camfire']
    elif parts[0]=='lab' and len(parts)>1:
        family,slug,colors='lab-detail',parts[1],LAB_WASH.get(parts[1],('#80988a','#bda78c'))
    elif parts[0]=='lab':
        family,slug,colors='lab','index',('#8c9b86','#c3a58f')
    elif parts[0]=='thinking' and len(parts)>1 and parts[1] in ARTICLE_WASH:
        family,slug,colors='article',parts[1],ARTICLE_WASH[parts[1]]
    elif parts[0]=='thinking':
        family,slug,colors='thinking','index',('#849789','#c2ae93')
    elif parts[0]=='about':
        family,slug,colors='about','index',('#ac8473','#d0b093')
    else:
        family,slug,colors='contact','index',('#b5876d','#a2aa91')
    return f'data-ambient="{family}" data-project="{slug}" style="--wash-a:{colors[0]};--wash-b:{colors[1]}"'

def image(name, alt, cls='', eager=False):
    w,h = Image.open(OUT/'assets'/name).size
    return f'<img src="/assets/{name}" alt="{esc(alt)}" width="{w}" height="{h}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def film(name, poster, label, hero=False):
    return f'''<div class="film {'hero-film' if hero else ''}"><video {'data-hero loop' if hero else 'controls'} muted playsinline preload="{'metadata' if hero else 'none'}" poster="/assets/{poster}" aria-label="{esc(label)}"><source src="/assets/{name}" type="video/mp4"></video>{'<div class="film-control-bar"><button type="button" data-play>Play reel</button></div>' if hero else ''}</div>'''

def button(text, href, secondary=False, download=False):
    return f'<a class="button {"secondary" if secondary else ""}" href="{href}" {"download" if download else ""}>{text}</a>'

def link(text, href):
    return f'<a class="text-link" href="{href}">{text}</a>'

def scope(label, text):
    return f'<div><span>{label}</span><p>{text}</p></div>'

def number(value, label):
    return f'<div class="metric"><strong>{value}</strong><span>{label}</span></div>'

def cta():
    return f'''<section class="closing wrap"><p class="eyebrow">Marketing leadership · Toronto, Canada</p><h2>Discuss a role<br><span>or project.</span></h2><div class="closing-bottom"><p>Senior marketing roles<br>and defined project engagements.</p>{button('Contact Sreshta','/contact/')}</div></section>'''

def page(path, title, description, body, active='', primary_image=None, article=False):
    canonical = ORIGIN + path
    if article:
        schema = {'@context':'https://schema.org','@type':'Article','headline':title.split(' | ')[0], 'author':{'@type':'Person','name':'Sreshta Joshi','url':ORIGIN+'/about/'},'mainEntityOfPage':canonical}
    else:
        schema = {'@context':'https://schema.org','@type':'Person','name':'Sreshta Joshi','url':ORIGIN,'sameAs':[LINKEDIN],'address':{'@type':'PostalAddress','addressLocality':'Toronto','addressCountry':'CA'},'alumniOf':{'@type':'CollegeOrUniversity','name':'Nirma University'},'knowsAbout':['Growth marketing','Brand strategy','Lifecycle marketing','Integrated marketing','Marketing leadership']}
    nav=''.join(f'<a href="/{slug}/" {"aria-current=\"page\"" if active==slug else ""}>{label}</a>' for slug,label in [('work','Work'),('thinking','Thinking'),('about','About'),('contact','Contact')])
    if active=='contact':
        identity=f'<a class="identity contact-header-brand" href="/" aria-label="Sreshta Joshi, Sivence home"><span class="brand-logo">{image("sivence-logo-light.png","Sivence",eager=True)}</span><span>Sreshta Joshi</span></a>'
    else:
        identity=f'<a class="identity" href="/" aria-label="Sreshta Joshi, Sivence home"><span>Sreshta Joshi<span class="identity-sub">Marketing Intelligence, Brand &amp; Growth</span></span><span class="brand-logo">{image("sivence-logo-light.png","Sivence",eager=True)}</span></a>'
    og = f'<meta property="og:image" content="{ORIGIN}/assets/{primary_image}"><meta name="twitter:image" content="{ORIGIN}/assets/{primary_image}">' if primary_image else ''
    interaction_assets = '<link rel="stylesheet" href="/portfolio-interactions.css"><script src="/portfolio-interactions.js" defer></script>' if path.startswith('/work/') or path.startswith('/lab/') else ''
    if path in ('/thinking/', '/thinking/before-you-increase-the-budget/', '/thinking/a-clear-brief/', '/thinking/ai-and-judgment/', '/lab/paintings/'):
        interaction_assets += '<link rel="stylesheet" href="/editorial-visuals.css">'
    html=f'''<!doctype html>
<html lang="en-CA" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="color-scheme" content="dark"><meta name="theme-color" content="#11120f"><link rel="canonical" href="{canonical}"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="preload" href="/assets/SivenceSans.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="/styles.css">{interaction_assets}<link rel="stylesheet" href="/ambient.css"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="Sreshta Joshi · Sivence"><meta name="twitter:card" content="{'summary_large_image' if primary_image else 'summary'}">{og}<script type="text/javascript">(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","yyfh42vze5");</script><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><script src="/app.js" defer></script><script src="/ambient.js" defer></script></head>
<body {ambient_attributes(path)}><a class="skip-link" href="#main-content">Skip to content</a><div class="scroll-progress" aria-hidden="true"></div><header class="site-header">{identity}<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button><nav id="site-nav" aria-label="Main navigation">{nav}</nav></header><main id="main-content">{body}</main><footer class="site-footer wrap"><div><a class="footer-name" href="/">Sreshta Joshi</a><p>Growth, Brand &amp; Lifecycle Marketing</p></div><div class="footer-links"><a href="mailto:{EMAIL}">Email</a><a href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">LinkedIn</a><a href="/lab/">Lab</a></div><div class="footer-last"><span>© 2026 Sivence</span><span>Signal + Evidence · Toronto, Canada</span></div></footer><dialog class="lightbox"><div class="lightbox-top"><span data-lightbox-label></span><button type="button" data-lightbox-close>Close</button></div><img alt=""></dialog></body></html>'''
    target=OUT/path.strip('/')/'index.html' if path!='/' else OUT/'index.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(html)
    ROUTES[path]={'title':title,'file':str(target.relative_to(OUT))}
    return html

CASES = {
 'camfire':dict(name='Camfire Media',label='Portfolio marketing · Leadership',headline='$7.2M in pipeline influenced.',sub='Eight brands, C$2.6M in client budgets and seven direct reports.',role='Senior Manager, Digital Marketing',period='2023',scope='C$2.6M managed marketing budget · Seven-person team · Paid media, CRM and content',
 summary='At Camfire, I directed marketing across eight consumer and technology brands, managed C$2.6M in client budgets and led seven direct reports. The campaigns influenced $7.2M in pipeline, increased marketing ROI by 24% and reduced CPC by 18%.',
 challenge='Coordinate different brand priorities, investment and delivery across the portfolio. Each brand needed a clear direction, while marketers, designers and agency partners needed a shared way to assess performance.',
 steps=[('Align the portfolio','Connected brand, content and demand initiatives with the business objectives of each brand.'),('Coordinate the delivery','Led seven marketers and designers, setting channel priorities and testing standards.'),('Test the investment','Directed campaign testing and optimization across paid media.'),('Extend the customer journey','Delivered activation, engagement and retention programs across CRM, email and push marketing.')],
 metrics=[('$7.2M','Pipeline influenced'),('+24%','Marketing ROI'),('−18%','Cost per click')],takeaway='Portfolio priorities, campaign ownership and performance reviews kept eight brands aligned with their commercial objectives.',cover=None, keywords='Portfolio marketing, team leadership, budget management, CRM and marketing ROI',description='Camfire Media marketing case study: C$2.6M managed budget, $7.2M influenced pipeline and a 24% ROI improvement across eight brands.'),
 'remic':dict(name='REMIC',label='Paid acquisition · Lifecycle',headline='2,260 conversions.<br>$35 CPA.',sub='Campaign creative, Search/PMax and the route from click to conversion.',role='Marketing Manager',period='2025',scope='Canadian financial education · Search · Lifecycle · Marketing operations',
 summary='At REMIC, I researched prospective students, developed campaign creative and managed the path from acquisition to tracked conversion. I rebuilt Google Search and Performance Max with value-based bidding and tighter query controls. Reporting recorded 45,800 clicks, 2,260 tracked conversions at $35 CPA and a 21% improvement in CTR.',
 challenge='Connect acquisition activity with campaign economics and a useful next step for prospective students. Integrated industry campaigns and faster marketing delivery were also part of the remit.',
 steps=[('Define the audience and offer','Researched prospective students, search intent and competitive positioning to shape campaign messages.'),('Create and launch','Developed campaign creative and copy, then connected Search and Performance Max with social, email, web and landing-page activity.'),('Extend the campaign','Built Fund My Dream and industry-event promotion across formats, alongside newsletters, cart recovery, retargeting and webinars.'),('Audit campaign controls','Reviewed purchase goals, bidding, asset reports and tracking in the February 2025 campaign review; identified overlapping HLLQP activity for consolidation.'),('Optimize the acquisition path','Reworked bidding and query controls, reviewed campaign reporting and adjusted the route from click to tracked conversion.'),('Improve delivery','Applied AI and automation to marketing operations, improving workflow efficiency by 32%.')],
 metrics=[('45,800','Search / PMax clicks'),('2,260','Tracked conversions'),('$35','Cost per tracked conversion'),('+21%','Click-through rate')],takeaway='Audience intent, ad creative and landing-page action were reviewed together when optimizing for tracked conversions.',cover='remic-paid-creatives.jpg',keywords='Paid acquisition, Google Ads, Performance Max, value-based bidding and lifecycle marketing',description='REMIC paid acquisition case study: original campaign creative, Google Search and Performance Max, with 2,260 tracked conversions at $35 CPA.'),
 'minimalance':dict(name='Minimalance',label='Brand launch · Customer experience',headline='₹5 crore in the first year.',sub='A furniture brand launch shaped by architects and interior designers.',role='Senior Manager, Marketing & Brand Strategy',period='2012–2018',scope='Brand strategy · Go-to-market · Product presentation · Sales and service',
 summary='I led go-to-market planning from product concept through rollout. Feedback from architects and interior designers shaped the positioning. I trained the sales team and coordinated production and delivery readiness. The brand exceeded its acquisition target within 90 days and generated ₹5 crore in first-year revenue.',
 challenge='Carry the brand promise consistently into launch communications, product presentation and the customer-facing experience. The campaign and the experience customers received needed to support the same positioning.',
 steps=[('Set the launch direction','Worked with Engineering, Sales and Communications to coordinate the brand launch.'),('Bring the brand to market','Developed integrated marketing across digital, print, events and PR.'),('Make the product tangible','Connected product stories, materials and finish options with customer consideration.'),('Carry the promise through','Coordinated go-to-market activity with procurement, sales, customer service and daily operations.')],
 metrics=[('₹5 crore','First-year revenue'),('$20K+','Media coverage'),('+250%','Customer-base growth'),('+40%','Brand awareness')],takeaway='The campaign, catalogue, showroom and sales experience expressed the same positioning throughout the launch.',cover='minimalance-launch.webp',keywords='Brand strategy, brand launch, go-to-market and integrated marketing',description='Minimalance brand launch case study: integrated marketing and customer experience, ₹5 crore first-year revenue and the acquisition target exceeded within 90 days.'),
 'incuse':dict(name='Incuse Digital',label='Commercial analytics · Creative operations',headline='From inquiry to order.',sub='A SQL analysis of which industrial buyers were most likely to place an order.',role='Senior Marketing & Brand Consultant',period='2024–Present',scope='Eight-person team · Canada, the U.S. and Dubai',
 summary='For an industrial-parts supplier, I used SQL to trace inquiries to orders and compared conversion by segment and source. I recommended focusing on maintenance teams and tightening lead qualification. During the pilot, 26% of qualified leads became orders, up from 20%. In separate creative work, I standardized briefs and reviews across an eight-person team. Revision cycles fell by 40%.',
 challenge='The industrial supplier needed to decide which inquiries deserved sales follow-up. Across our agency accounts, the team also needed a clearer way to brief and approve creative work.',
 steps=[('Trace the sales funnel','Compared customer, opportunity and order data in SQL to identify where qualified inquiries became orders.'),('Set the commercial direction','Partnered with senior executives on positioning, messaging, go-to-market plans and campaign KPIs.'),('Lead the team','Led an eight-person team supporting marketing and client engagements across three markets.'),('Improve creative operations','Standardized brand kits, review workflows and quality assurance.'),('Connect delivery with reporting','Brought demand-generation activity and analytics into client reviews.')],
 metrics=[('20% → 26%','Qualified leads that became orders during the pilot'),('−40%','Creative revision cycles across the team')],takeaway='Comparing inquiries with orders gave Sales a reason to prioritize maintenance teams. The creative examples below are from separate Incuse engagements.',cover='incuse-logo-drive.png',keywords='Brand consulting, marketing leadership, creative operations and international team leadership',description='Incuse Digital marketing case study covering SQL funnel analysis for an industrial-parts supplier and creative operations for an international team.'),
 'xipster':dict(name='Xipster',label='B2B SaaS · Demand generation',headline='28% more B2B leads.',sub='Campaigns for a payments product, measured in B2B leads.',role='Digital Marketing Specialist',period='2023–2024',scope='VenueVision · Email · SEO · Paid media · Content',
 summary='I managed Xipster’s email, social, paid media and SEO at VenueVision. B2B lead generation increased by 28%. Campaign reports and market research then shaped the next recommendations.',
 challenge='Connect the product proposition with acquisition activity across channels. The work needed to support commercial objectives and make the next action clear to prospective buyers.',
 steps=[('Connect the channels','Managed email, social, paid-media and SEO activity as an integrated digital strategy.'),('Develop search content','Prepared a payment-links article and page-level title and description plan for Xipster’s product and industry pages.'),('Review performance','Ran PPC campaigns and used analytics and reporting to inform decisions.'),('Understand the market','Researched trends, competitors and opportunities for product launches.'),('Support the commercial team','Worked with marketing and Sales leadership on product communication and acquisition recommendations.')],
 metrics=[('+28%','B2B lead generation')],takeaway='Campaign reporting informed which messages and channels received further investment.',cover='xipster-bull-campaign.png',keywords='B2B SaaS marketing, demand generation, SEO, SEM and sales enablement',description='Xipster B2B demand generation case study: integrated email, SEO, social and paid media, with 28% growth in leads.'),
 'nett-technologies':dict(name='Nett Technologies',label='Industrial B2B · CRM planning',headline='CRM evaluation<br>and lead management.',sub='A proposed qualification and follow-up model for an industrial technology business.',role='Sales & Marketing Coordinator',period='2024',scope='CRM evaluation · Lead qualification · Sales and marketing handoff',
 summary='At Nett Technologies, I evaluated CRM options against the needs of Sales, Marketing and Operations. The work covered lead capture, account assignment, follow-up, reporting and integration with Genius ERP. I also mapped how inquiries could move through qualification, quotation and post-sale service. These were planning deliverables; adoption and revenue impact are not claimed.',
 challenge='Sales inquiries arrived through different channels, while customer information, opportunity status and follow-up needed a common structure. The CRM decision also had to account for the existing Genius ERP system.',
 steps=[('Define the requirements','Documented lead capture, account ownership, follow-up, reporting and ERP integration needs.'),('Compare CRM options','Assessed six platforms against usability, workflow, integration, cost and onboarding criteria in a 2024 evaluation.'),('Map lead qualification','Developed account categories, BANT criteria and a lead-scoring model for sales prospecting.'),('Connect the handoff','Mapped the proposed path from inquiry and quote to order completion and post-sale follow-up.')],
 task='Give stakeholders a practical basis for CRM selection and a consistent process for qualifying and assigning incoming opportunities.',
 metrics=[],takeaway='The work tied CRM selection to the actual route from inquiry to quote, order and follow-up.',cover='nett-brand-banner.gif',keywords='B2B CRM evaluation, lead qualification, sales and marketing operations',description='Nett Technologies CRM evaluation and lead-management case study: requirements, platform comparison, qualification and proposed ERP handoff.'),
 'bhatt-bros-alea':dict(name='Bhatt Bros × ALEA',label='B2B manufacturing · Partnership launch',headline='An international partnership.<br>A clearer market story.',sub='A textile machine introduced through an Indo-Italian partnership.',role='Senior Manager, Marketing, Brand Management & Communication',period='2021–2023',scope='Brand · Communications · Go-to-market · Textile machinery',
 summary='During my Bhatt Bros tenure, I led brand, communications and go-to-market work for textile machinery. We introduced the Stabilo Relax Dryer through the joint venture with Italy’s Alea Impianti Tessili. International exhibitions generated 39 client inquiries from nine countries.',
 challenge='Translate technical capabilities and an international technology partnership into a consistent story customers could evaluate. Digital, offline and partner communications needed to support the same commercial direction.',
 steps=[('Modernize the brand','Led brand strategy and digital transformation across the business.'),('Explain the partnership','Connected the Stabilo Relax Dryer introduction with the value of the Indo-Italian joint venture.'),('Align delivery','Coordinated Sales, Operations, Logistics and PR around go-to-market work.'),('Develop new markets','Delivered integrated regional campaigns and community and partner engagement programs.')],
 metrics=[('39','Client inquiries from nine countries'),('2','New regional markets'),('−20%','Cost per lead'),('+15%','Active customer base')],takeaway='The exhibition work gave visitors a way to understand a technical partnership through the machine itself.',cover=None,keywords='B2B manufacturing marketing, international product launch, partnership marketing and brand strategy',description='Sreshta Joshi’s B2B brand and partnership work: the Bhatt Bros and ALEA Stabilo Relax Dryer introduction and regional market growth.'),
 'soaltech':dict(name='SoalTech',label='Incuse client engagement · Health-tech',headline='From research to<br>a healthcare interface.',sub='Research and brand guidance carried into the clinic-and-patient app.',role='Brand, positioning and UI/UX contribution',period='Nine-month engagement',scope='Seed-stage health-tech · Incuse client engagement',
 summary='During a nine-month Incuse engagement, I contributed competitor research, brand guidelines, product positioning and UI/UX for SoalTech. The work connected the brand direction with a clinic-and-patient web application in development.',
 challenge='Clarify how the business should differentiate and how that positioning should appear in the product experience.',
 steps=[('Review comparable products','Reviewed competitors and how they explain care to clinics and patients.'),('Support the brand direction','Contributed to brand guidelines and product positioning.'),('Connect promise and product','Contributed to UI/UX decisions for the clinic and patient platform.')],
 task='Translate the research and positioning into practical brand guidance and a coherent clinic-and-patient product experience.',
 metrics=[],takeaway='The research and positioning informed both brand guidance and product interface decisions.',cover='soaltech-healthcare-ui.png',keywords='Healthcare marketing, brand positioning, competitor research and UI/UX',description='SoalTech healthcare positioning and product experience: competitor research, brand guidance and UI/UX in a nine-month Incuse engagement.'),
 'autoreel':dict(name='AutoReel',label='Strategic proposal · Growth audit',headline='A 90-day plan<br>for product growth.',sub='Acquisition and activation strategy from discovery to first export.',role='Growth audit and funnel planning',period='Incuse client engagement',scope='Proposed plan · SEO · CRO · Lifecycle · Paid media · Messaging',
 summary='Through Incuse, I audited AutoReel’s search visibility, messaging, paid media, lifecycle activity and conversion path. The resulting 90-day proposal prioritizes discovery, first upload, export and upgrade.',
 challenge='Examine how the journey from listing photos to a finished video could make the value of exporting or upgrading easier to understand.',
 steps=[('Review discovery','Assessed audience, messaging and acquisition opportunities.'),('Map activation','Examined upload, generation, preview, export and upgrade as distinct steps.'),('Prioritize the plan','Proposed a phased approach to measurement, conversion testing and focused acquisition.')],
 task='Find where people were losing the path from discovery to first export and upgrade, then set out a 90-day plan for those gaps.',
 metrics=[],takeaway='The roadmap treats acquisition, first use and paid conversion as separate stages with distinct measures.',cover='autoreel-audience.jpg',keywords='Growth audit, B2B SaaS, conversion rate optimization, lifecycle marketing and funnel planning',description='AutoReel growth audit and proposed 90-day plan: SEO, conversion, lifecycle and paid-media priorities from discovery to upgrade.')
}

def operating_model():
    return '<div class="camfire-mark"><strong>Camfire<br>Media</strong><p>Portfolio leadership across paid media, CRM and content.</p><div class="camfire-proof"><span>C$2.6M managed budget</span><span>$7.2M influenced pipeline</span><span>Seven-person team</span></div></div>'

def partnership_model():
    return '<div class="partnership-model"><span class="eyebrow">India × Italy</span><strong>Bhatt Bros</strong><span class="partnership-times">×</span><strong>ALEA</strong><p>Stabilo Relax Dryer<br>International technology partnership</p></div>'

def card(slug, small=False):
    c=CASES[slug]
    visual=operating_model() if slug=='camfire' else partnership_model() if slug=='bhatt-bros-alea' else image(c['cover'],c['name']+' project material')
    labels={'camfire':'$7.2M pipeline influenced','remic':'2,260 conversions · $35 CPA','minimalance':'₹5 crore first-year revenue','incuse':'20% to 26% qualified-lead-to-order conversion','xipster':'28% more B2B leads','nett-technologies':'CRM evaluation · Lead qualification','bhatt-bros-alea':'International B2B partnership','soaltech':'Positioning · Brand · UI/UX','autoreel':'Growth audit · Funnel plan'}
    return f'''<a class="project-card {'small-card' if small else ''} card-{slug}" href="/work/{slug}/"><div class="card-visual" data-tilt>{visual}<span class="card-action">View case</span></div><div class="card-topline"><span>{c['name']}</span><span>{c['label']}</span></div><h3>{labels[slug]}</h3><p>{c['sub']}</p></a>'''

def case_visuals(slug):
    if slug=='minimalance':
        spreads=['cover','leman','paulistano','nest','floyd','eastwest','hex','craft','eagle','spider','trio','envelope','intube','pantheon','lock','roots']
        return f'''<div class="section-heading"><h2>The collection,<br>made tangible.</h2><p>Product stories, material details and finish options from the existing catalogue.</p></div><div class="catalogue-grid">{''.join(f'<button class="gallery-button" data-enlarge="catalogue-{s}.webp" data-caption="Minimalance catalogue · {s.title()}">{image('catalogue-'+s+'.webp','Minimalance catalogue, '+s+' spread')}<span>{s.title()}</span></button>' for s in spreads)}</div>{button('Download the full catalogue','/assets/minimalance-catalogue.pdf',True,True)}'''
    if slug=='remic':
        groups=[
            ('Audience and acquisition','',[
                ('remic-audience-research.jpg','REMIC audience research','Audience and journey research informing campaign decisions.'),
                ('remic-pmax.jpg','REMIC Performance Max campaign plan','Search and Performance Max structure and targeting.'),
                ('remic-course-ad.webp','REMIC Mortgage Agent course ad','Course ad with the offer and next action intact.'),
                ('remic-webcast-ad.webp','REMIC vertical webcast and course ad','Vertical campaign format; displayed at its full proportions.')]),
            ('Campaigns across formats','',[
                ('remic-fundmydream-post.webp','REMIC Fund My Dream social creative','Fund My Dream campaign artwork.'),
                ('remic-fundmydream-variant.webp','REMIC Fund My Dream alternate creative','An alternate execution of the same campaign.'),
                ('remic-career-fair.webp','REMIC Toronto Career Fair promotion','Career fair promotional artwork.'),
                ('remic-awards-sponsor.webp','REMIC Canadian Mortgage Awards sponsor graphic','Industry-event promotion and sponsor visibility.')]),
            ('From campaign to field','Events shown here are separate from the paid-media results.',[
                ('remic-event-team-retouched.png','REMIC team at a mortgage industry event','Team at an industry activation.'),
                ('remic-networking-lunch-retouched.png','REMIC Women in Mortgage Summit networking lunch','Networking lunch and event presence.'),
                ('remic-awards-collage.webp','Canadian Mortgage Awards event collage','Event environment and brand presence.')]),
            ('Measurement and refinement','',[
                ('remic-paid-performance.jpg','REMIC paid-media performance summary','Paid-media reporting and optimization material.'),
                ('remic-organic-paid.jpg','REMIC organic and paid channel analysis','Channel context for future investment decisions.')])]
        sections=''.join(f'<div class="section-heading remic-heading"><h2>{heading}</h2>{f"<p>{intro}</p>" if intro else ""}</div><div class="artifact-grid presentation-grid">'+''.join(figure(*asset) for asset in assets)+'</div>' for heading,intro,assets in groups)
        return sections+f'''<div class="document-row"><div><h3>The marketing plan</h3><p>Planning material supporting the campaign and channel work.</p></div>{button('Open marketing plan','/assets/remic-marketing-plan.pdf',True)}</div>'''
    if slug=='xipster':
        return f'''<div class="section-heading"><h2>Content, search<br>and paid campaigns.</h2></div><div class="artifact-grid xipster-content-grid">{figure('xipster-payment-links-blog.png','Xipster payment-links article screenshot','Payment-links article draft.', 'xipster-blog')}{figure('xipster-meta-description-plan.png','Xipster page titles and meta descriptions plan','Page-level title and meta-description plan.', 'xipster-meta')}</div>{film('xipster-reel.mp4','xipster-campaign.webp','Xipster campaign reel')}<div class="artifact-grid">{figure('xipster-get-paid-campaign.png','Xipster product campaign creative','Product campaign material.')}{figure('xipster-maple-leafs-yearbook-contest.jpg','Toronto Maple Leafs yearbook context for Xipster dealer activation','Dealer-engagement placement context; no team partnership is implied.')}</div>'''
    if slug=='nett-technologies':
        return f'''<div class="section-heading"><h2>CRM evaluation<br>and lead flow.</h2><p>2024 working documents. Platform details and pricing may have changed.</p></div><div class="artifact-grid presentation-grid">{figure('nett-crm-requirements.png','Nett Technologies CRM requirements slide','Lead capture, follow-up and Genius ERP integration requirements.')}{figure('nett-crm-comparison-2024.png','Nett Technologies 2024 CRM options comparison','CRM options compared in 2024.')}{figure('nett-lead-qualification.png','Nett Technologies lead qualification framework','BANT qualification framework.')}{figure('nett-lead-funnel.png','Nett Technologies lead generation funnel map','Proposed handoff from inquiry to post-sale follow-up.')}</div>'''
    if slug=='soaltech':
        assets=[
            ('soaltech-app.png','SoalTech healthcare application screens','Healthcare application screens from the client engagement.'),
            ('soaltech-dashboard.png','SoalTech clinic dashboard','Clinic dashboard and operational interface material.'),
            ('soaltech-healthcare-app-showcase.png','SoalTech healthcare application showcase','Clinic and patient platform interface material.'),
            ('soaltech-brand-kit.webp','Supplied SoalTech brand-kit reference','Brand-kit reference supplied for the engagement. My contribution covered research, positioning and UI/UX.')]
        return '<div class="artifact-grid presentation-grid">'+''.join(figure(*asset) for asset in assets)+'</div>'
    if slug=='autoreel':
        assets=[
            ('autoreel-semrush.jpg','AutoReel outside-in search snapshot','Outside-in search visibility snapshot used in the audit.'),
            ('autoreel-authority.jpg','AutoReel authority and backlink analysis','Authority and backlink-quality review.'),
            ('autoreel-traffic.jpg','AutoReel traffic-quality analysis','Outside-in traffic-quality indicators from the audit deck.'),
            ('autoreel-revenue-model.jpg','AutoReel product-led revenue model','Product-led revenue mechanics and pricing analysis.'),
            ('autoreel-activation.jpg','AutoReel activation flow','Activation path from upload through export.'),
            ('autoreel-limitations.jpg','AutoReel audit strengths and limitations','What the current journey supports and where it limits conversion.'),
            ('autoreel-90-day-plan.jpg','AutoReel 90-day plan','The proposed 30, 60 and 90-day sequence.'),
            ('autoreel-funnel-build.jpg','AutoReel funnel build phase','Initial measurement and funnel-building priorities.'),
            ('autoreel-funnel-optimize.jpg','AutoReel funnel optimization phase','Optimization and acquisition priorities.'),
            ('autoreel-kpis.jpg','AutoReel KPI framework','A KPI system for acquisition, activation, conversion and retention.')]
        return '<div class="section-heading"><h2>Growth audit<br>and 90-day plan.</h2><p>Proposed strategy; implementation and results are not claimed.</p></div><div class="artifact-grid presentation-grid">'+''.join(figure(*asset) for asset in assets)+'</div>'
    if slug=='incuse':return '<div class="brief-grid">'+''.join(f'<div><span>0{i}</span><h3>{a}</h3><p>{b}</p></div>' for i,(a,b) in enumerate([('Objective','What needs to change?'),('Audience','Who needs to act?'),('Message','What helps them decide?'),('Ownership','Who delivers and approves?')],1))+'</div><p class="caption">A view of the briefing structure used to organize delivery.</p>'
    if slug=='bhatt-bros-alea':
        archive=[
            ('bhatt-exhibition-1.webp','Bhatt Bros trade show stand with textile machinery','Exhibition stand and textile machinery.'),
            ('bhatt-exhibition-2.webp','Bhatt Bros booth and machine display','Product presentation on the exhibition floor.'),
            ('bhatt-exhibition-3.webp','Bhatt Bros booth overview','Brand presence at an industry exhibition.'),
            ('bhatt-exhibition-4.webp','Bhatt Bros branded exhibition space and machinery','Another view of the exhibition space.')]
        return '<div class="document-row"><div><h3>The international partnership</h3><p>Alea Impianti Tessili and Bhatt Bros developed the Stabilo Relax Dryer for textile applications including knits, terry towels and delicate fabrics.</p></div>'+button('View partnership announcement','https://bhattbros.com/aleabhattbros',True)+'</div><div class="section-heading"><h2>On the exhibition floor.</h2><p>Exhibition photography from my tenure at Bhatt Bros, where I led brand, communications and go-to-market work across industry events.</p></div><div class="artifact-grid bhatt-gallery">'+''.join(figure(*item) for item in archive)+'</div>'
    return '<div class="section-heading"><h2>H.E paid social.</h2><p>Three-day campaign view, separate from portfolio-wide ROI.</p></div><div class="artifact-grid presentation-grid">'+cropped_report('camfire-he-paid-social.png','Camfire H.E paid social performance screenshot','2,811 page likes · 80,866 reach · ₹2,187.48 spend. Platform-reported three-day results.','camfire-report')+'</div>'

def cropped_report(asset,alt,caption,cls):
    # Crop at presentation time: source pixels and reporting figures stay intact.
    return f'<figure class="artifact cropped-report {cls}"><div class="report-scroller" role="region" tabindex="0" aria-label="{esc(alt)}; scroll horizontally on narrow screens"><div class="report-crop">{image(asset,alt)}</div></div><figcaption><span>{caption}</span></figcaption></figure>'

def figure(asset,alt,caption,cls=''):
    original_link='' if asset.endswith('-retouched.png') else f'<a href="/assets/{asset}" target="_blank" rel="noopener" aria-label="Open original file: {esc(alt)}">Original ↗</a>'
    return f'<figure class="artifact {cls}"><button type="button" class="artifact-image" data-enlarge="{asset}" data-caption="{esc(alt)}" aria-label="Enlarge {esc(alt)}">{image(asset,alt)}</button><figcaption><span>{caption}</span>{original_link}</figcaption></figure>'

def create_case(slug):
    c=CASES[slug]
    hero_visual=operating_model() if slug=='camfire' else partnership_model() if slug=='bhatt-bros-alea' else image(c['cover'],c['name']+' project material',eager=True)
    impacts=''.join(number(*m) for m in c['metrics'])
    if slug=='bhatt-bros-alea': impacts='<p class="impact-context">Partnership launch and market-expansion outcomes reported during the Bhatt Bros engagement.</p><div class="metrics-row">'+impacts+'</div>'
    elif slug=='remic': impacts='<p class="impact-context">Search and Performance Max results recorded during my time at REMIC. Tracked conversions reflect the account setup; this figure does not claim confirmed enrolments.</p><div class="metrics-row">'+impacts+'</div>'
    elif slug=='camfire': impacts='<p class="impact-context">Portfolio-wide results from the Camfire engagement. The three-day H.E campaign view below is a separate snapshot.</p><div class="metrics-row">'+impacts+'</div>'
    elif impacts: impacts='<div class="metrics-row">'+impacts+'</div>'
    elif slug=='autoreel':impacts='<p class="large-copy">Deliverable: a growth audit and phased 90-day funnel plan. Implementation has not begun, so no performance result is reported.</p>'
    elif slug=='nett-technologies':impacts='<p class="large-copy">Deliverables: a CRM evaluation, lead-qualification framework and proposed sales-to-ERP funnel. Implementation or revenue impact has not been verified.</p>'
    else:impacts='<p class="large-copy">Deliverables: competitor research, brand guidance, product positioning and UI/UX input for the application in development.</p>'
    if slug in ['soaltech','autoreel','nett-technologies']:
        story=f'''<div class="story-row"><div class="story-label"><span>01</span><h2>Executive Summary</h2></div><p class="large-copy">{c['summary']}</p></div><div class="story-row"><div class="story-label"><span>02</span><h2>Situation</h2></div><p>{c['challenge']}</p></div><div class="story-row"><div class="story-label"><span>03</span><h2>Task</h2></div><p>{c['task']}</p></div><div class="story-row"><div class="story-label"><span>04</span><h2>Action</h2></div><ol class="execution-list">{''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a,b in c['steps'])}</ol></div><div class="story-row impact-row"><div class="story-label"><span>05</span><h2>Result</h2></div><div>{impacts}</div></div>'''
    else:
        story=f'''<div class="story-row"><div class="story-label"><span>01</span><h2>Executive Summary</h2></div><p class="large-copy">{c['summary']}</p></div><div class="story-row"><div class="story-label"><span>02</span><h2>The Challenge</h2></div><p>{c['challenge']}</p></div><div class="story-row"><div class="story-label"><span>03</span><h2>The Execution</h2></div><ol class="execution-list">{''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a,b in c['steps'])}</ol></div><div class="story-row impact-row"><div class="story-label"><span>04</span><h2>The Impact</h2></div><div>{impacts}{'<p class="impact-extra">Marketing workflow efficiency improved by 32% through AI and automation.</p>' if slug=='remic' else ''}</div></div>'''
    nxt=WORK_ORDER[(WORK_ORDER.index(slug)+1)%len(WORK_ORDER)] if slug in WORK_ORDER else 'remic'
    nxt_data=LAB[nxt] if nxt=='titanfile' else CASES[nxt]
    nxt_url='/work/'+nxt+'/'
    nxt_sub=nxt_data['intro'] if nxt=='titanfile' else nxt_data['sub']
    materials=f'<section class="case-artifacts wrap"><p class="eyebrow">Selected materials</p>{case_visuals(slug)}</section>'
    body=f'''<section class="case-hero wrap"><div class="breadcrumb">{link('All work','/work/')}<span>{c['name']}</span></div><p class="eyebrow">{c['label']}</p><h1>{c['headline']}</h1><p class="case-sub">{c['sub']}</p><div class="scope-grid">{scope('Role',c['role'])}{scope('Period',c['period'])}{scope('Scope',c['scope'])}</div><div class="case-cover cover-{slug}">{hero_visual}</div></section><section class="case-story wrap">{story}</section>{materials}<section class="takeaway wrap"><p class="eyebrow">Strategic insight</p><p>{c['takeaway']}</p></section><section class="next-case wrap"><p class="eyebrow">Next project</p><a href="{nxt_url}"><span>{nxt_data['name']}</span><span>{nxt_sub}</span></a></section>{cta()}'''
    case_titles={
        'camfire':'Camfire Media | Portfolio Marketing and Leadership',
        'remic':'REMIC | Google Ads and Paid Acquisition Case Study',
        'minimalance':'Minimalance | Brand Launch and Go-to-Market Case Study',
        'incuse':'Incuse Digital | Creative Operations Case Study',
        'xipster':'Xipster | B2B Demand Generation Case Study',
        'nett-technologies':'Nett Technologies | B2B CRM and Lead Management',
        'bhatt-bros-alea':'Bhatt Bros × ALEA | B2B Partnership Marketing',
        'soaltech':'SoalTech | Healthcare Brand and Product Positioning',
        'autoreel':'AutoReel | Growth Audit and Proposed 90-Day Plan',
    }
    page('/work/'+slug+'/',case_titles[slug]+' | Sreshta Joshi',c['description'],body,'work',c['cover'] if slug not in ['incuse'] else None)

def home():
    html=(ROOT/'homepage.html').read_text()
    (OUT/'index.html').write_text(html)
    ROUTES['/']={'title':'Sivence | Signal to Strategy. Evidence to Action.','file':'index.html'}

ARTICLES={
'before-you-increase-the-budget':('Before you increase the budget, inspect the journey.','Acquisition / Customer experience','A framework for deciding whether the next investment belongs in reach, relevance or the next action.','remic-campaign.webp'),
'a-clear-brief':('A clear brief is a leadership decision.','Leadership / Creative operations','What a brief should settle before work moves into production.','incuse-logo.webp'),
'ai-and-judgment':('Where AI improves marketing—and where judgment matters.','AI / Marketing operations','How I decide whether a tool deserves a place in the workflow.','healthcan-poster.jpg')}

def article_card(slug):
    title,tag,deck,asset=ARTICLES[slug]
    return f'<a class="article-card" href="/thinking/{slug}/"><span class="eyebrow">{tag}</span><h3>{title}</h3><p>{deck}</p><span class="text-link">Read the article</span></a>'

def work():
    order=WORK_ORDER
    work_media={
        'camfire':[],
        'remic':[('remic-course-ad.webp','REMIC mortgage course campaign creative'),('remic-career-fair.webp','REMIC Career Fair campaign creative')],
        'minimalance':[('minimalance-launch.webp','Minimalance launch interior'),('catalogue-leman.webp','Leman chair from the Minimalance catalogue')],
        'incuse':[('incuse-logo-drive.png','Incuse Digital brand mark'),('incuse-gisec-exhibition.png','Incuse GISEC exhibition announcement')],
        'xipster':[('xipster-bull-campaign.png','Xipster payment campaign creative'),('xipster-get-paid-campaign.png','Xipster Get Paid campaign creative')],
        'nett-technologies':[('nett-lead-funnel.png','Nett Technologies proposed lead-management funnel'),('nett-crm-requirements.png','Nett Technologies CRM requirements')],
        'bhatt-bros-alea':[('bhatt-exhibition-4.webp','Bhatt Bros textile machinery exhibition'),('bhatt-exhibition-2.webp','Bhatt Bros machinery display')],
        'soaltech':[('soaltech-healthcare-ui.png','SoalTech clinic-and-patient application screens')],
        'autoreel':[('autoreel-activation.jpg','AutoReel activation flow slide'),('autoreel-90-day-plan.jpg','AutoReel 90-day plan slide')],
        'titanfile':[('titanfile-event.jpg','TitanFile event-strategy assignment')]
    }
    work_notes={
        'camfire':('Marketing leadership across eight brands.','C$2.6M managed marketing budget, seven-person team and campaigns influencing $7.2M in pipeline.','Portfolio marketing · ROI +24%'),
        'remic':('Paid acquisition and campaign production.','Audience research, original creative, Search and Performance Max, email and conversion optimization.','2,260 tracked conversions at $35 CPA'),
        'minimalance':('An integrated brand launch.','Positioning across campaigns, catalogue, showroom and customer experience.','₹5 crore first-year revenue'),
        'incuse':('Commercial analytics for an industrial supplier.','SQL analysis informed targeting and lead qualification.','20% to 26% qualified-lead-to-order conversion'),
        'xipster':('B2B payments demand generation.','Coordinated search, paid media, email and social activity at VenueVision.','28% more B2B leads'),
        'nett-technologies':('CRM planning for industrial B2B sales.','Compared CRM platforms and mapped lead qualification, account assignment and the ERP handoff.','Evaluation and funnel plan · No adoption result claimed'),
        'bhatt-bros-alea':('B2B partnership and exhibition marketing.','Product and partnership communications during the Bhatt Bros tenure.','39 inquiries from nine countries'),
        'soaltech':('Healthcare positioning and product experience.','Competitor research, brand guidance and UI/UX for an Incuse health-tech client.','Nine-month client engagement'),
        'autoreel':('Growth audit and 90-day plan.','Proposed acquisition and activation roadmap from discovery to first export and upgrade.','Strategic proposal · not implemented'),
        'titanfile':('Event strategy assignment.','Pre-event promotion, booth roles, lead capture and contextual follow-up planning.','Planning assignment · no implementation claimed')
    }
    controls=''.join(f'''<li><button type="button" class="work-choice {'is-active' if i==0 else ''}" data-case-choice="{slug}" aria-pressed="{'true' if i==0 else 'false'}"><span class="work-choice-no">{i+1:02d}</span><span class="work-choice-name">{(LAB[slug] if slug=='titanfile' else CASES[slug])['name']}</span><span class="work-choice-arrow" aria-hidden="true">↗</span></button></li>''' for i,slug in enumerate(order))
    panels=[]
    for i,slug in enumerate(order):
        c=LAB[slug] if slug=='titanfile' else CASES[slug]; lead,detail,proof=work_notes[slug]
        if slug=='camfire':
            visual='''<div class="work-operating" aria-label="Camfire portfolio scope"><span>CAMFIRE MEDIA</span><strong>8 brands<br>7 people</strong><div><span>C$2.6M managed marketing budget</span><span>$7.2M pipeline influenced</span></div></div>'''
        else:
            visual='<div class="work-art work-art-'+slug+'">'+''.join(f'''<button type="button" class="work-artifact work-artifact-{j+1}" data-enlarge="{asset}" data-caption="{esc(alt)}" aria-label="Enlarge {esc(alt)}">{image(asset,alt)}</button>''' for j,(asset,alt) in enumerate(work_media[slug]))+'</div>'
        panels.append(f'''<article class="work-panel {'is-active' if i==0 else ''}" data-case-panel="{slug}" aria-hidden="{'false' if i==0 else 'true'}" {'inert' if i else ''}><div class="work-panel-copy"><p class="work-panel-type">{esc(c['label'])}</p><h2>{esc(c['name'])}</h2><p class="work-panel-lead">{esc(lead)}</p><div class="work-panel-foot"><span>{esc(proof)}</span><a href="/work/{slug}/">View project <span aria-hidden="true">↗</span></a></div></div><div class="work-panel-visual">{visual}</div></article>''')
    body=f'''<section class="page-intro wrap work-intro"><p class="eyebrow">Selected marketing projects</p><h1>Marketing work,<br><span>from strategy through delivery.</span></h1><p>Ten projects across paid acquisition, brand, creative operations, B2B demand generation and product marketing. AutoReel is a strategic proposal; TitanFile is an event strategy assignment.</p></section><section class="work-explorer wrap" aria-label="Explore ten marketing projects"><div class="work-explorer-head"><p class="eyebrow">Explore the work</p></div><div class="work-explorer-layout"><ol class="work-choices" aria-label="Choose a project">{controls}</ol><div class="work-stage" data-work-stage>{''.join(panels)}</div></div><p class="visually-hidden" data-work-announcement role="status">Showing Minimalance</p><noscript><p class="work-noscript">Browse the projects: {', '.join(link((LAB[s] if s=='titanfile' else CASES[s])['name'],'/work/'+s+'/') for s in order)}.</p></noscript></section><section class="lab-teaser wrap"><div><p class="eyebrow">Independent creative practice</p><h2>Films, interfaces<br><span>and paintings.</span></h2><p>Independent concept films, interface studies and painting, with the scope of each piece clearly identified.</p>{button('Explore the Lab','/lab/',True)}</div><a href="/lab/healthcan/">{image('healthcan-poster.jpg','HealthCan independent concept film poster')}</a></section>{cta()}'''
    page('/work/','Marketing Case Studies | Sreshta Joshi','Explore ten marketing projects across paid acquisition, brand launches, B2B demand generation, creative operations and event planning.',body,'work')

def thinking():
    body=f'''<section class="page-intro wrap"><p class="eyebrow">Marketing strategy</p><h1>Marketing decisions,<br><span>examined in practice.</span></h1><p>Perspectives on acquisition, creative leadership and AI in marketing, grounded in campaign work and the decisions required to improve it.</p></section><section class="method-feature wrap"><div><p class="eyebrow">The Sivence method</p><h2>From signal<br>to a better decision.</h2><p>A six-step framework connecting business questions, market evidence, campaign delivery and review.</p>{button('Explore the method','/thinking/the-sivence-method/',True)}</div><div class="method-index">{''.join(f'<span><b>0{i}</b>{s}</span>' for i,s in enumerate(['Business question','Signal map','Evidence check','Strategic choice','Bounded test','Review'],1))}</div></section><section class="wrap editorial-grid" aria-label="Three marketing decision notes">{thinking_cards()}</section>{cta()}'''
    page('/thinking/','Marketing Strategy & Thinking | Sreshta Joshi','The Sivence method and essays by Sreshta Joshi on budgets, creative briefs, customer journeys and AI in marketing.',body,'thinking')

def method():
    steps=[('Business question','Define the decision.','Start with the change the business needs. Is the priority qualified demand, brand clarity, adoption, retention or delivery? Define the audience and time horizon before selecting a channel.'),('Signal map','Collect what the market is saying.','Bring together customer questions, search behavior, sales feedback, CRM patterns, competitor movement and channel performance. A signal is an observation to investigate.'),('Evidence check','Test what holds up.','Compare sources, recency and relevance. Look for corroboration, identify contradictions and name the information that is missing.'),('Strategic choice','Choose the priority.','Select the audience problem and campaign priority. Make the reasoning visible, identify assumptions and clarify ownership.'),('Bounded test','Connect message, channel and experience.','Set the message, route to market, customer experience, owner and review window. Make the test focused enough to learn from and complete enough to expose friction.'),('Review','Keep, change or stop.','Read the outcome against the original objective. Keep what is supported, change what the evidence challenges and stop work that no longer earns its place.')]
    body=f'''<section class="page-intro wrap"><div class="breadcrumb">{link('Thinking','/thinking/')}</div><p class="eyebrow">The Sivence method / Signal + Evidence</p><h1>From a business question<br><span>to a marketing decision.</span></h1><p>A framework for connecting customer and channel evidence with a clear campaign priority, accountable delivery and a defined review point.</p></section><section class="method-detail wrap">{''.join(f'<div class="method-step"><span>0{i}</span><div><p class="eyebrow">{a}</p><h2>{b}</h2><p>{c}</p></div></div>' for i,(a,b,c) in enumerate(steps,1))}</section><section class="wrap method-film">{film('sivence-signal-evidence-film.mp4','sivence-signal-evidence-poster.jpg','Sivence Signal and Evidence concept film')}<p class="caption">Independent concept film exploring the Signal + Evidence idea.</p></section>{cta()}'''
    page('/thinking/the-sivence-method/','The Sivence Method: Signal + Evidence | Sreshta Joshi','Sreshta Joshi’s six-step marketing framework: define the question, investigate signals, test evidence, choose, deliver and review.',body,'thinking',article=True)

def about():
    timeline=[('2024–Present','Incuse Digital','Senior Marketing & Brand Consultant','Eight-person team across Canada, the U.S. and Dubai; 40% fewer revision cycles.'),('2025','REMIC','Marketing Manager','Search and lifecycle marketing in Canadian financial education; 2,260 conversions at $35 CPA.'),('2023–2024','VenueVision / Xipster','Digital Marketing Specialist','Integrated B2B SaaS marketing; 28% more B2B leads.'),('2024','Nett Technologies','Sales & Marketing Coordinator','CRM platform evaluation and lead qualification framework for industrial B2B sales.'),('2023','Camfire Media','Senior Manager, Digital Marketing','C$2.6M managed marketing budget, seven-person team, $7.2M influenced pipeline and ROI +24%.'),('2021–2023','Bhatt Bros','Senior Manager, Marketing, Brand Management & Communication','Brand modernization, international partnership communication and regional expansion.'),('2018–2019','Desjardins','Sales & Loyalty, Property & Casualty Agent','Customer relationships, needs analysis, service and retention.'),('2012–2018','Minimalance','Senior Manager, Marketing & Brand Strategy','Brand launch and business growth; ₹5 crore first-year revenue.'),('2011–2012','Mercedes-Benz','After Sales and Growth Assistant Manager','Owner events, service retention and monthly performance scorecards.')]
    body=f'''<section class="about-hero wrap"><div><p class="eyebrow">Sreshta Joshi, MBA · Toronto</p><h1>B2B product and<br><span>growth marketing.</span></h1><p class="large-copy">I’m Sreshta Joshi, a Toronto-based marketing leader with 14+ years in product launches, demand generation and customer marketing.</p><p>My work spans B2B SaaS, financial education, healthcare, manufacturing and consumer brands. I lead teams, work with Sales and make decisions about positioning, channel investment and the path from inquiry to order.</p><p>My analytics toolkit includes SQL, Microsoft Power BI and Google Analytics. At Incuse, I used SQL to trace inquiries through to orders and identify a priority customer segment.</p><div class="hero-actions">{button('View case studies','/work/')}</div></div><figure>{image('sreshta-portrait-color.webp','Portrait of Sreshta Joshi',eager=True)}<figcaption>Toronto, Canada</figcaption></figure></section><section class="wrap leadership"><div class="section-heading"><h2>Direction.<br><span>Ownership. Delivery.</span></h2><p>Direction, execution and measurement across the marketing function.</p></div><div class="brief-grid">{''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in [('Leadership','Team direction, marketing investment, agency coordination and executive partnership.'),('Delivery','Positioning, integrated campaigns, lifecycle marketing, acquisition and analytics.'),('Learning','AI and automation evaluated against the question, the quality of the work and the decision.')])}</div></section><section class="career wrap"><div class="section-heading"><div><p class="eyebrow">Experience</p><h2>Professional<br><span>experience.</span></h2></div><p>Roles and periods are shown as recorded, including overlapping engagements.</p></div><div class="timeline">{''.join(f'<div><span class="timeline-period">{a}</span><div><h3>{b}</h3><p class="timeline-title">{c}</p><p>{d}</p></div></div>' for a,b,c,d in timeline)}</div></section><section class="credentials-section wrap"><p class="eyebrow">Education &amp; training</p><h2>Education and qualifications.</h2><div class="credential-grid">{''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in [('MBA, Marketing','Nirma University · 2011'),('Digital Marketing','University of Toronto · 2023'),('Bachelor of Commerce','Gujarat University · 2009'),('Marketing qualifications','Google Ads Search · Google Analytics')])}</div></section>{cta()}'''
    page('/about/','About Sreshta Joshi | Marketing Leader, Toronto','Sreshta Joshi is a Toronto marketing leader with 14+ years in brand, growth and lifecycle marketing across B2B and consumer markets.',body,'about','sreshta-portrait-color.webp')

def contact():
    body=f'''<section class="contact-hero wrap contact-simple"><div class="contact-intro"><p class="eyebrow">Contact · Toronto, Canada</p><h1>Discuss a project<br><span>or leadership role.</span></h1><p>For project enquiries or leadership opportunities, reach out directly.</p></div><div class="contact-options" aria-label="Contact details"><div class="contact-option"><p class="eyebrow">Email</p><a class="contact-email" href="mailto:{EMAIL}">{EMAIL} <span aria-hidden="true">↗</span></a></div><div class="contact-option"><p class="eyebrow">LinkedIn</p><a class="contact-social" href="{LINKEDIN}" target="_blank" rel="noopener noreferrer">Connect on LinkedIn <span aria-hidden="true">↗</span></a></div></div></section>'''
    page('/contact/','Contact Sreshta Joshi | Toronto','Discuss a senior marketing opportunity, project brief or business question with Sreshta Joshi in Toronto.',body,'contact')

LAB={
 'creative-reel':dict(name='Selected Creative Reel',label='Independent concepts · Creative direction',asset='hero-main-poster.webp',headline='A reel of<br>creative exploration.',intro='Selected independent concepts from the existing portfolio, exploring film, visual direction and motion.',film='hero-desktop.mp4',sections=[('The format','Independent creative portfolio reel. Commercial campaign outcomes are not claimed.')]),
 'healthcan':dict(name='HealthCan',label='Independent concept · AI-assisted film',asset='healthcan-poster.jpg',headline='Making connected care<br>feel understandable.',intro='An imagined connected-care service, explained through an everyday story for a Canadian audience.',film='healthcan-concept.mp4',sections=[('The brief','Give a broad healthcare-service idea a clear human context.'),('The creative decision','Build the story around the audience and an everyday situation, then use the product idea to support that story.'),('The delivery','Concept development, character direction, scene planning and AI-assisted visual production.')]),
 'before-every-yes':dict(name='Before Every Yes',label='Independent financial-film concept',asset='pine-poster.jpg',headline='Before Every Yes.',intro='An independent exploration of financial storytelling through film.',film='pine-concept.mp4',sections=[('The exploration','A financial-film concept examining how a familiar decision can become the center of a story.'),('The format','Film-led creative practice. Commercial campaign results are not claimed.')]),
 'form-in-motion':dict(name='Form in Motion',label='Independent motion study',asset='motion-experiment-poster.jpg',headline='Exploring how form<br>becomes movement.',intro='An AI-assisted study in motion, composition and visual rhythm.',film='motion-experiment.mp4',sections=[('The exploration','Investigate how movement changes the way a form is perceived.'),('The format','Independent visual experimentation.')]),
 'marketing-intelligence':dict(name='Marketing Intelligence',label='Independent interface concept',asset='marketing-intelligence-interface-concept-poster.webp',headline='Turn scattered signals<br>into a clearer question.',intro='A visual study of how market signals, research and decision criteria could live in one interface.',film='marketing-intelligence-interface-concept.mp4',sections=[('The exploration','Connect the evidence available with the decision a marketer needs to make.'),('The boundary','An independent interface concept, rather than a deployed product or client system.')]),
 'connected-care':dict(name='Connected Care',label='Independent healthcare visual study',asset='incuse-workflow.webp',headline='A visual study<br>of connected care.',intro='Exploring how a service relationship can be represented through a connected visual system.',sections=[('The format','Independent visual practice in healthcare communication.')]),
 'titanfile':dict(name='TitanFile',label='Event strategy assignment',asset='titanfile-event.jpg',headline='Make the event conversation<br>lead somewhere.',intro='Pre-event promotion, booth roles, lead capture and contextual follow-up planning.',sections=[('The question','How should promotion, event conversations and follow-up connect around a useful next step?'),('The proposal','Invite relevant attendees, define greeting and demonstration roles, capture conversation context and organize follow-up by interest and readiness.'),('The deliverable','An event-strategy planning framework. Implementation and commercial results are not claimed.')]),
 'radhe-dhokla':dict(name='Radhe Dhokla',label='Strategy proposal',asset='radhe-campaign-cravings.webp',headline='Grow the routes to purchase.<br>Keep the experience consistent.',intro='An outside-in proposal across local discovery, ordering, catering and packaged products.',sections=[('The question','How could a food brand extend its reach while maintaining consistent ordering, presentation and customer expectations?'),('The proposal','Improve the route from local discovery to ordering, define a response process for catering and explore packaged products through a staged pilot.'),('The next check','Validate customer demand, operational capacity and service consistency before expansion.')]),
 'aritzia':dict(name='Aritzia',label='Individual academic project',asset='aritzia-customer-funnel.jpg',headline='Connect loyalty<br>with the customer journey.',intro='An individual academic exploration of acquisition, engagement and advocacy across channels.',sections=[('The question','How could a loyalty program organize a coherent journey across search, social, landing pages and follow-up?'),('The proposed approach','Use the program as the organizing layer for messaging, campaign concepts and automated follow-up.'),('The deliverable','A channel plan, funnel, campaign concepts, landing-page wireframe and workflow. Not commissioned by or affiliated with Aritzia.')]),
 'paintings':dict(name='Paintings',label='Personal painting practice',asset='art-verdure.webp',headline='Six original<br>paintings.',intro='Six original paintings presented in full, with room settings to show their scale.',sections=[])
}

def lab_card(slug):
    if slug=='spatial-studio':
        return '<a class="lab-card" href="/lab/spatial-studio/"><div>'+image('spatial-studio.webp','Orange, chrome and glass Sivence sculpture')+'</div><span class="eyebrow">Interactive sculpture</span><h3>Spatial Studio</h3></a>'
    c=LAB[slug]
    a,b=LAB_WASH.get(slug,('#80988a','#bda78c'))
    return f'<a class="lab-card" href="/lab/{slug}/" style="--wash-a:{a};--wash-b:{b}"><div>{image(c["asset"],c["name"]+" project preview")}</div><span class="eyebrow">{c["label"]}</span><h3>{c["name"]}</h3></a>'

def titanfile_document():
    pdf='/assets/titanfile-event-strategy.pdf'
    slides=''.join(f'<figure><a href="{pdf}#page={i}" target="_blank" rel="noopener" aria-label="Open TitanFile strategy PDF at page {i}">{image(f"titanfile-plan-{original_i:02d}.webp",f"TitanFile LegalWeek strategy slide {i} of 9")}</a><figcaption>Slide {i:02d} / 09 <span aria-hidden="true">↗</span></figcaption></figure>' for i,original_i in enumerate(range(2,11),1))
    return f'''<section class="titanfile-document wrap" aria-label="TitanFile event strategy presentation"><div class="section-heading"><div><p class="eyebrow">Presentation</p><h2>LegalWeek 2025<br>event strategy.</h2></div><div><p>Nine slides from the planning assignment. The proposed activities and budget are plans, not implemented results.</p>{button('Open PDF',pdf,True)}</div></div><div class="titanfile-slides">{slides}</div></section>'''

def lab():
    ROUTES['/lab/spatial-studio/']={'title':'Spatial Studio | Sivence','file':'lab/spatial-studio/index.html'}
    body=f'''<section class="page-intro wrap"><p class="eyebrow">The Lab</p><h1>Independent<br><span>creative practice.</span></h1><p>Concept films, interface studies, motion experiments and paintings exploring storytelling and visual direction. Each entry identifies its format and whether it was commissioned, proposed or independently created.</p></section><section class="lab-grid wrap">{''.join(lab_card(s) for s in ['spatial-studio','paintings','healthcan','before-every-yes','form-in-motion','marketing-intelligence','connected-care'])}</section><section class="archive-section wrap"><div class="section-heading"><h2>Additional<br><span>concept studies.</span></h2><p>A creative reel and two strategy studies, each presented with its original scope.</p></div><div class="lab-grid">{''.join(lab_card(s) for s in ['creative-reel','radhe-dhokla','aritzia'])}</div></section>{cta()}'''
    page('/lab/','Lab: Creative Experiments | Sreshta Joshi','Independent creative practice by Sreshta Joshi: concept films, interface studies, motion experiments and paintings.',body)
    for slug,c in LAB.items():
        if slug=='titanfile':continue
        if c.get('film'):visual=film(c['film'],c['asset'],c['name']+' film')
        elif slug=='paintings':
            names=['verdure','voyage','raga','pulse','drift','concrete']
            pieces=''.join(f'''<figure class="exhibit-piece {'is-active' if i==0 else ''}" data-painting-panel="{i}" aria-hidden="{'false' if i==0 else 'true'}" {'inert' if i else ''}><button class="exhibit-image" type="button" data-enlarge="art-{name}.webp" data-caption="{name.title()}" aria-label="Open {name.title()} at full size">{image("art-"+name+".webp",name.title()+" painting in a room mockup")}</button><figcaption><span>Painting {i+1:02d} / 06</span><h2>{name.title()}</h2></figcaption></figure>''' for i,name in enumerate(names))
            choices=''.join(f'''<button type="button" class="exhibit-choice {'is-active' if i==0 else ''}" data-painting-choice="{i}" aria-label="Show {name.title()}" aria-pressed="{'true' if i==0 else 'false'}"><span>{i+1:02d}</span>{name.title()}</button>''' for i,name in enumerate(names))
            visual=f'''<section class="painting-exhibition" aria-label="Six paintings"><div class="exhibit-heading"><span class="eyebrow">The painting room</span><p>Choose a title, use the arrows, or swipe on a phone.</p></div><div class="exhibit-stage" id="painting-room" data-exhibit-stage tabindex="0" aria-label="Painting viewer; use left and right arrow keys">{pieces}</div><div class="exhibit-footer"><button type="button" class="exhibit-arrow" data-painting-previous aria-label="Previous painting">←</button><div class="exhibit-choices" aria-label="Choose a painting">{choices}</div><button type="button" class="exhibit-arrow" data-painting-next aria-label="Next painting">→</button></div></section>'''
        else:visual=figure(c['asset'],c['name']+' supporting material',c['label'])
        if slug=='radhe-dhokla':visual+='<div class="artifact-grid">'+figure('radhe-campaign-festival.webp','Radhe Dhokla festival reference creative','Brand reference material supplied for context.')+figure('radhe-campaign-menu.webp','Radhe Dhokla menu reference creative','Brand reference material supplied for context.')+'</div>'
        if slug=='aritzia':visual+='<div class="artifact-grid">'+''.join(figure(a,b,'Individual academic project material.') for a,b in [('aritzia-sponsored-social-mockup.webp','Aritzia sponsored social mockup'),('aritzia-fashion-campaign-still.webp','Aritzia campaign direction still'),('aritzia-mobile-journey.jpg','Aritzia mobile customer journey concept'),('aritzia-automation-workflow.jpg','Aritzia follow-up workflow concept')])+'</div>'
        body=f'''<section class="page-intro wrap {'paint-intro' if slug=='paintings' else ''}"><div class="breadcrumb">{link('The Lab','/lab/')}</div><p class="eyebrow">{c['label']}</p><h1>{c['headline']}</h1><p>{c['intro']}</p></section><section class="lab-detail wrap {'paint-detail' if slug=='paintings' else ''}">{visual}{'<div class="lab-context">'+''.join(f'<div><h2>{a}</h2><p>{b}</p></div>' for a,b in c['sections'])+'</div>' if c['sections'] else ''}</section>{titanfile_document() if slug=='titanfile' else ''}{cta()}'''
        page('/lab/'+slug+'/',c['name']+' | Creative Work | Sreshta Joshi',c['intro'].replace('<br>',' '),body,primary_image=c['asset'])

def titanfile_work():
    c=LAB['titanfile']
    visual=figure(c['asset'],'TitanFile event strategy material',c['label'])
    context=''.join(f'<div><h2>{a}</h2><p>{b}</p></div>' for a,b in c['sections'])
    body=f'''<section class="page-intro wrap"><div class="breadcrumb">{link('All work','/work/')}</div><p class="eyebrow">{c['label']}</p><h1>{c['headline']}</h1><p>{c['intro']}</p></section><section class="lab-detail wrap">{visual}<div class="lab-context">{context}</div></section>{titanfile_document()}{cta()}'''
    page('/work/titanfile/','TitanFile | Event Strategy Assignment | Sreshta Joshi',c['intro'],body,'work',primary_image=c['asset'])

ARTICLE_BODIES={
'before-you-increase-the-budget':'''<p class="article-lead">When a campaign is underperforming, increasing the budget is one of the easiest decisions to make. It is also a decision that deserves a better diagnosis.</p><p>The useful question is where the next investment would change the outcome. That could be reach, a more relevant message, a clearer page or a better follow-up. Those are different problems, even when the headline symptom is the same.</p><h2>Start with the outcome being counted.</h2><p>A click, an enquiry, an enrolment and a qualified opportunity are different signals. Before using campaign performance to make an investment decision, define what the platform counts and what the business needs.</p><p>At REMIC, my acquisition work included rebuilding Search and Performance Max with value-based bidding and tighter query controls. The recorded results were 45,800 clicks and 2,260 tracked conversions at $35 CPA, with a 21% CTR improvement. Those figures describe campaign activity and economics. Understanding their business meaning also requires the conversion definition and the reporting period.</p><p>This distinction is useful because a platform can report a healthy number while the commercial team is looking at something else. The task is to connect the two views clearly enough to decide what to do.</p><h2>Inspect three points in the journey.</h2><h3>1. Who is arriving?</h3><p>Review search intent, targeting and the questions people bring to the campaign. Are they looking for the product, exploring the category or seeking something the business cannot provide? More reach can amplify a targeting problem.</p><h3>2. What are they being promised?</h3><p>Read the ad, the page and the offer together. A strong message should make the relevance easy to understand. If each part introduces a different proposition, the person has to do unnecessary work to connect them.</p><h3>3. What happens next?</h3><p>Follow the journey after the first response. Examine the form, purchase step, email or sales handoff. A campaign might attract relevant people while the next step introduces friction. In that situation, improving the journey could be a more useful next investment than buying additional visits.</p><h2>Choose a test that answers the diagnosis.</h2><p>Once the likely problem is clear, set a bounded test. Name the audience, the change, the owner and the review window. Decide what would count as support for the hypothesis before the test begins.</p><p>If the hypothesis concerns intent, test query controls or targeting. If it concerns clarity, review the message and page. If it concerns follow-up, examine the handoff. Running several unrelated changes together makes it harder to understand which decision affected the outcome.</p><h2>Keep the limits visible.</h2><p>Campaign performance can change with seasonality, demand, the offer and the available data. A short test may suggest a direction without establishing a durable result. A useful review should name those limits and look for supporting evidence from the customer journey and the commercial team.</p><p>Budget can help a working system reach more people. The decision becomes stronger when the system has been examined first.</p>''',
'a-clear-brief':'''<p class="article-lead">A brief is where a marketing decision becomes something other people can deliver.</p><p>It should make the objective, audience, message and approval responsibilities clear enough for a team to move forward. When those questions remain open, production becomes the place where the strategy is negotiated.</p><h2>Revision is sometimes a symptom.</h2><p>Feedback can improve creative work. Repeated revision can also reveal that people are judging the output against different objectives. One person may be looking for category clarity, another for lead volume and another for a preferred visual style.</p><p>At Incuse, I standardized brand kits, review workflows and quality assurance. The approved outcome is a 40% reduction in revision cycles. I use that example to explain why the direction and review process deserve attention alongside the creative itself.</p><p>The number does not mean that every project needs fewer reviews. Some work needs more careful discussion. The useful distinction is between revision that improves the decision and revision caused by avoidable ambiguity.</p><h2>Settle four things before production.</h2><h3>1. What needs to change?</h3><p>State the business objective in concrete terms. Awareness, qualified demand, adoption and retention ask different things of a campaign. A deliverable list does not settle that choice. The objective should help the team understand why the work exists and what a useful outcome would look like.</p><h3>2. Who needs to act?</h3><p>Identify the audience and the decision they are making. Describe the question, objection or need the communication should address. Broad demographic labels can provide context, but the audience’s situation gives the message its direction.</p><h3>3. What should the work communicate?</h3><p>Give the team a central proposition and the evidence supporting it. Identify the necessary claims, brand standards and constraints. This allows creative exploration within a direction that has already been agreed.</p><h3>4. Who owns delivery and approval?</h3><p>Name the person responsible for the next step and the people whose approval is required. Explain what each reviewer is assessing. A technical reviewer, brand reviewer and commercial stakeholder may have different responsibilities; making those responsibilities visible helps the team use feedback.</p><h2>Review against the brief.</h2><p>The review should return to the objective and audience. Does the work communicate the intended proposition? Is the evidence accurate? Is the next action clear? Do the execution and customer experience support the promise?</p><p>Preferences still matter, especially in brand work. They become more useful when connected to a reason the team can evaluate. Feedback such as “this changes the product meaning” gives a clearer basis for revision than an unexplained dislike.</p><h2>Update the brief when the evidence changes.</h2><p>A brief should be usable rather than fixed for its own sake. Customer feedback, new constraints or a changed business priority may justify revisiting it. When that happens, name the change and explain its implications to the people doing the work.</p><p>The leadership task is to keep the team’s direction clear. A well-constructed brief makes that direction visible, and a disciplined review process keeps it connected to delivery.</p>''',
'ai-and-judgment':'''<p class="article-lead">A new tool earns a place when it improves the work or the decision.</p><p>That is the question I use when evaluating AI in marketing. Speed is useful, but the time saved has to be considered alongside review effort, accuracy and whether the output helps the team move forward.</p><h2>Begin with a defined task.</h2><p>AI can support research synthesis, message exploration, analysis and creative production. Each of those tasks needs its own input and review standard. Asking a tool to produce a complete strategy before the business question is clear simply moves the ambiguity into the output.</p><p>At REMIC, I applied AI and automation to marketing operations. The recorded result is a 32% improvement in workflow efficiency. The relevant story is the operational improvement: identifying work that could be supported by automation while keeping the decision and quality checks visible.</p><h2>Separate observation from interpretation.</h2><p>Research summaries should preserve the underlying sources. A customer comment is an observation. A pattern across several comments is an interpretation that needs support. A proposed campaign is a decision made from those inputs.</p><p>Keeping these stages distinct makes the output easier to assess. It also helps the team identify where a tool has filled a gap with an assumption rather than evidence.</p><h2>Give production a clear direction.</h2><p>Creative generation benefits from the same discipline as other production work: an audience, a brief, a central message and standards for review. In HealthCan, the independent concept film, AI supported visual production while the audience, story, character direction and scene planning supplied the creative direction.</p><p>The value of that exercise is in the communication choices and the production exploration. It does not establish the performance of a live healthcare service or a commissioned campaign.</p><h2>Check the total workflow.</h2><p>A faster first draft can still create additional work if the team has to correct claims, reconcile inconsistent versions or rebuild an unusable format. Evaluate the full path from input to approved output.</p><p>A practical review can ask: Was the input accurate? Can the source be traced? Does the output fit the brand and task? How much correction was required? What changed in the final decision?</p><h2>Keep accountability clear.</h2><p>The marketer remains responsible for the published claim, the interpretation and the choice. Tools can extend the work, but ownership still needs a name. That includes deciding when the evidence is insufficient and when a task should be handled directly.</p><p>Useful automation gives the team more room for judgment. Its place in the workflow should be earned by the quality of that result.</p>'''}

ARTICLE_VISUALS = {
    'before-you-increase-the-budget': {
        'file': 'thinking-acquisition.webp',
        'alt': 'Illustrated acquisition path from search through campaign creative, landing page and form to human follow-up',
        'caption': 'Follow the route from intent to handoff before deciding where more spend belongs.',
        'after': '<h2>Inspect three points in the journey.</h2>',
        'infographic': '''<figure class="article-diagram" aria-labelledby="journey-diagram-title"><figcaption><span>Decision map / Acquisition</span><strong id="journey-diagram-title">Where does the journey lose momentum?</strong></figcaption><ol class="diagram-steps diagram-three"><li><span class="diagram-index">01</span><h3>Intent</h3><p>Are the right people arriving?</p></li><li><span class="diagram-index">02</span><h3>Promise</h3><p>Do the ad, page and offer agree?</p></li><li><span class="diagram-index">03</span><h3>Next step</h3><p>Is the form or handoff clear?</p></li></ol><p class="diagram-conclusion">Invest in the weak point the evidence reveals.</p></figure>''',
    },
    'a-clear-brief': {
        'file': 'thinking-brief-illustration.webp',
        'alt': 'Blank brief linked to objective, audience, evidence and approval symbols',
        'caption': 'A useful brief makes four decisions visible before production begins.',
        'after': '<h2>Settle four things before production.</h2>',
        'infographic': '''<figure class="article-diagram" aria-labelledby="brief-diagram-title"><figcaption><span>Working brief / Leadership</span><strong id="brief-diagram-title">Four decisions to make together</strong></figcaption><ol class="diagram-steps diagram-four"><li><span class="diagram-index">01</span><h3>Objective</h3><p>What needs to change?</p></li><li><span class="diagram-index">02</span><h3>Audience</h3><p>Who needs to act?</p></li><li><span class="diagram-index">03</span><h3>Proof</h3><p>What can the message support?</p></li><li><span class="diagram-index">04</span><h3>Owner</h3><p>Who decides and approves?</p></li></ol><p class="diagram-conclusion">Use these answers to review the work, not just to start it.</p></figure>''',
    },
    'ai-and-judgment': {
        'file': 'thinking-ai-judgment.webp',
        'alt': 'Source material enters an AI-assisted process, loops through verification and reaches human approval',
        'caption': 'Automation can move work forward; a person still checks the evidence and owns the decision.',
        'after': '<h2>Check the total workflow.</h2>',
        'infographic': '''<figure class="article-diagram" aria-labelledby="ai-diagram-title"><figcaption><span>Review path / AI and judgment</span><strong id="ai-diagram-title">Trace it before it goes live</strong></figcaption><ol class="diagram-steps diagram-four"><li><span class="diagram-index">01</span><h3>Source</h3><p>Start with traceable inputs.</p></li><li><span class="diagram-index">02</span><h3>Draft</h3><p>Use the tool for a defined task.</p></li><li><span class="diagram-index">03</span><h3>Verify</h3><p>Check claims, fit and corrections.</p></li><li><span class="diagram-index">04</span><h3>Decide</h3><p>A named person approves.</p></li></ol><p class="diagram-conclusion">If a claim cannot be traced, return to the source.</p></figure>''',
    },
}

def articles():
    for slug,(title,tag,deck,asset) in ARTICLES.items():
        editorial = ARTICLE_VISUALS[slug]
        article = ARTICLE_BODIES[slug].replace(editorial['after'], editorial['after'] + editorial['infographic'], 1)
        hero_image = image(editorial['file'], editorial['alt'], eager=True)
        body=f'''<section class="article-hero wrap"><div class="breadcrumb">{link('Thinking','/thinking/')}</div><p class="eyebrow">{tag}</p><h1>{title}</h1><p>{deck}</p><span class="article-byline">By Sreshta Joshi</span></section><article class="article-body"><figure class="article-illustration">{hero_image}<figcaption>{editorial['caption']}</figcaption></figure>{article}<div class="article-related"><h2>Explore the work</h2>{link('REMIC acquisition case','/work/remic/') if slug!='a-clear-brief' else link('Incuse creative operations case','/work/incuse/')}</div></article>{cta()}'''
        page('/thinking/'+slug+'/',title+' | Sreshta Joshi',deck,body,'thinking',primary_image=editorial['file'],article=True)

def aliases():
    # Preserve earlier direct links while giving every current page a clean canonical URL.
    mapping={'case-camfire':'/work/camfire/','case-remic':'/work/remic/','case-minimalance':'/work/minimalance/','case-xipster':'/work/xipster/','case-radhe':'/lab/radhe-dhokla/','project-experiments':'/lab/'}
    for old,new in mapping.items():
        source=OUT/new.strip('/')/'index.html'
        (OUT/old).mkdir(exist_ok=True)
        shutil.copyfile(source,OUT/old/'index.html')
        shutil.copyfile(source,OUT/(old+'.html'))
    for slug in ['about','work','contact']:
        shutil.copyfile(OUT/slug/'index.html',OUT/(slug+'.html'))
    # Keep the former painting-project URL working as the visible title and route change.
    legacy=OUT/'lab'/'echoes'
    legacy.mkdir(parents=True,exist_ok=True)
    legacy.joinpath('index.html').write_text('<!doctype html><html lang="en" data-theme="dark"><head><meta name="color-scheme" content="dark"><meta name="theme-color" content="#11120f"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url=/lab/paintings/"><link rel="canonical" href="'+ORIGIN+'/lab/paintings/"><title>Paintings | Sivence</title></head><body><h1>Paintings</h1><p><a href="/lab/paintings/">View the paintings</a></p></body></html>')
    former=OUT/'lab'/'titanfile'
    former.mkdir(parents=True,exist_ok=True)
    former.joinpath('index.html').write_text('<!doctype html><html lang="en" data-theme="dark"><head><meta name="color-scheme" content="dark"><meta name="theme-color" content="#11120f"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url=/work/titanfile/"><link rel="canonical" href="'+ORIGIN+'/work/titanfile/"><title>TitanFile | Sivence</title></head><body><h1>TitanFile</h1><p><a href="/work/titanfile/">View the assignment</a></p></body></html>')

def finalize():
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN+p}</loc></url>' for p in ROUTES)+'</urlset>')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
    (ROOT/'routes.json').write_text(json.dumps(ROUTES,indent=2))

if __name__=='__main__':
    home();work();thinking();method();about();contact();lab();titanfile_work();articles()
    for slug in CASES:create_case(slug)
    aliases();finalize()
    print(f'Generated {len(ROUTES)} canonical pages; existing assets preserved.')
