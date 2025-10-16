import tkinter as tk
from tkinter import messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Введення даних у таблиці")
        
        # ===== ПЕРША ТАБЛИЦЯ (3x2) =====
        self.row_labels_1 = [
            "n,\nкількість елементів системи;",
            "Tn - загальний час роботи системи;",
            "Rd - допустимий ризик;",
        ]
        tk.Label(root, text="Таблиця 1", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=3, pady=5)
        
        self.entries_1st = {}
        for i, row_label in enumerate(self.row_labels_1):
            tk.Label(root, text=row_label, width=25, relief="ridge").grid(row=i+1, column=0, padx=1, pady=1)
            e = tk.Entry(root, width=15)
            e.grid(row=i+1, column=1, padx=1, pady=1)
            self.entries_1st[i] = e
        
        # ===== ДРУГА ТАБЛИЦЯ (3x8) =====
        self.row_labels_2 = [
            "λ * 10^-4, год^-1",
            "μ * 10^-1, год^-1",
            "r, ум.один.",
        ]
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
        
        # ===== Віджет для f(T) =====
        tk.Label(root, text="f(T) для введеного T:", font=("Arial", 10, "bold")).grid(row=12, column=0, padx=5)
        self.entry_fT = tk.Entry(root, width=15)
        self.entry_fT.grid(row=12, column=1, padx=5)
        
        # ===== Місце для графіка =====
        self.canvas = None
    
    def get_data(self):
        # ===== Зчитування даних =====
        # Перша таблиця
        data1 = []
        for i in range(3):
            value = self.entries_1st[i].get()
            try:
                data1.append(float(value))
            except ValueError:
                data1.append(None)
        
        # Друга таблиця
        data2 = []
        for i in range(3):
            row_data = []
            for j in range(8):
                value = self.entries_2nd[i][j].get()
                try:
                    row_data.append(float(value))
                except ValueError:
                    row_data.append(None)
            data2.append(row_data)
        
        # ===== Обчислення =====
        self.data1 = data1
        self.data2 = data2
        
        self.calc = Calulations(data1, data2)
        avg_time = self.calc.avg_time()
        coefficient_sys_readiness = self.calc.coefficient_sys_readiness()
        func, formula_str = self.calc.func_coefficient_sys_readiness()
        sys_risk = self.calc.sys_risk()
        
        messagebox.showinfo("Введені дані", f"Перша таблиця: {data1}\nДруга таблиця: {data2}")
        messagebox.showinfo("Результати", f"T - середнє напрацювання до відмови: {avg_time:.1f} годин"
                            f"\nK - коефіцієнт готовності системи: {coefficient_sys_readiness:.2f}"
                            f"\nK - функція готовності системи: {formula_str}"
                            f"\nR - технічний ризик системи: {sys_risk}"
                            )
        
        # ===== Відобразити f(T) =====
        try:
            T_value = float(self.entries_1st[1].get())
            fT = func(T_value)
            self.entry_fT.delete(0, tk.END)
            self.entry_fT.insert(0, f"{fT:.4f}")
        except (ValueError, TypeError):
            self.entry_fT.delete(0, tk.END)
            self.entry_fT.insert(0, "Помилка")
        
        # ===== Побудова графіка =====
        self.plot_function(func)
    
    def plot_function(self, f):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        t_max = float(self.entries_1st[1].get()) if self.entries_1st[1].get() else 10
        t = np.linspace(0, t_max, 100)
        y = np.array([f(tt) for tt in t], dtype=float)
        
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(t, y, label='K(t)')
        ax.set_title("Графік готовності системи")
        ax.set_xlabel("t, години")
        ax.set_ylabel("K(t)")
        ax.grid(True)
        ax.legend()
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=13, column=0, columnspan=9, pady=10)


class Calulations:
    def __init__(self, data1: list, data2: list):
        self.data1 = data1
        self.data2 = data2
    
    def avg_time(self):
        result = pow(self.data1[0], 4) / sum(self.data2[0])
        return result
    
    def coefficient_sys_readiness(self):
        sum_lambda_mu = sum(x / y for x, y in zip(self.data2[0], self.data2[1]))
        self.sum_lambda_mu = sum_lambda_mu
        result = 1 / (sum_lambda_mu + 1)
        return result
    
    def func_coefficient_sys_readiness(self):
        if not hasattr(self, "sum_lambda_mu"):
            self.coefficient_sys_readiness()
        
        lambda_c = sum(self.data2[0]) * pow(self.data1[0], -4)
        mu_c = lambda_c / self.sum_lambda_mu
        lam_mu_csum = lambda_c + mu_c
        
        formula_str = f"{(mu_c / lam_mu_csum):.2f} + {(lambda_c / lam_mu_csum):.2f} * e^(-{lam_mu_csum:.6f}t)"
        
        def f(t):
            return (mu_c / lam_mu_csum) + (lambda_c / lam_mu_csum) * math.exp(-t * lam_mu_csum)
        
        return f, formula_str
    
    def sys_risk(self):
        sys_readiness_coeff = self.coefficient_sys_readiness()
        t = self.data1[1]
        lam_r_sum = sum(x * y for x, y in zip(self.data2[0], self.data2[2])) * pow(self.data1[0], -4)
        result = sys_readiness_coeff * t * lam_r_sum + t * lam_r_sum
        
        result = result / 2
        return round(result, 1)


# ===== Головна програма =====
if __name__ == "__main__":
    root = tk.Tk()
    app = TableApp(root)
    root.mainloop()
