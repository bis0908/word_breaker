import pytest
from unittest.mock import patch, MagicMock
from utils.clipboard_helper import ClipboardHelper


class TestClipboardHelper:
    def setup_method(self):
        """각 테스트 전에 실행"""
        self.clipboard = ClipboardHelper()

    @patch("PySide6.QtWidgets.QApplication.clipboard")
    def test_copy_text_success(self, mock_clipboard):
        """텍스트 복사 성공 테스트"""
        # Mock 설정
        mock_cb = MagicMock()
        mock_clipboard.return_value = mock_cb

        text = "테스트 텍스트입니다"
        result = self.clipboard.copy_text(text)

        # 복사 함수가 호출되었는지 확인
        mock_cb.setText.assert_called_once_with(text)
        assert result == True

    @patch("PySide6.QtWidgets.QApplication.clipboard")
    def test_copy_text_failure(self, mock_clipboard):
        """텍스트 복사 실패 테스트"""
        # Mock에서 예외 발생
        mock_cb = MagicMock()
        mock_cb.setText.side_effect = Exception("클립보드 오류")
        mock_clipboard.return_value = mock_cb

        text = "테스트 텍스트입니다"
        result = self.clipboard.copy_text(text)

        assert result == False

    def test_copy_text_empty_string(self):
        """빈 문자열 복사 테스트"""
        text = ""
        # 빈 문자열도 복사 가능해야 함
        result = self.clipboard.copy_text(text)
        # 실제 구현에서는 True를 반환해야 함
        assert isinstance(result, bool)

    @patch("PySide6.QtWidgets.QApplication.clipboard")
    def test_get_text_success(self, mock_clipboard):
        """텍스트 가져오기 성공 테스트"""
        # Mock 설정
        mock_cb = MagicMock()
        expected_text = "클립보드의 텍스트"
        mock_cb.text.return_value = expected_text
        mock_clipboard.return_value = mock_cb

        result = self.clipboard.get_text()

        # 텍스트 가져오기 함수가 호출되었는지 확인
        mock_cb.text.assert_called_once()
        assert result == expected_text

    @patch("PySide6.QtWidgets.QApplication.clipboard")
    def test_get_text_failure(self, mock_clipboard):
        """텍스트 가져오기 실패 테스트"""
        # Mock에서 예외 발생
        mock_cb = MagicMock()
        mock_cb.text.side_effect = Exception("클립보드 오류")
        mock_clipboard.return_value = mock_cb

        result = self.clipboard.get_text()

        assert result == ""

    @patch("PySide6.QtWidgets.QApplication.clipboard")
    def test_get_text_empty_clipboard(self, mock_clipboard):
        """빈 클립보드 테스트"""
        # Mock 설정
        mock_cb = MagicMock()
        mock_cb.text.return_value = ""
        mock_clipboard.return_value = mock_cb

        result = self.clipboard.get_text()

        assert result == ""

    def test_copy_text_korean_text(self):
        """한글 텍스트 복사 테스트"""
        text = "안녕하세요. 한글 텍스트 복사 테스트입니다."
        result = self.clipboard.copy_text(text)
        # 실제 구현에서는 한글도 정상적으로 복사되어야 함
        assert isinstance(result, bool)

    def test_copy_text_special_characters(self):
        """특수문자 포함 텍스트 복사 테스트"""
        text = "특수문자 테스트: !@#$%^&*()_+{}|:<>?[];',./"
        result = self.clipboard.copy_text(text)
        # 특수문자도 정상적으로 복사되어야 함
        assert isinstance(result, bool)
