"""
text_counter 모듈의 모든 함수에 대한 테스트
korean_counter의 기능도 포함하여 테스트
"""

import pytest
from utils.text_counter import (
    count_all_chars,
    count_visible_chars,
    is_visible_char,
    count_korean,
    is_korean_char,
)


class TestTextCounter:
    def test_count_all_chars_korean_english_mixed(self):
        """한글+영어+숫자 혼합 테스트"""
        text = "안녕 Hello 123"
        expected = 10  # 안녕(2) + Hello(5) + 123(3), 공백 제외
        result = count_all_chars(text)
        assert result == expected

    def test_count_all_chars_with_punctuation(self):
        """특수문자 포함 테스트"""
        text = "안녕하세요! Hello, World."
        expected = 18  # 모든 문자 (공백 2개 제외)
        result = count_all_chars(text)
        assert result == expected

    def test_count_all_chars_empty_string(self):
        """빈 문자열 테스트"""
        text = ""
        expected = 0
        result = count_all_chars(text)
        assert result == expected

    def test_count_all_chars_spaces_only(self):
        """공백만 있는 문자열 테스트"""
        text = "   "
        expected = 0
        result = count_all_chars(text)
        assert result == expected

    def test_count_all_chars_no_spaces(self):
        """공백이 없는 문자열 테스트"""
        text = "안녕하세요123ABC!@#"
        expected = 14  # 모든 문자
        result = count_all_chars(text)
        assert result == expected

    def test_count_visible_chars_with_whitespace(self):
        """공백, 탭, 개행이 포함된 텍스트 테스트"""
        text = "안녕\t하세요\n123"
        expected = 8  # 안녕하세요123 (공백문자 제외)
        result = count_visible_chars(text)
        assert result == expected

    def test_count_visible_chars_empty_string(self):
        """빈 문자열 테스트"""
        text = ""
        expected = 0
        result = count_visible_chars(text)
        assert result == expected

    def test_count_visible_chars_whitespace_only(self):
        """공백문자만 있는 문자열 테스트"""
        text = " \t\n "
        expected = 0
        result = count_visible_chars(text)
        assert result == expected

    def test_is_visible_char_valid_chars(self):
        """보이는 문자 판별 테스트"""
        assert is_visible_char("a") == True
        assert is_visible_char("가") == True
        assert is_visible_char("1") == True
        assert is_visible_char("!") == True

    def test_is_visible_char_invisible_chars(self):
        """보이지 않는 문자 판별 테스트"""
        assert is_visible_char(" ") == False
        assert is_visible_char("\t") == False
        assert is_visible_char("\n") == False
        assert is_visible_char("") == False

    def test_is_visible_char_invalid_input(self):
        """잘못된 입력 테스트"""
        assert is_visible_char("ab") == False  # 문자열 길이 > 1
        assert is_visible_char(None) == False

    def test_count_korean_compatibility(self):
        """기존 korean_counter와 호환성 테스트"""
        text = "안녕 Hello 세상"
        expected = 4  # 안녕(2) + 세상(2)
        result = count_korean(text)
        assert result == expected

    def test_count_korean_pure_korean(self):
        """순수 한글 문자열 테스트"""
        text = "안녕하세요"
        expected = 5
        result = count_korean(text)
        assert result == expected

    def test_count_korean_mixed_korean_english(self):
        """한글과 영어 혼합 문자열 테스트"""
        text = "안녕 Hello 세상"
        expected = 4  # 안녕(2) + 세상(2)
        result = count_korean(text)
        assert result == expected

    def test_count_korean_with_numbers_symbols(self):
        """한글, 숫자, 특수문자 혼합 테스트"""
        text = "안녕123!@#세상456"
        expected = 4  # 안녕(2) + 세상(2)
        result = count_korean(text)
        assert result == expected

    def test_count_korean_empty_string(self):
        """빈 문자열 테스트"""
        text = ""
        expected = 0
        result = count_korean(text)
        assert result == expected

    def test_count_korean_no_korean(self):
        """한글이 없는 문자열 테스트"""
        text = "Hello World 123!@#"
        expected = 0
        result = count_korean(text)
        assert result == expected

    def test_count_korean_long_text(self):
        """긴 텍스트 테스트"""
        text = "안녕하세요. 저는 텍스트 가다듬기 프로그램을 개발하고 있습니다. Hello World!"
        expected = 27  # 한글 문자만 카운트
        result = count_korean(text)
        assert result == expected

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

    def test_count_all_chars_vs_count_korean_comparison(self):
        """모든 문자 카운팅과 한글 카운팅 비교 테스트"""
        text = "안녕하세요 Hello 123!"
        all_chars = count_all_chars(text)  # 공백 제외 모든 문자
        korean_chars = count_korean(text)  # 한글만

        assert all_chars > korean_chars
        assert all_chars == 14  # 안녕하세요(5) + Hello(5) + 123(3) + !(1)
        assert korean_chars == 5  # 안녕하세요(5)

    def test_count_visible_chars_vs_count_all_chars_comparison(self):
        """보이는 문자 카운팅과 모든 문자 카운팅 비교 테스트"""
        text = "안녕\t하세요 123"
        all_chars = count_all_chars(text)  # 공백만 제외
        visible_chars = count_visible_chars(text)  # 모든 공백문자 제외

        assert all_chars > visible_chars  # 탭 문자 차이
        assert all_chars == 9  # 탭은 카운트, 공백은 제외
        assert visible_chars == 8  # 탭과 공백 모두 제외
