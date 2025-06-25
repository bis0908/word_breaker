import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QSpinBox,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
)
from PySide6.QtCore import Qt

from ui.ui_dialog import Ui_Dialog
from core.text_processor import TextProcessor, DEFAULT_LINE_LENGTH
from utils.clipboard_helper import ClipboardHelper


class TextBreakerApp(QDialog):
    """텍스트 문단 가다듬기 메인 애플리케이션"""

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 줄 길이 설정 (기본값: 18)
        self.line_length = DEFAULT_LINE_LENGTH

        # 새로운 옵션들
        self.use_all_chars = True  # 모든 문자 카운팅 사용
        self.separate_sentences = True  # 마침표 분리 사용

        # 모듈 인스턴스
        self.text_processor = TextProcessor()
        self.clipboard_helper = ClipboardHelper()

        # UI 초기화
        self._setup_ui()
        self._connect_events()

    def _setup_ui(self):
        """UI 설정 및 추가 요소 생성"""
        # 윈도우 제목 설정
        self.setWindowTitle("텍스트 문단 가다듬기 프로그램")

        # 최소화 버튼 설정
        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)

        # text_area 폭 조정 (오른쪽 UI 컨트롤과의 여백 확보)
        self.ui.plainTextEdit.setGeometry(10, 10, 400, 500)
        self.ui.label.setGeometry(10, 525, 500, 31)

        # 줄 길이 설정 그룹 추가
        self._setup_line_length_controls()

        # 추가 UI 컨트롤들 설정
        self._setup_additional_controls()

        # 초기 상태 메시지 설정
        self.ui.label.setText("작업 대기 중...")

        # 버튼 텍스트 변경
        self.ui.buttonBox.button(self.ui.buttonBox.StandardButton.Ok).setText("적용")
        self.ui.buttonBox.button(self.ui.buttonBox.StandardButton.Save).setText("복사")
        self.ui.buttonBox.button(self.ui.buttonBox.StandardButton.Close).setText("닫기")

        # Cancel 버튼이 있는 경우에만 숨기기
        cancel_button = self.ui.buttonBox.button(
            self.ui.buttonBox.StandardButton.Cancel
        )
        if cancel_button:
            cancel_button.hide()

    def _setup_additional_controls(self):
        """추가 UI 컨트롤들 설정"""
        # 마침표 분리 체크박스
        self.sentence_separation_checkbox = QCheckBox("마침표 분리", self)
        self.sentence_separation_checkbox.setGeometry(520, 140, 90, 20)
        self.sentence_separation_checkbox.setChecked(True)
        self.sentence_separation_checkbox.stateChanged.connect(
            self.on_sentence_separation_changed
        )

        # 초기화 버튼
        self.clear_button = QPushButton("내용 초기화", self)
        self.clear_button.setGeometry(530, 100, 81, 25)
        self.clear_button.clicked.connect(self.clear_text_area)

    def _setup_line_length_controls(self):
        """줄 길이 설정 컨트롤 생성"""
        # 줄 길이 설정 그룹박스 생성
        self.line_length_group = QGroupBox("줄 길이 설정")
        layout = QVBoxLayout()

        # SpinBox와 라벨을 위한 수평 레이아웃
        h_layout = QHBoxLayout()

        # SpinBox 생성
        self.line_length_spinbox = QSpinBox()
        self.line_length_spinbox.setMinimum(10)
        self.line_length_spinbox.setMaximum(100)
        self.line_length_spinbox.setValue(DEFAULT_LINE_LENGTH)
        self.line_length_spinbox.setSuffix("자")

        # 현재 값 표시 라벨
        self.current_length_label = QLabel(f"현재 줄 길이: {DEFAULT_LINE_LENGTH}자")

        h_layout.addWidget(QLabel("줄 길이:"))
        h_layout.addWidget(self.line_length_spinbox)
        h_layout.addStretch()

        layout.addLayout(h_layout)
        layout.addWidget(self.current_length_label)

        self.line_length_group.setLayout(layout)

        # 기존 레이아웃에 추가 (버튼 위에)
        self.line_length_group.setGeometry(441, 200, 170, 80)
        self.line_length_group.setParent(self)

    def _connect_events(self):
        """이벤트 연결"""
        # 기존 버튼 이벤트 연결 해제
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.rejected.disconnect()

        # 새로운 이벤트 연결
        self.ui.buttonBox.button(self.ui.buttonBox.StandardButton.Ok).clicked.connect(
            self.apply_formatting
        )
        self.ui.buttonBox.button(self.ui.buttonBox.StandardButton.Save).clicked.connect(
            self.copy_to_clipboard
        )
        self.ui.buttonBox.button(
            self.ui.buttonBox.StandardButton.Close
        ).clicked.connect(self.close)

        # 줄 길이 변경 이벤트
        self.line_length_spinbox.valueChanged.connect(self.on_line_length_changed)

    def on_sentence_separation_changed(self, state):
        """마침표 분리 체크박스 이벤트"""
        self.separate_sentences = state == Qt.CheckState.Checked.value

    def clear_text_area(self):
        """텍스트 영역 초기화"""
        self.ui.plainTextEdit.clear()
        self.update_status("텍스트 영역이 초기화되었습니다.", True)

    def apply_formatting(self):
        """텍스트 가다듬기 적용"""
        try:
            # 입력 텍스트 가져오기
            input_text = self.ui.plainTextEdit.toPlainText()

            if not input_text.strip():
                self.update_status("입력 텍스트가 비어있습니다.", False)
                return

            # 새로운 옵션들을 반영한 텍스트 처리
            result = self.text_processor.format_text_with_options(
                input_text,
                self.line_length,
                use_all_chars=self.use_all_chars,
                separate_sentences=self.separate_sentences,
            )

            # 결과를 입력 영역에 표시
            self.ui.plainTextEdit.setPlainText(result)

            # 모든 문자 카운팅으로 변경
            char_count = self.text_processor.count_all_chars(result)

            # 성공 메시지 표시
            self.update_status(
                f"작업 성공! 전체 텍스트 갯수(공백 제외): {char_count}자 (줄 길이: {self.line_length}자)",
                True,
            )

        except Exception as e:
            self.update_status(f"작업 실패: {str(e)}", False)

    def copy_to_clipboard(self):
        """클립보드로 복사"""
        try:
            # 현재 텍스트 영역의 내용 가져오기
            text = self.ui.plainTextEdit.toPlainText()

            if not text.strip():
                self.update_status("복사할 텍스트가 없습니다.", False)
                return

            # 클립보드로 복사
            success = self.clipboard_helper.copy_text(text)

            if success:
                self.update_status("클립보드로 복사 완료!", True)
            else:
                self.update_status("클립보드 복사 실패!", False)

        except Exception as e:
            self.update_status(f"복사 실패: {str(e)}", False)

    def on_line_length_changed(self, value):
        """줄 길이 변경 이벤트 처리"""
        self.line_length = value
        self.current_length_label.setText(f"현재 줄 길이: {value}자")

    def update_status(self, message: str, is_success: bool = True):
        """상태 메시지 업데이트"""
        self.ui.label.setText(message)

        # 성공/실패에 따른 색상 변경
        if is_success:
            self.ui.label.setStyleSheet("color: green;")
        else:
            self.ui.label.setStyleSheet("color: red;")


def main():
    """메인 함수"""
    app = QApplication(sys.argv)

    # 애플리케이션 생성 및 실행
    window = TextBreakerApp()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
