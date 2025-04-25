import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np
import os


class StatsWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Statistics Window")
        self.root.geometry("1000x630")

        # Configure style tabs
        style = ttk.Style()
        style.configure("TNotebook", font=("Arial", 20))

        # Font
        self.font_topic = ("Arial", 14)

        # Notebook = Tabs
        tab_control = ttk.Notebook(self.root)

        # Create tabs
        self.overall_stats_tab(tab_control)
        self.create_keystroke_tab(tab_control)
        self.create_order_per_dish_tab(tab_control)
        self.create_mistake_tab(tab_control)
        self.create_ingredients_used_tab(tab_control)
        self.create_total_time_per_dish_tab(tab_control)

        tab_control.pack(expand=1, fill="both")

        self.root.mainloop()

    def overall_stats_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Overall Stats')

        # Main container with scrollbar
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Title
        ttk.Label(content_frame,
                  text="Overall Game Statistics",
                  font=("Arial", 16, "bold")).pack(pady=20)

        try:
            # Load all relevant data
            order_df = pd.read_csv('order_per_session.csv') if os.path.exists('order_per_session.csv') else None
            mistake_df = pd.read_csv('mistake.csv') if os.path.exists('mistake.csv') else None
            ingredient_df = pd.read_csv('ingredient_used.csv') if os.path.exists('ingredient_used.csv') else None
            keystroke_df = pd.read_csv('keystroke_per_dish.csv') if os.path.exists('keystroke_per_dish.csv') else None

            # Calculate basic stats
            total_sessions = len(order_df)
            max_score = order_df['total_score'].max()
            avg_score = order_df['total_score'].mean() if 'total_score' in order_df.columns else 0

            # Calculate total orders safely
            dish_columns = [col for col in
                            ['sandwich', 'egg fried', 'chicken fried', 'lamb fried', 'chicken drumpstick fried']
                            if col in order_df.columns]
            total_orders = order_df[dish_columns].sum().sum() if dish_columns else 0

            # Calculate time metrics safely
            if all(col in order_df.columns for col in ['session_start', 'session_end']):
                order_df['session_start'] = pd.to_datetime(order_df['session_start'])
                order_df['session_end'] = pd.to_datetime(order_df['session_end'])
                order_df['duration'] = (order_df['session_end'] - order_df['session_start']).dt.total_seconds()
                total_time = order_df['duration'].sum()
                avg_time = order_df['duration'].mean()
            else:
                total_time = 0
                avg_time = 0

            # Calculate other metrics safely
            total_mistakes = len(mistake_df) if mistake_df is not None else 0
            total_keystrokes = keystroke_df[
                'total_key'].sum() if keystroke_df is not None and 'total_key' in keystroke_df.columns else 0

            # Create stats frame
            stats_frame = ttk.Frame(content_frame, padding=10)
            stats_frame.pack(fill=tk.X, pady=10)

            # Key metrics section
            metrics = [
                ("Total Sessions Played", f"{total_sessions}"),
                ("Total Orders Completed", f"{total_orders}"),
                ("Max Score Earned", f"{max_score}"),
                ("Average Score per Session", f"{avg_score:.1f}"),
                ("Total Mistakes Made", f"{total_mistakes}"),
                ("Total Keystrokes", f"{total_keystrokes}"),
                ("Total Play Time", f"{total_time:.1f} seconds"),
                ("Average Session Duration", f"{avg_time:.1f} seconds")
            ]

            # Configure two equal columns per side (4 total)
            for col in range(4):
                stats_frame.grid_columnconfigure(col, weight=1)

            for i, (label, value) in enumerate(metrics):
                value_str = f"{value:.1f}" if isinstance(value, float) else str(value)
                ttk.Label(stats_frame, text=label, font=("Arial", 10, "bold")).grid(
                    row=i // 2, column=(i % 2) * 2, padx=10, pady=5, sticky="nsew")
                ttk.Label(stats_frame, text=value_str, font=("Arial", 10)).grid(
                    row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5, sticky="nsew")

            # Add visualizations only if we have data
            fig = plt.Figure(figsize=(10, 8))
            gs = fig.add_gridspec(2, 2)

            # Score distribution (if available)
            ax1 = fig.add_subplot(gs[0, 0])
            if 'total_score' in order_df.columns:
                ax1.hist(order_df['total_score'], bins=10, color='skyblue', edgecolor='black')
                ax1.set_title('Score Distribution per Session')
                ax1.set_xlabel('Score')
                ax1.set_ylabel('Frequency')
            else:
                ax1.text(0.5, 0.5, 'No score data available', ha='center', va='center')
                ax1.set_axis_off()

            # Time vs Score (if available)
            ax2 = fig.add_subplot(gs[0, 1])
            if all(col in order_df.columns for col in ['duration', 'total_score']):
                ax2.scatter(order_df['duration'], order_df['total_score'], alpha=0.6)
                ax2.set_title('Session Duration vs Score')
                ax2.set_xlabel('Duration (seconds)')
                ax2.set_ylabel('Score')
            else:
                ax2.text(0.5, 0.5, 'No duration/score data', ha='center', va='center')
                ax2.set_axis_off()

            # Mistake types (if available)
            ax3 = fig.add_subplot(gs[1, 0])
            if mistake_df is not None and 'type' in mistake_df.columns:
                mistake_counts = mistake_df['type'].value_counts()
                ax3.bar(mistake_counts.index, mistake_counts.values, color='salmon')
                ax3.set_title('Mistake Types')
                ax3.tick_params(axis='x', rotation=45)
            else:
                ax3.text(0.5, 0.5, 'No mistake data', ha='center', va='center')
                ax3.set_axis_off()

            # Keystroke distribution (if available)
            ax4 = fig.add_subplot(gs[1, 1])
            if keystroke_df is not None and all(col in keystroke_df.columns for col in ['up', 'down', 'left', 'right']):
                keystroke_cols = ['up', 'down', 'left', 'right']
                keystroke_totals = keystroke_df[keystroke_cols].sum()
                ax4.pie(keystroke_totals, labels=keystroke_totals.index, autopct='%1.1f%%')
                ax4.set_title('Keystroke Distribution')
            else:
                ax4.text(0.5, 0.5, 'No keystroke data', ha='center', va='center')
                ax4.set_axis_off()

            fig.tight_layout(pad=3.0)

            # Embed in tkinter
            chart_canvas = FigureCanvasTkAgg(fig, master=content_frame)
            chart_canvas.draw()
            chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            error_msg = f"Error loading data: {str(e)}\n\nAvailable columns in order_per_session.csv:\n"
            try:
                if os.path.exists('order_per_session.csv'):
                    test_df = pd.read_csv('order_per_session.csv')
                    error_msg += f"{', '.join(test_df.columns)}"
            except:
                error_msg += "Could not read file"

            ttk.Label(content_frame,
                      text=error_msg,
                      foreground="red",
                      wraplength=800).pack()

        # Configure scrolling
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(1, width=event.width)

        content_frame.bind("<Configure>", on_configure)

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)

        content_frame.bind("MouseWheel>", _on_mousewheel)

    def load_stats(self):
        # Placeholder for loading stats logic
        print("Loading stats...")

        # Example: Update the label with loaded stats
        stats_label = ttk.Label(self.root, text="Stats Loaded Successfully!", font=self.font_topic)
        stats_label.pack(pady=10)

    def create_keystroke_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Keystroke Analysis')

        # Create main container with scrollbar
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        df = pd.read_csv('keystroke_per_dish.csv', skipinitialspace=True)
        x = range(1, len(df) + 1)

        # Create figure with custom grid layout
        fig = plt.Figure(figsize=(10, 8), dpi=100)
        gs = fig.add_gridspec(2, 2, width_ratios=[3, 1], height_ratios=[1, 1])

        # Top-left: Total keystrokes trend
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(x, df['total_key'], marker='o', color='steelblue', linewidth=2)
        ax1.set_ylabel('Total Keystrokes')
        ax1.set_title('Total Keystrokes Trend')
        ax1.set_xticks(x)
        ax1.set_xticklabels(df['id'].astype(str), rotation=90)
        ax1.xaxis.set_major_formatter(plt.NullFormatter())
        ax1.grid(True, linestyle='--', alpha=0.6)

        # Top-right: Statistics table
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.axis('off')  # Hide axes for table

        stats_data = [
            ["Mean", f"{df['total_key'].mean():.2f}"],
            ["Median", f"{df['total_key'].median():.2f}"],
            ["Std Dev", f"{df['total_key'].std():.2f}"],
            ["Min", f"{df['total_key'].min()}"],
            ["Max", f"{df['total_key'].max()}"],
            ["Total", f"{df['total_key'].sum()}"]
        ]

        table = ax2.table(
            cellText=stats_data,
            colLabels=["Statistic", "Value"],
            loc='center',
            cellLoc='center',
            colWidths=[0.4, 0.4]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        # Bottom: Individual key trends (full width)
        ax3 = fig.add_subplot(gs[1, :])
        ax3.plot(x, df['up'], marker='o', label='Up', color='skyblue')
        ax3.plot(x, df['down'], marker='o', label='Down', color='salmon')
        ax3.plot(x, df['left'], marker='o', label='Left', color='lightgreen')
        ax3.plot(x, df['right'], marker='o', label='Right', color='orange')
        ax3.set_xlabel('Dish ID')
        ax3.set_ylabel('Keystroke Count')
        ax3.set_title('Keystroke Trends by Direction')
        ax3.set_xticks(x)
        ax3.set_xticklabels(df['id'].astype(str), rotation=90)
        ax3.legend()
        ax3.grid(True, linestyle='--', alpha=0.6)

        fig.tight_layout(pad=3.0)

        # Embed in tkinter
        chart_canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Update scroll region
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(1, width=event.width)

        scrollable_frame.bind("<Configure>", on_configure)

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_order_per_dish_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Order Analysis')

        label = ttk.Label(tab, text="Order Patterns Across Sessions", font=self.font_topic)
        label.pack(pady=20)

        # Load CSV
        df = pd.read_csv('order_per_session.csv', skipinitialspace=True, on_bad_lines='skip')

        # Convert timestamps to datetime and calculate session duration
        df['session_start'] = pd.to_datetime(df['session_start'])
        df['session_end'] = pd.to_datetime(df['session_end'])
        df['duration_sec'] = (df['session_end'] - df['session_start']).dt.total_seconds()

        dish_columns = ['sandwich', 'egg fried', 'chicken fried', 'lamb fried', 'chicken drumpstick fried']

        # Create scatter plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot each dish type with different markers
        markers = ['o', 's', 'D', '^', 'v']  # Circle, square, diamond, triangle up/down
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

        for i, dish in enumerate(dish_columns):
            ax.scatter(
                x=df['duration_sec'],
                y=df[dish] * df['total_score'],  # Weight orders by score
                label=dish.title(),
                marker=markers[i],
                color=colors[i],
                s=100,  # Marker size
                alpha=0.7,
                edgecolors='w'
            )

        # Customize plot
        ax.set_title('Order Patterns by Session Duration', pad=20)
        ax.set_xlabel('Session Duration (seconds)')
        ax.set_ylabel('Order Value (Count × Score)')
        ax.grid(True, linestyle=':', alpha=0.3)
        ax.legend(title="Dish Types")

        # Add trendlines
        for dish in dish_columns:
            z = np.polyfit(df['duration_sec'], df[dish] * df['total_score'], 1)
            p = np.poly1d(z)
            ax.plot(df['duration_sec'], p(df['duration_sec']), '--', alpha=0.3)

        # Show in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_mistake_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Mistakes')

        label = ttk.Label(tab, text="Mistakes during the game session", font=self.font_topic)
        label.pack(pady=20)

        try:
            df = pd.read_csv('mistake.csv', skipinitialspace=True)

            # Group by mistake type and count occurrences
            mistake_counts = df['mistake_type'].value_counts()

            # Plot
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(mistake_counts.index, mistake_counts.values, color='salmon', edgecolor='black')

            ax.set_title('Mistakes Made')
            ax.set_xlabel('Mistake Type')
            ax.set_ylabel('Count')

            # Show on Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=tab)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        except FileNotFoundError:
            ttk.Label(tab, text="Error: File 'mistake.csv' not found.").pack(pady=10)
        except Exception as e:
            ttk.Label(tab, text=f"Error: {str(e)}").pack(pady=10)

    def create_ingredients_used_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Ingredients Used')

        label = ttk.Label(tab, text="Ingredients Taken Summary", font=self.font_topic)
        label.pack(pady=10)

        try:
            df = pd.read_csv('ingredient_used.csv', skipinitialspace=True)

            # Filter only 'Taken'
            taken_df = df[df['action'].str.lower() == 'taken']

            # Group and sum quantities
            total_taken = taken_df.groupby('ingredient')['quantity'].sum()

            if total_taken.empty:
                ttk.Label(tab, text="No 'Taken' data to show.").pack(pady=10)
                return

            # Layout frame: pie chart on left, distribution on right
            content_frame = ttk.Frame(tab)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # ---- Left: Pie Chart with Pastel Colors ----
            fig, ax = plt.subplots(figsize=(5, 5))

            # Define pastel colors using the Pastel1 colormap
            pastel_cmap = plt.get_cmap("Pastel1")
            colors = pastel_cmap(np.linspace(0, 1, len(total_taken)))

            ax.pie(
                total_taken.values,
                labels=total_taken.index,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 9},
                colors=colors
            )
            ax.set_title('Ingredients Taken', fontsize=12)

            canvas = FigureCanvasTkAgg(fig, master=content_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # ---- Right: Distribution Text ----
            dist_frame = ttk.Frame(content_frame)
            dist_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

            ttk.Label(dist_frame, text="Quantity Taken per Ingredient", font=('Helvetica', 10, 'bold')).pack(anchor='w')

            text_widget = tk.Text(dist_frame, height=15, width=30, font=('Courier', 10))
            text_widget.pack(pady=5)

            for ingredient, qty in total_taken.items():
                text_widget.insert(tk.END, f"{ingredient:<15} {qty}\n")

            text_widget.config(state=tk.DISABLED)

            max_ingredient = total_taken.idxmax()
            max_qty = total_taken.max()
            min_ingredient = total_taken.idxmin()
            min_qty = total_taken.min()

            summary_label = ttk.Label(
                dist_frame,
                text=f"Most Taken:      {max_ingredient}    ({max_qty})\n\n"
                     f"Least Taken:     {min_ingredient}    ({min_qty})",
                font=('Helvetica', 10, 'bold'),
            )
            summary_label.pack(anchor='w', pady=(10, 5))

        except FileNotFoundError:
            ttk.Label(tab, text="Error: File 'ingredient_used.csv' not found.").pack(pady=10)
        except Exception as e:
            ttk.Label(tab, text=f"Error: {str(e)}").pack(pady=10)

    def create_total_time_per_dish_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Total Time per Dish')

        label = ttk.Label(tab, text="Total Time per Dish Statistics", font=self.font_topic)
        label.pack(pady=20)


if __name__ == "__main__":
    StatsWindow()
