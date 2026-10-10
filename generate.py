import os, json, html, datetime, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
root=Path(__file__).parent
queries={'AI & Software':'AI agents software development','Creators & Marketing':'Instagram video advertising creator economy','Vietnam & Manufacturing':'Vietnam European manufacturing investment','Science & Society':'robotics science economics discoveries'}
candidates=[]
for category,q in queries.items():
 url='https://news.google.com/rss/search?q='+urllib.parse.quote(q+' when:7d')+'&hl=en-US&gl=US&ceid=US:en'
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'CuriosityFeed/1.0'})
  with urllib.request.urlopen(req,timeout=25) as r: feed=ET.fromstring(r.read())
  for item in feed.findall('.//item')[:20]:
   title=item.findtext('title','').strip(); link=item.findtext('link','').strip()
   if title and link: candidates.append({'title':title,'url':link,'category':category})
 except Exception as e: print('Feed error',category,e)
if len(candidates)<15: raise RuntimeError('Insufficient feed results; preserving last edition')
key=os.environ['OPENAI_API_KEY']
body={'model':'gpt-4.1-mini','response_format':{'type':'json_object'},'messages':[{'role':'system','content':'Return valid JSON with a stories array of exactly 10 unique entries. Choose from supplied candidates only. Each entry must have url, summary, why. Be cautious: only headlines are provided, not full articles. Keep descriptions concise and avoid unverified specifics.'},{'role':'user','content':json.dumps({'interests':'AI, entrepreneurship, Vietnam-Europe manufacturing, economics, science, culture and surprising discoveries','candidates':candidates})}]}
req=urllib.request.Request('https://api.openai.com/v1/chat/completions',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
with urllib.request.urlopen(req,timeout=120) as r: answer=json.load(r)
selected=json.loads(answer['choices'][0]['message']['content'])['stories']
lookup={x['url']:x for x in candidates}; stories=[]; seen=set()
for s in selected:
 url=s.get('url')
 if url in lookup and url not in seen:
  seen.add(url); stories.append({**lookup[url],'summary':str(s.get('summary',''))[:500],'why':str(s.get('why',''))[:250]})
if len(stories)!=10: raise RuntimeError('Model did not return exactly 10 valid unique stories')
today=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
archive=root/'archive'; archive.mkdir(exist_ok=True)
def e(s): return html.escape(str(s),quote=True)
blocks=''.join(f'<article><small>{i:02d} / {e(s["category"])}</small><h2>{e(s["title"])}</h2><p>{e(s["summary"])}</p><p class="why">{e(s["why"])}</p><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">Read original ↗</a></article>' for i,s in enumerate(stories,1))
previous=''.join(f'<a href="archive/{p.stem}.html">{p.stem}</a> ' for p in sorted(archive.glob('????-??-??.html'),reverse=True) if p.stem!=today)
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0d1118"><title>Curiosity — {today}</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#0d1118;color:#f2f6fa;font:17px/1.65 -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif}}main{{max-width:750px;margin:auto;padding:55px 24px 100px}}h1{{font-size:clamp(46px,9vw,74px);line-height:1.05;letter-spacing:-.05em}}h2{{font-size:26px;line-height:1.25}}small{{color:#9ce8c1;letter-spacing:.15em;text-transform:uppercase;font-weight:bold}}p{{color:#afbbca}}.why{{color:#d3e6db}}article{{border-top:1px solid #35404e;padding:28px 0}}a{{color:#9ce8c1;text-underline-offset:4px}}footer{{font-size:13px;color:#8998a9;margin-top:55px}}</style></head><body><main><small>Curiosity / {today}</small><h1>Your world,<br>curated.</h1><p>Ten stories worth your attention. Less noise, more ideas.</p>{blocks}<h2>Archive</h2>{previous or '<p>First edition.</p>'}<footer>AI-curated from public news headlines, not full article text. Verify claims with original publishers.</footer></main></body></html>'''
(root/'index.html').write_text(page,encoding='utf-8');(archive/(today+'.html')).write_text(page,encoding='utf-8');(root/'stories.json').write_text(json.dumps({'date':today,'stories':stories},ensure_ascii=False,indent=2),encoding='utf-8')
print('Published',today)
