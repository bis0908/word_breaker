from PySide6.QtWidgets import QApplication


class ClipboardHelper:
    """클립보드 처리 도우미 클래스"""

    def copy_text(self, text: str) -> bool:
        """
        텍스트를 클립보드로 복사합니다.

        Args:
            text (str): 복사할 텍스트

        Returns:
            bool: 성공 시 True, 실패 시 False
        """
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            return True
        except Exception as e:
            print(f"클립보드 복사 실패: {e}")
            return False

    def get_text(self) -> str:
        """
        클립보드에서 텍스트를 가져옵니다.

        Returns:
            str: 클립보드의 텍스트, 실패 시 빈 문자열
        """
        try:
            clipboard = QApplication.clipboard()
            return clipboard.text()
        except Exception as e:
            print(f"클립보드 텍스트 가져오기 실패: {e}")
            return ""
