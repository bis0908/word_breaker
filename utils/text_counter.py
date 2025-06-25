"""
모든 문자 카운팅 유틸리티
기존 korean_counter.py를 대체하여 사용
korean_counter.py는 호환성을 위해 유지하되 미사용 상태
"""

import re


def count_all_chars(text: str) -> int:
    """
    모든 문자 카운팅 (공백 제외)

    Args:
        text (str): 카운트할 텍스트

    Returns:
        int: 공백을 제외한 모든 문자 수
    """
    if not text:
        return 0
    return len([char for char in text if char != " "])


def count_visible_chars(text: str) -> int:
    """
    보이는 문자만 카운팅 (공백, 탭, 개행 제외)

    Args:
        text (str): 카운트할 텍스트

    Returns:
        int: 보이는 문자만의 수
    """
    if not text:
        return 0
    return len([char for char in text if char.strip()])


def is_visible_char(char: str) -> bool:
    """
    보이는 문자 판별 (공백, 탭, 개행이 아닌 문자)

    Args:
        char (str): 판별할 문자

    Returns:
        bool: 보이는 문자면 True, 아니면 False
    """
    if not char or len(char) != 1:
        return False
    return char.strip() != ""


def count_korean(text: str) -> int:
    """
    한글 문자 카운팅 (호환성 유지용)
    기존 korean_counter.count_korean과 동일한 기능

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
    단일 문자가 한글인지 판별합니다. (호환성 유지용)

    Args:
        char (str): 판별할 문자

    Returns:
        bool: 한글 문자면 True, 아니면 False
    """
    if not char or len(char) != 1:
        return False

    # 완성형 한글 범위: \uAC00-\uD7A3
    return "\uac00" <= char <= "\ud7a3"
