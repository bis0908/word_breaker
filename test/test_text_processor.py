import pytest
from core.text_processor import TextProcessor, DEFAULT_LINE_LENGTH


class TestTextProcessor:
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.processor = TextProcessor()

    def test_format_text_default_length(self):
        """기본 줄 길이(18자)로 텍스트 가다듬기 테스트"""
        text = "안녕하세요 저는 텍스트 가다듬기 프로그램을 개발하고 있는 개발자입니다"
        result = self.processor.format_text(text)
        lines = result.split("\n")

        # 각 줄이 18자 이하인지 확인
        for line in lines:
            korean_count = sum(1 for char in line if "\uac00" <= char <= "\ud7a3")
            assert korean_count <= DEFAULT_LINE_LENGTH

    def test_format_text_custom_length(self):
        """사용자 지정 줄 길이로 텍스트 가다듬기 테스트"""
        text = "안녕하세요 저는 개발자입니다"
        line_length = 5
        result = self.processor.format_text(text, line_length)
        lines = result.split("\n")

        # 각 줄이 5자 이하인지 확인
        for line in lines:
            korean_count = sum(1 for char in line if "\uac00" <= char <= "\ud7a3")
            assert korean_count <= line_length

    def test_format_text_empty_string(self):
        """빈 문자열 테스트"""
        text = ""
        result = self.processor.format_text(text)
        assert result == ""

    def test_format_text_single_word(self):
        """단일 단어 테스트"""
        text = "안녕하세요"
        result = self.processor.format_text(text, 10)
        assert result == "안녕하세요"

    def test_split_by_korean_count_basic(self):
        """기본 한글 카운트 분할 테스트"""
        text = "안녕하세요 저는 개발자입니다"
        length = 5
        result = self.processor.split_by_korean_count(text, length)

        # 결과가 리스트인지 확인
        assert isinstance(result, list)

        # 각 요소가 지정 길이 이하인지 확인
        for item in result:
            korean_count = sum(1 for char in item if "\uac00" <= char <= "\ud7a3")
            assert korean_count <= length

    def test_split_by_korean_count_exact_length(self):
        """정확한 길이의 텍스트 분할 테스트"""
        text = "안녕하세요"  # 5자
        length = 5
        result = self.processor.split_by_korean_count(text, length)

        assert len(result) == 1
        assert result[0] == text

    def test_split_by_korean_count_long_text(self):
        """긴 텍스트 분할 테스트"""
        text = "안녕하세요. 저는 텍스트 가다듬기 프로그램을 개발하고 있는 개발자입니다. 이 프로그램은 한글 문자 수를 기준으로 텍스트를 분할합니다."
        length = 10
        result = self.processor.split_by_korean_count(text, length)

        # 모든 분할된 텍스트가 지정 길이 이하인지 확인
        for item in result:
            korean_count = sum(1 for char in item if "\uac00" <= char <= "\ud7a3")
            assert korean_count <= length

    def test_split_by_korean_count_with_punctuation(self):
        """구두점이 포함된 텍스트 분할 테스트"""
        text = "안녕하세요! 저는 개발자입니다."
        length = 7
        result = self.processor.split_by_korean_count(text, length)

        # 구두점은 카운트에서 제외되므로 한글만 확인
        for item in result:
            korean_count = sum(1 for char in item if "\uac00" <= char <= "\ud7a3")
            assert korean_count <= length

    def test_count_korean_chars(self):
        """한글 문자 카운팅 테스트"""
        text = "안녕 Hello 세상"
        expected = 4  # 안녕(2) + 세상(2)
        result = self.processor.count_korean_chars(text)
        assert result == expected

    # 새로운 메서드들에 대한 테스트 추가
    def test_count_all_chars_method(self):
        """TextProcessor.count_all_chars 메서드 테스트"""
        text = "안녕 Hello 123!"
        expected = 11  # 공백 제외 모든 문자
        result = self.processor.count_all_chars(text)
        assert result == expected

    def test_format_text_with_options_all_chars(self):
        """모든 문자 카운팅 모드 테스트"""
        text = "안녕 Hello 123"
        result = self.processor.format_text_with_options(
            text, line_length=7, use_all_chars=True, separate_sentences=False
        )
        lines = result.split("\n")

        # 각 줄이 7자 이하인지 확인 (공백 제외)
        for line in lines:
            char_count = len([char for char in line if char != " "])
            assert char_count <= 7

    def test_format_text_with_options_sentence_separation(self):
        """마침표 분리 기능 테스트"""
        text = "안녕하세요. 저는 개발자입니다."
        result = self.processor.format_text_with_options(
            text, line_length=20, use_all_chars=True, separate_sentences=True
        )

        # 마침표 뒤에 빈 행이 추가되었는지 확인
        assert "\n\n" in result

    def test_split_by_all_chars(self):
        """모든 문자 기준 분할 테스트"""
        text = "안녕 Hello 123"
        length = 7
        result = self.processor.split_by_all_chars(text, length)

        # 결과가 리스트인지 확인
        assert isinstance(result, list)

        # 각 요소가 지정 길이 이하인지 확인 (공백 제외)
        for item in result:
            char_count = len([char for char in item if char != " "])
            assert char_count <= length

    def test_separate_sentences_by_period(self):
        """마침표 기준 문장 분리 테스트"""
        text = "안녕하세요. 저는 개발자입니다. 반갑습니다."
        result = self.processor.separate_sentences_by_period(text)

        # 마침표 뒤에 빈 행이 추가되었는지 확인
        assert result.count("\n\n") >= 1

    def test_separate_sentences_by_period_with_space(self):
        """마침표 뒤 공백이 있는 경우 테스트"""
        text = "안녕하세요. 저는 개발자입니다."
        result = self.processor.separate_sentences_by_period(text)

        # 마침표 뒤 공백이 빈 행으로 변경되었는지 확인
        assert "\n\n" in result

    def test_separate_sentences_by_period_no_period(self):
        """마침표가 없는 경우 테스트"""
        text = "안녕하세요 저는 개발자입니다"
        result = self.processor.separate_sentences_by_period(text)

        # 원본과 동일해야 함
        assert result == text

    def test_separate_sentences_by_period_empty_string(self):
        """빈 문자열 테스트"""
        text = ""
        result = self.processor.separate_sentences_by_period(text)
        assert result == ""

    def test_format_text_with_options_korean_mode(self):
        """한글 카운팅 모드 테스트 (호환성)"""
        text = "안녕 Hello 123"
        result = self.processor.format_text_with_options(
            text,
            line_length=5,
            use_all_chars=False,  # 한글 카운팅 모드
            separate_sentences=False,
        )
        lines = result.split("\n")

        # 각 줄이 한글 5자 이하인지 확인
        for line in lines:
            korean_count = sum(1 for char in line if "\uac00" <= char <= "\ud7a3")
            assert korean_count <= 5

    def test_split_by_all_chars_long_word(self):
        """긴 단어 분할 테스트 (모든 문자 기준)"""
        text = "verylongwordthatexceedslimit"
        length = 10
        result = self.processor.split_by_all_chars(text, length)

        # 각 부분이 지정 길이 이하인지 확인
        for item in result:
            char_count = len([char for char in item if char != " "])
            assert char_count <= length

    def test_format_text_with_options_all_options_enabled(self):
        """모든 옵션이 활성화된 경우 테스트"""
        text = "안녕하세요. 저는 Hello World 123 개발자입니다."
        result = self.processor.format_text_with_options(
            text, line_length=10, use_all_chars=True, separate_sentences=True
        )

        # 마침표 분리와 모든 문자 카운팅이 모두 적용되었는지 확인
        assert "\n\n" in result  # 마침표 분리
        lines = result.split("\n")
        for line in lines:
            if line.strip():  # 빈 행 제외
                char_count = len([char for char in line if char != " "])
                assert char_count <= 10  # 모든 문자 카운팅
