"""
현재 미사용, text_counter.py로 이관됨
호환성을 위해 유지하되 새로운 기능은 text_counter를 사용
"""

import re


def count_korean(text: str) -> int:
    """
    텍스트에서 한글 문자의 수를 카운트합니다.

    Args:
        text (str): 카운트할 텍스트

    Returns:
        int: 한글 문자의 수
    """
    if not text:
        return 0

    # 완성형 한글 범위: \uAC00-\uD7A3
    korean_pattern = re.compile(r"[\uAC00-\uD7A3]")
    korean_chars = korean_pattern.findall(text)
    return len(korean_chars)


def is_korean_char(char: str) -> bool:
    """
    단일 문자가 한글인지 판별합니다.

    Args:
        char (str): 판별할 문자

    Returns:
        bool: 한글 문자면 True, 아니면 False
    """
    if not char or len(char) != 1:
        return False

    # 완성형 한글 범위: \uAC00-\uD7A3
    return "\uac00" <= char <= "\ud7a3"
