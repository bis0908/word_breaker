from typing import List
from utils.korean_counter import count_korean


# 기본 줄 길이 설정
DEFAULT_LINE_LENGTH = 18


class TextProcessor:
    """텍스트 가다듬기 처리 클래스"""

    def format_text(self, text: str, line_length: int = DEFAULT_LINE_LENGTH) -> str:
        """
        텍스트를 지정된 줄 길이에 맞춰 가다듬습니다.

        Args:
            text (str): 가다듬을 텍스트
            line_length (int): 한 줄당 한글 문자 수 (기본값: 18)

        Returns:
            str: 가다듬어진 텍스트
        """
        if not text.strip():
            return ""

        # 텍스트를 줄 길이에 맞춰 분할
        lines = self.split_by_korean_count(text, line_length)

        # 줄바꿈으로 결합
        return "\n".join(lines)

    def split_by_korean_count(self, text: str, length: int) -> List[str]:
        """
        텍스트를 한글 문자 수 기준으로 분할합니다.

        Args:
            text (str): 분할할 텍스트
            length (int): 한 줄당 최대 한글 문자 수

        Returns:
            List[str]: 분할된 문자열 리스트
        """
        if not text.strip():
            return []

        # 공백으로 단어 분리
        words = text.split()
        if not words:
            return []

        lines = []
        current_line = ""
        current_korean_count = 0

        for word in words:
            word_korean_count = self.count_korean_chars(word)

            # 현재 줄에 단어를 추가했을 때의 한글 문자 수 계산
            if current_line:
                # 공백 1개 추가
                total_korean_count = current_korean_count + word_korean_count
            else:
                # 첫 번째 단어
                total_korean_count = word_korean_count

            # 길이 제한 확인
            if total_korean_count <= length:
                # 현재 줄에 추가
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
                current_korean_count = total_korean_count
            else:
                # 새로운 줄 시작
                if current_line:
                    lines.append(current_line)

                # 단어 자체가 길이 제한을 초과하는 경우
                if word_korean_count > length:
                    # 단어를 강제로 분할
                    split_word = self._split_long_word(word, length)
                    lines.extend(split_word[:-1])  # 마지막 부분 제외하고 추가
                    current_line = split_word[-1]  # 마지막 부분을 현재 줄로
                    current_korean_count = self.count_korean_chars(current_line)
                else:
                    current_line = word
                    current_korean_count = word_korean_count

        # 마지막 줄 추가
        if current_line:
            lines.append(current_line)

        return lines

    def _split_long_word(self, word: str, max_length: int) -> List[str]:
        """긴 단어를 강제로 분할합니다."""
        if not word:
            return []

        result = []
        current_part = ""
        current_korean_count = 0

        for char in word:
            char_is_korean = "\uac00" <= char <= "\ud7a3"
            char_korean_count = 1 if char_is_korean else 0

            if current_korean_count + char_korean_count <= max_length:
                current_part += char
                current_korean_count += char_korean_count
            else:
                if current_part:
                    result.append(current_part)
                current_part = char
                current_korean_count = char_korean_count

        if current_part:
            result.append(current_part)

        return result if result else [word]

    def count_korean_chars(self, text: str) -> int:
        """
        텍스트의 한글 문자 수를 카운트합니다.

        Args:
            text (str): 카운트할 텍스트

        Returns:
            int: 한글 문자 수
        """
        return count_korean(text)
