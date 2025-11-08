import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Lab3App:
    def __init__(self, root):
        self.root = root
        self.root.title("Введення даних у таблиці")
        
        # ===== ПЕРША ТАБЛИЦЯ (3x2) =====
        self.row_labels_1 = [
            "n,\nкількість елементів системи;",
            "m,\nкратність резервування",
            "t,\nчас роботи системи"
        ]
        tk.Label(root, text="Таблиця 1", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=5)
        
        self.entries_1st = {}
        for i, row_label in enumerate(self.row_labels_1):
            tk.Label(root, text=row_label, width=25, relief="ridge").grid(row=i+1, column=0, padx=1, pady=1)
            e = tk.Entry(root, width=15)
            e.grid(row=i+1, column=1, padx=1, pady=1)
            self.entries_1st[i] = e
        
        # ===== ДРУГА ТАБЛИЦЯ (1x8) =====
        self.row_labels_2 = ["λ * 10^-3, год^-1"]
        self.col_labels_2 = [str(i) for i in range(1, 9)]
        
        tk.Label(root, text="Таблиця 2", font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=9, pady=5)
        
        tk.Label(root, text="Номер елемента", width=15, relief="ridge").grid(row=6, column=0)
        for j, label in enumerate(self.col_labels_2):
            tk.Label(root, text=label, width=12, relief="ridge").grid(row=6, column=j+1, padx=1, pady=1)
        
        self.entries_2nd = []
        for i, row_label in enumerate(self.row_labels_2):
            tk.Label(root, text=row_label, width=15, relief="ridge").grid(row=7+i, column=0, padx=1, pady=1)
            row_entries = []
            for j in range(8):
                e = tk.Entry(root, width=12)
                e.grid(row=7+i, column=j+1, padx=1, pady=1)
                row_entries.append(e)
            self.entries_2nd.append(row_entries)
            
        # ===== КНОПКА =====
        button = tk.Button(root, text="Обчислити", command=self.get_data)
        button.grid(row=11, column=0, columnspan=9, pady=10)
        
        # ===== Віджет для P(T) =====
        tk.Label(root, text="P(t) для введеного t:", font=("Arial", 10, "bold")).grid(row=12, column=0, padx=5)
        self.entry_Pt = tk.Entry(root, width=15)
        self.entry_Pt.grid(row=12, column=1, padx=5)
        
        # ===== ПРОКРУЧУВАНИЙ ФРЕЙМ ДЛЯ ГРАФІКІВ =====
        container = tk.Frame(root)
        container.grid(row=13, column=0, columnspan=9, sticky="nsew", pady=10)

        # Створюємо Canvas (для скролу) і Scrollbar
        self.canvas_frame = tk.Canvas(container, height=400)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas_frame.yview)
        self.scrollable_frame = tk.Frame(self.canvas_frame)

        # Прив’язка фрейму до Canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_frame.configure(scrollregion=self.canvas_frame.bbox("all"))
        )

        self.canvas_frame.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_frame.configure(yscrollcommand=scrollbar.set)

        # Розташування
        self.canvas_frame.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ===== ЗБІР ДАНИХ =====
    def get_data(self):
        data1 = []
        for i in range(3):
            value = self.entries_1st[i].get()
            try:
                data1.append(int(value))
            except ValueError:
                data1.append(None)
        
        data2 = []
        for i in range(1):
            row_data = []
            for j in range(8):
                value = self.entries_2nd[i][j].get()
                try:
                    row_data.append(float(value))
                except ValueError:
                    row_data.append(None)
            data2.append(row_data)
            
        self.data1 = data1
        self.data2 = data2
        
        self.calc = Calulations(data1, data2)
        first_avg_time = self.calc.first_type_avg_time()
        second_avg_time = self.calc.second_type_avg_time()
        third_avg_time = self.calc.third_type_avg_time()
        fourth_avg_time = self.calc.fourth_type_avg_time()
        
        f1 = self.calc.first_type_probability_func()
        f2 = self.calc.second_type_probability_func()
        f3 = self.calc.third_type_probability_func()
        f4 = self.calc.fourth_type_probability_func()

        # Побудова графіка одразу для кількох функцій
        self.plot_function([f1, f2, f3, f4])
        
        messagebox.showinfo("Введені дані", f"Перша таблиця: {data1}\nДруга таблиця: {data2}")
        messagebox.showinfo("Середній час безвідмовної роботи", f"Середній час: \nПерший тип резервування: {first_avg_time:.1f} годин"
                            f"\nДругий тип резервування: {second_avg_time:.4f} годин"
                            f"\nТретій тип резервування: {third_avg_time:.4f} годин"
                            f"\n Четвертий тип резервування: {fourth_avg_time:.4f}")

    # ===== ПОБУДОВА ГРАФІКА =====
    def plot_function(self, functions):
        """
        Приймає список до 4 функцій [f1, f2, f3, f4]
        і будує всі на одному графіку.
        """
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(pady=10)

        # Фільтруємо тільки ті, що існують
        valid_functions = [f for f in functions if callable(f)]
        if not valid_functions:
            messagebox.showwarning("Увага", "Немає функцій для побудови графіка.")
            return

        # Вісь часу
        try:
            t_max = float(self.entries_1st[2].get()) if self.entries_1st[2].get() else 10
        except ValueError:
            t_max = 10
        t = np.linspace(0, t_max, 200)

        # Створюємо фігуру
        fig, ax = plt.subplots(figsize=(6, 4))

        # Кольори для графіків
        colors = ["blue", "red", "green", "orange"]

        # Побудова всіх доступних функцій
        for idx, f in enumerate(valid_functions):
            try:
                y = np.array([f(tt) for tt in t], dtype=float)
                ax.plot(t, y, label=f"P{idx+1}(t)", color=colors[idx % len(colors)])
            except Exception as e:
                print(f"Помилка у функції {idx+1}: {e}")

        ax.set_title("Графіки імовірності безвідмовної роботи системи")
        ax.set_xlabel("t, години")
        ax.set_ylabel("P(t)")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


class Calulations:
    def __init__(self, data1: list, data2: list):
        self.data1 = data1
        self.data2 = data2
        
        self.i_lambda = sum(self.data2[0]) * pow(10, -3)
    
    def first_type_avg_time(self): # Загальне резервування з постійно включеним резервом
        avg_time = (1 * sum(1 / i for i in range(1, self.data1[0] + 1))) / self.i_lambda
        return avg_time
    
    def first_type_probability_func(self):
        def f(t):
            return (1 - (1 - math.exp(-1 * self.i_lambda * t)))
        return f
      
    def second_type_avg_time(self): # Роздільне резервування з постійно включеним резервом
      m = self.data1[1]
      n = self.data1[0]
      
      total = 0
      for i in range(0, m + 1):
          prod_results = []
          for k in range(0, n + 2):
              prod = (i + 1) / (m + 1) + k
              prod_results.append(prod)
          
          total += 1 / math.prod(prod_results)
      
      total2 = (1 * math.factorial(n - 1)) / (self.i_lambda * math.factorial(m + 1))
      return total * total2
  
    def second_type_probability_func(self):
        m = self.data1[1]
        n = self.data1[0]
        def f(t):
            result = math.pow((1 - (1 - math.exp(-1 * self.i_lambda * t))), (m + 1) * n)
            return result
        return f
    
    def third_type_avg_time(self):
        m = self.data1[1]
        return 1 * (m + 1) / self.i_lambda
    
    def third_type_probability_func(self):
        m = self.data1[1]
        def f(t):
            result = math.exp(-1 * self.i_lambda * t) * sum((pow(self.i_lambda * t, i) / math.factorial(i)) for i in range(0, m + 1))
            return result
        return f
    
    def fourth_type_avg_time(self):
        m = self.data1[1]
        n = self.data1[0]
        return (1 * (m + 1)) / (self.i_lambda * (n - m))
    
    def fourth_type_probability_func(self):
        m = self.data1[1]
        n = self.data1[0]
        def f(t):
            result = sum(pow(self.i_lambda * t * (n - m), i) / math.factorial(i) for i in range(0, m + 1)) * math.exp(-1 * self.i_lambda * t * (n-m))
            return result
        return f
        

# ===== Головна програма =====
if __name__ == "__main__":
    root = tk.Tk()
    app = Lab3App(root)
    root.mainloop()
