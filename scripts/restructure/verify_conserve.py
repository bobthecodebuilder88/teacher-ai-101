import re, sys
EXPECT = {  # 2026-06-10 baseline (AI중점학교 탭 포함)
    "copy": (r'class="[^"]*ait-copy', 95),
    "cta": (r'class="[^"]*ait-cta', 58),
    "blank": (r'target="_blank"', 760),
    "utm": (r'utm_source=ai101', 294),
    "chip": (r'class="[^"]*ait-chip', 19),
    "panel": (r'class="[^"]*ait-subpanel', 20),
}
h = open(sys.argv[1] if len(sys.argv) > 1 else "index.html", encoding="utf-8").read()
ok = True
for k, (pat, exp) in EXPECT.items():
    n = len(re.findall(pat, h))
    flag = "OK" if n == exp else "FAIL"
    if n != exp: ok = False
    print(f"[{flag}] {k}: {n} (expect {exp})")
secs = len(re.findall(r'class="ait-section"', h))
print(f"[{'OK' if secs == 49 else 'FAIL'}] sections: {secs} (expect 49)")
if secs != 49: ok = False
# 정확도 가드
gem = re.findall(r'Gemini.{0,40}?13\s*세', h)
print(f"[{'OK' if gem else 'WARN'}] Gemini 13세 유지: {len(gem)}건")
dash = len(re.findall(r'[–—]', h))
print(f"[{'OK' if dash==0 else 'FAIL'}] em/en dash: {dash} (expect 0)")
if dash: ok = False
curly = len(re.findall(r'[‘’“”]', h))
print(f"[{'OK' if curly==0 else 'FAIL'}] 곡선따옴표: {curly} (expect 0)")
if curly: ok = False
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
