import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np

from theme_manager import ThemeManager

class VisualComponents:
    """Utility class for creating visual components"""
    
    @staticmethod
    def setup_matplotlib_style():
        """Configure matplotlib styling for the application"""
        plt.style.use('ggplot')
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
        plt.rcParams['axes.facecolor'] = '#FFFFFF'
        plt.rcParams['axes.edgecolor'] = '#CCCCCC'
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.color'] = '#EEEEEE'
        plt.rcParams['figure.facecolor'] = '#FFFFFF'
        
    @staticmethod
    def create_health_indicator(parent, width=100, height=30):
        """Create a health status indicator widget"""
        frame = ttk.Frame(parent, width=width, height=height)
        
        # Status label
        status_label = ttk.Label(frame, text="Normal", style="Normal.TLabel")
        status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Color indicator
        indicator = ttk.Frame(frame, width=15, height=15, style="Normal.TFrame")
        indicator.pack(side=tk.LEFT)
        
        # Make sure the indicator keeps its size
        indicator.pack_propagate(False)
        
        # Create a method to update the indicator
        def update_status(status):
            status_label.config(text=status, style=f"{status}.TLabel")
            indicator.config(style=f"{status}.TFrame")
        
        # Attach the method to the frame
        frame.update_status = update_status
        
        return frame
        
    @staticmethod
    def create_gauge(parent, label, min_val, max_val, initial_val, unit="", width=200, height=120, 
                    warning_threshold=None, danger_threshold=None):
        """Create a gauge widget for displaying a health metric"""
        frame = ttk.Frame(parent, width=width, height=height)
        frame.pack_propagate(False)  # Don't shrink
        
        # Create canvas for the gauge
        canvas = tk.Canvas(frame, width=width, height=height-30, 
                           bg=ThemeManager.COLORS['card'], highlightthickness=0)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Add label
        header = ttk.Label(frame, text=label, style="SubHeader.TLabel")
        header.pack(side=tk.TOP, pady=(0, 5))
        
        # Add value display with units
        value_var = tk.StringVar(value=f"{initial_val} {unit}")
        value_label = ttk.Label(frame, textvariable=value_var, font=("Arial", 14))
        value_label.pack(side=tk.TOP)
        
        # Draw the gauge
        def draw_gauge(value):
            canvas.delete("gauge")
            
            # Calculate position
            value = max(min_val, min(value, max_val))  # Clamp value
            angle_range = 120  # Degrees
            start_angle = 180 + (angle_range / 2)  # Start from bottom left
            
            # Calculate angle based on value
            ratio = (value - min_val) / (max_val - min_val)
            angle = start_angle - (ratio * angle_range)
            
            # Determine color based on thresholds
            color = ThemeManager.COLORS['accent']  # Default green
            if danger_threshold is not None and value >= danger_threshold:
                color = ThemeManager.COLORS['danger']
            elif warning_threshold is not None and value >= warning_threshold:
                color = ThemeManager.COLORS['warning']
            
            # Draw background arc
            cx = width / 2
            cy = (height - 30) - 10  # center y with some padding
            radius = min(cx, cy) - 10
            
            # Background arc (gray)
            start_rad = np.deg2rad(start_angle)
            end_rad = np.deg2rad(start_angle - angle_range)
            
            # Create points for background arc
            bg_points = []
            for i in range(int(start_angle), int(start_angle - angle_range - 1), -5):
                rad = np.deg2rad(i)
                x = cx + radius * np.cos(rad)
                y = cy + radius * np.sin(rad)
                bg_points.extend([x, y])
            
            if bg_points:
                canvas.create_line(bg_points, fill="#CCCCCC", width=5, smooth=True, tags="gauge")
            
            # Value arc (colored)
            val_points = []
            for i in range(int(start_angle), int(angle - 1), -5):
                rad = np.deg2rad(i)
                x = cx + radius * np.cos(rad)
                y = cy + radius * np.sin(rad)
                val_points.extend([x, y])
            
            if val_points:
                canvas.create_line(val_points, fill=color, width=5, smooth=True, tags="gauge")
            
            # Draw min and max labels
            canvas.create_text(cx - radius * 0.8, cy + 15, 
                               text=str(min_val), fill=ThemeManager.COLORS['text_dark'],
                               font=("Arial", 8), tags="gauge")
            canvas.create_text(cx + radius * 0.8, cy + 15, 
                               text=str(max_val), fill=ThemeManager.COLORS['text_dark'],
                               font=("Arial", 8), tags="gauge")
            
            # Update the displayed value
            value_var.set(f"{value} {unit}")
        
        # Initial draw
        draw_gauge(initial_val)
        
        # Create update method
        def update_value(new_value):
            draw_gauge(new_value)
        
        # Attach the method to the frame
        frame.update_value = update_value
        
        return frame
    
    @staticmethod
    def setup_charts(fig, axes):
        """Set up the trend charts with better styling"""
        
        # Apply style to all subplots
        for ax in axes.flat:
            ax.set_facecolor('#FFFFFF')
            ax.grid(True, linestyle='--', alpha=0.7, color='#EEEEEE')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('#CCCCCC')
            ax.spines['left'].set_color('#CCCCCC')
            ax.tick_params(colors='#666666')
            ax.set_xlabel('Time', color='#666666', fontsize=9)
            
        # Heart Rate plot
        axes[0, 0].set_title('Heart Rate', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('BPM', color='#666666', fontsize=9)
        
        # Blood Pressure plot
        axes[0, 1].set_title('Blood Pressure', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('mmHg', color='#666666', fontsize=9)
        
        # Oxygen Level plot
        axes[1, 0].set_title('Oxygen Level', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('SpO2 %', color='#666666', fontsize=9)
        
        # Temperature plot
        axes[1, 1].set_title('Temperature', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('°C', color='#666666', fontsize=9)
        
        # Format figures
        fig.tight_layout(pad=3.0)
        
    @staticmethod
    def update_charts(axes, timestamps, heart_rates, bp_systolic, bp_diastolic, oxygen_levels, temperatures):
        """Update the trend charts with data"""
        
        # Clear previous plots
        for ax in axes.flat:
            ax.clear()
            ax.grid(True, linestyle='--', alpha=0.7, color='#EEEEEE')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        # Plot heart rate with improved styling
        axes[0, 0].plot(timestamps, heart_rates, color=ThemeManager.COLORS['danger'], 
                       marker='o', markersize=3, linewidth=2)
        axes[0, 0].fill_between(timestamps, heart_rates, alpha=0.1, color=ThemeManager.COLORS['danger'])
        axes[0, 0].set_title('Heart Rate', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('BPM', color='#666666', fontsize=9)
        
        # Reference ranges for heart rate
        axes[0, 0].axhspan(60, 100, alpha=0.1, color=ThemeManager.COLORS['accent'], label='Normal Range')
        
        # Plot blood pressure with improved styling
        axes[0, 1].plot(timestamps, bp_systolic, color=ThemeManager.COLORS['danger'], 
                      marker='o', markersize=3, linewidth=2, label='Systolic')
        axes[0, 1].plot(timestamps, bp_diastolic, color=ThemeManager.COLORS['info'], 
                      marker='o', markersize=3, linewidth=2, label='Diastolic')
        axes[0, 1].fill_between(timestamps, bp_systolic, bp_diastolic, alpha=0.1, 
                             color=ThemeManager.COLORS['secondary'])
        axes[0, 1].set_title('Blood Pressure', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('mmHg', color='#666666', fontsize=9)
        axes[0, 1].legend(loc='upper right', frameon=True, fontsize=8)
        
        # Reference ranges for blood pressure
        axes[0, 1].axhspan(120, 129, alpha=0.1, color='yellow', label='Elevated (Systolic)')
        axes[0, 1].axhspan(70, 80, alpha=0.1, color=ThemeManager.COLORS['accent'], label='Normal (Diastolic)')
        
        # Plot oxygen level with improved styling
        axes[1, 0].plot(timestamps, oxygen_levels, color=ThemeManager.COLORS['info'], 
                      marker='o', markersize=3, linewidth=2)
        axes[1, 0].fill_between(timestamps, oxygen_levels, alpha=0.1, color=ThemeManager.COLORS['info'])
        axes[1, 0].set_title('Oxygen Level', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('SpO2 %', color='#666666', fontsize=9)
        
        # Reference ranges for oxygen
        axes[1, 0].axhspan(95, 100, alpha=0.1, color=ThemeManager.COLORS['accent'], label='Normal Range')
        axes[1, 0].axhspan(90, 94, alpha=0.1, color='yellow', label='Concerning Range')
        
        # Plot temperature with improved styling
        axes[1, 1].plot(timestamps, temperatures, color=ThemeManager.COLORS['warning'], 
                      marker='o', markersize=3, linewidth=2)
        axes[1, 1].fill_between(timestamps, temperatures, alpha=0.1, color=ThemeManager.COLORS['warning'])
        axes[1, 1].set_title('Temperature', color=ThemeManager.COLORS['primary'], fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('°C', color='#666666', fontsize=9)
        
        # Reference ranges for temperature
        axes[1, 1].axhspan(36.5, 37.5, alpha=0.1, color=ThemeManager.COLORS['accent'], label='Normal Range')
        
        # Format x-axis for all plots
        for ax in axes.flat:
            ax.set_xlabel('Time', color='#666666', fontsize=9)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
            ax.tick_params(axis='x', rotation=45, colors='#666666', labelsize=8)
            ax.tick_params(axis='y', colors='#666666', labelsize=8)

            ax.legend(loc='upper right', frameon=True, fontsize=8)
                    

