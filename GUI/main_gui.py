import sys
import json
import csv
import os
import hashlib
from functools import partial
from dataclasses import dataclass, field, asdict
from typing import Optional, List
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, 
                               QStackedWidget, QGridLayout, QSizePolicy, QHBoxLayout,
                               QLineEdit, QMessageBox, QScrollArea, QTableWidget, 
                               QTableWidgetItem, QHeaderView, QAbstractItemView)
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QObject

import random
import time
from power import power_runner
from reaction_time import reaction_time_runner as rt_runner

# Import from new compartmentalized modules
from core import TrainingConfig, TechCorrConfig, AppState, PageIndex, ButtonStyle
from utils import (
    get_users_csv_path, hash_password, load_users, save_users,
    get_user_level, set_user_level, get_user_progress, update_user_progress,
    calculate_user_progress_from_combos, get_training_csv_path
)



# ============================================================================
# Page Classes
# ============================================================================

def get_users_csv_path():
    """Get the path to the users CSV file."""
    return os.path.join(os.path.dirname(__file__), "users.csv")


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users() -> dict:
    """Load users from CSV file. Returns dict of {username: {"password_hash": ..., "level": ..., "progress": ...}}."""
    users = {}
    csv_path = get_users_csv_path()
    if os.path.exists(csv_path):
        try:
            with open(csv_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    users[row['username']] = {
                        'password_hash': row['password_hash'],
                        'level': row.get('level', 'Beginner'),
                        'progress': float(row.get('progress', '0.0'))
                    }
        except Exception as e:
            print(f"Error loading users: {e}")
    return users


def save_users(users: dict) -> bool:
    """Save users dict to CSV file. Returns True on success."""
    csv_path = get_users_csv_path()
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'password_hash', 'level', 'progress'])
            writer.writeheader()
            for username, user_data in users.items():
                if isinstance(user_data, dict):
                    writer.writerow({
                        'username': username,
                        'password_hash': user_data['password_hash'],
                        'level': user_data.get('level', 'Beginner'),
                        'progress': user_data.get('progress', 0.0)
                    })
                else:
                    # Backward compatibility for old format
                    writer.writerow({
                        'username': username,
                        'password_hash': user_data,
                        'level': 'Beginner',
                        'progress': 0.0
                    })
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False


def get_user_level(username: str) -> str:
    """Get the current level of a user. Returns 'Beginner', 'Intermediate', or 'Advanced'."""
    users = load_users()
    if username in users:
        user_data = users[username]
        if isinstance(user_data, dict):
            return user_data.get('level', 'Beginner')
        return 'Beginner'
    return 'Beginner'


def set_user_level(username: str, level: str) -> bool:
    """Set the level of a user. Returns True on success."""
    if level not in ['Beginner', 'Intermediate', 'Advanced']:
        print(f"Invalid level: {level}")
        return False
    users = load_users()
    if username in users:
        users[username]['level'] = level
        return save_users(users)
    return False


def get_user_progress(username: str) -> float:
    """Get the current progress percentage of a user (0.0-100.0)."""
    users = load_users()
    if username in users:
        user_data = users[username]
        if isinstance(user_data, dict):
            return user_data.get('progress', 0.0)
        return 0.0
    return 0.0


def update_user_progress(username: str, progress: float) -> bool:
    """
    Update user's progress percentage and auto-level up if thresholds met.
    
    Progress thresholds:
    - Beginner -> Intermediate: 80% progress at Beginner level
    - Intermediate -> Advanced: 80% progress at Intermediate level
    
    Args:
        username: Username to update
        progress: Progress percentage (0.0-100.0)
    
    Returns:
        bool: True on success
    """
    users = load_users()
    if username not in users:
        return False
    
    # Clamp progress to 0-100
    progress = max(0.0, min(100.0, progress))
    
    current_level = users[username].get('level', 'Beginner')
    users[username]['progress'] = progress
    
    # Auto level-up logic
    if current_level == 'Beginner' and progress >= 80.0:
        users[username]['level'] = 'Intermediate'
        users[username]['progress'] = 0.0  # Reset progress for new level
        print(f"User {username} leveled up to Intermediate!")
    elif current_level == 'Intermediate' and progress >= 80.0:
        users[username]['level'] = 'Advanced'
        users[username]['progress'] = 0.0  # Reset progress for new level
        print(f"User {username} leveled up to Advanced!")
    
    return save_users(users)


def calculate_user_progress_from_combos(username: str, db_path: str) -> float:
    """
    Calculate user's progress based on combo mastery from database.
    
    Progress = (Average mastery score of all combos at current level) * 100
    
    Args:
        username: Username to calculate progress for
        db_path: Path to combos.db database
    
    Returns:
        float: Progress percentage (0.0-100.0)
    """
    try:
        import sys
        import os
        # Add combo_curriculum to path if not already there
        curriculum_path = os.path.join(os.path.dirname(__file__), 'combo_curriculum')
        if curriculum_path not in sys.path:
            sys.path.insert(0, curriculum_path)
        
        from combo_curriculum import ComboCurriculum
        
        # Get user's current level
        level = get_user_level(username)
        
        # Query combos at that level
        with ComboCurriculum(db_path) as curriculum:
            combos = curriculum.get_combos_by_difficulty(level)
            
            if not combos:
                return 0.0
            
            # Calculate average mastery score
            total_mastery = sum(combo.get('mastery_score', 0.0) for combo in combos)
            avg_mastery = total_mastery / len(combos)
            
            # Convert to percentage (mastery_score is 0.0-1.0)
            progress = avg_mastery * 100.0
            
            return progress
    
    except Exception as e:
        print(f"Error calculating progress from combos: {e}")
        return 0.0


def get_training_csv_path(username: str):
    """Get the path to a user's training history CSV file."""
    return os.path.join(os.path.dirname(__file__), f"training_{username}.csv")


class LoginPage(QWidget):
    """Login/Signup page shown on application startup."""
    
    def __init__(self, stacked_widget, app_state):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.current_user = None
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(100, 30, 100, 30)
        
        # Title
        title = QLabel("Boxing Training App")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: white;")
        title.setFixedHeight(50)

        
        # Username field
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        username_label.setFixedHeight(25)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 8px;
                min-width: 350px;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        
        # Password field
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        password_label.setFixedHeight(25)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 8px;
                min-width: 350px;
                background-color: white;
                color: black;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)
        
        # Status label for error messages
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
        self.status_label.setFixedHeight(20)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        login_btn = QPushButton("Login")
        signup_btn = QPushButton("Sign Up")
        manage_users_btn = QPushButton("Manage Users")
        
        login_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        signup_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        manage_users_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        
        login_btn.setFixedSize(180, 45)
        signup_btn.setFixedSize(180, 45)
        manage_users_btn.setFixedSize(180, 45)
        
        login_btn.clicked.connect(self.on_login)
        signup_btn.clicked.connect(self.on_signup)
        manage_users_btn.clicked.connect(self.on_manage_users)
        
        # Enable login on Enter key press
        self.password_input.returnPressed.connect(self.on_login)
        self.username_input.returnPressed.connect(lambda: self.password_input.setFocus())
        
        button_layout.addStretch()
        button_layout.addWidget(login_btn)
        button_layout.addWidget(signup_btn)
        button_layout.addStretch()
        
        # Layout assembly - compact spacing
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addSpacing(15)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(5)
        layout.addWidget(self.status_label)
        layout.addSpacing(15)
        layout.addLayout(button_layout)
        layout.addSpacing(10)
        layout.addWidget(manage_users_btn, alignment=Qt.AlignCenter)
        layout.addStretch(1)
        
        self.setLayout(layout)
    
    def on_login(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText("Please enter both username and password")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        users = load_users()
        password_hash = hash_password(password)
        
        if username in users and isinstance(users[username], dict) and users[username]['password_hash'] == password_hash:
            self.current_user = username
            self.status_label.setText(f"Welcome back, {username}!")
            self.status_label.setStyleSheet("font-size: 14px; color: #4CAF50;")
            # Clear inputs
            self.username_input.clear()
            self.password_input.clear()
            # Navigate to homepage
            QTimer.singleShot(500, lambda: self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE))
        else:
            self.status_label.setText("Invalid username or password")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
    
    def on_signup(self):
        """Handle signup button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.status_label.setText("Please enter both username and password")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        if len(username) < 3:
            self.status_label.setText("Username must be at least 3 characters")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        if len(password) < 4:
            self.status_label.setText("Password must be at least 4 characters")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        users = load_users()
        
        if username in users:
            self.status_label.setText("Username already exists")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
            return
        
        # Add new user with Beginner level and 0% progress
        users[username] = {
            'password_hash': hash_password(password),
            'level': 'Beginner',
            'progress': 0.0
        }
        if save_users(users):
            self.current_user = username
            self.status_label.setText(f"Account created! Welcome, {username}!")
            self.status_label.setStyleSheet("font-size: 14px; color: #4CAF50;")
            # Clear inputs
            self.username_input.clear()
            self.password_input.clear()
            # Navigate to homepage
            QTimer.singleShot(500, lambda: self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE))
        else:
            self.status_label.setText("Error creating account. Please try again.")
            self.status_label.setStyleSheet("font-size: 14px; color: #f44336;")
    
    def on_manage_users(self):
        """Navigate to user management page."""
        self.stacked_widget.setCurrentIndex(PageIndex.USER_MANAGEMENT)
    
    def get_current_user(self):
        """Return the currently logged in user."""
        return self.current_user


class UserManagementPage(QWidget):
    """Page to view and delete users."""
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 30, 50, 30)
        
        # Title
        title = QLabel("User Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 20px; color: white;")
        
        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(["Username", "Level", "Progress", "Training Sessions", "Actions"])
        self.user_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.user_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.user_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.user_table.setStyleSheet("""
            QTableWidget {
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: white;
                color: black;
            }
            QTableWidget::item {
                padding: 10px;
                color: black;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
        """)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        refresh_btn = QPushButton("Refresh")
        back_btn = QPushButton("Back to Login")
        
        refresh_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        
        refresh_btn.setFixedSize(200, 50)
        back_btn.setFixedSize(200, 50)
        
        refresh_btn.clicked.connect(self.refresh_users)
        back_btn.clicked.connect(self.on_back)
        
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()
        
        # Layout assembly
        layout.addWidget(title)
        layout.addWidget(self.user_table)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def showEvent(self, event):
        """Refresh user list when page is shown."""
        super().showEvent(event)
        self.refresh_users()
    
    def refresh_users(self):
        """Load and display all users."""
        users = load_users()
        self.user_table.setRowCount(len(users))
        for row, username in enumerate(users.keys()):
            # Username
            username_item = QTableWidgetItem(username)
            username_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 0, username_item)

            # Level
            user_data = users[username]
            level = user_data.get('level', 'Beginner') if isinstance(user_data, dict) else 'Beginner'
            level_item = QTableWidgetItem(level)
            level_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 1, level_item)

            # Progress
            progress = user_data.get('progress', 0.0) if isinstance(user_data, dict) else 0.0
            progress_item = QTableWidgetItem(f"{progress:.1f}%")
            progress_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 2, progress_item)

            # Training sessions count
            training_csv = get_training_csv_path(username)
            session_count = 0
            if os.path.exists(training_csv):
                try:
                    with open(training_csv, 'r', newline='', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        next(reader, None)  # Skip header
                        session_count = sum(1 for _ in reader)
                except:
                    pass
            sessions_item = QTableWidgetItem(str(session_count))
            sessions_item.setTextAlignment(Qt.AlignCenter)
            self.user_table.setItem(row, 3, sessions_item)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
                QPushButton:pressed {
                    background-color: #c41504;
                }
            """)
            delete_btn.clicked.connect(partial(self.delete_user, username))
            self.user_table.setCellWidget(row, 4, delete_btn)
        
        self.user_table.resizeRowsToContents()
    
    def delete_user(self, username: str):
        """Delete a user after confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete user '{username}'?\nThis will also delete their training history.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            users = load_users()
            if username in users:
                del users[username]
                if save_users(users):
                    # Delete user's training file if exists
                    training_csv = get_training_csv_path(username)
                    if os.path.exists(training_csv):
                        try:
                            os.remove(training_csv)
                        except:
                            pass
                    QMessageBox.information(self, "Success", f"User '{username}' deleted successfully.")
                    self.refresh_users()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete user.")
    
    def on_back(self):
        """Return to login page."""
        self.stacked_widget.setCurrentIndex(PageIndex.LOGIN)


class Homepage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        title = QLabel("Homepage")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        training_btn = QPushButton("Training")
        performance_btn = QPushButton("Performance")
        others_btn = QPushButton("Others")
        back_btn = QPushButton("Back to Login")

        training_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        performance_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        others_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        training_btn.clicked.connect(self.on_training_clicked)
        performance_btn.clicked.connect(self.on_performance_clicked)
        others_btn.clicked.connect(self.on_others_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(training_btn)
        layout.addStretch()
        layout.addWidget(performance_btn)
        layout.addStretch()
        layout.addWidget(others_btn)
        layout.addStretch()
        layout.addWidget(back_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_training_clicked(self):
        print("Training button clicked")
        self.stacked_widget.setCurrentIndex(PageIndex.TRAINING)

    def on_performance_clicked(self):
        print("Performance button clicked")
        self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

    def on_others_clicked(self):
        print("Others button clicked")
        self.stacked_widget.setCurrentIndex(PageIndex.OTHERS)

    def on_back_clicked(self):
        """Navigate back to login page."""
        self.stacked_widget.setCurrentIndex(PageIndex.LOGIN)


class OthersPage(QWidget):
    """Simple page with History and stance toggle."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Others")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        history_btn = QPushButton("History")
        self.stance_btn = QPushButton("Orthodox")
        back_btn = QPushButton("Back")

        history_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        self.stance_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        history_btn.clicked.connect(self.on_history_clicked)
        self.stance_btn.clicked.connect(self.on_stance_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(history_btn)
        layout.addStretch()
        layout.addWidget(self.stance_btn)
        layout.addStretch()
        layout.addWidget(back_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_history_clicked(self):
        print("History clicked - implement others history navigation")

    def on_stance_clicked(self):
        # Toggle button label between Orthodox and Southpaw
        current = self.stance_btn.text().strip()
        new_stance = "Southpaw" if current == "Orthodox" else "Orthodox"
        self.stance_btn.setText(new_stance)
        # Send stance JSON message
        try:
            print(json.dumps({"stance": new_stance}))
        except Exception as e:
            print(f"Error sending stance message: {e}")

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE)

class PerformancePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Performance")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        power_btn = QPushButton("Power")
        stamina_btn = QPushButton("Stamina")
        reaction_time_btn = QPushButton("Reaction Time")
        back_btn = QPushButton("Back")

        power_btn.setStyleSheet(ButtonStyle.PRIMARY_WIDE)
        stamina_btn.setStyleSheet(ButtonStyle.PRIMARY_WIDE)
        reaction_time_btn.setStyleSheet(ButtonStyle.PRIMARY_WIDE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        power_btn.clicked.connect(self.on_power_clicked)
        stamina_btn.clicked.connect(self.on_stamina_clicked)
        reaction_time_btn.clicked.connect(self.on_reaction_time_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(power_btn)
        layout.addStretch()
        layout.addWidget(stamina_btn)
        layout.addStretch()
        layout.addWidget(reaction_time_btn)
        layout.addStretch()
        layout.addWidget(back_btn)
        layout.addStretch()

        self.setLayout(layout)

    def on_power_clicked(self):
        print("Power button clicked")
        # Navigate to Power Instructions page (index 15)
        self.stacked_widget.setCurrentIndex(PageIndex.POWER_INSTRUCTIONS)

    def on_stamina_clicked(self):
        print("Stamina button clicked")
        # Navigate to Stamina Instructions page (index 18)
        self.stacked_widget.setCurrentIndex(PageIndex.STAMINA_INSTRUCTIONS)

    def on_reaction_time_clicked(self):
        print("Reaction Time button clicked")
        # Navigate to Reaction Instructions page (index 19)
        self.stacked_widget.setCurrentIndex(PageIndex.REACTION_INSTRUCTIONS)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE)


class StaminaInstructionsPage(QWidget):
    """Instructions page for the Stamina mode."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold;")

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw as many punches to the head.\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 28px; font-weight: bold;")

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)

        back_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(start_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(instructions)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

    def on_start_clicked(self):
        try:
            countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
            countdown_page.on_finished = self.launch_stamina_punch_page
            countdown_page.return_page_index = PageIndex.STAMINA_INSTRUCTIONS  # back should return to stamina instructions
            countdown_page.start_countdown()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.COUNTDOWN)

    def launch_stamina_punch_page(self):
        try:
            punch_page = self.stacked_widget.widget(PageIndex.POWER_PUNCH)
            punch_page.reset_counter()
            self.stacked_widget.setCurrentIndex(PageIndex.POWER_PUNCH)
        except Exception:
            self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)


class ReactionInstructionsPage(QWidget):
    """Instructions page for the Reaction Time mode."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.skip_countdown = False  # Flag to skip countdown on restart

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Instructions")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold;")

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Wait until the screen turns green.\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 28px; font-weight: bold;")

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)

        back_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(start_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(instructions)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_back_clicked(self):
        self.skip_countdown = False
        self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

    def on_start_clicked(self):
        if self.skip_countdown:
            # Skip countdown and go directly to reaction test
            self.skip_countdown = False
            self.launch_reaction_test_page()
        else:
            # Show countdown normally
            try:
                countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
                countdown_page.on_finished = self.launch_reaction_test_page
                countdown_page.return_page_index = PageIndex.REACTION_INSTRUCTIONS  # back should return to reaction instructions
                countdown_page.start_countdown()
            except Exception:
                pass
            self.stacked_widget.setCurrentIndex(PageIndex.COUNTDOWN)

    def launch_reaction_test_page(self):
        try:
            reaction_test_page = self.stacked_widget.widget(PageIndex.REACTION_TEST)
            reaction_test_page.start_test()
            self.stacked_widget.setCurrentIndex(PageIndex.REACTION_TEST)
        except Exception:
            self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

class PowerInstructionsPage(QWidget):
    """Instructions page for the Power mode."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        instructions_1 = QLabel(
            "Instructions"
        )
        instructions_1.setAlignment(Qt.AlignCenter)
        instructions_1.setStyleSheet("font-size: 40px; font-weight: bold;")

        instructions = QLabel(
            "1. Wait for timer to countdown\n"
            "2. Throw 10 power hooks to the body\n"
            "3. See results at the end"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet("font-size: 28px; font-weight: bold;")

        # Buttons at the bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        start_btn = QPushButton("Start")

        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)

        back_btn.setFixedWidth(250)
        start_btn.setFixedWidth(250)

        back_btn.clicked.connect(self.on_back_clicked)
        start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(start_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(instructions_1)
        layout.addStretch()
        layout.addWidget(instructions)
        layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_back_clicked(self):
        # Return to Performance page
        self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

    def on_start_clicked(self):
        # Start the existing countdown flow then show CountdownPage (index 9)
        try:
            countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
            # When countdown finishes, go to Power Punch page
            countdown_page.on_finished = self.launch_power_punch_page
            countdown_page.return_page_index = PageIndex.POWER_INSTRUCTIONS  # back should return to instructions
            countdown_page.start_countdown()
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.COUNTDOWN)

    def launch_power_punch_page(self):
        """Switch to the punch counting page after countdown."""
        try:
            punch_page = self.stacked_widget.widget(PageIndex.POWER_PUNCH)
            punch_page.reset_counter()
            self.stacked_widget.setCurrentIndex(PageIndex.POWER_PUNCH)
        except Exception:
            # If page not available, fall back to Performance page
            self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

class PowerPunchPage(QWidget):
    """Page to count power punches after countdown."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.target = 10
        self.count = 0
        self._worker_thread: Optional[QThread] = None
        self._measuring = False

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50,50,50,50)

        self.counter_label = QLabel(self.counter_text())
        self.counter_label.setAlignment(Qt.AlignCenter)
        self.counter_label.setStyleSheet("font-size: 32px; font-weight: bold;")

        self.instruction_label = QLabel("Throw 10 Powerful Body Hooks")
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Quit button at bottom
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        quit_btn = QPushButton("Quit")
        quit_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        quit_btn.setFixedWidth(250)
        quit_btn.clicked.connect(self.on_quit_clicked)

        button_layout.addWidget(quit_btn)
        button_layout.addStretch()

        main_layout.addStretch()
        main_layout.addWidget(self.counter_label)
        main_layout.addStretch()
        main_layout.addWidget(self.instruction_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def counter_text(self):
        return f"Punch Count: {self.count}/{self.target}"

    def reset_counter(self):
        # Reset UI and begin measurement run
        self.count = 0
        self.counter_label.setText(self.counter_text())
        if not self._measuring:
            self.start_measurement()

    def mousePressEvent(self, event):
        """Increment punch count on screen press until target reached."""
        # Manual taps no longer drive the flow; measurement is from sensor
        # Keep tap to give user feedback count if desired
        if self.count < self.target:
            self.count += 1
            self.counter_label.setText(self.counter_text())
        super().mousePressEvent(event)
    
    def on_completed(self, punches_data: List[tuple]):
        """Called when measurement completes; shows the result page."""
        try:
            # Calculate peak g-force from punches
            peak_g_force = max([g for _, g in punches_data], default=0.0) if punches_data else 0.0
            result_page = self.stacked_widget.widget(PageIndex.POWER_RESULT)
            if hasattr(result_page, "set_power_output"):
                result_page.set_power_output(f"Peak: {peak_g_force:.2f} g")
            self.stacked_widget.setCurrentIndex(PageIndex.POWER_RESULT)
        except Exception:
            self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

    def on_quit_clicked(self):
        # Abort and return to Performance page
        self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

    def start_measurement(self):
        """Start background measurement using serial to detect 10 punches."""
        class _Worker(QObject):
            finished = Signal(list)  # Emit list of (punch_number, g_force) tuples
            punch_detected = Signal(int, float)  # Emit (punch_count, g_force) in real-time

            def __init__(self, parent=None):
                super().__init__(parent)

            def run(self):
                try:
                    # Use the callback version for real-time updates
                    punches = power_runner.measure_punches_with_callback(
                        port="COM10",  # Changed from COM10 to match your other script
                        baud=115200,
                        punch_threshold_ms2=100.0,
                        max_punches=10,
                        debounce_ms=300,
                        max_duration_s=120.0,
                        callback=self._on_punch_callback  # Real-time callback
                    )
                except Exception as ex:
                    print(f"Error during measurement: {ex}")
                    punches = []
                self.finished.emit(punches)
            
            def _on_punch_callback(self, punch_num: int, g_force: float):
                """Called immediately when a punch is detected by the serial reader."""
                self.punch_detected.emit(punch_num, g_force)

        # Set UI state
        self._measuring = True
        self.instruction_label.setText("Measuring... Throw 10 Powerful Body Hooks")

        # Spin worker thread
        self._worker_thread = QThread(self)
        self._worker = _Worker()
        self._worker.moveToThread(self._worker_thread)
        self._worker_thread.started.connect(self._worker.run)
        self._worker.punch_detected.connect(self._on_punch_detected)
        self._worker.finished.connect(self._on_worker_finished)
        self._worker.finished.connect(self._worker_thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._worker_thread.finished.connect(self._worker_thread.deleteLater)
        self._worker_thread.start()

    def _on_punch_detected(self, punch_count: int, g_force: float):
        """Update UI when a punch is detected - called in real-time via signal."""
        self.count = punch_count
        self.counter_label.setText(self.counter_text())
        # Optional: Show visual feedback
        self.instruction_label.setText(f"💥 {g_force:.1f}g! Keep going...")
        # Reset instruction text after a moment
        QTimer.singleShot(500, lambda: self.instruction_label.setText("Throw 10 Powerful Body Hooks"))

    def _on_worker_finished(self, punches_data: list):
        self._measuring = False
        self.on_completed(punches_data)

class PowerResultPage(QWidget):
    """Result page shown after completing the Power punches."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        # Center message
        self.result_label = QLabel("Punches Thrown in a Minute: 100")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        history_btn = QPushButton("History")
        restart_btn = QPushButton("Restart")
        quit_btn = QPushButton("Quit")

        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        restart_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        quit_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        history_btn.setFixedWidth(250)
        restart_btn.setFixedWidth(250)
        quit_btn.setFixedWidth(250)

        history_btn.clicked.connect(self.on_history_clicked)
        restart_btn.clicked.connect(self.on_restart_clicked)
        quit_btn.clicked.connect(self.on_quit_clicked)

        button_layout.addWidget(history_btn)
        button_layout.addWidget(restart_btn)
        button_layout.addWidget(quit_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_power_output(self, value_str: str):
        self.result_label.setText(f"G-Force Output: {value_str}")

    def on_history_clicked(self):
        # Placeholder: no history page yet
        print("History clicked - implement history page navigation here")

    def on_restart_clicked(self):
        # Return to the Power Instructions to restart the flow
        self.stacked_widget.setCurrentIndex(PageIndex.POWER_INSTRUCTIONS)

    def on_quit_clicked(self):
        # Return to Performance menu
        self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

class ReactionTestPage(QWidget):
    """Red/green screen to measure reaction time using camera after countdown."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.state = "red"
        self._init_thread: Optional[QThread] = None
        self._measurement_thread: Optional[QThread] = None
        self._init_in_progress = False
        self._measuring = False

        # Allow style sheets to paint the entire widget background
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setAutoFillBackground(True)

        self.green_timer = QTimer()
        self.green_timer.setSingleShot(True)
        self.green_timer.timeout.connect(self.go_green)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)

        self.status_label = QLabel("Do Not Punch")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 48px; font-weight: bold; color: white; background: transparent;")

        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addStretch()

        self.setLayout(layout)
        self.set_red_state()

    def set_red_state(self):
        self.state = "red"
        self.setStyleSheet("background-color: #b71c1c;")
        self.status_label.setText("Do Not Punch")

    def schedule_green(self):
        delay_ms = random.randint(5, 8) * 1000
        self.green_timer.stop()
        self.green_timer.start(delay_ms)

    def start_test(self):
        """Start test: show setup screen and initialize camera/model."""
        self.set_red_state()
        self.status_label.setText("Setting up camera...")
        self._init_in_progress = True
        
        # Start initialization in background thread
        self._start_initialization()

    def _start_initialization(self):
        """Initialize camera and model in a worker thread."""
        class _InitWorker(QObject):
            finished = Signal(bool, str)  # success, error_message

            def __init__(self, parent=None):
                super().__init__(parent)

            def run(self):
                try:
                    success, error_msg = rt_runner.initialize_camera_and_model()
                    self.finished.emit(success, error_msg or "")
                except Exception as ex:
                    self.finished.emit(False, f"Initialization error: {str(ex)}")

        # Spin worker thread
        self._init_thread = QThread(self)
        self._init_worker = _InitWorker()
        self._init_worker.moveToThread(self._init_thread)
        self._init_thread.started.connect(self._init_worker.run)
        self._init_worker.finished.connect(self._on_init_finished)
        self._init_worker.finished.connect(self._init_thread.quit)
        self._init_worker.finished.connect(self._init_worker.deleteLater)
        self._init_thread.finished.connect(self._init_thread.deleteLater)
        self._init_thread.start()

    def _on_init_finished(self, success: bool, error_message: str):
        """Called when initialization completes."""
        self._init_in_progress = False
        
        if success:
            # Schedule green light
            self.schedule_green()
        else:
            # Show error
            self.status_label.setText(f"Error: {error_message}")
            QTimer.singleShot(2000, lambda: self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE))

    def flash_text(self):
        self.status_label.setText("")
        QTimer.singleShot(150, lambda: self.status_label.setText("Do Not Punch"))

    def go_green(self):
        """Signal to punch and start reaction measurement."""
        self.state = "green"
        self.setStyleSheet("background-color: #2e7d32;")
        self.status_label.setText("Punch Now!")
        
        # Start background measurement when green appears
        if not self._measuring:
            self.start_measurement()

    def mousePressEvent(self, event):
        if self.state == "red" and not self._init_in_progress:
            self.flash_text()
            self.schedule_green()
        super().mousePressEvent(event)

    def start_measurement(self):
        """Start background measurement using camera to detect punch."""
        class _MeasurementWorker(QObject):
            finished = Signal(object)  # ReactionResult

            def __init__(self, parent=None):
                super().__init__(parent)

            def run(self):
                try:
                    result = rt_runner.measure_reaction_time()
                    self.finished.emit(result)
                except Exception as ex:
                    from reaction_time.reaction_time_runner import ReactionResult
                    result = ReactionResult(success=False, status="error", 
                                          error_message=f"Measurement error: {str(ex)}")
                    self.finished.emit(result)

        # Set UI state
        self._measuring = True
        self.status_label.setText("Measuring... Punch Now!")

        # Spin worker thread
        self._measurement_thread = QThread(self)
        self._measurement_worker = _MeasurementWorker()
        self._measurement_worker.moveToThread(self._measurement_thread)
        self._measurement_thread.started.connect(self._measurement_worker.run)
        self._measurement_worker.finished.connect(self._on_measurement_finished)
        self._measurement_worker.finished.connect(self._measurement_thread.quit)
        self._measurement_worker.finished.connect(self._measurement_worker.deleteLater)
        self._measurement_thread.finished.connect(self._measurement_thread.deleteLater)
        self._measurement_thread.start()

    def _on_measurement_finished(self, result):
        """Called when camera measurement completes."""
        self._measuring = False
        self.green_timer.stop()
        
        try:
            result_page = self.stacked_widget.widget(PageIndex.REACTION_RESULT)
            if result.success and result.reaction_ms is not None:
                # Convert milliseconds to seconds for display
                reaction_seconds = result.reaction_ms / 1000.0
                if hasattr(result_page, "set_reaction_time"):
                    result_page.set_reaction_time(reaction_seconds)
            else:
                # Show error/status
                status_text = result.status or "unknown"
                if result.status == "too_soon":
                    status_text = "Too Soon!"
                elif result.status == "timeout":
                    status_text = "No Punch Detected"
                if hasattr(result_page, "set_error_message"):
                    result_page.set_error_message(status_text)
            
            self.stacked_widget.setCurrentIndex(PageIndex.REACTION_RESULT)
        except Exception:
            self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

class ReactionResultPage(QWidget):
    """Shows measured reaction time after the test."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        self.result_label = QLabel("Reaction Time: -- s")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        history_btn = QPushButton("History")
        restart_btn = QPushButton("Restart")
        back_btn = QPushButton("Back")

        history_btn.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        restart_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        history_btn.setFixedWidth(250)
        restart_btn.setFixedWidth(250)
        back_btn.setFixedWidth(250)

        history_btn.clicked.connect(self.on_history_clicked)
        restart_btn.clicked.connect(self.on_restart_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        button_layout.addWidget(history_btn)
        button_layout.addWidget(restart_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(self.result_label)
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()

        self.setLayout(layout)

    def set_reaction_time(self, seconds: float):
        self.result_label.setText(f"Reaction Time: {seconds:.3f} s")

    def set_error_message(self, message: str):
        """Display error or status message instead of reaction time."""
        self.result_label.setText(message)

    def on_history_clicked(self):
        # Placeholder: add history navigation when available
        print("History clicked - implement reaction history navigation")

    def on_restart_clicked(self):
        # Set flag to skip countdown and go directly to test
        try:
            reaction_instructions_page = self.stacked_widget.widget(PageIndex.REACTION_INSTRUCTIONS)
            reaction_instructions_page.skip_countdown = True
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.REACTION_INSTRUCTIONS)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.PERFORMANCE)

class TrainingPage(QWidget):
    """
    TrainingPage class for displaying training options in a GUI application.
    This class extends QWidget and provides a user interface for selecting different
    training activities. It displays a centered layout with buttons for accessing
    techniques and sparring features, along with a back button for navigation.
    Attributes:
        stacked_widget (QStackedWidget): Reference to the parent stacked widget for
            managing page navigation between different sections of the application.
        main_window: Reference to the MainWindow to get current user and check level.
    Methods:
        __init__(stacked_widget, main_window): Initializes the TrainingPage with UI components
            including title, buttons, and layout configuration.
        on_techniques_clicked(): Handles the techniques button click event and
            navigates to the Techniques page (index 2).
        on_spar_clicked(): Handles the spar button click event and navigates to
            the SparPage (index 12) if user is Intermediate or Advanced.
        on_back_clicked(): Handles the back button click event and returns to
            the main page (index 0).
    """
    def __init__(self, stacked_widget, main_window=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_window = main_window

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Training")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        techniques_btn = QPushButton("Techniques")
        self.spar_btn = QPushButton("Spar")
        back_btn = QPushButton("Back")

        techniques_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        self.spar_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        techniques_btn.clicked.connect(self.on_techniques_clicked)
        self.spar_btn.clicked.connect(self.on_spar_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(techniques_btn)
        layout.addWidget(self.spar_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_techniques_clicked(self):
        print("Techniques button clicked")
        self.stacked_widget.setCurrentIndex(PageIndex.TECHNIQUES)

    def on_spar_clicked(self):
        print("Spar button clicked")
        # SparPage is now at index 12 after removing DefenseTechniquePage
        self.stacked_widget.setCurrentIndex(PageIndex.SPAR)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.HOMEPAGE)

class TechniquesPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Training Options")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 30px;")

        punch_lib_btn = QPushButton("Punch Combination Library")
        technique_correction_btn = QPushButton("Technique Correction")
        back_btn = QPushButton("Back")

        punch_lib_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        technique_correction_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        punch_lib_btn.clicked.connect(self.on_punch_combination_library_clicked)
        technique_correction_btn.clicked.connect(self.on_technique_correction_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(punch_lib_btn)
        layout.addWidget(technique_correction_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_punch_combination_library_clicked(self):
        print("Punch Combination Library button clicked")
        self.stacked_widget.setCurrentIndex(PageIndex.PUNCH_COMBINATIONS)

    def on_technique_correction_clicked(self):
        print("Technique Correction button clicked")
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TRAINING)

class PunchCombinationPage(QWidget):
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Punch Combinations")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        self.beginner_btn = QPushButton("Beginner")
        self.intermediate_btn = QPushButton("Intermediate")
        self.advanced_btn = QPushButton("Advanced")
        self.self_select_btn = QPushButton("Self-Select")
        back_btn = QPushButton("Back")

        self.beginner_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.intermediate_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.advanced_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.self_select_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        self.beginner_btn.clicked.connect(lambda: self.on_difficulty_clicked("Beginner"))
        self.intermediate_btn.clicked.connect(lambda: self.on_difficulty_clicked("Intermediate"))
        self.advanced_btn.clicked.connect(lambda: self.on_difficulty_clicked("Advanced"))
        self.self_select_btn.clicked.connect(lambda: self.on_difficulty_clicked("Self-Select"))
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(self.beginner_btn)
        layout.addWidget(self.intermediate_btn)
        layout.addWidget(self.advanced_btn)
        layout.addWidget(self.self_select_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        username = None
        main_window = self.parent()
        if hasattr(main_window, 'get_current_user'):
            username = main_window.get_current_user()
        elif self.app_state and hasattr(self.app_state, 'current_user'):
            username = self.app_state.current_user
        level = get_user_level(username) if username else 'Beginner'
        # Only enable the button matching user level
        self.beginner_btn.setEnabled(level == 'Beginner')
        self.intermediate_btn.setEnabled(level == 'Intermediate')
        self.advanced_btn.setEnabled(level == 'Advanced')
        self.self_select_btn.setEnabled(level == 'Beginner')

    def on_difficulty_clicked(self, difficulty):
        print(f"{difficulty} button clicked")
        # Store difficulty via app_state
        if self.app_state:
            self.app_state.update_difficulty(difficulty)
            self.app_state.previous_page = PageIndex.PUNCH_COMBINATIONS
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.selected_difficulty = difficulty
                basic_page.previous_page = PageIndex.PUNCH_COMBINATIONS
            except Exception:
                pass
        
        if difficulty == "Self-Select":
            self_select_page = self.stacked_widget.widget(PageIndex.SELF_SELECT_SEQUENCE)
            self_select_page.previous_page = PageIndex.PUNCH_COMBINATIONS
            self.stacked_widget.setCurrentIndex(PageIndex.SELF_SELECT_SEQUENCE)
        else:
            self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TECHNIQUES)

class TechCorrParametersPage(QWidget):
    """Setup page for Technique Correction mode, mirroring BasicParametersPage pattern."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        # Stored selections (require explicit user selection for all six)
        self.selected_difficulty = None
        self.selected_rounds = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Technique Correction Setup")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        # Parameter buttons (label + placeholder until selected)
        self.difficulty_btn = QPushButton("Difficulty\n--")
        self.rounds_btn = QPushButton("Rounds\n--")
        self.speed_btn = QPushButton("Speed\n--")
        self.time_btn = QPushButton("Time\n--")
        self.rest_btn = QPushButton("Rest\n--")

        for btn in [self.difficulty_btn, self.rounds_btn, self.speed_btn, self.time_btn, self.rest_btn]:
            btn.setStyleSheet(ButtonStyle.INFO_SMALL)

        self.difficulty_btn.clicked.connect(self.on_difficulty_clicked)
        self.rounds_btn.clicked.connect(self.on_rounds_clicked)
        self.speed_btn.clicked.connect(self.on_speed_clicked)
        self.time_btn.clicked.connect(self.on_time_clicked)
        self.rest_btn.clicked.connect(self.on_rest_clicked)

        layout.addWidget(title)
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(self.difficulty_btn, 0, 0)
        grid.addWidget(self.rounds_btn,     0, 1)
        grid.addWidget(self.speed_btn,      1, 0)
        grid.addWidget(self.time_btn,       1, 1)
        # Center the rest button in row 2
        rest_layout = QHBoxLayout()
        rest_layout.addStretch()
        rest_layout.addWidget(self.rest_btn)
        rest_layout.addStretch()
        layout.addLayout(grid)
        layout.addLayout(rest_layout)

        # Bottom buttons (Back + Start) like BasicParametersPage
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        back_btn = QPushButton("Back")
        self.start_btn = QPushButton("Start")

        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self.start_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)

        back_btn.clicked.connect(self.on_back_clicked)
        self.start_btn.clicked.connect(self.on_start_clicked)

        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.start_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initial enable state similar to BasicParametersPage
        self.update_start_button()

    def on_difficulty_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_DIFFICULTY)

    def on_rounds_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_ROUNDS)

    def on_speed_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_SPEED)

    def on_time_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_TIME)

    def on_rest_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_REST)

    def update_start_button(self):
        # Enable only when all five have a concrete value (not '--')
        def value_of(btn: QPushButton) -> str:
            txt = btn.text()
            return txt.split("\n")[-1].strip() if "\n" in txt else txt.strip()
        values = [
            value_of(self.difficulty_btn),
            value_of(self.rounds_btn),
            value_of(self.speed_btn),
            value_of(self.time_btn),
            value_of(self.rest_btn),
        ]
        all_selected = all(v not in ("--", "") for v in values)
        self.start_btn.setEnabled(all_selected)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TECHNIQUES)

    def on_start_clicked(self):
        # Parse time value to seconds
        time_text = self.time_btn.text().split("\n")[-1]
        def parse_time_to_seconds(t: str) -> int:
            t = t.strip()
            mins = 0
            secs = 0
            if "min" in t and "sec" in t:
                try:
                    parts = t.replace("sec", "").split("min")
                    mins = int(parts[0]) if parts[0] else 0
                    secs = int(parts[1]) if parts[1] else 0
                except Exception:
                    mins, secs = 0, 0
            elif "min" in t:
                try:
                    mins = int(t.replace("min", ""))
                except Exception:
                    mins = 0
            elif "sec" in t:
                try:
                    secs = int(t.replace("sec", ""))
                except Exception:
                    secs = 0
            return mins * 60 + secs

        round_seconds = parse_time_to_seconds(time_text)
        
        # Parse rest time
        rest_text = self.rest_btn.text().split("\n")[-1]
        rest_seconds = parse_time_to_seconds(rest_text)
        
        # Get speed
        speed_text = self.speed_btn.text().split("\n")[-1]

        if self.app_state is not None:
            cfg = TechCorrConfig(
                difficulty=self.selected_difficulty,
                rounds=self.selected_rounds,
                round_seconds=round_seconds,
                rest_seconds=rest_seconds,
                speed=speed_text,
            )
            self.app_state.set_tech_corr_config(cfg)

        # Navigate to session and let it load from AppState
        session_page = self.stacked_widget.widget(PageIndex.TECH_CORR_SESSION)
        if hasattr(session_page, "load_from_state") and (self.app_state is not None):
            session_page.load_from_state(self.app_state)
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_SESSION)

    # Methods to update from selection pages
    def set_difficulty(self, val: str):
        self.selected_difficulty = val
        self.difficulty_btn.setText(f"Difficulty\n{val}")
        self.update_start_button()

    def set_rounds(self, n: int):
        self.selected_rounds = n
        self.rounds_btn.setText(f"Rounds\n{n}")
        self.update_start_button()

    def set_speed(self, val: str):
        self.speed_btn.setText(f"Speed\n{val}")
        self.update_start_button()

    def set_time(self, val: str):
        self.time_btn.setText(f"Time\n{val}")
        self.update_start_button()

    def set_rest(self, val: str):
        self.rest_btn.setText(f"Rest\n{val}")
        self.update_start_button()

class TechCorrSessionPage(QWidget):
    """Session page for Technique Correction mode, mirroring TrainingSessionPage layout."""

    INTERVAL_SECONDS = 25
    ANALYTICS_SECONDS = 5

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.is_paused = False
        
        # Timing and session state
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.current_round = 1
        self.total_rounds = 1
        self.round_seconds = 30
        self.interval_plan = [self.INTERVAL_SECONDS]
        self.current_interval_index = 0
        self.time_remaining = self.INTERVAL_SECONDS
        self.showing_analytics = False
        self.analytics_time_remaining = 0

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Round counter at the top
        self.round_label = QLabel("Round 1 / 3")
        self.round_label.setAlignment(Qt.AlignCenter)
        self.round_label.setStyleSheet("font-size: 40px; font-weight: bold;")

        # Interval counter
        self.interval_label = QLabel("Interval 1 / 5")
        self.interval_label.setAlignment(Qt.AlignCenter)
        self.interval_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #666;")

        # Countdown timer for interval
        self.timer_label = QLabel("00:30")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        # Target combo (large, centered)
        self.target_combo_label = QLabel("Jab - Cross - Hook")
        self.target_combo_label.setAlignment(Qt.AlignCenter)
        self.target_combo_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #2196F3; margin-top: 20px;")

        # Feedback label (large)
        self.feedback_label = QLabel("Good")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("font-size: 56px; font-weight: bold; color: #4CAF50; margin-top: 15px;")

        # Post-interval analytics panel (hidden by default)
        self.analytics_panel = QWidget()
        analytics_layout = QVBoxLayout()
        analytics_layout.setAlignment(Qt.AlignCenter)
        analytics_layout.setSpacing(10)
        analytics_layout.setContentsMargins(20, 20, 20, 20)

        self.analytics_title = QLabel("Interval Summary")
        self.analytics_title.setAlignment(Qt.AlignCenter)
        self.analytics_title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")

        self.guard_discipline_label = QLabel("Guard discipline: —")
        self.guard_discipline_label.setAlignment(Qt.AlignCenter)
        self.guard_discipline_label.setStyleSheet("font-size: 18px; color: #333;")

        self.distance_selection_label = QLabel("Distance selection: —")
        self.distance_selection_label.setAlignment(Qt.AlignCenter)
        self.distance_selection_label.setStyleSheet("font-size: 18px; color: #333;")

        self.combo_accuracy_label = QLabel("Combo accuracy: —")
        self.combo_accuracy_label.setAlignment(Qt.AlignCenter)
        self.combo_accuracy_label.setStyleSheet("font-size: 18px; color: #333;")

        analytics_layout.addWidget(self.analytics_title)
        analytics_layout.addWidget(self.guard_discipline_label)
        analytics_layout.addWidget(self.distance_selection_label)
        analytics_layout.addWidget(self.combo_accuracy_label)
        self.analytics_panel.setLayout(analytics_layout)
        self.analytics_panel.hide()

        # Buttons (Pause/Resume and Stop)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        self.pause_btn = QPushButton("Pause")
        stop_btn = QPushButton("Stop")

        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        stop_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        self.pause_btn.setFixedWidth(250)
        stop_btn.setFixedWidth(250)

        self.pause_btn.clicked.connect(self.toggle_pause)
        stop_btn.clicked.connect(self.on_stop_clicked)

        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(stop_btn)
        button_layout.addStretch()

        # Assemble main layout
        main_layout.addStretch()
        main_layout.addWidget(self.round_label)
        main_layout.addWidget(self.interval_label)
        main_layout.addStretch()
        main_layout.addWidget(self.timer_label)
        main_layout.addWidget(self.target_combo_label)
        main_layout.addWidget(self.feedback_label)
        main_layout.addStretch()
        main_layout.addWidget(self.analytics_panel)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def format_time(self, seconds):
        """Format seconds as MM:SS."""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def toggle_pause(self):
        """Toggle between pause and resume."""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_btn.setText("Resume")
            self.timer.stop()
        else:
            self.pause_btn.setText("Pause")
            self.timer.start(1000)

    def on_stop_clicked(self):
        """Stop session and return to parameters page."""
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)

    def load_from_state(self, app_state: AppState):
        """Load and start Technique Correction session from config."""
        cfg = getattr(app_state, "tech_corr_config", None)
        if cfg:
            self.total_rounds = cfg.rounds
            self.round_seconds = cfg.round_seconds

            # Build interval plan (25s slices, last interval may be shorter)
            self.interval_plan = self.build_interval_plan(self.round_seconds)
            self.current_round = 1
            self.current_interval_index = 0
            self.time_remaining = self.interval_plan[0]
            self.showing_analytics = False
            self.analytics_time_remaining = 0
            self.is_paused = False

            self.round_label.setText(f"Round {self.current_round} / {self.total_rounds}")
            self.interval_label.setText(f"Interval {self.current_interval_index + 1} / {len(self.interval_plan)}")
            self.timer_label.setText(self.format_time(self.time_remaining))
            self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")
            self.target_combo_label.show()
            self.feedback_label.setText("Good")
            self.feedback_label.show()
            self.analytics_panel.hide()
            self.pause_btn.setText("Pause")

            print(f"[TechCorr] Start Round {self.current_round}/{self.total_rounds}, Intervals: {len(self.interval_plan)}")
            print(f"[TechCorr] Start Interval 1/{len(self.interval_plan)} (Round {self.current_round})")

            self.timer.start(1000)

    def update_timer(self):
        """Update the countdown timer and handle state transitions."""
        if self.showing_analytics:
            if self.analytics_time_remaining > 0:
                # Show countdown during analytics phase
                self.timer_label.setText(self.format_time(self.analytics_time_remaining))
                self.analytics_time_remaining -= 1
                return

            # Analytics finished; decide next step
            self.analytics_panel.hide()
            self.showing_analytics = False
            self.timer_label.show()
            self.target_combo_label.show()
            self.feedback_label.show()

            last_interval_of_round = (self.current_interval_index == len(self.interval_plan) - 1)
            if last_interval_of_round:
                if self.current_round < self.total_rounds:
                    # Next round
                    self.current_round += 1
                    self.interval_plan = self.build_interval_plan(self.round_seconds)
                    self.current_interval_index = 0
                    self.time_remaining = self.interval_plan[0]
                    self.round_label.setText(f"Round {self.current_round} / {self.total_rounds}")
                    self.interval_label.setText(f"Interval {self.current_interval_index + 1} / {len(self.interval_plan)}")
                    self.timer_label.setText(self.format_time(self.time_remaining))
                    self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")
                    print(f"[TechCorr] Start Round {self.current_round}/{self.total_rounds}, Intervals: {len(self.interval_plan)}")
                else:
                    # Session complete
                    print("[TechCorr] Session complete")
                    self.timer.stop()
                    self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)
                return

            # Move to next interval in same round
            self.current_interval_index += 1
            self.time_remaining = self.interval_plan[self.current_interval_index]
            self.interval_label.setText(f"Interval {self.current_interval_index + 1} / {len(self.interval_plan)}")
            self.timer_label.setText(self.format_time(self.time_remaining))
            self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")
            print(f"[TechCorr] Start Interval {self.current_interval_index + 1}/{len(self.interval_plan)} (Round {self.current_round})")
            return

        # Interval countdown
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.setText(self.format_time(self.time_remaining))
            return

        # Interval complete -> show analytics
        self.showing_analytics = True
        self.analytics_time_remaining = self.ANALYTICS_SECONDS
        self.target_combo_label.hide()
        self.feedback_label.hide()
        self.timer_label.show()
        last_interval = (self.current_interval_index == len(self.interval_plan) - 1)
        summary_text = "End of Round Summary" if last_interval else f"Interval {self.current_interval_index + 1} Summary"
        self.analytics_title.setText(summary_text)
        self.interval_label.setText(summary_text)
        self.timer_label.setText(self.format_time(self.analytics_time_remaining))
        self.analytics_panel.show()
        print(f"[TechCorr] Interval {self.current_interval_index + 1} complete -> Analytics")

    def build_interval_plan(self, round_seconds: int):
        """Compute interval durations for a round based on 25s slices and remainder."""
        if round_seconds <= 0:
            return [self.INTERVAL_SECONDS]
        count = (round_seconds + self.INTERVAL_SECONDS - 1) // self.INTERVAL_SECONDS
        base = [self.INTERVAL_SECONDS] * count
        remainder = round_seconds - self.INTERVAL_SECONDS * (count - 1)
        base[-1] = remainder if remainder > 0 else self.INTERVAL_SECONDS
        return base

class TechCorrDifficultySelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Difficulty")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        btns = []
        for label in ["Beginner", "Intermediate", "Advanced"]:
            b = QPushButton(label)
            b.setStyleSheet(ButtonStyle.INFO_SMALL)
            b.clicked.connect(partial(self.select_difficulty, label))
            btns.append(b)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS))

        layout.addWidget(title)
        for b in btns:
            layout.addWidget(b)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def select_difficulty(self, val: str):
        try:
            params = self.stacked_widget.widget(PageIndex.TECH_CORR_PARAMETERS)
            if hasattr(params, "set_difficulty"):
                params.set_difficulty(val)
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)

class TechCorrRoundsSelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Rounds")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)
        for idx in range(12):
            n = idx + 1
            btn = QPushButton(str(n))
            btn.setStyleSheet(ButtonStyle.ROUND_SELECTION)
            btn.clicked.connect(partial(self.select_rounds, n))
            row = idx // 6
            col = idx % 6
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_rounds(self, n: int):
        try:
            params = self.stacked_widget.widget(PageIndex.TECH_CORR_PARAMETERS)
            if hasattr(params, "set_rounds"):
                params.set_rounds(n)
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)

class TechCorrSpeedSelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Speed")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        speeds = ["25%", "50%", "75%", "100%"]
        for col, val in enumerate(speeds):
            btn = QPushButton(str(val))
            btn.setStyleSheet(ButtonStyle.SPEED_SELECTION)
            btn.clicked.connect(partial(self.select_speed, val))
            grid.addWidget(btn, 0, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_speed(self, val: str):
        try:
            params = self.stacked_widget.widget(PageIndex.TECH_CORR_PARAMETERS)
            if hasattr(params, "set_speed"):
                params.set_speed(val)
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)

class TechCorrTimeSelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)
        for c in range(3):
            grid.setColumnStretch(c, 1)

        times = ["30sec", "1min", "1min30sec", "2min", "2min30sec", "3min"]
        for idx, val in enumerate(times):
            btn = QPushButton(val)
            btn.setStyleSheet(ButtonStyle.TIME_SELECTION)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            btn.clicked.connect(partial(self.select_time, val))
            row = idx // 3
            col = idx % 3
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_time(self, val: str):
        try:
            params = self.stacked_widget.widget(PageIndex.TECH_CORR_PARAMETERS)
            if hasattr(params, "set_time"):
                params.set_time(val)
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)

class TechCorrRestSelectionPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Rest Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)
        for c in range(3):
            grid.setColumnStretch(c, 1)

        rest_times = ["10sec", "20sec", "30sec", "40sec", "50sec", "1min"]
        for idx, val in enumerate(rest_times):
            btn = QPushButton(val)
            btn.setStyleSheet(ButtonStyle.TIME_SELECTION)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            btn.clicked.connect(partial(self.select_rest, val))
            row = idx // 3
            col = idx % 3
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_rest(self, val: str):
        try:
            params = self.stacked_widget.widget(PageIndex.TECH_CORR_PARAMETERS)
            if hasattr(params, "set_rest"):
                params.set_rest(val)
        except Exception:
            pass
        self.stacked_widget.setCurrentIndex(PageIndex.TECH_CORR_PARAMETERS)

class BasicParametersPage(QWidget):
    """Page for basic parameters (index 4)."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.previous_page = PageIndex.PUNCH_COMBINATIONS  # Fallback for when no app_state

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Basic Parameters")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        # store as instance attribute so other pages can update it
        self.round_btn = QPushButton("Round")
        self.speed_btn = QPushButton("Speed")
        self.time_btn = QPushButton("Time")
        self.rest_btn = QPushButton("Rest")
        
        self.round_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.speed_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.time_btn.setStyleSheet(ButtonStyle.INFO_SMALL)
        self.rest_btn.setStyleSheet(ButtonStyle.INFO_SMALL)

        self.round_btn.clicked.connect(self.on_round_clicked)
        self.speed_btn.clicked.connect(self.on_speed_clicked)
        self.time_btn.clicked.connect(self.on_time_clicked)
        self.rest_btn.clicked.connect(self.on_rest_clicked)

        layout.addWidget(title)
        # center the buttons horizontally
        layout.addWidget(self.round_btn)
        layout.addWidget(self.speed_btn)
        layout.addWidget(self.time_btn)
        layout.addWidget(self.rest_btn)
        # layout.addStretch()

        # Create horizontal layout for back and continue buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()  # Add space on the left
        
        back_btn = QPushButton("Back")
        self.continue_btn = QPushButton("Continue")  # Initialize continue_btn here
        
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        # Continue button should be green like Start actions
        self.continue_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
        
        back_btn.clicked.connect(self.on_back_clicked)
        self.continue_btn.clicked.connect(self.on_continue_clicked)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.continue_btn)
        button_layout.addStretch()  # Add space on the right

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initialize button displays from state and update continue availability
        self.update_button_displays()

    def update_button_displays(self):
        """Refresh parameter buttons from app_state config and labels."""
        if self.app_state:
            config = self.app_state.get_config()
            self.round_btn.setText(f"Round\n{config.rounds}")
            self.speed_btn.setText(f"Speed\n{config.speed}")

            time_text = self.app_state.time_label or config.get_time_str()
            rest_text = self.app_state.rest_label or config.get_rest_str()
            self.time_btn.setText(f"Time\n{time_text}")
            self.rest_btn.setText(f"Rest\n{rest_text}")

        self.update_continue_button()

    def is_parameter_selected(self, btn):
        """Check if a parameter button has been selected (has more than just the label)."""
        text = btn.text()
        return "\n" in text  # Selected buttons have format "Label\nValue"

    def update_continue_button(self):
        """Enable continue button only if all parameters are selected."""
        all_selected = (
            self.is_parameter_selected(self.round_btn) and
            self.is_parameter_selected(self.speed_btn) and
            self.is_parameter_selected(self.time_btn) and
            self.is_parameter_selected(self.rest_btn)
        )
        self.continue_btn.setEnabled(all_selected)

    def on_round_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.ROUND_SELECTION)

    def on_speed_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.SPEED_SELECTION)

    def on_time_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TIME_SELECTION)

    def on_rest_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.REST_SELECTION)

    def on_back_clicked(self):
        prev_page = self.app_state.previous_page if self.app_state else self.previous_page
        self.stacked_widget.setCurrentIndex(prev_page)

    def on_continue_clicked(self):
        print("Continue button clicked")
        # Start countdown and move to CountdownPage
        countdown_page = self.stacked_widget.widget(PageIndex.COUNTDOWN)
        # Ensure training flow uses the training session start callback
        parent_window = self.stacked_widget.parent()
        if parent_window and hasattr(parent_window, "start_training_session"):
            countdown_page.on_finished = parent_window.start_training_session
        # Back from countdown should return to Basic Parameters during training flow
        countdown_page.return_page_index = PageIndex.BASIC_PARAMETERS
        countdown_page.start_countdown()
        self.stacked_widget.setCurrentIndex(PageIndex.COUNTDOWN)

class RoundSelectionPage(QWidget):
    """Page showing 12 numbered round buttons and a back button."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Round")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        # Create 12 numbered buttons (1..12)
        for idx in range(12):
            n = idx + 1
            btn = QPushButton(str(n))
            btn.setStyleSheet(ButtonStyle.ROUND_SELECTION)
            # call select_round with the selected number and return to BasicParametersPage
            btn.clicked.connect(partial(self.select_round, n))
            row = idx // 4
            col = idx % 4
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        # go back to BasicParametersPage (index 4)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_round(self, n: int):
        """Set the chosen round on BasicParametersPage and switch back."""
        if self.app_state:
            self.app_state.update_rounds(n)
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.round_btn.setText(f"Round\n{n}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

class SpeedSelectionPage(QWidget):
    """Page offering speed choices (25, 50, 75, 100)."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Speed")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        speeds = ["25%", "50%", "75%", "100%"]
        for col, val in enumerate(speeds):
            btn = QPushButton(str(val))
            btn.setStyleSheet(ButtonStyle.SPEED_SELECTION)
            btn.clicked.connect(partial(self.select_speed, val))
            grid.addWidget(btn, 0, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_speed(self, n: int):
        """Update BasicParametersPage speed button text and return."""
        if self.app_state:
            self.app_state.update_speed(n)
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.speed_btn.setText(f"Speed\n{n}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

class TimeSelectionPage(QWidget):
    """Page offering time choices (30sec, 1min, 1min30sec, 2min, 2min30sec, 3min)."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        # make columns stretch so buttons get equal width regardless of text
        for c in range(3):
            grid.setColumnStretch(c, 1)

        times = ["30sec", "1min", "1min30sec", "2min", "2min30sec", "3min"]
        # arrange in 3 columns x 2 rows
        for idx, val in enumerate(times):
            btn = QPushButton(val)
            btn.setStyleSheet(ButtonStyle.TIME_SELECTION)
            # ensure all buttons have the same width (columns stretch) and same height
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            # Use ButtonStyle.TIME_SELECTION min-height; no fixed height override
            btn.clicked.connect(partial(self.select_time, val))
            row = idx // 3
            col = idx % 3
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_time(self, n: str):
        """Update BasicParametersPage time button text and return."""
        if self.app_state:
            self.app_state.update_time(n)
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.time_btn.setText(f"Time\n{n}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

class RestSelectionPage(QWidget):
    """Page offering rest choices (10sec to 60sec in 10sec increments)."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(50,50,50,50)

        title = QLabel("Select Rest Time")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: bold; margin-bottom: 10px;")

        grid = QGridLayout()
        grid.setSpacing(8)

        # make columns stretch so buttons get equal width
        for c in range(3):
            grid.setColumnStretch(c, 1)

        rest_times = ["10sec", "20sec", "30sec", "40sec", "50sec", "1min"]
        # arrange in 3 columns x 2 rows
        for idx, val in enumerate(rest_times):
            btn = QPushButton(val)
            btn.setStyleSheet(ButtonStyle.TIME_SELECTION)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            # Use ButtonStyle.TIME_SELECTION min-height; no fixed height override
            btn.clicked.connect(partial(self.select_rest, val))
            row = idx // 3
            col = idx % 3
            grid.addWidget(btn, row, col)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS))

        main_layout.addWidget(title)
        main_layout.addLayout(grid)
        main_layout.addStretch()
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def select_rest(self, n: str):
        """Update BasicParametersPage rest button text and return."""
        if self.app_state:
            self.app_state.update_rest(n)
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.update_button_displays()
            except Exception:
                pass
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.rest_btn.setText(f"Rest\n{n}")
                basic_page.update_continue_button()
            except Exception:
                pass
        self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

class CountdownPage(QWidget):
    """Page with 20 second countdown and pause button."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.countdown_value = 20
        self.is_paused = False
        self.on_finished = None  # callback to start training session
        # Where to return if user presses Back during countdown
        self.return_page_index = PageIndex.BASIC_PARAMETERS
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Wear Your Gloves")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: bold; margin-bottom: 20px;")

        self.countdown_label = QLabel(str(self.countdown_value))
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        # Create horizontal layout for pause and back buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        self.pause_btn = QPushButton("Pause")
        back_btn = QPushButton("Back")

        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        self.pause_btn.setFixedWidth(250)
        back_btn.setFixedWidth(250)

        self.pause_btn.clicked.connect(self.toggle_pause)
        back_btn.clicked.connect(self.on_back_clicked)

        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()

        main_layout.addStretch()
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addWidget(self.countdown_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def start_countdown(self):
        """Start the countdown timer."""
        self.countdown_value = 3
        self.is_paused = False
        self.countdown_label.setText(str(self.countdown_value))
        self.pause_btn.setText("Pause")
        # Ensure Pause button starts in red style
        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self.timer.start(1000)  # Update every 1000ms (1 second)

    def update_countdown(self):
        """Update countdown display."""
        if self.countdown_value > 0:
            self.countdown_value -= 1
            self.countdown_label.setText(str(self.countdown_value))
        else:
            self.timer.stop()
            if callable(self.on_finished):
                self.on_finished()

    def toggle_pause(self):
        """Pause or resume the countdown."""
        if self.is_paused:
            self.timer.start(1000)
            self.pause_btn.setText("Pause")
            # Back to red when resuming (showing "Pause")
            self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
            self.is_paused = False
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            # Green while paused (showing "Resume")
            self.pause_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
            self.is_paused = True

    def on_back_clicked(self):
        """Stop timer and go back to BasicParametersPage."""
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(self.return_page_index)

class TrainingSessionPage(QWidget):
    """Page showing the actual training session with round counter and timer."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_round = 1
        self.total_rounds = 1
        self.work_time = 60  # in seconds
        self.rest_time = 30  # in seconds
        self.time_remaining = self.work_time
        self.is_resting = False
        self.is_paused = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        # Training mode attributes
        self.difficulty = None
        self.battle_style = None

        # Combo curriculum state
        self.current_combo = None  # Stores combo dict from database
        self.combo_display_text = ""  # Text to display on screen

        # self-select state
        self.is_self_select_mode = False
        self.sequences = []
        self.sequence_index = 0
        self.sequence_cycle_seconds = 6  # each sequence shows for 6 seconds
        self.sequence_time_remaining = 0

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # Round counter at the top
        self.round_label = QLabel(f"Round {self.current_round}/{self.total_rounds}")
        self.round_label.setAlignment(Qt.AlignCenter)
        self.round_label.setStyleSheet("font-size: 40px; font-weight: bold; margin-bottom: 20px;")

        # Rest indicator (hidden during work periods)
        self.rest_label = QLabel("Rest")
        self.rest_label.setAlignment(Qt.AlignCenter)
        self.rest_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #FF9800; margin-bottom: 10px;")
        self.rest_label.hide()

        # Sequence display (visible for combo/self-select modes during work)
        self.sequence_label = QLabel("")
        self.sequence_label.setAlignment(Qt.AlignCenter)
        self.sequence_label.setStyleSheet("font-size: 40px; font-weight: bold; color: #2196F3; margin-bottom: 20px;")
        self.sequence_label.hide()

        # Timer in the middle
        self.timer_label = QLabel(self.format_time(self.time_remaining))
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")

        # Create horizontal layout for pause and back buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.addStretch()

        self.pause_btn = QPushButton("Pause")
        stop_btn = QPushButton("Stop")

        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        stop_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        self.pause_btn.setFixedWidth(250)
        stop_btn.setFixedWidth(250)

        self.pause_btn.clicked.connect(self.toggle_pause)
        stop_btn.clicked.connect(self.on_stop_clicked)

        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(stop_btn)
        button_layout.addStretch()

        main_layout.addStretch()
        main_layout.addWidget(self.round_label)
        main_layout.addStretch()
        main_layout.addWidget(self.rest_label)
        main_layout.addStretch()
        main_layout.addWidget(self.sequence_label)  # combo display above timer
        main_layout.addWidget(self.timer_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def format_time(self, seconds):
        """Format seconds as MM:SS."""
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def parse_time_to_seconds(self, time_str):
        """Convert time string to seconds."""
        time_map = {
            "30sec": 30,
            "1min": 60,
            "1min30sec": 90,
            "2min": 120,
            "2min30sec": 150,
            "3min": 180,
            "10sec": 10,
            "20sec": 20,
            "40sec": 40,
            "50sec": 50
        }
        return time_map.get(time_str, 60)

    def send_round_start_message(self):
        """Send JSON message at the start of each round for non-Self-Select modes."""
        if self.is_self_select_mode:
            return  # Skip for Self-Select mode
        
        try:
            if self.difficulty == "Battle":
                # For Battle mode, send both mode and battle_style
                payload = {
                    "mode": self.difficulty,
                    "battle_style": self.battle_style,
                }
            elif self.difficulty in ["Beginner", "Intermediate", "Advanced"]:
                # For Punch Combination modes
                mode_str = f"Punch-Combination {self.difficulty}"
                payload = {
                    "mode": mode_str,
                }
                # Add combo info if available
                if self.current_combo:
                    payload["combo_id"] = self.current_combo.get("id", "")
                    payload["combo_name"] = self.current_combo.get("name", "")
                    payload["combo_sequence"] = self.current_combo.get("sequence", "")
            else:
                # For other modes (Stamina, Reaction Time, Power, etc.)
                payload = {
                    "mode": self.difficulty,
                }
            print(json.dumps(payload))
        except Exception as e:
            print(f"Error sending round start message: {e}")

    def start_session(self, rounds, time_str, rest_str, difficulty=None, sequences=None, battle_style=None):
        """Start the training session with the given parameters."""
        self.current_round = 1
        self.total_rounds = rounds
        self.difficulty = difficulty
        self.battle_style = battle_style

        # Convert time strings to seconds
        self.work_time = self.parse_time_to_seconds(time_str)
        self.rest_time = self.parse_time_to_seconds(rest_str)

        # Self-select setup
        self.is_self_select_mode = (difficulty == "Self-Select") and sequences and len(sequences) > 0
        self.sequences = sequences if self.is_self_select_mode else []
        self.sequence_index = 0
        self.sequence_time_remaining = self.sequence_cycle_seconds if self.sequences else 0

        # Fetch combo from database for Beginner/Intermediate/Advanced modes
        self.current_combo = None
        self.combo_display_text = ""
        if difficulty in ["Beginner", "Intermediate", "Advanced"]:
            try:
                import sys
                import os
                # Add combo_curriculum to path if not already there
                curriculum_path = os.path.join(os.path.dirname(__file__), 'combo_curriculum')
                if curriculum_path not in sys.path:
                    sys.path.insert(0, curriculum_path)
                
                from combo_curriculum import ComboCurriculum
                
                db_path = os.path.join(os.path.dirname(__file__), 'setup', 'combos.db')
                
                with ComboCurriculum(db_path) as curriculum:
                    self.current_combo = curriculum.get_next_combo(difficulty)
                    if self.current_combo:
                        self.combo_display_text = self.current_combo.get('sequence', '')
                        print(f"Training combo: {self.current_combo.get('name', 'Unknown')} - {self.combo_display_text}")
            except Exception as e:
                print(f"Error fetching combo from database: {e}")
                # Fallback to showing difficulty level
                self.combo_display_text = f"{difficulty} Combo"

        self.time_remaining = self.work_time
        self.is_resting = False
        self.is_paused = False

        self.round_label.setText(f"Round {self.current_round}/{self.total_rounds}")
        self.rest_label.hide()
        self.timer_label.setText(self.format_time(self.time_remaining))
        self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")
        self.pause_btn.setText("Pause")
        # Ensure Pause button starts in red style
        self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)

        # Show sequence/combo for Self-Select and Punch Combination modes
        if self.is_self_select_mode:
            self.sequence_label.show()
            self.update_sequence_display()
        elif self.difficulty in ["Beginner", "Intermediate", "Advanced"] and self.combo_display_text:
            self.sequence_label.show()
            self.sequence_label.setText(self.combo_display_text)
        else:
            self.sequence_label.hide()

        # Send round start message for non-Self-Select modes
        self.send_round_start_message()

        self.timer.start(1000)  # Update every 1 second

    def update_sequence_display(self):
        """Show the current sequence text."""
        if self.is_self_select_mode and self.sequences:
            current_sequence = self.sequences[self.sequence_index]
            self.sequence_label.setText(current_sequence)
            try:
                payload = {
                    "mode": self.difficulty,
                    "sequence": current_sequence,
                    "sequence_index": self.sequence_index,
                }
                print(json.dumps(payload))
            except Exception:
                pass
        else:
            self.sequence_label.setText("")

    def update_timer(self):
        """Update the timer display."""
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.setText(self.format_time(self.time_remaining))

            # Cycle self-select sequences every 6s during work
            if self.is_self_select_mode and not self.is_resting and self.sequences:
                if self.sequence_time_remaining > 0:
                    self.sequence_time_remaining -= 1
                if self.sequence_time_remaining <= 0 and self.time_remaining > 0:
                    self.sequence_index = (self.sequence_index + 1) % len(self.sequences)
                    self.sequence_time_remaining = self.sequence_cycle_seconds
                    self.update_sequence_display()
        else:
            if self.is_resting:
                # Rest finished -> next round
                self.current_round += 1
                self.is_resting = False
                self.time_remaining = self.work_time
                self.round_label.setText(f"Round {self.current_round}/{self.total_rounds}")
                self.rest_label.hide()
                self.timer_label.setText(self.format_time(self.time_remaining))
                self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #4CAF50;")
                
                # Send round start message for new round
                self.send_round_start_message()
                
                # reset sequence cycling for new round
                if self.is_self_select_mode and self.sequences:
                    self.sequence_index = 0
                    self.sequence_time_remaining = self.sequence_cycle_seconds
                    self.sequence_label.show()
                    self.update_sequence_display()
                elif self.difficulty in ["Beginner", "Intermediate", "Advanced"] and self.combo_display_text:
                    # Show combo for Punch Combination modes
                    self.sequence_label.show()
                    self.sequence_label.setText(self.combo_display_text)
                else:
                    self.sequence_label.hide()
            else:
                # Work finished
                if self.current_round < self.total_rounds:
                    # start rest
                    self.is_resting = True
                    self.time_remaining = self.rest_time
                    self.rest_label.show()
                    self.timer_label.setText(self.format_time(self.time_remaining))
                    self.timer_label.setStyleSheet("font-size: 120px; font-weight: bold; color: #FF9800;")
                    self.sequence_label.hide()
                    # Send Rest JSON message
                    try:
                        print(json.dumps({"action": "Rest"}))
                    except Exception as e:
                        print(f"Error sending rest message: {e}")
                else:
                    # final round done
                    self.timer.stop()
                    self.sequence_label.hide()
                    # Send Log Training Session JSON message
                    try:
                        print(json.dumps({"action": "Log Training Session"}))
                    except Exception as e:
                        print(f"Error sending log training session message: {e}")
                    self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

    def toggle_pause(self):
        """Pause or resume the timer."""
        if self.is_paused:
            self.timer.start(1000)
            self.pause_btn.setText("Pause")
            # Back to red when resuming (showing "Pause")
            self.pause_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
            self.is_paused = False
            if not self.is_resting:
                # Send Resume JSON message
                try:
                    print(json.dumps({"action": "Resume"}))
                except Exception as e:
                    print(f"Error sending resume message: {e}")
                
                # Resend mode-specific information after resume
                try:
                    if self.is_self_select_mode and self.sequences:
                        # For Self-Select mode, send current sequence info
                        current_sequence = self.sequences[self.sequence_index]
                        payload = {
                            "mode": "Self-Select",
                            "sequence": current_sequence,
                            "sequence_index": self.sequence_index,
                        }
                        print(json.dumps(payload))
                    elif self.difficulty == "Battle":
                        # For Battle mode, send mode and battle_style
                        payload = {
                            "mode": self.difficulty,
                            "battle_style": self.battle_style,
                        }
                        print(json.dumps(payload))
                    elif self.difficulty in ["Beginner", "Intermediate", "Advanced"]:
                        # For Punch Combination modes
                        mode_str = f"Punch-Combination {self.difficulty}"
                        payload = {
                            "mode": mode_str,
                        }
                        print(json.dumps(payload))
                except Exception as e:
                    print(f"Error resending mode info after resume: {e}")
        else:
            self.timer.stop()
            self.pause_btn.setText("Resume")
            # Green while paused (showing "Resume")
            self.pause_btn.setStyleSheet(ButtonStyle.PRIMARY_MEDIUM)
            self.is_paused = True
            if not self.is_resting:
                # Send Pause JSON message
                try:
                    print(json.dumps({"action": "Pause"}))
                except Exception as e:
                    print(f"Error sending pause message: {e}")

    def on_stop_clicked(self):
        """Stop timer and go back to BasicParametersPage."""
        self.timer.stop()
        # Send Stop JSON message
        try:
            print(json.dumps({"action": "Stop"}))
        except Exception as e:
            print(f"Error sending stop message: {e}")
        self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

class SelfSelectSequencePage(QWidget):
    """Page for creating custom punch sequences."""
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state
        self.current_sequence = []  # Current sequence being built
        self.sequence_list = []  # List of confirmed sequences (max 5)
        self.editing_index = None  # Track which sequence is being edited
        
        main_layout = QHBoxLayout()
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(50, 50, 50, 50)

        # LEFT SIDE - Sequence List
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)

        list_title = QLabel("Sequence List")
        list_title.setAlignment(Qt.AlignCenter)
        list_title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 10px;")

        # Container for sequence buttons
        self.sequence_buttons_layout = QVBoxLayout()
        self.sequence_buttons_layout.setSpacing(10)
        self.sequence_buttons = []
        
        # Create 5 sequence slots
        for i in range(5):
            h_layout = QHBoxLayout()
            h_layout.setSpacing(10)
            
            # Sequence button (clickable to edit)
            seq_btn = QPushButton(f"{i+1}) ")
            seq_btn.setStyleSheet("""
                QPushButton {
                    font-size: 18px;
                    padding: 10px;
                    background-color: #f0f0f0;
                    border: 2px solid #ccc;
                    border-radius: 8px;
                    text-align: left;
                    color: black;
                    min-height: 50px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                    border: 2px solid #2196F3;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """)
            seq_btn.clicked.connect(lambda checked, idx=i: self.edit_sequence(idx))
            
            # Up button
            up_btn = QPushButton("▲")
            up_btn.setFixedSize(40, 50)
            up_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            up_btn.clicked.connect(lambda checked, idx=i: self.move_sequence_up(idx))
            
            # Down button
            down_btn = QPushButton("▼")
            down_btn.setFixedSize(40, 50)
            down_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            down_btn.clicked.connect(lambda checked, idx=i: self.move_sequence_down(idx))
            
            # Delete button
            del_btn = QPushButton("✖")
            del_btn.setFixedSize(40, 50)
            del_btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    background-color: #f44336;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #da190b;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
            """)
            del_btn.clicked.connect(lambda checked, idx=i: self.delete_sequence(idx))
            
            h_layout.addWidget(seq_btn, stretch=1)
            h_layout.addWidget(up_btn)
            h_layout.addWidget(down_btn)
            h_layout.addWidget(del_btn)
            
            self.sequence_buttons_layout.addLayout(h_layout)
            self.sequence_buttons.append({
                'button': seq_btn,
                'up': up_btn,
                'down': down_btn,
                'delete': del_btn
            })

        # Back and Next buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        back_btn = QPushButton("Back")
        self.next_btn = QPushButton("Next")
        
        back_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        self.next_btn.setStyleSheet(ButtonStyle.BACK_MEDIUM)
        
        back_btn.setFixedWidth(150)
        self.next_btn.setFixedWidth(150)
        
        back_btn.clicked.connect(self.on_back_clicked)
        self.next_btn.clicked.connect(self.on_next_clicked)
        
        button_layout.addWidget(back_btn)
        button_layout.addWidget(self.next_btn)

        left_layout.addWidget(list_title)
        left_layout.addLayout(self.sequence_buttons_layout)
        left_layout.addStretch()
        left_layout.addLayout(button_layout)

        # RIGHT SIDE - Input Area
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)

        # Text box showing current sequence
        self.sequence_input = QLabel("")
        self.sequence_input.setAlignment(Qt.AlignCenter)
        self.sequence_input.setStyleSheet("""
            font-size: 24px;
            padding: 15px;
            background-color: white;
            border: 2px solid #2196F3;
            border-radius: 8px;
            min-height: 60px;
            color: black;
        """)

        # Numpad grid (1-6)
        numpad_grid = QGridLayout()
        numpad_grid.setSpacing(10)
        
        for i in range(6):
            btn = QPushButton(str(i + 1))
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 28px;
                    padding: 20px;
                    min-width: 80px;
                    min-height: 80px;
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
            btn.clicked.connect(lambda checked, val=str(i + 1): self.add_to_sequence(val))
            row = i // 3
            col = i % 3
            numpad_grid.addWidget(btn, row, col)

        # Defense buttons (Slip-L, Slip-R, Block-L, Block-R)
        defense_grid = QGridLayout()
        defense_grid.setSpacing(10)
        
        defense_moves = ["Slip-L", "Slip-R", "Block-L", "Block-R"]
        for i, move in enumerate(defense_moves):
            btn = QPushButton(move)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    padding: 15px;
                    min-width: 100px;
                    min-height: 60px;
                    background-color: #FF9800;
                    color: white;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #F57C00;
                }
                QPushButton:pressed {
                    background-color: #E65100;
                }
            """)
            btn.clicked.connect(lambda checked, val=move: self.add_to_sequence(val))
            row = i // 2
            col = i % 2
            defense_grid.addWidget(btn, row, col)

        # Backspace and Confirm buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(15)
        
        backspace_btn = QPushButton("Backspace")
        self.confirm_btn = QPushButton("Confirm")
        
        backspace_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                padding: 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        backspace_btn.clicked.connect(self.backspace_sequence)
        self.confirm_btn.clicked.connect(self.confirm_sequence)
        
        action_layout.addWidget(backspace_btn)
        action_layout.addWidget(self.confirm_btn)

        right_layout.addWidget(self.sequence_input)
        right_layout.addLayout(numpad_grid)
        right_layout.addLayout(defense_grid)
        right_layout.addLayout(action_layout)
        right_layout.addStretch()

        # Add left and right layouts to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)

        self.setLayout(main_layout)
        
        # Initial state
        self.update_sequence_buttons()
        self.update_buttons()

    def update_sequence_buttons(self):
        """Update all sequence button displays and states."""
        for i in range(5):
            if i < len(self.sequence_list):
                self.sequence_buttons[i]['button'].setText(f"{i+1}) {self.sequence_list[i]}")
                self.sequence_buttons[i]['button'].setEnabled(True)
                self.sequence_buttons[i]['delete'].setEnabled(True)
                # Enable up button if not first
                self.sequence_buttons[i]['up'].setEnabled(i > 0)
                # Enable down button if not last in list
                self.sequence_buttons[i]['down'].setEnabled(i < len(self.sequence_list) - 1)
            else:
                self.sequence_buttons[i]['button'].setText(f"{i+1}) ")
                self.sequence_buttons[i]['button'].setEnabled(False)
                self.sequence_buttons[i]['up'].setEnabled(False)
                self.sequence_buttons[i]['down'].setEnabled(False)
                self.sequence_buttons[i]['delete'].setEnabled(False)

    def edit_sequence(self, index):
        """Load a sequence for editing."""
        if index < len(self.sequence_list):
            self.editing_index = index
            # Load the sequence into current_sequence
            self.current_sequence = self.sequence_list[index].split()
            self.sequence_input.setText(" ".join(self.current_sequence))
            self.update_buttons()

    def move_sequence_up(self, index):
        """Move sequence up in the list."""
        if index > 0 and index < len(self.sequence_list):
            self.sequence_list[index], self.sequence_list[index - 1] = \
                self.sequence_list[index - 1], self.sequence_list[index]
            self.update_sequence_buttons()

    def move_sequence_down(self, index):
        """Move sequence down in the list."""
        if index < len(self.sequence_list) - 1:
            self.sequence_list[index], self.sequence_list[index + 1] = \
                self.sequence_list[index + 1], self.sequence_list[index]
            self.update_sequence_buttons()

    def delete_sequence(self, index):
        """Delete a sequence from the list."""
        if index < len(self.sequence_list):
            self.sequence_list.pop(index)
            # Clear editing if we're editing this sequence
            if self.editing_index == index:
                self.editing_index = None
                self.current_sequence = []
                self.sequence_input.setText("")
            elif self.editing_index is not None and self.editing_index > index:
                # Adjust editing index if needed
                self.editing_index -= 1
            self.update_sequence_buttons()
            self.update_buttons()

    def add_to_sequence(self, value):
        """Add a move to the current sequence."""
        if len(self.current_sequence) < 9:
            self.current_sequence.append(value)
            self.sequence_input.setText(" ".join(self.current_sequence))
            self.update_buttons()

    def backspace_sequence(self):
        """Remove the last item from current sequence."""
        if self.current_sequence:
            self.current_sequence.pop()
            self.sequence_input.setText(" ".join(self.current_sequence))
            self.update_buttons()

    def confirm_sequence(self):
        """Add current sequence to the sequence list or update existing."""
        if 1 <= len(self.current_sequence) <= 9:
            sequence_str = " ".join(self.current_sequence)
            
            if self.editing_index is not None:
                # Update existing sequence
                self.sequence_list[self.editing_index] = sequence_str
                self.editing_index = None
            elif len(self.sequence_list) < 5:
                # Add new sequence
                self.sequence_list.append(sequence_str)
            
            self.current_sequence = []
            self.sequence_input.setText("")
            self.update_sequence_buttons()
            self.update_buttons()

    def update_buttons(self):
        """Update button states based on current input."""
        # Confirm button: enabled if 1-9 items
        sequence_valid = 1 <= len(self.current_sequence) <= 9
        
        if self.editing_index is not None:
            # Editing mode - always allow confirm
            self.confirm_btn.setEnabled(sequence_valid)
        else:
            # Adding mode - check if we can add more
            can_add_more = len(self.sequence_list) < 5
            self.confirm_btn.setEnabled(sequence_valid and can_add_more)
        
        # Next button: enabled if at least one sequence exists
        self.next_btn.setEnabled(len(self.sequence_list) >= 1)

    def on_back_clicked(self):
        """Go back to Punch Combination page."""
        # Reset state
        self.current_sequence = []
        self.sequence_list = []
        self.editing_index = None
        self.sequence_input.setText("")
        self.update_sequence_buttons()
        self.update_buttons()
        self.stacked_widget.setCurrentIndex(PageIndex.PUNCH_COMBINATIONS)

    def on_next_clicked(self):
        """Go to Basic Parameters page."""
        if len(self.sequence_list) >= 1:
            # Store sequences via app_state
            if self.app_state:
                self.app_state.set_sequences(self.sequence_list.copy())
                try:
                    basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                    basic_page.update_button_displays()
                except Exception:
                    pass
            else:
                try:
                    basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                    basic_page.custom_sequences = self.sequence_list.copy()
                except Exception:
                    pass
            self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

class SparPage(QWidget):
    """Page with Spar options."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(50,50,50,50)

        title = QLabel("Spar")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 15px;")

        battle_btn = QPushButton("Battle")
        back_btn = QPushButton("Back")

        # Make Battle button look the same as the Spar button in TrainingPage
        battle_btn.setStyleSheet(ButtonStyle.PRIMARY_LARGE)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        battle_btn.clicked.connect(self.on_battle_clicked)
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addWidget(title)
        layout.addWidget(battle_btn)
        layout.addStretch()
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def on_battle_clicked(self):
        # BattlePage index moved to 13 after removing defense page
        self.stacked_widget.setCurrentIndex(PageIndex.BATTLE)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.TRAINING)

class BattlePage(QWidget):
    def __init__(self, stacked_widget, app_state=None):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.app_state = app_state

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(24)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Battle")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 30px; font-weight: bold; margin-bottom: 8px;")

        buttons = [
            QPushButton("Pressure Fighter"),
            QPushButton("Counter Puncher"),
            QPushButton("Infighter"),
            QPushButton("Out Boxer"),
            QPushButton("Random"),
        ]
        back_btn = QPushButton("Back")

        for b in buttons:
            b.setStyleSheet(ButtonStyle.INFO_MEDIUM)
        back_btn.setStyleSheet(ButtonStyle.BACK_LARGE)

        # wire clicks
        buttons[0].clicked.connect(lambda: self.on_style_clicked("Pressure Fighter"))
        buttons[1].clicked.connect(lambda: self.on_style_clicked("Counter Puncher"))
        buttons[2].clicked.connect(lambda: self.on_style_clicked("Balanced Boxer"))
        buttons[3].clicked.connect(lambda: self.on_style_clicked("Out Boxer"))
        buttons[4].clicked.connect(lambda: self.on_style_clicked("Random"))
        back_btn.clicked.connect(self.on_back_clicked)

        layout.addStretch(1)
        layout.addWidget(title)
        for b in buttons:
            layout.addStretch(1)
            layout.addWidget(b)
        layout.addStretch(1)
        layout.addWidget(back_btn)
        layout.addStretch(1)

        self.setLayout(layout)

    def on_style_clicked(self, style):
        """Store style via app state and go to Basic Parameters page."""
        print(f"{style} selected")
        if self.app_state:
            self.app_state.update_battle_style(style)
            self.app_state.update_difficulty("Battle")
            self.app_state.previous_page = PageIndex.BATTLE
        else:
            try:
                basic_page = self.stacked_widget.widget(PageIndex.BASIC_PARAMETERS)
                basic_page.selected_battle_style = style
                basic_page.selected_difficulty = "Battle"
                basic_page.previous_page = PageIndex.BATTLE
            except Exception:
                pass
        self.stacked_widget.setCurrentIndex(PageIndex.BASIC_PARAMETERS)

    def on_back_clicked(self):
        self.stacked_widget.setCurrentIndex(PageIndex.SPAR)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boxing Training App")
        self.setFixedSize(1024, 600)

        # Auto-setup database on first run
        self._ensure_database_setup()

        self.stacked_widget = QStackedWidget()
        self.app_state = AppState(initial_page=PageIndex.HOMEPAGE)

        # Create pages
        self.homepage = Homepage(self.stacked_widget)
        self.training_page = TrainingPage(self.stacked_widget)
        self.techniques_page = TechniquesPage(self.stacked_widget)
        self.punch_combinations_page = PunchCombinationPage(self.stacked_widget, self.app_state)
        self.basic_parameters_page = BasicParametersPage(self.stacked_widget, self.app_state)
        self.round_selection_page = RoundSelectionPage(self.stacked_widget, self.app_state)
        self.speed_selection_page = SpeedSelectionPage(self.stacked_widget, self.app_state)
        self.time_selection_page = TimeSelectionPage(self.stacked_widget, self.app_state)
        self.rest_selection_page = RestSelectionPage(self.stacked_widget, self.app_state)
        self.countdown_page = CountdownPage(self.stacked_widget)
        self.training_session_page = TrainingSessionPage(self.stacked_widget)
        self.self_select_sequence_page = SelfSelectSequencePage(self.stacked_widget, self.app_state)
        self.spar_page = SparPage(self.stacked_widget)
        self.battle_page = BattlePage(self.stacked_widget, self.app_state)
        self.performance_page = PerformancePage(self.stacked_widget)
        self.power_instructions_page = PowerInstructionsPage(self.stacked_widget)
        self.power_punch_page = PowerPunchPage(self.stacked_widget)
        self.power_result_page = PowerResultPage(self.stacked_widget)
        self.stamina_instructions_page = StaminaInstructionsPage(self.stacked_widget)
        self.reaction_instructions_page = ReactionInstructionsPage(self.stacked_widget)
        self.reaction_test_page = ReactionTestPage(self.stacked_widget)
        self.reaction_result_page = ReactionResultPage(self.stacked_widget)
        self.others_page = OthersPage(self.stacked_widget)
        self.tech_corr_parameters_page = TechCorrParametersPage(self.stacked_widget, self.app_state)
        self.tech_corr_session_page = TechCorrSessionPage(self.stacked_widget)
        self.tech_corr_difficulty_page = TechCorrDifficultySelectionPage(self.stacked_widget)
        self.tech_corr_rounds_page = TechCorrRoundsSelectionPage(self.stacked_widget)
        self.tech_corr_speed_page = TechCorrSpeedSelectionPage(self.stacked_widget)
        self.tech_corr_time_page = TechCorrTimeSelectionPage(self.stacked_widget)
        self.tech_corr_rest_page = TechCorrRestSelectionPage(self.stacked_widget)
        
        # Login and User Management pages
        self.login_page = LoginPage(self.stacked_widget, self.app_state)
        self.user_management_page = UserManagementPage(self.stacked_widget)

        # Wire countdown completion to start the training session
        self.countdown_page.on_finished = self.start_training_session

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.homepage)                # 0
        self.stacked_widget.addWidget(self.training_page)           # 1
        self.stacked_widget.addWidget(self.techniques_page)         # 2
        self.stacked_widget.addWidget(self.punch_combinations_page) # 3
        self.stacked_widget.addWidget(self.basic_parameters_page)   # 4
        self.stacked_widget.addWidget(self.round_selection_page)    # 5
        self.stacked_widget.addWidget(self.speed_selection_page)    # 6
        self.stacked_widget.addWidget(self.time_selection_page)     # 7
        self.stacked_widget.addWidget(self.rest_selection_page)     # 8
        self.stacked_widget.addWidget(self.countdown_page)          # 9
        self.stacked_widget.addWidget(self.training_session_page)   # 10
        self.stacked_widget.addWidget(self.self_select_sequence_page) # 11
        self.stacked_widget.addWidget(self.spar_page)            # 12
        self.stacked_widget.addWidget(self.battle_page)          # 13
        self.stacked_widget.addWidget(self.performance_page)     # 14
        self.stacked_widget.addWidget(self.power_instructions_page) # 15
        self.stacked_widget.addWidget(self.power_punch_page) # 16
        self.stacked_widget.addWidget(self.power_result_page) # 17
        self.stacked_widget.addWidget(self.stamina_instructions_page) # 18
        self.stacked_widget.addWidget(self.reaction_instructions_page) # 19
        self.stacked_widget.addWidget(self.reaction_test_page) # 20
        self.stacked_widget.addWidget(self.reaction_result_page) # 21
        self.stacked_widget.addWidget(self.others_page) # 22
        self.stacked_widget.addWidget(self.tech_corr_parameters_page) # 23
        self.stacked_widget.addWidget(self.tech_corr_session_page) # 24
        self.stacked_widget.addWidget(self.tech_corr_difficulty_page) # 25
        self.stacked_widget.addWidget(self.tech_corr_rounds_page) # 26
        self.stacked_widget.addWidget(self.tech_corr_speed_page) # 27
        self.stacked_widget.addWidget(self.tech_corr_time_page) # 28
        self.stacked_widget.addWidget(self.tech_corr_rest_page) # 29
        self.stacked_widget.addWidget(self.login_page) # 30
        self.stacked_widget.addWidget(self.user_management_page) # 31

        # Start on the login page
        self.stacked_widget.setCurrentIndex(PageIndex.LOGIN)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
    
    def _ensure_database_setup(self):
        """Ensure the combo database exists and has tables. If not, set it up automatically."""
        db_path = os.path.join(os.path.dirname(__file__), 'setup', 'combos.db')
        
        try:
            # Check if database exists and has tables
            needs_setup = False
            
            if not os.path.exists(db_path):
                needs_setup = True
                print("Database file not found, running setup...")
            else:
                # Check if tables exist
                try:
                    import sqlite3
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='combos'")
                    if cursor.fetchone() is None:
                        needs_setup = True
                        print("Database tables not found, running setup...")
                    conn.close()
                except Exception as e:
                    print(f"Error checking database: {e}")
                    needs_setup = True
            
            # Run setup if needed
            if needs_setup:
                setup_script = os.path.join(os.path.dirname(__file__), 'setup', 'setup_combo_database.py')
                if os.path.exists(setup_script):
                    print(f"Running database setup from: {setup_script}")
                    import subprocess
                    try:
                        db_path = os.path.join(os.path.dirname(__file__), 'setup', 'combos.db')
                        result = subprocess.run(
                            [sys.executable, setup_script, '--db-path', db_path, '--force'],
                            cwd=os.path.dirname(__file__),
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if result.returncode == 0:
                            print("✓ Database setup completed successfully!")
                        else:
                            print(f"✗ Database setup failed: {result.stderr}")
                    except subprocess.TimeoutExpired:
                        print("✗ Database setup timed out (30 seconds)")
                else:
                    print(f"Setup script not found at: {setup_script}")
        
        except Exception as e:
            print(f"Error in database setup: {e}")
            import traceback
            traceback.print_exc()
    
    def get_current_user(self):
        """Get the currently logged in user."""
        return self.login_page.get_current_user()

    def start_training_session(self):
        """Extract parameters and start the training session."""
        try:
            config = self.app_state.get_config()
            rounds = config.rounds

            time_str = self.app_state.time_label or config.get_time_str()
            rest_str = self.app_state.rest_label or config.get_rest_str()

            difficulty = config.difficulty
            sequences = config.custom_sequences
            battle_style = config.battle_style

            # Emit payload when countdown ends (battle or punch-library flows)
            # Skip emission for Self-Select; it will emit per-sequence refresh instead
            # if (difficulty != "Self-Select") and (difficulty or battle_style):
            #     payload = {
            #         "mode": difficulty,
            #         "battle_style": battle_style,
            #         "sequences": sequences,
            #     }
            #     print(json.dumps(payload))

            training_page = self.stacked_widget.widget(PageIndex.TRAINING_SESSION)
            training_page.start_session(rounds, time_str, rest_str, difficulty, sequences, battle_style)
            self.stacked_widget.setCurrentIndex(PageIndex.TRAINING_SESSION)
        except Exception as e:
            print(f"Error starting training session: {e}")

def main():
    """
    Initialize and run the PyQt application.

    Creates a QApplication instance, instantiates the main window,
    displays it, and starts the application event loop.

    Returns:
        None
    """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()