# -*- coding: utf-8 -*-
"""SSOT(index.html)에서 SEO 서브페이지를 생성한다. 콘텐츠 무수정(섹션 HTML 축자 재사용)."""
import re, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDX = os.path.join(ROOT, "index.html")
BASE = "https://ai101.gyopooledu.com"
TODAY = datetime.date.today().isoformat()

h = open(IDX, encoding="utf-8").read()

# ---- SSOT 블록 추출 ----
css = h[h.index("<style>") + 7 : h.index("</style>")]
ga_loader = '<script async src="https://www.googletagmanager.com/gtag/js?id=G-PC8M7K7HC4"></script>'
m = re.search(r'<script async src="https://www\.googletagmanager\.com[^>]*></script>\s*<script>(.*?)</script>\s*<script>(.*?)</script>', h, re.S)
assert m, "GA 블록 추출 실패"
ga_init, ga_iife = m.group(1), m.group(2)
tj = re.search(r'// TOOLJS_START(.*?)// TOOLJS_END', h, re.S)
assert tj, "TOOLJS 추출 실패"
tooljs = tj.group(1)

def section(sid):
    sm = re.search(r'<section class="ait-section" id="%s"[^>]*>' % re.escape(sid), h)
    assert sm, "섹션 없음: " + sid
    e = h.index("</section>", sm.end()) + len("</section>")
    return h[sm.start():e]

COPY_JS = """
document.querySelectorAll('.ait-copy').forEach(function(btn){
  btn.addEventListener('click',function(){
    var pre=btn.parentElement.querySelector('.ait-pre'); if(!pre)return;
    var text=pre.innerText, label=btn.textContent;
    function done(ok){btn.textContent=ok?'복사됨':'복사 실패';setTimeout(function(){btn.textContent=label;},1800);}
    function fb(){var ok=false;var ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{ok=document.execCommand('copy');}catch(e){}document.body.removeChild(ta);return ok;}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(function(){done(true);},function(){done(fb());});}else{done(fb());}
  });
});
"""

PAGE_CSS = """
.ait-pg{max-width:var(--maxw);margin:0 auto;padding:18px 22px 40px}
.ait-pg .ait-main{counter-reset:ait-sec}
.ait-crumb{font-size:.85rem;color:var(--muted);margin:6px 0 0}
.ait-crumb a{color:var(--teal-d);text-decoration:none}
.ait-backlink{margin:34px 0 0;font-weight:700}
.ait-backlink a{color:var(--teal-d);text-decoration:none}
.ait-hd .ait-brand a{color:inherit;text-decoration:none}
"""

FOOTER = """<footer class="ait-ft">
  <div class="ait-shell">
    <p class="ait-ft-disc">본 안내는 교육부/교육청 공식 자료를 교사 편의를 위해 재구성한 정보물입니다. 규정의 최종 해석과 기재의 책임은 교사와 학교에 있으며, 실제 적용 전 원문과 소속 시도교육청 지침을 확인하시기 바랍니다.</p>
    <p class="ait-ft-gyo">이 작업들을 더 빠르게 - 전교과 AI 에듀테크 <a href="https://gyopooledu.com/promotion?utm_source=ai101&amp;utm_medium=portal_brand&amp;utm_campaign=subpage" target="_blank" rel="noopener">교풀AI 살펴보기</a></p>
    <p class="ait-ft-meta">만든 곳: 교풀에듀 (주식회사 휴몬랩) · <a href="/">AI로운 교사생활 전체 보기</a></p>
  </div>
</footer>"""

# ---- 페이지 정의 (콘텐츠는 섹션 축자, 메타만 신규) ----
PAGES = [
 dict(path="/go/setuk/", lv="go", cat="admin", crumb="고등학교", sids=["go-ait-saengbu"], spa="#go-ait-saengbu",
      title="고등학교 세특 작성 AI 활용 - 글자수, 금지사항, 프롬프트 | AI로운 교사생활",
      desc="고등 과목별 세특 500자 기준과 AI 활용 경계선. 기재요령상 금지·허용 범위, 바로 쓰는 세특 초안 프롬프트와 자가점검까지 교육부 공식 자료로 정리했습니다."),
 dict(path="/cho/haengbal/", lv="cho", cat="admin", crumb="초등학교", sids=["cho-ait-saengbu"], spa="#cho-ait-saengbu",
      title="초등 생기부 행동특성 및 종합의견(행발) 작성과 AI 활용 | AI로운 교사생활",
      desc="초등 행발·교과 성취수준 기재 원칙과 AI 활용법. 관찰 기록을 바탕으로 한 초안 작성 프롬프트, 기재 금지사항, 검증 체크리스트를 담았습니다."),
 dict(path="/jung/saengbu/", lv="jung", cat="admin", crumb="중학교", sids=["jung-ait-saengbu"], spa="#jung-ait-saengbu",
      title="중학교 생기부·세특 작성 AI 활용 - 성취평가제 기준 | AI로운 교사생활",
      desc="중학교 생기부가 고등과 다른 점(성취평가제·자유학기제), 영역별 글자수, AI로 세특 초안을 잡는 법과 금지선을 교육부 기재요령 기준으로 정리했습니다."),
 dict(path="/jung/free-semester/", lv="jung", cat="admin", crumb="중학교", sids=["jung-ait-freesem"], spa="#jung-ait-freesem",
      title="자유학기제 생기부 기재와 과정중심평가 - AI 활용 | AI로운 교사생활",
      desc="자유학기활동 4영역(진로탐색·주제선택·예술체육·동아리) 각 1,000자 기재 기준과 과정중심평가 운영, AI 활용 포인트를 정리했습니다."),
 dict(path="/go/credit/", lv="go", cat="admin", crumb="고등학교", sids=["go-ait-credit"], spa="#go-ait-credit",
      title="고교학점제 한눈에 - 성취도와 석차등급, 교사가 챙길 것 | AI로운 교사생활",
      desc="2025학년도 고1부터 적용된 고교학점제 평가 구조(성취도 A~E, 석차 5등급)와 학기말 교사 업무, AI 활용 가능 범위를 정리했습니다."),
 dict(path="/go/admin/", lv="go", cat="admin", crumb="고등학교", sids=["go-ait-admin"], spa="#go-ait-admin",
      title="교사 행정업무 AI로 빠르게 - 공문·통신문·계획서 초안 | AI로운 교사생활",
      desc="공문, 가정통신문, 각종 계획서를 AI 초안으로 줄이는 법. 개인정보를 넣지 않는 원칙과 바로 쓰는 행정 프롬프트를 담았습니다."),
 dict(path="/go/lesson/", lv="go", cat="start", crumb="고등학교", sids=["go-ait-lesson"], spa="#go-ait-lesson",
      title="수업자료·평가문항 제작 AI 활용 - 검증 책임과 경계선 | AI로운 교사생활",
      desc="수업자료와 평가문항을 AI로 만들 때의 원칙. 미공개 시험 문항 입력 금지, 성취기준 기반 문항 설계 프롬프트를 정리했습니다."),
 dict(path="/go/image/", lv="go", cat="start", crumb="고등학교", sids=["go-ait-image"], spa="#go-ait-image",
      title="수업용 이미지·미디어 생성 AI 활용법 | AI로운 교사생활",
      desc="수업 자료와 학교 행사 포스터를 이미지 생성 AI로 만드는 법, 저작권과 초상권에서 교사가 지켜야 할 선을 정리했습니다."),
 dict(path="/cho/lesson/", lv="cho", cat="start", crumb="초등학교", sids=["cho-ait-lesson"], spa="#cho-ait-lesson",
      title="초등 수업·평가·가정통신문 AI 활용 - 교사의 도구로 | AI로운 교사생활",
      desc="초등 담임의 전과목 수업 준비, 서술형 평가, 가정통신문을 AI 초안으로 줄이는 법. 학생 직접 사용이 아닌 교사 도구 원칙으로 정리했습니다."),
 dict(path="/teuk/setuk/", lv="teuk", cat="admin", crumb="특성화고", sids=["teuk-ait-saengbu"], spa="#teuk-ait-saengbu",
      title="특성화고 전공 세특 작성 - 전공 적합성과 AI 활용 | AI로운 교사생활",
      desc="특성화고 세특의 본질인 전공 적합성. 보통교과와 전공교과 세특을 직무 역량 중심으로 쓰는 법과 AI 윤문 활용 경계를 정리했습니다."),
 dict(path="/teuk/ncs/", lv="teuk", cat="admin", crumb="특성화고", sids=["teuk-ait-ncs"], spa="#teuk-ait-ncs",
      title="NCS 전문교과·현장실습 기록과 AI 활용 | AI로운 교사생활",
      desc="NCS 능력단위 기반 전공실무 기록, 현장실습 운영과 기록에서 AI를 안전하게 쓰는 법을 특성화고 교사 기준으로 정리했습니다."),
 dict(path="/spec/iep/", lv="spec", cat="special", crumb="특수교육", sids=["spec-ait-iep"], spa="#spec-ait-iep",
      title="IEP(개별화교육계획) 작성과 AI 활용 - 30일 시한·구성요소 | AI로운 교사생활",
      desc="매 학기 30일 이내 IEP 수립, 7가지 구성요소, 개별화교육지원팀 운영까지. 민감정보 비식별 원칙과 AI 윤문 활용법을 정리했습니다."),
 dict(path="/spec/tonghap/", lv="spec", cat="special", crumb="특수교육", sids=["spec-ait-tonghap"], spa="#spec-ait-tonghap",
      title="통합교육·기본교육과정·현장실습 - 특수교사 AI 활용 | AI로운 교사생활",
      desc="통합학급 협력, 기본교육과정과 공통교육과정의 구분, 장애학생 현장실습 4유형을 특수교사 관점에서 AI 활용과 함께 정리했습니다."),
 dict(path="/start/", lv="go", cat="start", crumb="시작하기", sids=["go-ait-start"], spa="#start",
      title="교사를 위한 생성형 AI 처음 시작하기 - LLM·프롬프트 5요소 | AI로운 교사생활",
      desc="AI, 생성형 AI, LLM의 구분부터 할루시네이션의 원리, 좋은 프롬프트의 5요소(역할·맥락·과제·형식·제약)까지 교사 눈높이로 정리했습니다."),
 dict(path="/guide/", lv="go", cat="start", crumb="시작하기", sids=["go-ait-guide"], spa="#start",
      title="교육부·교육청 생성형 AI 공식 가이드라인 정리 | AI로운 교사생활",
      desc="교육부와 시도교육청의 생성형 AI 가이드라인을 3층위로 정리. 학생 연령 기준, 생기부 AI 사용 원칙, 개인정보 보호 기준을 출처와 함께 담았습니다."),
 dict(path="/rubric/", lv="go", cat="eval", crumb="평가", sids=["rubric-ait-what","rubric-ait-make","rubric-ait-curri","rubric-ait-template","rubric-ait-src"], spa="#eval",
      title="분석적 루브릭(채점기준표) 만드는 법 - 템플릿과 프롬프트 | AI로운 교사생활",
      desc="평가 요소별로 채점하는 분석적 루브릭을 성취기준에서 출발해 만드는 절차. 빈 템플릿, 진술문 작성 원칙, 바로 쓰는 프롬프트를 담았습니다."),
 dict(path="/jungjeom/", lv="go", cat="jungjeom", crumb="AI중점학교", sids=["jungjeom-ait-now","jungjeom-ait-jungjeom","jungjeom-ait-budget","jungjeom-ait-run","jungjeom-ait-safe","jungjeom-ait-src"], spa="#jungjeom",
      title="AI중점학교 운영 가이드 - 지정 의무·예산·연수·학생 안전 | AI로운 교사생활",
      desc="AI중점학교 담당 교사를 위한 운영 정보. 지정 의무와 시수, 특별교부금 집행, 교원연수, 학생 AI 안전 기준을 교육부 공식 자료로 정리했습니다."),
 dict(path="/tools/byte-counter/", lv="go", cat="tool", crumb="도구", sids=["tool-ait-counter"], spa="#tool-ait-counter", tool=True,
      title="생기부 글자수·Byte 카운터 - NEIS 한글 3Byte 영역별 한도 | AI로운 교사생활",
      desc="학교급과 영역을 고르면 한도 대비 글자수와 NEIS Byte(한글 1자 3Byte)를 실시간으로 계산합니다. 입력 내용은 저장되지 않습니다. 무료, 로그인 없음."),
 dict(path="/tools/forbidden-checker/", lv="go", cat="tool", crumb="도구", sids=["tool-ait-forbidden"], spa="#tool-ait-forbidden", tool=True,
      title="생기부 금지표현 점검기 - 어학시험·교외수상 자동 확인 | AI로운 교사생활",
      desc="생기부 초안을 붙여넣으면 어학시험, 교외 수상, 자격증, 특수문자 등 기재 금지·주의 표현을 표시합니다. 브라우저에서만 처리되고 저장되지 않습니다."),
 dict(path="/tools/deidentify/", lv="go", cat="tool", crumb="도구", sids=["tool-ait-deid"], spa="#tool-ait-deid", tool=True,
      title="개인정보 비식별 도우미 - AI에 넣기 전 학생 이름 치환 | AI로운 교사생활",
      desc="AI에 글을 넣기 전에 학생 이름을 학생A, 학생B로 바꿔 줍니다. 치환 결과는 반드시 눈으로 확인하세요. 브라우저에서만 처리됩니다."),
 dict(path="/tools/group-maker/", lv="go", cat="tool", crumb="도구", sids=["tool-ait-group"], spa="#tool-ait-group", tool=True,
      title="모둠 편성·랜덤 뽑기 - 학생 명단으로 바로 | AI로운 교사생활",
      desc="학생 명단을 붙여넣으면 모둠을 무작위로 나누거나 발표자를 뽑아 줍니다. 로그인 없이 브라우저에서 바로 쓰는 무료 도구입니다."),
 dict(path="/tools/timer/", lv="go", cat="tool", crumb="도구", sids=["tool-ait-timer"], spa="#tool-ait-timer", tool=True,
      title="수업 타이머 - 활동 시간 카운트다운 | AI로운 교사생활",
      desc="활동 시간을 정해 카운트다운하고 끝나면 소리로 알려 줍니다. 모둠 활동, 발표, 시험 대비에 로그인 없이 바로 쓰세요."),
]

def build_page(p):
    secs = "\n".join(section(s) for s in p["sids"])
    url = BASE + p["path"]
    ld = ('{"@context":"https://schema.org","@type":"Article","headline":%s,"description":%s,'
          '"inLanguage":"ko-KR","mainEntityOfPage":%s,"publisher":{"@type":"Organization","name":"교풀에듀"},"dateModified":"%s"}'
          ) % (jstr(p["title"]), jstr(p["desc"]), jstr(url), TODAY)
    crumb_ld = ('{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
                '{"@type":"ListItem","position":1,"name":"AI로운 교사생활","item":"%s/"},'
                '{"@type":"ListItem","position":2,"name":%s,"item":%s}]}') % (BASE, jstr(p["crumb"]), jstr(url))
    tool_block = ("<script>" + tooljs + "</script>") if p.get("tool") else ""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<script>if(location.protocol==="http:"&&/gyopooledu\\.com$/.test(location.hostname)){{location.replace("https://"+location.host+location.pathname+location.search+location.hash);}}</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]}</title>
<meta name="description" content="{p["desc"]}">
<link rel="canonical" href="{url}">
<meta name="naver-site-verification" content="907490e7ae9a76f6450bfe3cab721e0ad26e86c1" />
<meta property="og:type" content="article">
<meta property="og:site_name" content="AI로운 교사생활">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{p["desc"]}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script type="application/ld+json">{ld}</script>
<script type="application/ld+json">{crumb_ld}</script>
{ga_loader}
<script>{ga_init}</script>
<script>window.__aitState={{cat:"{p["cat"]}",lv:"{p["lv"]}"}};</script>
<script>{ga_iife}</script>
<style>{css}{PAGE_CSS}</style>
</head>
<body>
<header class="ait-hd">
  <div class="ait-shell ait-hd-in">
    <p class="ait-brand"><a href="/">AI로운 교사생활</a></p>
    <p class="ait-free">무료 · 교육부/교육청 공식 자료 기반</p>
  </div>
</header>
<div class="ait-pg">
  <nav class="ait-crumb" aria-label="현재 위치"><a href="/">AI로운 교사생활</a> &rsaquo; {p["crumb"]}</nav>
  <main class="ait-main">
{secs}
  </main>
  <p class="ait-backlink"><a href="/{p["spa"]}">포털 전체에서 이어 보기 &#8594;</a></p>
</div>
{FOOTER}
<script>{COPY_JS}</script>
{tool_block}
</body>
</html>
"""

def jstr(s):
    import json
    return json.dumps(s, ensure_ascii=False)

written = []
for p in PAGES:
    out = os.path.join(ROOT, p["path"].strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(build_page(p))
    written.append(p["path"])

# sitemap
urls = [f"  <url>\n    <loc>{BASE}/</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>"]
for p in PAGES:
    urls.append(f"  <url>\n    <loc>{BASE}{p['path']}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")

print(f"빌드 완료: {len(written)} 페이지 + sitemap({len(urls)} URL)")
for w in written: print(" ", w)
