import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                               QHBoxLayout, QPushButton, QSlider, QSizePolicy)
from PySide6.QtGui import QPixmap, QPainter, QFont
from PySide6.QtCore import QUrl, Qt, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

class VideoPlayerWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 2px solid #333;
                border-radius: 10px;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title/Banner area with image overlay
        self.create_banner_section(layout)
        
        # Video player section
        self.create_video_section(layout)
        
        # Video controls
        self.create_controls_section(layout)
        
        # Initialize media player
        self.setup_media_player()
        
    def create_banner_section(self, layout):
        """Create simple centered Guide header"""
        title_label = QLabel("Guide")
        title_label.setFont(QFont("Arial", 32, QFont.Bold))
        title_label.setStyleSheet("color: white; padding: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
    
    def create_video_section(self, layout):
        """Create the video display section with optional image overlay"""
        # Video container
        video_container = QFrame()
        video_container.setStyleSheet("""
            QFrame {
                background-color: #000;
                border-radius: 8px;
                border: 1px solid #444;
            }
        """)
        
        video_layout = QVBoxLayout(video_container)
        video_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create a stacked widget-like container
        video_stack = QFrame()
        video_stack.setStyleSheet("background: transparent;")
        stack_layout = QVBoxLayout(video_stack)
        stack_layout.setContentsMargins(0, 0, 0, 0)
        
        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(400)
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Image overlay (poster)
        self.image_overlay = QLabel()
        self.image_overlay.setAlignment(Qt.AlignCenter)
        self.image_overlay.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 200);
                border-radius: 8px;
            }
        """)
        
        # Try to load banner image for overlay
        banner_path = "resources/images/guide_banner.png"
        if os.path.exists(banner_path):
            pixmap = QPixmap(banner_path)
            if not pixmap.isNull():
                # Scale image to fit nicely as an overlay
                scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_overlay.setPixmap(scaled_pixmap)
                self.image_overlay.show()
            else:
                self.image_overlay.hide()
        else:
            # Show play button if no image
            self.image_overlay.setText("▶ Click to Play")
            self.image_overlay.setStyleSheet("""
                QLabel {
                    background-color: rgba(0, 0, 0, 150);
                    color: white;
                    font-size: 24px;
                    font-weight: bold;
                    border-radius: 8px;
                }
            """)
        
        # Position overlay on top of video
        stack_layout.addWidget(self.video_widget)
        self.image_overlay.setParent(video_stack)
        
        video_layout.addWidget(video_stack)
        layout.addWidget(video_container)
    
    def create_controls_section(self, layout):
        """Create video control buttons and progress bar"""
        controls_frame = QFrame()
        controls_frame.setMaximumHeight(60)
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid #444;
            }
        """)
        
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setContentsMargins(15, 10, 15, 10)
        
        # Play/Pause button
        self.play_button = QPushButton("▶")
        self.play_button.setFixedSize(40, 40)
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5ba0f2;
            }
            QPushButton:pressed {
                background-color: #3a80d2;
            }
        """)
        self.play_button.clicked.connect(self.toggle_playback)
        controls_layout.addWidget(self.play_button)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Horizontal)
        self.progress_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #444;
                height: 8px;
                background: #333;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4a90e2;
                border: 1px solid #4a90e2;
                width: 18px;
                border-radius: 9px;
                margin: -5px 0;
            }
            QSlider::sub-page:horizontal {
                background: #4a90e2;
                border-radius: 4px;
            }
        """)
        controls_layout.addWidget(self.progress_slider)
        
        # Time label
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setStyleSheet("color: #ccc; margin-left: 10px;")
        self.time_label.setMinimumWidth(100)
        controls_layout.addWidget(self.time_label)
        
        layout.addWidget(controls_frame)
    
    def setup_media_player(self):
        """Initialize the media player"""
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        
        # Connect signals
        self.media_player.positionChanged.connect(self.update_position)
        self.media_player.durationChanged.connect(self.update_duration)
        self.progress_slider.sliderMoved.connect(self.set_position)
        
        # Hide overlay when video starts
        self.media_player.playbackStateChanged.connect(self.on_playback_state_changed)
        
        # Load video file
        video_path = os.path.abspath("video/intro.mp4")
        if os.path.exists(video_path):
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
        else:
            # Show error message in video widget
            self.show_video_error("Video file not found: video/intro.mp4")
    
    def show_video_error(self, message):
        """Display error message when video cannot be loaded"""
        error_label = QLabel(message)
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                font-size: 14px;
                background-color: #1a1a1a;
                padding: 20px;
                border-radius: 8px;
            }
        """)
        
        # Replace video widget with error label temporarily
        layout = self.video_widget.parent().layout()
        layout.replaceWidget(self.video_widget, error_label)
        self.video_widget.hide()
    
    def toggle_playback(self):
        """Toggle between play and pause"""
        if self.media_player.playbackState() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText("▶")
        else:
            self.media_player.play()
            self.play_button.setText("⏸")
            # Hide image overlay when video starts playing
            if hasattr(self, 'image_overlay'):
                self.image_overlay.hide()
    
    def update_position(self, position):
        """Update progress slider position"""
        self.progress_slider.setValue(position)
        self.update_time_label(position, self.media_player.duration())
    
    def update_duration(self, duration):
        """Update progress slider range"""
        self.progress_slider.setRange(0, duration)
        self.update_time_label(self.media_player.position(), duration)
    
    def set_position(self, position):
        """Set media player position"""
        self.media_player.setPosition(position)
    
    def update_time_label(self, position, duration):
        """Update time display"""
        def format_time(ms):
            s = ms // 1000
            m, s = divmod(s, 60)
            return f"{m:02d}:{s:02d}"
        
        current_time = format_time(position)
        total_time = format_time(duration)
        self.time_label.setText(f"{current_time} / {total_time}")
    
    def on_playback_state_changed(self, state):
        """Handle playback state changes"""
        if state == QMediaPlayer.PlayingState and hasattr(self, 'image_overlay'):
            self.image_overlay.hide()
        elif state == QMediaPlayer.StoppedState and hasattr(self, 'image_overlay'):
            self.image_overlay.show()


class GuideWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Set up main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add the video player widget
        self.video_player = VideoPlayerWidget()
        layout.addWidget(self.video_player)
        
        # Set background style
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a1a;
                color: white;
            }
        """)