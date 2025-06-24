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
