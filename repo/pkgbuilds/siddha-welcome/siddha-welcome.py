#!/usr/bin/env python3
"""
Sydra OS Welcome Application (PySide6 / Qt6)
First-run onboarding wizard and quick setup.
"""

import sys
import os
import subprocess
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QListWidget, QListWidgetItem,
    QFrame, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class SydraWelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Sydra OS")
        self.setMinimumSize(800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #12141A;
            }
            QWidget {
                color: #F2F4F8;
                font-family: 'Inter', sans-serif;
            }
            QListWidget {
                background-color: rgba(18, 20, 28, 0.6);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 8px;
            }
            QListWidget::item:selected {
                background-color: #5B8DEF;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #5B8DEF;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A7CDD;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Navigation sidebar
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(200)
        self.nav_list.addItem("Welcome")
        self.nav_list.addItem("Appearance")
        self.nav_list.addItem("Gaming & GPU")
        self.nav_list.addItem("Developer Hub")
        self.nav_list.addItem("Snapshots")
        self.nav_list.currentRowChanged.connect(self.switch_page)
        main_layout.addWidget(self.nav_list)

        # Pages stack
        self.stack = QStackedWidget()
        self.stack.addWidget(self.create_welcome_page())
        self.stack.addWidget(self.create_appearance_page())
        self.stack.addWidget(self.create_gaming_page())
        self.stack.addWidget(self.create_dev_page())
        self.stack.addWidget(self.create_snapshots_page())
        main_layout.addWidget(self.stack)

        self.nav_list.setCurrentRow(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Welcome to Sydra OS")
        title.setFont(QFont("Inter", 22, QFont.Bold))
        layout.addWidget(title)

        desc = QLabel(
            "A professional glass desktop engineered for developers and gamers.\n"
            "Powered by Arch Linux, KDE Plasma 6 Wayland, and Siddha Glass Pro."
        )
        desc.setFont(QFont("Inter", 12))
        desc.setWordWrap(True)
        layout.addWidget(desc)
        layout.addStretch()
        return page

    def create_appearance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Desktop Appearance & Glass Presets")
        title.setFont(QFont("Inter", 18, QFont.Bold))
        layout.addWidget(title)

        desc = QLabel("Switch between tuned glass intensity modes:")
        layout.addWidget(desc)

        btn_pro = QPushButton("Set Mode: Pro (Subtle Glass)")
        btn_pro.clicked.connect(lambda: subprocess.run(["siddha-glass-set", "graphite", "pro"]))
        layout.addWidget(btn_pro)

        btn_flat = QPushButton("Set Mode: Flat (Battery / Low GPU Saver)")
        btn_flat.clicked.connect(lambda: subprocess.run(["siddha-glass-set", "graphite", "flat"]))
        layout.addWidget(btn_flat)

        layout.addStretch()
        return page

    def create_gaming_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Gaming & Hardware Setup")
        title.setFont(QFont("Inter", 18, QFont.Bold))
        layout.addWidget(title)

        status_box = QTextEdit()
        status_box.setReadOnly(True)
        status_box.setStyleSheet("background-color: rgba(0,0,0,0.4); border-radius: 8px; padding: 8px;")
        
        # Query GPU status
        try:
            res = subprocess.check_output(["siddha-gpu-setup", "--status"], text=True)
            status_box.setPlainText(res)
        except Exception as e:
            status_box.setPlainText(f"GPU check: {e}")
            
        layout.addWidget(status_box)

        btn_steam = QPushButton("Launch Steam")
        btn_steam.clicked.connect(lambda: subprocess.Popen(["steam"]))
        layout.addWidget(btn_steam)

        layout.addStretch()
        return page

    def create_dev_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("Developer Workstation")
        title.setFont(QFont("Inter", 18, QFont.Bold))
        layout.addWidget(title)

        desc = QLabel("Launch the interactive Sydra Developer Hub in terminal to configure toolchains:")
        layout.addWidget(desc)

        btn_dev = QPushButton("Open Developer Hub CLI")
        btn_dev.clicked.connect(lambda: subprocess.Popen(["konsole", "-e", "siddha-dev"]))
        layout.addWidget(btn_dev)

        layout.addStretch()
        return page

    def create_snapshots_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        title = QLabel("System Rollback & Snapshots")
        title.setFont(QFont("Inter", 18, QFont.Bold))
        layout.addWidget(title)

        desc = QLabel(
            "Sydra OS automatically captures snapshots before and after system updates using Snapper.\n\n"
            "If an update ever breaks something, simply reboot, select an earlier snapshot directly in the "
            "GRUB bootloader menu, and roll back effortlessly."
        )
        desc.setWordWrap(True)
        layout.addWidget(desc)
        layout.addStretch()
        return page

def main():
    app = QApplication(sys.argv)
    window = SydraWelcomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
