# 텍스트 문단 가다듬기 프로그램 설계안

## 1. 프로젝트 개요

### 목적

한 줄당 설정된 길이에 맞춰 한글 텍스트를 자동으로 가다듬어 주는 GUI 애플리케이션 개발

### 주요 기능

- 한글 문자만 카운트하여 텍스트 분할 (공백 제외)
- UI에서 실시간 한 줄당 문자 수 조절 (기본값: 18자)
- 클립보드 복사 기능
- 직관적인 GUI 인터페이스

## 2. 기술 스택

### 개발 환경

- **언어**: Python 3.11+
- **GUI 프레임워크**: PySide6
- **패키지 매니저**: uv
- **빌드 도구**: pyinstaller
- **대상 플랫폼**: Windows

### 주요 라이브러리

- PySide6: GUI 개발
- pyperclip: 클립보드 처리 (대안)

## 3. 프로젝트 구조

```
word_breaker/
├── main.py                    # 애플리케이션 진입점
├── pyproject.toml            # 프로젝트 설정
├── ui/
│   ├── ui_dialog.py          # UI 클래스 (자동 생성)
│   └── untitled.ui           # UI 디자인 파일
├── core/
│   ├── __init__.py
│   └── text_processor.py     # 텍스트 처리 로직
├── utils/
│   ├── __init__.py
│   ├── clipboard_helper.py   # 클립보드 유틸리티
│   └── korean_counter.py     # 한글 문자 카운팅
└── document/
    ├── text_breaker.md       # 기본 요구사항
    └── design.md             # 설계 문서
```

## 4. 클래스 설계

### 4.1 TextBreakerApp (main.py)

- **역할**: 메인 애플리케이션 클래스
- **주요 속성**:
  - `line_length`: 현재 줄 길이 설정값 (기본값: 18)
- **주요 메서드**:
  - `__init__()`: UI 초기화 및 이벤트 연결
  - `apply_formatting()`: 텍스트 가다듬기 실행 (현재 line_length 사용)
  - `copy_to_clipboard()`: 클립보드 복사
  - `update_status()`: 상태 라벨 업데이트
  - `on_line_length_changed()`: 줄 길이 변경 이벤트 처리

### 4.2 TextProcessor (core/text_processor.py)

- **역할**: 텍스트 가다듬기 로직
- **상수**: `DEFAULT_LINE_LENGTH = 18` (기본값)
- **주요 메서드**:
  - `format_text(text: str, line_length: int) -> str`: 메인 처리 함수
  - `split_by_korean_count(text: str, length: int) -> List[str]`: 한글 기준 분할
  - `count_korean_chars(text: str) -> int`: 한글 문자 카운팅

### 4.3 KoreanCounter (utils/korean_counter.py)

- **역할**: 한글 문자 카운팅 유틸리티
- **주요 메서드**:
  - `count_korean(text: str) -> int`: 한글 문자 수 반환
  - `is_korean_char(char: str) -> bool`: 한글 문자 판별

### 4.4 ClipboardHelper (utils/clipboard_helper.py)

- **역할**: 클립보드 처리
- **주요 메서드**:
  - `copy_text(text: str) -> bool`: 텍스트 복사
  - `get_text() -> str`: 클립보드에서 텍스트 가져오기

## 5. 주요 알고리즘

### 5.1 텍스트 가다듬기 알고리즘

```python
DEFAULT_LINE_LENGTH = 18  # 기본값

def format_text(text: str, line_length: int = DEFAULT_LINE_LENGTH) -> str:
    """
    1. 입력 텍스트를 문장 단위로 분리
    2. 각 문장에서 한글 문자만 카운트
    3. 지정된 길이에 도달하면 줄바꿈 삽입
    4. 가능한 경우 단어 경계에서 분할
    5. 최종 텍스트 반환
    """
```

### 5.2 한글 문자 카운팅

```python
import re

def count_korean_chars(text: str) -> int:
    """
    정규식을 사용하여 한글 문자만 카운팅
    유니코드 범위: [\uAC00-\uD7A3] (완성형 한글)
    """
    korean_pattern = re.compile(r'[\uAC00-\uD7A3]')
    return len(korean_pattern.findall(text))
```

## 6. UI 연동 설계

### 6.1 UI 구성 요소

#### 메인 레이아웃

- **텍스트 입력 영역**: 가다듬을 텍스트 입력 (PlainTextEdit)
- **줄 길이 설정 그룹**:
  - 라벨: "줄 길이 설정"
  - SpinBox: 값 조절 (기본값: 18, 범위: 10-100)
  - 현재 값 표시: "현재 줄 길이: {line_length}자"
- **버튼 그룹**: 적용, 복사, 닫기
- **상태 표시 라벨**: 작업 결과 메시지

#### UI 배치 예시

```
┌─────────────────────────────────────┬─────────────┐
│                                     │  [적용]     │
│         텍스트 입력 영역              │  [복사]     │
│                                     │  [닫기]     │
│                                     │             │
│                                     │ 줄 길이 설정 │
│                                     │ [18] [+][-] │
│                                     │ 현재: 18자   │
└─────────────────────────────────────┴─────────────┘
│ 상태: 작업 대기 중...                              │
└───────────────────────────────────────────────────┘
```

### 6.2 버튼 이벤트 처리

- **적용 버튼 (OK)**: `apply_formatting()` 호출 (현재 line_length 사용)
- **복사 버튼 (Save)**: `copy_to_clipboard()` 호출  
- **닫기 버튼 (Close)**: 애플리케이션 종료

### 6.3 상태 표시

- **성공**: "작업 성공! 전체 텍스트 갯수(공백 제외): {count}자 (줄 길이: {line_length}자)"
- **실패**: "작업 실패: {error_message}"

## 7. 기본 설정값

### 7.1 상수 정의

```python
# core/text_processor.py
DEFAULT_LINE_LENGTH = 18        # 기본 한 줄당 한글 문자 수
MIN_LINE_LENGTH = 10           # 최소 줄 길이
MAX_LINE_LENGTH = 100          # 최대 줄 길이
WINDOW_TITLE = "텍스트 문단 가다듬기"
```

## 8. 에러 처리

### 8.1 주요 예외 상황

- 빈 텍스트 입력
- 클립보드 액세스 실패
- 텍스트 처리 오류

### 8.2 에러 처리 전략

```python
try:
    # 텍스트 처리 로직 (현재 설정된 줄 길이 사용)
    result = text_processor.format_text(input_text, self.line_length)
    count = korean_counter.count_korean(result)
    self.update_status(f"작업 성공! 전체 텍스트 갯수: {count}자 (줄 길이: {self.line_length}자)", True)
except Exception as e:
    self.update_status(f"작업 실패: {str(e)}", False)
```

## 9. 빌드 및 배포

### 9.1 개발 명령어

```bash
# 의존성 설치
uv sync

# 개발 실행
uv run python main.py

# 실행파일 빌드
uv run pyinstaller --onefile --windowed --name "텍스트_가다듬기" main.py
```

### 9.2 배포 파일

- 단일 실행파일 (.exe)
- 사용자 매뉴얼

## 10. 개발 단계

### Phase 1: 기본 구조 구현

1. 프로젝트 구조 생성
2. 기본 UI 연동
3. 텍스트 처리 로직 구현

### Phase 2: 기능 완성

1. 클립보드 기능
2. 에러 처리
3. UI/UX 개선

### Phase 3: 최적화 및 빌드

1. 성능 최적화
2. UI/UX 개선
3. 실행파일 빌드

## 11. 테스트 계획

### 11.1 단위 테스트

- 한글 문자 카운팅 정확성
- 텍스트 분할 로직 (다양한 줄 길이)
- UI 줄 길이 조절 기능
- 클립보드 처리 기능

### 11.2 통합 테스트

- UI 이벤트 처리
- 전체 워크플로우
- 에러 상황 처리

### 11.3 사용자 테스트

- 다양한 한글 텍스트 처리
- Windows 환경 호환성
- 성능 테스트
