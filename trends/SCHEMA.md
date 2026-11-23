# production.json — trends-v2

GPT가 만드는 ZIP의 `production.json`은 이 형식을 따른다. 파이프라인은 이 파일만 보고 음성·화면·자막을 자동으로 만든다.

```json
{
  "schema": "trends-v2",
  "job_id": "US-YT-2026-11-22-taylor-cma",
  "mode": "YOUTUBE_TRENDS",
  "country": "US",
  "language": "en",
  "voice_style": "pop_culture",
  "theme": "stage",
  "accent": "#FF78A0",
  "header": "US YOUTUBE TRENDS · NOV 22, 2026",
  "title": "Taylor Swift's 13-Year CMA Comeback Had a Twist #shorts",
  "description": "...",
  "first_comment": "...",
  "sentences": [
    {"id": 1, "delivery": "excited", "chunks": [
      {"spoken": "Thirteen years.", "caption": "13 years."},
      {"spoken": "That's how long it had been", "caption": "That's how long it had been"}
    ]}
  ],
  "scenes": [
    {"sentences": [1], "layout": "hero_number", "source": "Sources: AP · NBC News", "fact_ids": ["F01"],
     "data": {"kicker": "CMA AWARDS STAGE", "number": "13", "count_up": true,
              "label": "YEARS SINCE HER LAST CMA PERFORMANCE", "sub": "2013 → NOV 18, 2026"}}
  ]
}
```

## 필드

| 필드 | 값 |
|---|---|
| country | US, IN, ID, BR, MX |
| language | en, hi, id, pt, es |
| voice_style | pop_culture, sports, lifestyle_viral, tech_business, serious_news |
| theme | stage(음악·연예), stadium(미식축구·농구·축구 등), pitch(크리켓), news(일반 뉴스·정치·경제), tech(기술·게임), viral(밈·생활) |
| accent | 이슈에 맞는 강조색 hex (팀 색, 브랜드 느낌 등). 생략 가능 |
| header | 화면 상단 고정 문구. 채널 언어로, 현지 날짜 포함 |
| delivery | normal, excited, shouting, curious, calm (음성 감정 지시. 읽지 않음) |

## 문장과 chunk

- 문장은 4~8개. 각 문장은 chunk 2~4개로 나눈다. chunk 하나가 자막 한 화면이다.
- `spoken`은 읽는 글(숫자는 단어로), `caption`은 자막(숫자 표기). 같은 뜻이어야 한다.
- chunk의 caption은 영어 기준 6단어 이하, 힌디어 5단어 이하.
- 모든 문장의 spoken을 이어 붙이면 내레이션 전체가 된다. 따옴표·괄호는 spoken에 넣지 않는다.

## scenes

- 장면 4~7개. 각 장면은 `sentences`에 연속된 문장 번호를 넣는다. 모든 문장이 순서대로 한 번씩 쓰여야 한다.
- 화면 문구는 모두 facts.json으로 확인된 내용만. `fact_ids`에 근거를 적는다.
- `source`: 화면 하단 작은 출처 문구 (예: "Source: ESPNcricinfo"). 없으면 생략.
- `stamp`(선택, 모든 레이아웃): `{"text": "THE TWIST", "color": "red", "at_chunk": 0}` — 장면 안에서 몇 번째 chunk가 시작될 때 찍힐지(0부터).
- 색 이름: accent, red, green, blue, gold, pink, teal, orange, white, 또는 hex.

### layout 종류와 data

**title_card** — 큰 문구 카드
`{"kicker": "OPENED BACKSTAGE", "lines": ["“I Knew It,", "I Knew You”"], "sub": "from the Toy Story 5 soundtrack"}`

**hero_number** — 큰 숫자 하나
`{"kicker": "Tilak Varma", "number": "100", "count_up": true, "label": "runs", "sub": "India A", "color": "orange"}`

**scoreboard** — 두 팀/두 대상 점수
`{"kicker": "Nov 22, 2026 · Doha", "rows": [{"name": "Pakistan Shaheens", "score": "313", "sub": "49.2 overs", "color": "green"}, {"name": "India A", "score": "265", "sub": "49.1 overs", "color": "blue"}], "banner": "Pakistan won by 48 runs", "banner_at_chunk": 1}`

**bars** — 항목별 막대
`{"title": "Pakistan Shaheens 313", "sub": "batting first", "items": [{"label": "Hasan Nawaz", "value": 79}, {"label": "Maaz Sadaqat", "value": 59}], "max": 90, "start_chunk": 0}`

**progress** — 목표 대비 진행 (추격, 득표, 목표 금액 등)
`{"title": "India A · target 314", "max": 330, "target": 314, "target_label": "314", "from": 0, "value": 129, "value_fmt": "{v}/{p}", "pips_total": 10, "pips_from": 0, "pips": 6, "start_chunk": 1}`
- 값이 `from`에서 `value`로, 점이 `pips_from`에서 `pips`로 start_chunk부터 차오른다. `value_fmt`의 {v}=값, {p}=채워진 점 수.

**versus** — 두 대상 비교 카드
`{"title": "MASHUP", "left": {"top": "2026", "lines": ["“I Knew It,", "I Knew You”"], "color": "pink"}, "right": {"top": "2006", "lines": ["“Our Song”"], "color": "gold"}, "right_at_chunk": 1, "chip": "Keith Urban on banjo", "chip_at_chunk": 0}`

**list_card** — 목록/후보/결과
`{"title": "CMA SINGLE OF THE YEAR", "rows": [{"tag": "NOMINEE", "text": "“I Knew It, I Knew You”"}, {"tag": "WINNER", "text": "Ella Langley — “Choosin’ Texas”", "highlight": true}]}`

**trend_card** — 마지막 근거 카드 (트렌드/차트)
`{"platform": "Google Trends · India", "query": "pakistan a vs india a", "big": "2M+", "sub": "searches · past 24 hours", "chip": "#1 by search volume", "observed": "Captured Nov 23, 4:24 AM IST"}`
- YouTube Trends면 `{"platform": "YouTube Charts · United States", "title": "TRENDING MUSIC", "big": "#1", "query": "“I Knew It, I Knew You”", "sub": "Taylor Swift · uploaded Nov 19, 2026", "observed": "Observed Nov 22, 2026 · 3:02 PM PT"}`

## 같은 틀 반복 금지

- 연속된 영상에서 같은 layout 순서를 반복하지 않는다. 소재에 맞는 layout을 고르고, theme·accent를 이슈에 맞게 바꾼다.
- 마지막 장면은 보통 trend_card로 "왜 지금 화제인지"의 근거를 보여준다.
