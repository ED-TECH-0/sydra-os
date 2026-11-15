#!/usr/bin/env python3
"""
Sydra Game Hub (PySide6 / Qt6)
Curated native game catalog and Steam library launcher with status badges.
"""

import sys
import os
import subprocess

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QLabel, QPushButton, QListWidget, QListWidgetItem, QFrame,
        QCheckBox
    )
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QFont, QColor
except ImportError:
    QMainWindow = object
    QApplication = None

try:
    import yaml
except ImportError:
    yaml = None

def load_yaml_fallback(filepath):
    # Simple parser for the flat catalog structure
    games = []
    current = {}
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('- id:'):
                if current:
                    games.append(current)
                current = {'id': line.split(':', 1)[1].strip()}
            elif ':' in line and current:
                k, v = line.split(':', 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                current[k] = v
    if current:
        games.append(current)
    return games

class SydraGameHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sydra Game Hub")
        self.setMinimumSize(900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #12141A;
            }
            QWidget {
                color: #F2F4F8;
                font-family: 'Inter', sans-serif;
            }
            QListWidget {
                background-color: rgba(18, 20, 28, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 12px;
                padding: 10px;
            }
            QListWidget::item {
                padding: 14px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            }
            QPushButton {
                background-color: #5B8DEF;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4A7CDD;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Game list
        list_container = QWidget()
        list_layout = QVBoxLayout(list_container)
        
        header = QLabel("Discover Games & Native Catalog")
        header.setFont(QFont("Inter", 16, QFont.Bold))
        list_layout.addWidget(header)

        self.game_list = QListWidget()
        self.game_list.currentRowChanged.connect(self.display_game_details)
        list_layout.addWidget(self.game_list)
        main_layout.addWidget(list_container, stretch=3)

        # Details & Launch Panel
        self.detail_panel = QFrame()
        self.detail_panel.setStyleSheet("""
            QFrame {
                background-color: rgba(25, 28, 38, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.14);
                border-radius: 14px;
                padding: 16px;
            }
        """)
        self.detail_layout = QVBoxLayout(self.detail_panel)
        
        self.lbl_title = QLabel("Select a game")
        self.lbl_title.setFont(QFont("Inter", 20, QFont.Bold))
        self.detail_layout.addWidget(self.lbl_title)

        self.lbl_badge = QLabel("")
        self.lbl_badge.setFont(QFont("Inter", 11, QFont.Bold))
        self.detail_layout.addWidget(self.lbl_badge)

        self.lbl_genre = QLabel("")
        self.detail_layout.addWidget(self.lbl_genre)

        self.lbl_notes = QLabel("")
        self.lbl_notes.setWordWrap(True)
        self.detail_layout.addWidget(self.lbl_notes)

        self.detail_layout.addSpacing(20)
        self.detail_layout.addWidget(QLabel("Launch Optimizations:"))

        self.chk_prime = QCheckBox("PRIME Offload (Run on NVIDIA dGPU)")
        self.chk_gamemode = QCheckBox("GameMode (Unload compositor blur)")
        self.chk_gamemode.setChecked(True)
        self.chk_mangohud = QCheckBox("MangoHud (FPS & Performance overlay)")

        self.detail_layout.addWidget(self.chk_prime)
        self.detail_layout.addWidget(self.chk_gamemode)
        self.detail_layout.addWidget(self.chk_mangohud)

        self.detail_layout.addSpacing(20)
        self.btn_action = QPushButton("Install / Play")
        self.btn_action.clicked.connect(self.launch_game)
        self.detail_layout.addWidget(self.btn_action)

        self.detail_layout.addStretch()
        main_layout.addWidget(self.detail_panel, stretch=2)

        self.load_catalog()

    def load_catalog(self):
        catalog_path = None
        for p in [
            "/usr/share/siddha/catalog/native-games.yaml",
            "/usr/share/siddha/gamehub/native-games.yaml",
            "catalog/native-games.yaml",
        ]:
            if os.path.exists(p):
                catalog_path = p
                break

        self.games = []
        if catalog_path and os.path.exists(catalog_path):
            if yaml:
                try:
                    with open(catalog_path) as f:
                        self.games = yaml.safe_load(f) or []
                except Exception as e:
                    print(f"YAML load failed, trying fallback: {e}")
                    self.games = load_yaml_fallback(catalog_path)
            else:
                self.games = load_yaml_fallback(catalog_path)

        for g in self.games:
            item = QListWidgetItem(f"{g.get('name', 'Unknown')} [{g.get('badge', 'NATIVE')}]")
            self.game_list.addItem(item)

        if self.games:
            self.game_list.setCurrentRow(0)

    def display_game_details(self, index):
        if index < 0 or index >= len(self.games):
            return
        g = self.games[index]
        self.lbl_title.setText(g.get("name", "Unknown"))
        badge = g.get("badge", "NATIVE")
        self.lbl_badge.setText(f"Status: {badge}")
        
        if badge == "NATIVE":
            self.lbl_badge.setStyleSheet("color: #4FB3BF; font-weight: bold;")
        elif badge == "PROTON":
            self.lbl_badge.setStyleSheet("color: #5B8DEF; font-weight: bold;")
        else:
            self.lbl_badge.setStyleSheet("color: #EB5F5F; font-weight: bold;")

        self.lbl_genre.setText(f"Genre: {g.get('genre', 'Gaming')} | Source: {g.get('source', 'pacman')}")
        self.lbl_notes.setText(g.get("notes", ""))
        self.selected_game = g

    def launch_game(self):
        if not hasattr(self, "selected_game"):
            return
        g = self.selected_game
        install_target = g.get("install", "")
        source = g.get("source", "pacman")

        cmd = []
        if self.chk_prime.isChecked():
            cmd.append("prime-run")
        if self.chk_gamemode.isChecked():
            cmd.append("gamemoderun")
        if self.chk_mangohud.isChecked():
            cmd.append("mangohud")

        if source == "pacman":
            if subprocess.run(["which", install_target], capture_output=True).returncode == 0:
                cmd.append(install_target)
                subprocess.Popen(cmd)
            else:
                subprocess.Popen(["konsole", "-e", f"sudo pacman -S --needed {install_target}"])
        elif source == "steam":
            subprocess.Popen(["steam", f"steam://rungameid/{install_target}"])

def dump_badges():
    for p in [
        "/usr/share/siddha/catalog/native-games.yaml",
        "/usr/share/siddha/gamehub/native-games.yaml",
        "catalog/native-games.yaml",
    ]:
        if os.path.exists(p):
            catalog_path = p
            break
    else:
        print("Catalog not found")
        return

    if yaml:
        with open(catalog_path) as f:
            data = yaml.safe_load(f) or []
    else:
        data = load_yaml_fallback(catalog_path)
        
    for item in data:
        print(f"{item.get('name')}: {item.get('badge')}")

if __name__ == "__main__":
    if "--dump-badges" in sys.argv:
        dump_badges()
        sys.exit(0)

    if QApplication is None:
        print("Error: PySide6 is required to run Sydra Game Hub UI.", file=sys.stderr)
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("Sydra Game Hub")
    window = SydraGameHub()
    window.show()
    sys.exit(app.exec())
