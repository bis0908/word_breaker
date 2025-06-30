from typing import List
from utils.text_counter import (
    count_korean,
    count_all_chars,
    count_all_chars_with_period,
)
import re


# 기본 줄 길이 설정
DEFAULT_LINE_LENGTH = 18


class TextProcessor:
    """텍스트 가다듬기 처리 클래스"""

    def format_text(self, text: str, line_length: int = DEFAULT_LINE_LENGTH) -> str:
        """
        deprecated
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
        deprecated
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
        텍스트의 한글 문자 수를 카운트합니다. (호환성 유지)

        Args:
            text (str): 카운트할 텍스트

        Returns:
            int: 한글 문자 수
        """
        return count_korean(text)

    def count_all_chars(self, text: str) -> int:
        """
        텍스트의 모든 문자 수를 카운트합니다. (공백, 쉼표, 마침표 제외)

        Args:
            text (str): 카운트할 텍스트

        Returns:
            int: 모든 문자 수 (공백, 쉼표, 마침표 제외)
        """
        return count_all_chars(text)

    def count_all_chars_with_period(self, text: str) -> int:
        return count_all_chars_with_period(text)

    def format_text_with_options(
        self,
        text: str,
        line_length: int,
        use_all_chars: bool = True,
        separate_sentences: bool = True,
    ) -> str:
        """
        옵션을 고려한 텍스트 가다듬기

        Args:
            text (str): 가다듬을 텍스트
            line_length (int): 한 줄당 문자 수
            use_all_chars (bool): 모든 문자 카운팅 여부 (True: 모든 문자, False: 한글만)
            separate_sentences (bool): 마침표 분리 여부

        Returns:
            str: 가다듬어진 텍스트
        """
        if not text.strip():
            return ""

        # 마침표 분리 처리
        if separate_sentences:
            text = self.separate_sentences_by_period(text)

        # 문자 카운팅 방식에 따른 분할
        if use_all_chars:
            if separate_sentences:
                # 마침표 분리가 활성화된 경우: 빈 행을 보존하는 방식
                lines = self.split_by_all_chars(text, line_length)
            else:
                # 마침표 분리가 비활성화된 경우: 기존 방식과 동일한 개행 처리
                lines = self.split_by_all_chars_simple(text, line_length)
        else:
            lines = self.split_by_korean_count(text, line_length)

        return "\n".join(lines)

    def split_by_all_chars_simple(self, text: str, length: int) -> List[str]:
        """
        텍스트를 모든 문자 수 기준으로 분할합니다. (기존 방식과 동일한 개행 처리)
        모든 개행문자를 무시하고 공백으로만 단어를 분리하여 줄 길이에 맞춰 재배열합니다.

        Args:
            text (str): 분할할 텍스트
            length (int): 한 줄당 최대 문자 수 (공백 제외)

        Returns:
            List[str]: 분할된 문자열 리스트
        """
        if not text.strip():
            return []

        # 공백으로 단어 분리 (기존 방식과 동일)
        words = text.split()
        if not words:
            return []

        lines = []
        current_line = ""
        current_char_count = 0

        for word in words:
            word_char_count = count_all_chars(word)

            # 현재 줄에 단어를 추가했을 때의 문자 수 계산
            if current_line:
                # 공백 1개 추가하지만 공백은 카운트하지 않음
                total_char_count = current_char_count + word_char_count
            else:
                # 첫 번째 단어
                total_char_count = word_char_count

            # 길이 제한 확인
            if total_char_count <= length:
                # 현재 줄에 추가
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
                current_char_count = total_char_count
            else:
                # 새로운 줄 시작
                if current_line:
                    lines.append(current_line)

                # 단어 자체가 길이 제한을 초과하는 경우
                if word_char_count > length:
                    # 단어를 강제로 분할
                    split_word = self._split_long_word_by_all_chars(word, length)
                    lines.extend(split_word[:-1])  # 마지막 부분 제외하고 추가
                    current_line = split_word[-1]  # 마지막 부분을 현재 줄로
                    current_char_count = count_all_chars(current_line)
                else:
                    current_line = word
                    current_char_count = word_char_count

        # 마지막 줄 추가
        if current_line:
            lines.append(current_line)

        return lines

    def split_by_all_chars(self, text: str, length: int) -> List[str]:
        """
        텍스트를 모든 문자 수 기준으로 분할합니다.

        Args:
            text (str): 분할할 텍스트
            length (int): 한 줄당 최대 문자 수 (공백 제외)

        Returns:
            List[str]: 분할된 문자열 리스트
        """
        if not text.strip():
            return []

        # 빈 행(\n\n)을 보존하기 위해 먼저 빈 행으로 분할
        paragraphs = text.split("\n\n")
        result = []

        for i, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                # 빈 문단은 빈 행으로 추가
                result.append("")
                continue

            # 각 문단을 단어로 분할하여 처리
            words = paragraph.split()
            if not words:
                result.append("")
                continue

            lines = []
            current_line = ""
            current_char_count = 0

            for word in words:
                word_char_count = count_all_chars(word)

                # 현재 줄에 단어를 추가했을 때의 문자 수 계산
                if current_line:
                    # 공백 1개 추가하지만 공백은 카운트하지 않음
                    total_char_count = current_char_count + word_char_count
                else:
                    # 첫 번째 단어
                    total_char_count = word_char_count

                # 길이 제한 확인
                if total_char_count <= length:
                    # 현재 줄에 추가
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                    current_char_count = total_char_count
                else:
                    # 새로운 줄 시작
                    if current_line:
                        lines.append(current_line)

                    # 단어 자체가 길이 제한을 초과하는 경우
                    if word_char_count > length:
                        # 단어를 강제로 분할
                        split_word = self._split_long_word_by_all_chars(word, length)
                        lines.extend(split_word[:-1])  # 마지막 부분 제외하고 추가
                        current_line = split_word[-1]  # 마지막 부분을 현재 줄로
                        current_char_count = count_all_chars(current_line)
                    else:
                        current_line = word
                        current_char_count = word_char_count

            # 마지막 줄 추가
            if current_line:
                lines.append(current_line)

            # 처리된 문단을 결과에 추가
            result.extend(lines)

            # 마지막 문단이 아니라면 빈 행 추가 (원래 \n\n을 보존)
            if i < len(paragraphs) - 1:
                result.append("")

        return result

    def _split_long_word_by_all_chars(self, word: str, max_length: int) -> List[str]:
        """긴 단어를 모든 문자 기준으로 강제 분할합니다."""
        if not word:
            return []

        result = []
        current_part = ""
        current_char_count = 0

        for char in word:
            char_count = 0 if char == " " else 1  # 공백은 카운트하지 않음

            if current_char_count + char_count <= max_length:
                current_part += char
                current_char_count += char_count
            else:
                if current_part:
                    result.append(current_part)
                current_part = char
                current_char_count = char_count

        if current_part:
            result.append(current_part)

        return result if result else [word]

    def separate_sentences_by_period(self, text: str) -> str:
        """
        마침표 기준 문장 분리 (마침표 뒤에 빈 행 추가하고 공백 정리)

        Args:
            text (str): 분리할 텍스트

        Returns:
            str: 마침표로 분리되고 공백이 정리된 텍스트
        """
        if not text.strip():
            return ""

        # 보이지 않는 문자들 제거 (Zero-Width Space 등)
        invisible_chars = [
            "\u200b",  # Zero Width Space
            "\u200c",  # Zero Width Non-Joiner
            "\u200d",  # Zero Width Joiner
            "\u200e",  # Left-to-Right Mark
            "\u200f",  # Right-to-Left Mark
            "\ufeff",  # Zero Width No-Break Space
            "\u2060",  # Word Joiner
        ]

        for char in invisible_chars:
            text = text.replace(char, "")

        # 마침표가 나오기 전까지의 개행을 공백으로 변경
        # 마침표 앞의 개행들을 공백으로 치환
        text = re.sub(r"\n+(?=[^.]*\.)", " ", text)

        # 연속된 공백을 하나로 정리
        text = re.sub(r"\s+", " ", text)

        # 마침표 뒤에 공백이나 줄바꿈이 있는 경우 빈 행 추가
        pattern = r"(\.)(\s+)"
        result = re.sub(pattern, r"\1\n\n", text)

        # 마침표 뒤에 바로 문자가 오는 경우도 처리
        pattern2 = r"(\.)([^\s\n])"
        result = re.sub(pattern2, r"\1\n\n\2", result)

        # 빈 행 뒤의 앞쪽 공백 제거
        result = re.sub(r"\n\n\s+", "\n\n", result)

        return result
