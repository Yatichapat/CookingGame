import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


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

        label = ttk.Label(tab, text="Overall Statistics", font=self.font_topic)
        label.pack(pady=20)

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
        tab_control.add(tab, text='Order')

        label = ttk.Label(tab, text="Player Performance Statistics", font=self.font_topic)
        label.pack(pady=20)

        # Load CSV
        df = pd.read_csv('order_per_session.csv', skipinitialspace=True, on_bad_lines='skip')

        # Sum total orders for each dish
        dish_columns = ['sandwich', 'egg fried', 'chicken fried', 'lamb fried']
        order_counts = df[dish_columns].sum()

        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(order_counts.index, order_counts.values, color='lightgreen', edgecolor='black')

        ax.set_title('Total Orders per Dish')
        ax.set_xlabel('Dish')
        ax.set_ylabel('Total Ordered')

        # Show on Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def create_mistake_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Settings')

        label = ttk.Label(tab, text="Settings & Filters", font=self.font_topic)
        label.pack(pady=20)

    def create_ingredients_used_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Ingredients Used')

        label = ttk.Label(tab, text="Ingredients Used Statistics", font=self.font_topic)
        label.pack(pady=20)

    def create_total_time_per_dish_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Total Time per Dish')

        label = ttk.Label(tab, text="Total Time per Dish Statistics", font=self.font_topic)
        label.pack(pady=20)



if __name__ == "__main__":
    StatsWindow()
