# Fomalhaut
### 멀티프로세싱 디스코드 봇


## Changelog
#### 버전명 규칙
**a.b.c.d**
- a - 코드 재작성 등 전체적인 코드에 변화가 생긴 경우
- b - 트위치 API, 봇 코드 등 일부 서비스에 대한 코드에 변화가 생긴 경우
- c - 오류 수정
- d - 기타 변화
  - 핫픽스 등 코드에 아주 약간의 변화만 생긴 경우
  - `./fomalhaut/` 외부 파일의 변화가 생긴 경우
  - 코드 서식, 타겟 정보 등이 변화한 경우

#### 실험용 코드
`./labortary/` 디렉토리에 실험용 코드를 생성합니다.

### 0.1.0.0
- Initial Commit

### 0.1.0.1
- Fomalhaut
  - Kurzgesagt, Kurzgesagt Korea, Veritasium Korea 채널 프로필 이미지 추가

### 0.2.0.0
- All
  - Twitch API 동기화 되지 않는 문제 해결, 캐시 문제 해결
  - 기타 코드 개선
  - 코드 분석 개선

### 0.2.1.0
- All
  - `Instance.process()` 오류 처리 개선
  - `embed.element.ColourElement` 보안 이슈 해결
- Earendel
  - `/what_song` 명령어 코루틴 대기 오류 해결
