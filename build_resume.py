from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).parent
OUT=ROOT/'dist/assets/Sreshta-Joshi-Resume.pdf'
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='NameX',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=colors.HexColor('#172017'),spaceAfter=7))
styles.add(ParagraphStyle(name='KickerX',fontName='Helvetica-Bold',fontSize=9,leading=13,textColor=colors.HexColor('#9c3d19'),spaceAfter=8))
styles.add(ParagraphStyle(name='SectionX',fontName='Helvetica-Bold',fontSize=10,leading=13,textColor=colors.HexColor('#9c3d19'),spaceBefore=15,spaceAfter=8))
styles.add(ParagraphStyle(name='RoleX',fontName='Helvetica-Bold',fontSize=10,leading=13,spaceBefore=10,spaceAfter=3))
styles.add(ParagraphStyle(name='TextX',fontName='Helvetica',fontSize=9,leading=13,spaceAfter=5))
styles.add(ParagraphStyle(name='BulletX',fontName='Helvetica',fontSize=9,leading=12.5,leftIndent=9,firstLineIndent=-9,spaceAfter=4))
story=[]
def p(text,style='TextX'):story.append(Paragraph(text,styles[style]))
def section(text):p(text,'SectionX')
def role(company,title,dates,bullets):
 p(company+' <font color="#626b61">| '+dates+'</font>','RoleX');p(title)
 for text in bullets:p('• '+text,'BulletX')
def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#d5dbd0'));canvas.line(40,35,572,35);canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#626b61'));canvas.drawString(40,22,'Sreshta Joshi  |  sivencestudio.com');canvas.drawRightString(572,22,str(doc.page));canvas.restoreState()
p('SRESHTA JOSHI, MBA','NameX');p('GROWTH, BRAND &amp; LIFECYCLE MARKETING','KickerX')
p('Toronto, ON  |  +1 437 606 0757  |  <link href="mailto:joshisreshta@gmail.com">joshisreshta@gmail.com</link><br/><link href="https://www.linkedin.com/in/sreshtajoshi/">linkedin.com/in/sreshtajoshi</link>  |  <link href="https://sivencestudio.com">sivencestudio.com</link>')
section('PROFESSIONAL SUMMARY')
p('Marketing leader with 14+ years across SaaS, financial education, healthcare client engagements, agencies and consumer brands in B2B and B2C markets. Connects business priorities with positioning, integrated campaigns and customer journeys. Leads cross-functional teams, coordinates international agencies, manages marketing investment and stays directly involved in creative delivery, analytics, AI and automation.')
section('CORE COMPETENCIES')
p('<b>Strategy &amp; leadership:</b> Marketing strategy, go-to-market, team leadership, budget and ROI analysis.<br/><b>Growth &amp; brand:</b> Paid acquisition, demand generation, positioning, integrated marketing and product launches.<br/><b>Lifecycle &amp; operations:</b> CRM, email, loyalty, retention, creative operations, analytics, AI and automation.')
section('PROFESSIONAL EXPERIENCE')
role('INCUSE DIGITAL','Marketing &amp; Brand Consulting Manager','2024–Present',[
'Led an eight-person team supporting fintech, real estate and healthcare marketing across Canada, the U.S. and Dubai.',
'Partnered with executives on positioning, go-to-market, channel plans and campaign KPIs.',
'Standardized brand kits, review workflows and quality assurance, reducing creative revision cycles by 40%.'])
role('REMIC','Manager, Marketing','2025',[
'Rebuilt Google Search and Performance Max using value-based bidding and tighter query controls: 45,800 clicks, 2,260 tracked conversions, $35 CPA and a 21% CTR improvement.',
'Delivered integrated email, social, web and landing-page campaigns, including the Canadian Mortgage Summit and Awards.',
'Worked across newsletters, cart recovery, retargeting, webinars and direct mail; AI and automation improved marketing workflow efficiency by 32%.'])
role('VENUEVISION / XIPSTER','Digital Marketing Specialist','2023–2024',[
'Increased B2B lead generation by 28% through integrated email, SEO, social and paid-media marketing.',
'Worked with Sales leadership on product communication, competitive research and acquisition recommendations.'])
role('CAMFIRE MEDIA','Senior Manager, Digital Marketing','2023',[
'Directed marketing across eight brands with a $2.7M budget, a seven-person team and agencies across four countries.',
'Campaigns influenced $7.2M in pipeline and improved marketing ROI by 27%; testing reduced CPC by 18% and increased conversions by 10%.',
'Delivered activation, engagement and retention programs across CRM, email and push marketing.'])
story.append(PageBreak())
p('EXPERIENCE &amp; CAPABILITIES','KickerX')
role('BHATT BROS','Senior Manager, Marketing, Brand Management &amp; Communication','2021–2023',[
'Led brand, communications and go-to-market for a B2B textile-machinery manufacturer.',
'Led the market introduction of the Stabilo Relax Dryer, connecting the story with the joint venture with Italy’s ALEA Impianti Tessili.',
'Broader marketing work opened two regional markets, reduced cost per lead by 20% and grew the active customer base by 15%.'])
role('DESJARDINS GENERAL INSURANCE','Sales &amp; Loyalty, Property &amp; Casualty Agent','2018–2019',[
'Supported customer retention through coverage reviews, renewals, needs analysis and service across phone and digital channels.'])
role('MINIMALANCE','Senior Manager, Marketing &amp; Brand Strategy','2012–2018',[
'Connected positioning and launch activity across digital, print, events and PR; exceeded the acquisition target by 150% within 90 days.',
'Generated $800K in first-year revenue, with go-to-market, procurement, sales, customer service and operations in scope.',
'Collaborated with Engineering, Sales and Communications on brand and customer experience.'])
role('MERCEDES-BENZ','Assistant Aftersales Manager','2011–2012',[
'Improved owner retention by 20% through service reminders, referral rewards, owner events and customer feedback.',
'Supported daily KPI tracking and customer-care scorecards for dealership management.'])
section('SELECTED CLIENT ENGAGEMENTS AT INCUSE')
p('<b>SoalTech:</b> Nine-month health-tech engagement covering competitor research, brand guidelines, positioning and UI/UX for a clinic and patient platform.')
p('<b>AutoReel:</b> Growth audit across SEO, CRO, lifecycle, paid media and messaging, with a phased 90-day funnel plan.')
section('EDUCATION &amp; TRAINING')
p('<b>MBA, Marketing</b> — Nirma University, 2011<br/><b>Bachelor of Commerce</b> — Gujarat University, 2009<br/><b>Digital Marketing</b> — University of Toronto School of Continuing Studies, 2023<br/>Google Ads Search Certification; Google Analytics Individual Qualification<br/>Mortgage Brokers, Bankers and Agents course — REMIC, 2020<br/>Other Than Life Insurance course — Insurance Institute of Canada, 2019')
section('TECHNOLOGY')
p('<b>Paid media &amp; analytics:</b> Google Ads, Meta Ads, LinkedIn Ads, GA4, Google Tag Manager, Looker Studio, Google Search Console.<br/><b>SEO, web &amp; commerce:</b> SEMrush, Ahrefs, Similarweb, WordPress, Shopify.<br/><b>CRM &amp; automation:</b> HubSpot, Salesforce, Zoho CRM, Customer.io, Klaviyo, Mailchimp, Zapier, n8n.<br/><b>AI &amp; creative:</b> ChatGPT, Claude, Gemini, ElevenLabs, Midjourney, Runway, HeyGen, Canva, Adobe, MS Office.')
SimpleDocTemplate(str(OUT),pagesize=(612,792),rightMargin=40,leftMargin=40,topMargin=35,bottomMargin=47,title='Sreshta Joshi — Growth, Brand & Lifecycle Marketing',author='Sreshta Joshi').build(story,onFirstPage=footer,onLaterPages=footer)
from pypdf import PdfReader
count=len(PdfReader(OUT).pages)
assert count==2, f'Resume must be 2 pages, got {count}'
print(f'Created {OUT.name}: {count} pages')
