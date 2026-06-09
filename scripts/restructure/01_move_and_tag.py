import re
h = open("index.html", encoding="utf-8").read()

MOVE = {"cho-ait-lesson":"cho","go-ait-lesson":"go","go-ait-image":"go"}

def extract(html, sid):
    m = re.search(r'<section class="ait-section" id="%s"[^>]*>' % re.escape(sid), html)
    assert m, "section not found: " + sid
    start = m.start()
    end = html.index("</section>", m.end()) + len("</section>")
    blk = html[start:end]
    assert blk.count("<section") == 1 and blk.count("</section>") == 1, "nested section in " + sid
    return start, end, blk

# 1) 이동할 3개 추출 + 태깅 후 제거
blocks = {}
for sid, lvl in MOVE.items():
    s, e, blk = extract(h, sid)
    blk2 = re.sub(r'(<section class="ait-section" id="%s")' % re.escape(sid),
                  r'\1 data-cat="aiclass" data-level="%s"' % lvl, blk, count=1)
    assert 'data-cat="aiclass"' in blk2, "tag failed: " + sid
    blocks[sid] = blk2
    h = h[:s] + h[e:]

# 2) aiclass 컨테이너 닫는 </div> (tool 컨테이너 직전) 앞에 삽입
tpos = h.index('<div class="ait-level" data-level="tool"')
close = h.rindex("</div>", 0, tpos)
insert = "\n" + "\n".join(blocks[k] for k in ["cho-ait-lesson", "go-ait-lesson", "go-ait-image"]) + "\n"
h = h[:close] + insert + h[close:]

# 3) 레벨 컨테이너(cho/jung/go/teuk) 섹션에 data-cat/data-level 태깅
CAT = {"now":"start","start":"start","guide":"start","src":"start",
       "saengbu":"admin","admin":"admin","credit":"admin","freesem":"admin","ncs":"admin"}
def tagrepl(m):
    full, pre, suf = m.group(0), m.group(1), m.group(2)
    if "data-cat=" in full: return full
    cat = CAT.get(suf)
    if not cat: return full
    return full[:-1] + ' data-cat="%s" data-level="%s">' % (cat, pre)
h = re.sub(r'<section class="ait-section" id="(cho|jung|go|teuk)-ait-([a-z0-9]+)"[^>]*>', tagrepl, h)

open("index.html", "w", encoding="utf-8").write(h)

print("moved present:", all(('id="%s"' % s) in h for s in MOVE))
print("aiclass data-cat sections:", len(re.findall(r'<section class="ait-section"[^>]*data-cat="aiclass"', h)))
print("level data-cat tagged:", len(re.findall(r'<section class="ait-section" id="(?:cho|jung|go|teuk)-ait-[a-z0-9]+" data-cat="', h)))
print("total ait-section:", len(re.findall(r'class="ait-section"', h)))
# 이동 후 레벨 컨테이너에 lesson/image 잔존 없어야
for sid in MOVE:
    pos = h.find('id="%s"' % sid)
    cont = h.rfind('data-level="', 0, pos)
    print(f"{sid} now under container level=", h[cont+12:cont+20].split('"')[0])
