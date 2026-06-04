#!/usr/bin/env bash
# 본문(<body> 이하)이 기준 해시와 동일한지 검증한다. SEO head 편집은 허용, 본문 드리프트는 차단.
set -euo pipefail
cd "$(dirname "$0")/.."

sha() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum | awk '{print $1}';
  else shasum -a 256 | awk '{print $1}'; fi
}

cur=$(awk '/<body/{f=1} f' index.html | sha)
exp=$(cat meta/content.sha256)

if [ "$cur" = "$exp" ]; then
  echo "PASS: 본문 동결 유지 ($cur)"
else
  echo "FAIL: 본문 드리프트 감지!"
  echo "  현재: $cur"
  echo "  기준: $exp"
  echo "  -> index.html <body> 이하가 변경됨. 의도된 콘텐츠 갱신이면 meta/content.sha256을 갱신, 아니면 되돌릴 것."
  exit 1
fi
