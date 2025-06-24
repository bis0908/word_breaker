import pytest
from utils.korean_counter import count_korean, is_korean_char


class TestKoreanCounter:
    def test_count_korean_pure_korean(self):
        """순수 한글 문자열 테스트"""
        text = "안녕하세요"
        expected = 5
        assert count_korean(text) == expected

    def test_count_korean_mixed_korean_english(self):
        """한글과 영어 혼합 문자열 테스트"""
        text = "안녕 Hello 세상"
        expected = 4  # 안녕(2) + 세상(2) - 공백 제외
        assert count_korean(text) == expected

    def test_count_korean_with_numbers_symbols(self):
        """한글, 숫자, 특수문자 혼합 테스트"""
        text = "안녕123!@#세상456"
        expected = 4  # 안녕(2) + 세상(2)
        assert count_korean(text) == expected

    def test_count_korean_empty_string(self):
        """빈 문자열 테스트"""
        text = ""
        expected = 0
        assert count_korean(text) == expected

    def test_count_korean_no_korean(self):
        """한글이 없는 문자열 테스트"""
        text = "Hello World 123!@#"
        expected = 0
        assert count_korean(text) == expected

    def test_count_korean_spaces_only(self):
        """공백만 있는 문자열 테스트"""
        text = "   "
        expected = 0
        assert count_korean(text) == expected

    def test_is_korean_char_valid_korean(self):
        """유효한 한글 문자 테스트"""
        assert is_korean_char("가") == True
        assert is_korean_char("힣") == True
        assert is_korean_char("나") == True

    def test_is_korean_char_invalid_korean(self):
        """한글이 아닌 문자 테스트"""
        assert is_korean_char("A") == False
        assert is_korean_char("1") == False
        assert is_korean_char(" ") == False
        assert is_korean_char("!") == False

    def test_count_korean_long_text(self):
        """긴 텍스트 테스트"""
        text = "안녕하세요. 저는 텍스트 가다듬기 프로그램을 개발하고 있습니다. Hello World!"
        expected = 27  # 한글 문자만 카운트
        assert count_korean(text) == expected
