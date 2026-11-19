#!/usr/bin/env python3
"""
Sydra OS - Glass & UI Customization Control Panel
Provides a graphical interface to customize Glassmorphism levels, themes,
panel/dock translucency, autohide, interface density, and active window hints.
"""

import sys
import os
import subprocess

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QSlider, QComboBox, QCheckBox, QGroupBox,
        QRadioButton, QButtonGroup, QScrollArea, QFrame, QMessageBox
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QColor
except ImportError:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QSlider, QComboBox, QCheckBox, QGroupBox,
        QRadioButton, QButtonGroup, QScrollArea, QFrame, QMessageBox
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont, QColor

class SydraGlassControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sydra Glass & UI Customizer")
        self.setMinimumSize(680, 720)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #12141A;
            }
            QWidget {
                color: #F1F5F9;
                font-family: 'Inter', sans-serif;
                font-size: 13px;
            }
            QGroupBox {
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                margin-top: 18px;
                padding: 16px;
                background-color: rgba(26, 30, 42, 0.50);
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 6px;
                color: #5B8DEF;
            }
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(255, 255, 255, 0.15);
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #5B8DEF;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #FFFFFF;
                border: 2px solid #5B8DEF;
                width: 18px;
                margin-top: -6px;
                margin-bottom: -6px;
                border-radius: 9px;
            }
            QComboBox {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                padding: 6px 12px;
                min-height: 24px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1A1E2B;
                selection-background-color: #5B8DEF;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
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
            QPushButton#resetBtn {
                background-color: rgba(255, 255, 255, 0.08);
                color: #CBD5E1;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            QPushButton#resetBtn:hover {
                background-color: rgba(255, 255, 255, 0.15);
                color: #FFFFFF;
            }
            QRadioButton {
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                background: transparent;
            }
            QRadioButton::indicator:checked {
                border: 2px solid #5B8DEF;
                background: #5B8DEF;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                background: transparent;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #5B8DEF;
                background: #5B8DEF;
            }
        """)

        # Main scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(scroll)

        container = QWidget()
        scroll.setWidget(container)
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header
        header = QLabel("Sydra Glass & Desktop Customizer")
        header.setFont(QFont("Inter", 20, QFont.Bold))
        subhead = QLabel("Personalize glassmorphism transparency, desktop panel & dock styling, and window aesthetics.")
        subhead.setStyleSheet("color: #94A3B8; font-size: 13px;")
        main_layout.addWidget(header)
        main_layout.addWidget(subhead)

        # 1. Color Palette Presets
        grp_preset = QGroupBox("Color & Aesthetic Presets")
        l_preset = QVBoxLayout(grp_preset)
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Obsidian (Sydra Signature Dark & Sapphire Blue)",
            "Teal (Electric Cyan & Deep Midnight)",
            "Cyber-Cyan (Vivid Neon Cyan & Carbon)",
            "Emerald (Matrix Deep Emerald Glass)",
            "Amethyst (Purple Aurora Neon Glass)",
            "Sunset (Warm Amber Coral Glass)",
            "Slate-Light (Clean Frosted Daylight)",
            "OLED (Pure Pitch Black - Battery Saver)"
        ])
        l_preset.addWidget(self.preset_combo)
        main_layout.addWidget(grp_preset)

        # 2. Glassmorphism Transparency Level
        grp_glass = QGroupBox("Window Glassmorphism Transparency")
        l_glass = QVBoxLayout(grp_glass)
        self.glass_combo = QComboBox()
        self.glass_combo.addItems([
            "Crystal (Ultra-Translucent Glass - 20% Opacity)",
            "Sleek Pro (Tuned Sydra Glass - 35% Opacity)",
            "Standard (Balanced Glass - 55% Opacity)",
            "Frost (Diffused Matte Frost - 75% Opacity)",
            "Flat (Solid Opaque - Zero Blur)"
        ])
        self.glass_combo.setCurrentIndex(1) # Default: Sleek Pro
        l_glass.addWidget(self.glass_combo)
        main_layout.addWidget(grp_glass)

        # 3. Panel & Dock Opacity Controls
        grp_panel = QGroupBox("Top Panel & Bottom Dock Opacity")
        l_panel = QVBoxLayout(grp_panel)

        # Panel Slider
        l_p_lbl = QHBoxLayout()
        l_p_lbl.addWidget(QLabel("Top Panel Opacity:"))
        self.panel_val_lbl = QLabel("5%")
        self.panel_val_lbl.setStyleSheet("color: #4FB3BF; font-weight: bold;")
        l_p_lbl.addStretch()
        l_p_lbl.addWidget(self.panel_val_lbl)
        l_panel.addLayout(l_p_lbl)

        self.panel_slider = QSlider(Qt.Horizontal)
        self.panel_slider.setRange(0, 100)
        self.panel_slider.setValue(5)
        self.panel_slider.valueChanged.connect(lambda v: self.panel_val_lbl.setText(f"{v}%"))
        l_panel.addWidget(self.panel_slider)

        # Dock Slider
        l_d_lbl = QHBoxLayout()
        l_d_lbl.addWidget(QLabel("Bottom Dock Opacity:"))
        self.dock_val_lbl = QLabel("29%")
        self.dock_val_lbl.setStyleSheet("color: #4FB3BF; font-weight: bold;")
        l_d_lbl.addStretch()
        l_d_lbl.addWidget(self.dock_val_lbl)
        l_panel.addLayout(l_d_lbl)

        self.dock_slider = QSlider(Qt.Horizontal)
        self.dock_slider.setRange(0, 100)
        self.dock_slider.setValue(29)
        self.dock_slider.valueChanged.connect(lambda v: self.dock_val_lbl.setText(f"{v}%"))
        l_panel.addWidget(self.dock_slider)

        # Dock Autohide
        l_ah = QHBoxLayout()
        l_ah.addWidget(QLabel("Dock Autohide:"))
        self.autohide_combo = QComboBox()
        self.autohide_combo.addItems([
            "Never (Always Visible)",
            "On Overlap (Intellihide - Hide on Window Maximize)",
            "Always (Hover to Reveal)"
        ])
        l_ah.addWidget(self.autohide_combo)
        l_panel.addLayout(l_ah)

        main_layout.addWidget(grp_panel)

        # 4. Interface Density & Active Window Hint
        grp_density = QGroupBox("Interface & Window Behavior")
        l_density = QVBoxLayout(grp_density)

        # Density Radios
        l_d_radios = QHBoxLayout()
        l_d_radios.addWidget(QLabel("Interface Density:"))
        self.density_group = QButtonGroup(self)
        self.rb_compact = QRadioButton("Compact")
        self.rb_comfy = QRadioButton("Comfortable")
        self.rb_spacious = QRadioButton("Spacious")
        self.rb_comfy.setChecked(True)
        self.density_group.addButton(self.rb_compact, 0)
        self.density_group.addButton(self.rb_comfy, 1)
        self.density_group.addButton(self.rb_spacious, 2)
        l_d_radios.addWidget(self.rb_compact)
        l_d_radios.addWidget(self.rb_comfy)
        l_d_radios.addWidget(self.rb_spacious)
        l_d_radios.addStretch()
        l_density.addLayout(l_d_radios)

        # Corner Roundness
        l_round = QHBoxLayout()
        l_round.addWidget(QLabel("Window Corner Roundness:"))
        self.round_combo = QComboBox()
        self.round_combo.addItems([
            "Modern Rounded (14px - Default)",
            "Sharp (4px)",
            "Extra-Round (24px)"
        ])
        l_round.addWidget(self.round_combo)
        l_density.addLayout(l_round)

        # Active Window Hint
        self.chk_hint = QCheckBox("Show Active Window Highlight Border Hint")
        self.chk_hint.setChecked(False) # Off by default
        l_density.addWidget(self.chk_hint)

        main_layout.addWidget(grp_density)

        # Action Buttons
        btn_bar = QHBoxLayout()
        self.btn_reset = QPushButton("Reset to Sydra Defaults")
        self.btn_reset.setObjectName("resetBtn")
        self.btn_reset.clicked.connect(self.reset_defaults)
        btn_bar.addWidget(self.btn_reset)

        self.btn_apply = QPushButton("Apply Glassmorphism")
        self.btn_apply.clicked.connect(self.apply_settings)
        btn_bar.addWidget(self.btn_apply)

        main_layout.addLayout(btn_bar)

    def reset_defaults(self):
        self.preset_combo.setCurrentIndex(0) # Obsidian
        self.glass_combo.setCurrentIndex(1)  # Sleek Pro
        self.panel_slider.setValue(5)
        self.dock_slider.setValue(29)
        self.autohide_combo.setCurrentIndex(0) # Never
        self.rb_comfy.setChecked(True)
        self.round_combo.setCurrentIndex(0)
        self.chk_hint.setChecked(False)
        self.apply_settings()

    def apply_settings(self):
        preset_map = [
            "obsidian", "teal", "cyber-cyan", "emerald",
            "amethyst", "sunset", "slate-light", "oled"
        ]
        glass_map = ["crystal", "pro", "standard", "frost", "flat"]
        density_map = ["compact", "comfortable", "spacious"]
        autohide_map = ["never", "overlap", "always"]
        round_map = ["rounded", "sharp", "extra"]

        sel_preset = preset_map[self.preset_combo.currentIndex()]
        sel_glass = glass_map[self.glass_combo.currentIndex()]
        sel_density = density_map[self.density_group.checkedId()]
        sel_autohide = autohide_map[self.autohide_combo.currentIndex()]
        sel_round = round_map[self.round_combo.currentIndex()]
        sel_hint = "on" if self.chk_hint.isChecked() else "off"

        panel_opacity = round(self.panel_slider.value() / 100.0, 2)
        dock_opacity = round(self.dock_slider.value() / 100.0, 2)

        cmd = [
            "/usr/bin/siddha-glass-set",
            "--preset", sel_preset,
            "--glass", sel_glass,
            "--panel-opacity", str(panel_opacity),
            "--dock-opacity", str(dock_opacity),
            "--density", sel_density,
            "--autohide", sel_autohide,
            "--roundness", sel_round,
            "--hint", sel_hint
        ]

        try:
            subprocess.run(cmd, check=True)
            msg = QMessageBox(self)
            msg.setWindowTitle("Settings Applied")
            msg.setText("Sydra Glassmorphism settings updated successfully!\nCOSMIC UI has reloaded.")
            msg.setStyleSheet("background-color: #1A1E2B; color: #FFFFFF;")
            msg.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply settings:\n{e}")

def main():
    app = QApplication(sys.argv)
    window = SydraGlassControl()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
