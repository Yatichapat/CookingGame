import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import os
import seaborn as sns


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

            # Update scroll region
            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(1, width=event.width)

            content_frame.bind("<Configure>", on_configure)

            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def bind_mousewheel(widget):
                widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
                widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

            bind_mousewheel(content_frame)
            bind_mousewheel(chart_canvas.get_tk_widget())

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

        # --- Table Section ---
        table_container = ttk.Frame(scrollable_frame)
        table_container.pack(fill=tk.BOTH, expand=True, pady=(10, 20), padx=10)

        ttk.Label(table_container, text="Full Order Complete History", font=('Helvetica', 10, 'bold')).pack(
            pady=(10, 5))

        table_frame = ttk.Frame(table_container)
        table_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(table_frame, columns=list(df.columns), show='headings', height=8)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=120)

        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

        tree.pack(fill=tk.BOTH, expand=True)

        # Update scroll region
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(1, width=event.width)

        scrollable_frame.bind("<Configure>", on_configure)

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def bind_mousewheel(widget):
            widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
            widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        bind_mousewheel(scrollable_frame)
        bind_mousewheel(chart_canvas.get_tk_widget())

    def create_order_per_dish_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Order Analysis')

        # Configure grid to expand
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)

        # Main scrollable frame
        main_frame = ttk.Frame(tab)
        main_frame.grid(row=0, column=0, sticky="nsew")

        canvas = tk.Canvas(main_frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ttk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Update scrollregion and stretch canvas width
        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(window_id, width=canvas.winfo_width())

        scrollable_frame.bind("<Configure>", on_configure)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Universal mousewheel binding for scrollable_frame
        def bind_mousewheel(widget):
            widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
            widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # --- Content begins here ---
        label = ttk.Label(scrollable_frame, text="Order Patterns Across Sessions", font=self.font_topic)
        label.pack(pady=20)

        # Load CSV
        df = pd.read_csv('order_per_session.csv', skipinitialspace=True, on_bad_lines='skip')

        # Convert timestamps
        df['session_start'] = pd.to_datetime(df['session_start'])
        df['session_end'] = pd.to_datetime(df['session_end'])
        df['duration_sec'] = (df['session_end'] - df['session_start']).dt.total_seconds()

        dish_columns = ['sandwich', 'egg fried', 'chicken fried', 'lamb fried', 'chicken drumpstick fried']

        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        markers = ['o', 's', 'D', '^', 'v']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

        for i, dish in enumerate(dish_columns):
            ax.scatter(
                x=df['duration_sec'],
                y=df[dish] * df['total_score'],
                label=dish.title(),
                marker=markers[i],
                color=colors[i],
                s=100,
                alpha=0.7,
                edgecolors='w'
            )
            z = np.polyfit(df['duration_sec'], df[dish] * df['total_score'], 1)
            p = np.poly1d(z)
            ax.plot(df['duration_sec'], p(df['duration_sec']), '--', alpha=0.3)

        ax.set_title('Order Patterns by Session Duration', pad=20)
        ax.set_xlabel('Session Duration (seconds)')
        ax.set_ylabel('Order Value (Count × Score)')
        ax.grid(True, linestyle=':', alpha=0.3)
        ax.legend(title="Dish Types")

        # Embed plot
        canvas_plot = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- Table Section ---
        table_container = ttk.Frame(scrollable_frame)
        table_container.pack(fill=tk.BOTH, expand=True, pady=(10, 20), padx=10)

        ttk.Label(table_container, text="Full Order Complete History", font=('Helvetica', 10, 'bold')).pack(
            pady=(10, 5))

        table_frame = ttk.Frame(table_container)
        table_frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(table_frame, columns=list(df.columns), show='headings', height=8)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=120)

        for _, row in df.iterrows():
            tree.insert("", tk.END, values=list(row))

        tree.pack(fill=tk.BOTH, expand=True)

        # Universal mousewheel binding for scrollable_frame
        def bind_mousewheel(widget):
            widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
            widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        bind_mousewheel(scrollable_frame)
        bind_mousewheel(canvas_plot.get_tk_widget())
        bind_mousewheel(table_frame)

    def create_mistake_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Mistakes')

        # Create a canvas and scrollbar for the entire tab
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create window in canvas for the scrollable frame
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind the frame's configure event to update the scrollregion
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)

        label = ttk.Label(scrollable_frame, text="Mistakes during the game session", font=self.font_topic)
        label.pack(pady=20)

        try:
            df = pd.read_csv('mistake.csv', skipinitialspace=True)

            # Group by mistake type and count occurrences
            mistake_counts = df['mistake_type'].value_counts()

            # Create a frame for the plot to better control its size
            plot_frame = ttk.Frame(scrollable_frame)
            plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Plot with adjusted size
            fig, ax = plt.subplots(figsize=(8, 5))  # Slightly shorter height
            ax.bar(mistake_counts.index, mistake_counts.values, color='salmon', edgecolor='black')

            ax.set_title('Mistakes Made', pad=15)
            ax.set_xlabel('Mistake Type')
            ax.set_ylabel('Count')

            # Rotate x-axis labels if they're long
            if any(len(str(x)) > 10 for x in mistake_counts.index):
                plt.xticks(rotation=45, ha='right')

            # Show on Tkinter window
            canvas_plot = FigureCanvasTkAgg(fig, master=plot_frame)
            canvas_plot.draw()
            canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # ---- Table: Centered below the content ----
            table_container = ttk.Frame(scrollable_frame)
            table_container.pack(fill=tk.BOTH, expand=True, pady=(10, 20), padx=10)

            # Add a label above the table
            ttk.Label(table_container,
                      text="Full Mistakes History",
                      font=('Helvetica', 10, 'bold')).pack(pady=(10, 5))

            # Create Treeview with its own frame for scrollbars
            table_frame = ttk.Frame(table_container)
            table_frame.pack(fill=tk.BOTH, expand=True)

            # Create Treeview with adjusted height
            tree = ttk.Treeview(table_frame, columns=list(df.columns), show='headings', height=8)

            # Define column headers
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.CENTER, width=120)  # Slightly wider columns

            # Insert rows into Treeview
            for _, row in df.iterrows():
                tree.insert("", tk.END, values=list(row))

            # Scrollbars for the Treeview
            vsb_tree = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            hsb_tree = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb_tree.set, xscrollcommand=hsb_tree.set)

            # Grid layout for better control
            tree.grid(row=0, column=0, sticky="nsew")
            vsb_tree.grid(row=0, column=1, sticky="ns")
            hsb_tree.grid(row=1, column=0, sticky="ew")
            table_frame.grid_rowconfigure(0, weight=1)
            table_frame.grid_columnconfigure(0, weight=1)

            # Add some padding at the bottom to ensure everything is visible
            ttk.Frame(scrollable_frame, height=10).pack()

            # Update scroll region
            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(window_id, width=canvas.winfo_width())

            scrollable_frame.bind("<Configure>", on_configure)

            # Mousewheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def bind_mousewheel(widget):
                widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
                widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

            bind_mousewheel(scrollable_frame)
            bind_mousewheel(canvas_plot.get_tk_widget())

        except FileNotFoundError:
            ttk.Label(scrollable_frame, text="Error: File 'mistake.csv' not found.").pack(pady=10)
        except Exception as e:
            ttk.Label(scrollable_frame, text=f"Error: {str(e)}").pack(pady=10)

    def create_ingredients_used_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Ingredients Used')

        # Create a canvas and scrollbar for the entire tab
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create window in canvas for the scrollable frame
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Now put all your content inside scrollable_frame instead of tab
        label = ttk.Label(scrollable_frame, text="Ingredients Taken Summary", font=self.font_topic)
        label.pack(pady=10)

        try:
            df = pd.read_csv('ingredient_used.csv', skipinitialspace=True)

            # Filter only 'Taken'
            taken_df = df[df['action'].str.lower() == 'taken']

            # Group and sum quantities
            total_taken = taken_df.groupby('ingredient')['quantity'].sum()

            if total_taken.empty:
                ttk.Label(scrollable_frame, text="No 'Taken' data to show.").pack(pady=10)
                return

            # Layout frame: pie chart on left, distribution on right
            content_frame = ttk.Frame(scrollable_frame)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # ---- Left: Pie Chart with Pastel Colors ----
            pie_frame = ttk.Frame(content_frame)
            pie_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            fig, ax = plt.subplots(figsize=(6, 6))  # Increased figure size

            # Define pastel colors using the Pastel1 colormap
            colors = sns.color_palette("pastel", n_colors=len(total_taken))

            ax.pie(
                total_taken.values,
                labels=total_taken.index,
                autopct='%1.1f%%',
                startangle=90,
                textprops={'fontsize': 10},  # Increased font size
                colors=colors,
                wedgeprops={'linewidth': 1, 'edgecolor': 'white'}  # Better visual separation
            )
            ax.set_title('Ingredients Taken', fontsize=12, pad=20)

            canvas_pie = FigureCanvasTkAgg(fig, master=pie_frame)
            canvas_pie.draw()
            canvas_pie.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # ---- Right: Distribution Text ----
            dist_frame = ttk.Frame(content_frame)
            dist_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

            ttk.Label(dist_frame, text="Quantity Taken per Ingredient",
                      font=('Helvetica', 10, 'bold')).pack(anchor='w', pady=(0, 5))

            # Use a Frame to contain the text widget and its scrollbar
            text_container = ttk.Frame(dist_frame)
            text_container.pack(fill=tk.BOTH, expand=True)

            text_widget = tk.Text(text_container, height=15, width=30,
                                  font=('Courier', 10), wrap=tk.NONE)
            vsb_text = ttk.Scrollbar(text_container, orient="vertical", command=text_widget.yview)
            hsb_text = ttk.Scrollbar(text_container, orient="horizontal", command=text_widget.xview)
            text_widget.configure(yscrollcommand=vsb_text.set, xscrollcommand=hsb_text.set)

            vsb_text.pack(side=tk.RIGHT, fill=tk.Y)
            hsb_text.pack(side=tk.BOTTOM, fill=tk.X)
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            for ingredient, qty in total_taken.items():
                text_widget.insert(tk.END, f"{ingredient:<20} {qty:>10}\n")  # Better alignment

            text_widget.config(state=tk.DISABLED)

            max_ingredient = total_taken.idxmax()
            max_qty = total_taken.max()
            min_ingredient = total_taken.idxmin()
            min_qty = total_taken.min()

            summary_frame = ttk.Frame(dist_frame)
            summary_frame.pack(fill=tk.X, pady=(10, 5))

            ttk.Label(
                summary_frame,
                text=f"Most Taken: {max_ingredient} ({max_qty})",
                font=('Helvetica', 10, 'bold'),
            ).pack(anchor='w')

            ttk.Label(
                summary_frame,
                text=f"Least Taken: {min_ingredient} ({min_qty})",
                font=('Helvetica', 10, 'bold'),
            ).pack(anchor='w')

            # ---- Table: Centered below the content ----
            table_container = ttk.Frame(scrollable_frame)
            table_container.pack(fill=tk.BOTH, expand=True, pady=(20, 10))

            # Add a label above the table
            ttk.Label(table_container,
                      text="Full Ingredient Usage History",
                      font=('Helvetica', 10, 'bold')).pack(pady=(10, 5))

            # Create Treeview with its own frame for scrollbars
            table_frame = ttk.Frame(table_container)
            table_frame.pack(fill=tk.BOTH, expand=True)

            # Create Treeview with adjusted height
            tree = ttk.Treeview(table_frame, columns=list(df.columns), show='headings', height=8)

            # Define column headers
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, anchor=tk.CENTER, width=100)  # Set minimum width

            # Insert rows into Treeview
            for _, row in df.iterrows():
                tree.insert("", tk.END, values=list(row))

            # Scrollbars for the Treeview
            vsb_tree = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
            hsb_tree = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=vsb_tree.set, xscrollcommand=hsb_tree.set)

            # Grid layout for better control
            tree.grid(row=0, column=0, sticky="nsew")
            vsb_tree.grid(row=0, column=1, sticky="ns")
            hsb_tree.grid(row=1, column=0, sticky="ew")
            table_frame.grid_rowconfigure(0, weight=1)
            table_frame.grid_columnconfigure(0, weight=1)

            # In on_configure
            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(window_id, width=canvas.winfo_width())

            scrollable_frame.bind("<Configure>", on_configure)

            # Mousewheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def bind_mousewheel(widget):
                widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
                widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

            bind_mousewheel(scrollable_frame)
            bind_mousewheel(canvas_pie.get_tk_widget())

        except FileNotFoundError:
            ttk.Label(scrollable_frame, text="Error: File 'ingredient_used.csv' not found.").pack(pady=10)
        except Exception as e:
            ttk.Label(scrollable_frame, text=f"Error: {str(e)}").pack(pady=10)

    def create_total_time_per_dish_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Time per Dish')

        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)

        main_frame = ttk.Frame(tab)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(main_frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = ttk.Frame(canvas)
        window_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")

        ttk.Label(content_frame,
                  text="Dish Preparation Time Analysis",
                  font=("Arial", 16, "bold")).pack(pady=20)

        try:
            df = pd.read_csv("total_time_per_dish.csv")

            if df.empty:
                ttk.Label(content_frame, text="No preparation time data available").pack()
                return

            # ---------- CALCULATE STATISTICS ----------
            stats = df.groupby('dish_type')['preparation_time_seconds'].agg(
                ['count', 'mean', 'median', 'min', 'max', 'std']
            ).reset_index()

            stats.columns = [
                'Dish Type', 'Count', 'Mean (s)', 'Median (s)',
                'Min (s)', 'Max (s)', 'Std Dev'
            ]

            stats['Mean (s)'] = stats['Mean (s)'].round(1)
            stats['Median (s)'] = stats['Median (s)'].round(1)
            stats['Std Dev'] = stats['Std Dev'].round(1)

            # ---------- CREATE BOX PLOT ----------
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.boxplot(data=df, x='dish_type', y='preparation_time_seconds',
                        ax=ax, palette="husl")
            ax.set_title('Preparation Time Range by Dish Type')
            ax.set_xlabel('')
            ax.set_ylabel('Time (seconds)')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            ax.grid(True, alpha=0.3)
            fig.tight_layout()

            # ========== Plot + Summary Table in One Horizontal Frame ==========
            viz_summary_frame = ttk.Frame(content_frame)
            viz_summary_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 10))

            # Left: Boxplot
            plot_canvas = FigureCanvasTkAgg(fig, master=viz_summary_frame)
            plot_canvas.draw()
            plot_widget = plot_canvas.get_tk_widget()
            plot_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Right: Summary Table
            summary_table_frame = ttk.Frame(viz_summary_frame)
            summary_table_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0))

            summary_table = ttk.Treeview(summary_table_frame, show='headings', height=4)
            summary_table['columns'] = ['Metric', 'Value']

            for col in ['Metric', 'Value']:
                summary_table.heading(col, text=col)
                summary_table.column(col, anchor=tk.CENTER, width=150)

            fastest_dish = stats.loc[stats['Mean (s)'].idxmin()]
            slowest_dish = stats.loc[stats['Mean (s)'].idxmax()]
            total_dishes = stats['Count'].sum()

            summary_table.insert('', 'end',
                                 values=["Fastest Dish", f"{fastest_dish['Dish Type']} ({fastest_dish['Mean (s)']}s)"])
            summary_table.insert('', 'end',
                                 values=["Slowest Dish", f"{slowest_dish['Dish Type']} ({slowest_dish['Mean (s)']}s)"])
            summary_table.insert('', 'end', values=["Total Dishes Prepared", total_dishes])

            summary_table.pack()

            # ========== STATISTICS TABLE SECTION ==========
            stats_frame = ttk.Frame(content_frame)
            stats_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

            table = ttk.Treeview(stats_frame)
            table['columns'] = list(stats.columns)
            table.column("#0", width=0, stretch=tk.NO)

            for col in stats.columns:
                table.column(col, anchor=tk.CENTER, width=100)
                table.heading(col, text=col, anchor=tk.CENTER)

            for _, row in stats.iterrows():
                table.insert("", tk.END, values=list(row))

            vsb = ttk.Scrollbar(stats_frame, orient="vertical", command=table.yview)
            hsb = ttk.Scrollbar(stats_frame, orient="horizontal", command=table.xview)
            table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

            table.grid(row=0, column=0, sticky="nsew")
            vsb.grid(row=0, column=1, sticky="ns")
            hsb.grid(row=1, column=0, sticky="ew")
            stats_frame.grid_rowconfigure(0, weight=1)
            stats_frame.grid_columnconfigure(0, weight=1)

            # Update scroll region
            def on_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(window_id, width=canvas.winfo_width())

            content_frame.bind("<Configure>", on_configure)

            # Mousewheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        except Exception as e:
            ttk.Label(content_frame, text=f"Error loading data: {str(e)}").pack()


if __name__ == "__main__":
    StatsWindow()
