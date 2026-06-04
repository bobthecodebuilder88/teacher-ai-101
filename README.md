# AI로운 교사생활 (teacher-ai-101)

초중고 교사를 위한 생성형 AI 업무활용 무료 정보 포털. 교육부/교육청 공식자료 기반.
라이브: https://ai101.gyopool.com

## 구조
자체완결 단일 HTML(`index.html`). 외부 의존 없음. GitHub Pages 정적 서빙.

## 콘텐츠 갱신 (진실의 원천은 모노레포)
1. 모노레포 `_projects/ai-teacher-portal/`에서 내용 수정 후 `scripts/build_portal.py`로 `portal.html` 재생성
2. 결과를 이 리포 `index.html`로 복사
3. `awk '/<body/{f=1} f' index.html | shasum -a 256 | awk '{print $1}' > meta/content.sha256` 로 기준 갱신
4. `bash scripts/verify-content-frozen.sh` 통과 확인 후 commit/push -> Actions가 자동 배포

## 정확도
모든 사실은 공식 원문 대조 검증됨(기재요령 PDF 바이너리 눈대조 완료). 본문 임의 수정 금지(`scripts/verify-content-frozen.sh` 게이트).
