"""
PyHelios GUI Demo (高度模块化/可扩展)
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QLabel, QLineEdit, QColorDialog, QGroupBox, QFormLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from .core import PyHelios

class PlotControlPanel(QGroupBox):
    """参数设置面板，可扩展更多控件"""
    def __init__(self, parent=None):
        super().__init__("Plot Controls", parent)
        self.xlim_edit = QLineEdit()
        self.ylim_edit = QLineEdit()
        self.linewidth_edit = QLineEdit("0.5")
        self.linecolor_btn = QPushButton("Choose Color")
        self.linecolor = 'black'
        self.linecolor_btn.clicked.connect(self.choose_color)
        layout = QFormLayout()
        layout.addRow("xlim (e.g. 0,5)", self.xlim_edit)
        layout.addRow("ylim (e.g. -20,120)", self.ylim_edit)
        layout.addRow("Line Width", self.linewidth_edit)
        layout.addRow("Line Color", self.linecolor_btn)
        self.setLayout(layout)
    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.linecolor = color.name()
            self.linecolor_btn.setStyleSheet(f"background:{self.linecolor}")
    def get_params(self):
        params = {}
        if self.xlim_edit.text():
            try:
                params['xlim'] = tuple(float(x) for x in self.xlim_edit.text().split(','))
            except Exception:
                pass
        if self.ylim_edit.text():
            try:
                params['ylim'] = tuple(float(y) for y in self.ylim_edit.text().split(','))
            except Exception:
                pass
        try:
            params['line_width'] = float(self.linewidth_edit.text())
        except Exception:
            pass
        params['line_color'] = self.linecolor
        return params

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
    def clear(self):
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.draw()

class PyHeliosGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyHelios GUI Demo")
        self.helios = None
        self.data_file = None
        self.init_ui()
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        # 左侧：按钮和参数
        left_panel = QVBoxLayout()
        self.file_label = QLabel("No file loaded.")
        self.btn_load = QPushButton("选择数据文件")
        self.btn_load.clicked.connect(self.choose_file)
        self.btn_read = QPushButton("读取数据")
        self.btn_read.clicked.connect(self.read_data)
        self.btn_plot = QPushButton("Plot Radius")
        self.btn_plot.clicked.connect(self.plot_radius)
        self.plot_controls = PlotControlPanel()
        left_panel.addWidget(self.file_label)
        left_panel.addWidget(self.btn_load)
        left_panel.addWidget(self.btn_read)
        left_panel.addWidget(self.btn_plot)
        left_panel.addWidget(self.plot_controls)
        left_panel.addStretch()
        # 中间：matplotlib画布
        self.canvas = MatplotlibCanvas()
        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(self.canvas, 3)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    def choose_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "选择数据文件", "", "All Files (*)")
        if fname:
            self.data_file = fname
            self.file_label.setText(fname)
    def read_data(self):
        if not self.data_file:
            self.file_label.setText("请先选择数据文件！")
            return
        self.helios = PyHelios(self.data_file)
        self.helios.load_and_process()
        self.file_label.setText(f"已读取: {self.data_file}")
    def plot_radius(self):
        if not self.helios:
            self.file_label.setText("请先读取数据！")
            return
        params = self.plot_controls.get_params()
        self.canvas.clear()
        ax = self.helios.plotter.plot_radius(self.helios.data, **params)
        # 将ax绘制到self.canvas
        self.canvas.ax.clear()
        for line in ax.get_lines():
            self.canvas.ax.plot(line.get_xdata(), line.get_ydata(), color=line.get_color(), lw=line.get_linewidth())
        if 'xlim' in params:
            self.canvas.ax.set_xlim(*params['xlim'])
        if 'ylim' in params:
            self.canvas.ax.set_ylim(*params['ylim'])
        self.canvas.ax.set_xlabel(ax.get_xlabel())
        self.canvas.ax.set_ylabel(ax.get_ylabel())
        self.canvas.ax.set_title(ax.get_title())
        self.canvas.draw()

# 入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PyHeliosGUI()
    win.show()
    sys.exit(app.exec_()) 