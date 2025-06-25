# 프로젝트 수정 계획서

## 개요

`document/additional_function.md`에 명시된 요구사항을 반영하여 현재 프로젝트를 수정하는 계획서입니다.

## 요구사항 분석

### 1. 마침표 기준 문장 분리 기능

- **요구사항**: 마침표를 기준으로 문장을 빈 행으로 분리
- **UI 변경**: 체크박스 추가 (기본 선택, 줄길이 설정 위에 배치)
- **로직 변경**: TextProcessor에 마침표 분리 기능 추가

### 2. 문자 카운팅 방식 변경

- **기존**: 한글 문자만 카운팅 (공백 제외)
- **변경**: 모든 문자 카운팅 (숫자, 영어, 특수문자 포함, 공백 제외)
- **영향 범위**: TextProcessor, 상태 표시, 테스트 케이스

### 3. 초기화 버튼 추가

- **위치**: 복사 버튼 바로 아래
- **기능**: text_area 내용 제거

### 4. 최소화 버튼 추가

- **위치**: 우측 상단 닫기 버튼(X) 왼쪽
- **구현**: WindowFlags 설정

## 파일별 수정 계획

### 1. 새로운 파일 생성

#### `utils/text_counter.py`

```python
"""
모든 문자 카운팅 유틸리티
기존 korean_counter.py를 대체하여 사용
korean_counter.py는 호환성을 위해 유지하되 미사용 상태
"""

def count_all_chars(text: str) -> int:
    """모든 문자 카운팅 (공백 제외)"""
    if not text:
        return 0
    return len([char for char in text if char != ' '])
    
def count_visible_chars(text: str) -> int:
    """보이는 문자만 카운팅 (공백, 탭, 개행 제외)"""
    if not text:
        return 0
    return len([char for char in text if char.strip()])
    
def is_visible_char(char: str) -> bool:
    """보이는 문자 판별 (공백, 탭, 개행이 아닌 문자)"""
    if not char or len(char) != 1:
        return False
    return char.strip() != ''

def count_korean(text: str) -> int:
    """
    한글 문자 카운팅 (호환성 유지용)
    기존 korean_counter.count_korean과 동일한 기능
    """
    import re
    if not text:
        return 0
    korean_pattern = re.compile(r"[\uAC00-\uD7A3]")
    korean_chars = korean_pattern.findall(text)
    return len(korean_chars)
```

### 2. 기존 파일 수정

#### `core/text_processor.py`

**import 변경**:

```python
# 기존
from utils.korean_counter import count_korean

# 변경
from utils.text_counter import count_all_chars, count_korean
```

**추가할 메서드**:

```python
def format_text_with_options(self, text: str, line_length: int, 
                           use_all_chars: bool = True, 
                           separate_sentences: bool = True) -> str:
    """옵션을 고려한 텍스트 가다듬기"""
    if not text.strip():
        return ""
    
    # 마침표 분리 처리
    if separate_sentences:
        text = self.separate_sentences_by_period(text)
    
    # 문자 카운팅 방식에 따른 분할
    if use_all_chars:
        lines = self.split_by_all_chars(text, line_length)
    else:
        lines = self.split_by_korean_count(text, line_length)
    
    return "\n".join(lines)

def split_by_all_chars(self, text: str, length: int) -> List[str]:
    """모든 문자 기준으로 분할"""

def separate_sentences_by_period(self, text: str) -> str:
    """마침표 기준 문장 분리 (마침표 뒤에 빈 행 추가)"""
    import re
    # 마침표 뒤에 공백이나 줄바꿈이 있는 경우 빈 행 추가
    pattern = r'(\.)(\s*)'
    return re.sub(pattern, r'\1\n\n', text)
```

**수정할 메서드**:

```python
def count_korean_chars(self, text: str) -> int:
    """
    텍스트의 한글 문자 수를 카운트합니다. (호환성 유지)
    """
    from utils.text_counter import count_korean
    return count_korean(text)

def count_all_chars(self, text: str) -> int:
    """
    텍스트의 모든 문자 수를 카운트합니다. (공백 제외)
    """
    from utils.text_counter import count_all_chars
    return count_all_chars(text)
```

**기존 메서드 유지**:

- `format_text()`: 기본 동작 유지 (호환성)
- `split_by_korean_count()`: 기존 이름 유지 (호환성)

#### `ui/untitled.ui`

**추가할 컨트롤**:

```xml
<!-- 마침표 분리 체크박스 -->
<widget class="QCheckBox" name="sentence_separation_checkbox">
    <property name="geometry">
        <rect><x>530</x><y>140</y><width>81</width><height>20</height></rect>
    </property>
    <property name="text"><string>마침표 분리</string></property>
    <property name="checked"><bool>true</bool></property>
</widget>

<!-- 초기화 버튼 -->
<widget class="QPushButton" name="clear_button">
    <property name="geometry">
        <rect><x>530</x><y>100</y><width>81</width><height>25</height></rect>
    </property>
    <property name="text"><string>초기화</string></property>
</widget>
```

**레이아웃 조정**:

- 기존 컨트롤들의 Y 좌표 조정
- 체크박스와 초기화 버튼 공간 확보
- 기존 Dialog의 크기는 유지하는 것이 조건

#### `main.py`

**클래스 속성 추가**:

```python
class TextBreakerApp(QDialog):
    def __init__(self):
        # 기존 코드
        self.use_all_chars = True  # 모든 문자 카운팅 사용
        self.separate_sentences = True  # 마침표 분리 사용
```

**새로운 메서드 추가**:

```python
def _setup_sentence_separation_checkbox(self):
    """마침표 분리 체크박스 설정"""

def _setup_clear_button(self):
    """초기화 버튼 설정"""

def _setup_minimize_button(self):
    """최소화 버튼 설정"""

def on_sentence_separation_changed(self, state):
    """마침표 분리 체크박스 이벤트"""

def clear_text_area(self):
    """텍스트 영역 초기화"""

def show_minimized_window(self):
    """창 최소화"""
```

**수정할 메서드**:

```python
def apply_formatting(self):
    # 새로운 옵션들을 반영한 텍스트 처리
    result = self.text_processor.format_text_with_options(
        input_text, 
        self.line_length,
        use_all_chars=self.use_all_chars,
        separate_sentences=self.separate_sentences
    )
    
    # 상태 표시도 모든 문자 카운팅으로 변경
    char_count = self.text_processor.count_all_chars(result)
    self.update_status(
        f"작업 성공! 전체 텍스트 갯수(공백 제외): {char_count}자 (줄 길이: {self.line_length}자)",
        True
    )
```

**호환성 유지 정책**:

```python
# 기존 한글 카운팅 방식도 계속 지원
def apply_formatting_korean_only(self):
    """한글 카운팅 방식 (기존 방식, 호환성 유지)"""
    result = self.text_processor.format_text(input_text, self.line_length)
    korean_count = self.text_processor.count_korean_chars(result)
    # 기존 방식으로 상태 표시
```

### 3. 테스트 파일 수정

#### `test/test_text_counter.py` (신규)

```python
"""
text_counter 모듈의 모든 함수에 대한 테스트
korean_counter의 기능도 포함하여 테스트
"""

class TestTextCounter:
    def test_count_all_chars_korean_english_mixed(self):
        """한글+영어+숫자 혼합 테스트"""
        text = "안녕 Hello 123"
        expected = 10  # 공백 제외 모든 문자
        
    def test_count_all_chars_with_punctuation(self):
        """특수문자 포함 테스트"""
        
    def test_count_korean_compatibility(self):
        """기존 korean_counter와 호환성 테스트"""
        
    def test_count_visible_chars(self):
        """보이는 문자 카운팅 테스트"""
```

#### `test/test_text_processor.py` (수정)

**import 변경**:

```python
# 기존 import 유지하되 새로운 기능 테스트 추가
from core.text_processor import TextProcessor
```

**추가할 테스트**:

```python
def test_format_text_with_options_all_chars(self):
    """모든 문자 카운팅 모드 테스트"""
    
def test_format_text_with_options_sentence_separation(self):
    """마침표 분리 기능 테스트"""
    
def test_split_by_all_chars(self):
    """모든 문자 기준 분할 테스트"""
    
def test_separate_sentences_by_period(self):
    """마침표 기준 문장 분리 테스트"""
    
def test_count_all_chars_method(self):
    """TextProcessor.count_all_chars 메서드 테스트"""
```

#### `test/test_korean_counter.py` (유지)

- 기존 테스트 파일은 그대로 유지
- 미사용 상태이지만 호환성을 위해 보존
- 주석으로 "현재 미사용, text_counter로 이관됨" 표시

## 구현 단계

### Phase 1: 기반 로직 구현 및 테스트

1. **모든 문자 카운팅 로직 구현 및 이관**
   - `utils/text_counter.py` 생성
   - `count_all_chars()`, `count_visible_chars()`, `is_visible_char()` 함수 구현
   - `count_korean()` 함수 추가 (korean_counter에서 이관)

2. **텍스트 처리 로직 확장 및 import 변경**
   - `core/text_processor.py`의 import를 `text_counter`로 변경
   - 새로운 메서드 추가: `format_text_with_options()`, `split_by_all_chars()`, `separate_sentences_by_period()`
   - 기존 메서드 유지: `count_korean_chars()`, `split_by_korean_count()` (호환성)

3. **단위 테스트 작성 및 실행**
   - `test/test_text_counter.py` 생성 (korean_counter 기능 포함 테스트)
   - `test/test_text_processor.py` 수정 (새로운 메서드 테스트 추가)
   - `test/test_korean_counter.py` 유지 (미사용 표시 주석 추가)
   - `uv run pytest test/test_text_counter.py -v` 테스트 실행은 사용자가 직접 수행한다
   - `uv run pytest test/test_text_processor.py -v`

4. **기능 검증 및 호환성 확인**
   - 마침표 분리 기능 동작 확인
   - 모든 문자 카운팅 정확성 검증
   - 기존 한글 카운팅과의 호환성 확인
   - `korean_counter.py` 파일은 유지하되 미사용 상태 확인

### Phase 2: UI 컨트롤 추가 및 테스트

1. **UI 파일 수정**
   - `ui/untitled.ui`에 체크박스, 초기화 버튼 추가
   - 레이아웃 조정 (기존 Dialog 크기 유지)

2. **UI 컴파일 및 확인**
   - `uv run pyside6-uic ui/untitled.ui -o ui/ui_dialog.py`
   - UI 렌더링 상태 확인

3. **UI 컨트롤 테스트**
   - 새로운 컨트롤들의 배치 확인
   - 기존 레이아웃과의 조화 검증
   - 반응형 동작 테스트

### Phase 3: 이벤트 처리 구현 및 테스트

1. **main.py 확장**
   - 새로운 속성 추가 (`use_all_chars`, `separate_sentences`)
   - 체크박스, 초기화 버튼 이벤트 핸들러 구현
   - 최소화 기능 구현

2. **기존 메서드 수정**
   - `apply_formatting()` 메서드에 새로운 옵션 적용
   - 상태 표시 로직 업데이트 (모든 문자 카운팅)

3. **기능별 테스트 실행**
   - 체크박스 토글 동작 테스트
   - 초기화 버튼 기능 테스트
   - 최소화 기능 테스트
   - `uv run python main.py`로 통합 동작 확인

4. **기존 기능 호환성 테스트**
   - 기존 텍스트 가다듬기 기능 정상 동작 확인
   - 줄 길이 설정 기능 정상 동작 확인

### Phase 4: 통합 테스트 및 최종 검증

1. **전체 테스트 실행**
   - `uv run pytest test/ -v` (모든 테스트 케이스)
   - 기존 테스트와 새로운 테스트 모두 통과 확인

2. **시나리오 기반 테스트**
   - 다양한 텍스트 입력으로 전체 워크플로우 테스트
   - 옵션 조합별 동작 검증
   - 에러 상황 처리 확인

3. **성능 및 안정성 검증**
   - 대용량 텍스트 처리 테스트
   - 메모리 사용량 모니터링
   - UI 응답성 확인

4. **빌드 테스트**
   - `uv run pyinstaller --onefile --windowed --name "텍스트_가다듬기" main.py`
   - 실행 파일 정상 동작 확인

## 주의사항

### 1. 호환성 유지

- 기존 줄 길이 설정 유지
- 기존 테스트 케이스 보존
- 점진적 기능 추가

### 2. UI 배치

- 기존 레이아웃과 조화
- 사용자 편의성 고려
- 반응형 레이아웃 유지

### 3. 성능 고려

- 텍스트 처리 속도 유지
- 메모리 사용량 최적화
- 대용량 텍스트 처리 지원

## 예상 결과

### 1. 기능 개선

- 더 정확한 문자 카운팅
- 마침표 기준 가독성 향상
- 사용자 편의 기능 추가

### 2. UI/UX 개선

- 직관적인 옵션 제어
- 빠른 텍스트 초기화
- 창 관리 편의성

### 3. 코드 품질

- 모듈화된 기능 구조
- 확장 가능한 아키텍처
- 종합적인 테스트 커버리지

## 코딩 가이드 준수

- 기존 SOLID 원칙 유지
- uv 패키지 매니저 사용
- 단일 실행파일 빌드 지원
- 모듈별 기능 분리 원칙

## 파일 이관 및 호환성 전략

### `korean_counter.py` → `text_counter.py` 이관 계획

1. **이관 대상 함수들**:
   - `count_korean()` → `text_counter.py`로 이관
   - `is_korean_char()` → 유지 (호환성)

2. **호환성 유지 방식**:
   - `korean_counter.py` 파일은 삭제하지 않고 유지
   - 파일 상단에 "현재 미사용, text_counter.py로 이관됨" 주석 추가
   - 기존 import 구문들은 모두 `text_counter`로 변경

3. **단계적 이관**:
   - Phase 1에서 `text_counter.py` 생성 및 기능 구현
   - 모든 테스트 통과 확인 후
   - `core/text_processor.py`의 import 변경
   - `korean_counter.py`는 미사용 상태로 보존

### 기존 코드와의 호환성

- **메서드명 유지**: `count_korean_chars()` 등 기존 메서드는 그대로 유지
- **기능 확장**: 새로운 `count_all_chars()` 메서드 추가
- **옵션 제공**: 한글 카운팅과 모든 문자 카운팅 중 선택 가능
- **테스트 보존**: 기존 테스트 케이스는 모두 통과해야 함
