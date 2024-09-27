import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

def step_by_step_solution(func, x):
    solution_steps = []
    
    simplified_func = sp.simplify(func)
    solution_steps.append(f"Упрощенная функция: {simplified_func}")
    
    derivative_func = sp.diff(func, x)
    solution_steps.append(f"Производная функции: {derivative_func}")
    
    critical_points = sp.solveset(derivative_func, x, domain=sp.S.Reals)
    solution_steps.append(f"Критические точки (экстремумы): {critical_points}")
    
    for point in critical_points:
        if point.is_real:
            value_at_point = func.subs(x, point)
            solution_steps.append(f"Значение функции в точке x = {point}: {value_at_point}")
    
    return simplified_func, derivative_func, critical_points, solution_steps

def plot_function(func, x, critical_points):
    fig, ax = plt.subplots(figsize=(5, 4))
    
    x_vals = np.linspace(-10, 10, 400)
    
    func_lambda = sp.lambdify(x, func, "numpy")
    
    y_vals = func_lambda(x_vals)
    
    ax.plot(x_vals, y_vals, label=str(func))
    
    for point in critical_points:
        if point.is_real:
            ax.scatter(float(point), float(func.subs(x, point)), color='red')
            ax.text(float(point), float(func.subs(x, point)), f'({point},{float(func.subs(x, point))})', color='red')
    
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.set_title("График функции")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True)
    
    return fig

def calculate():
    try:
        func_str = entry.get()
        x = sp.Symbol('x')
        func = sp.sympify(func_str)
        
        simplified_func, derivative_func, critical_points, solution_steps = step_by_step_solution(func, x)
        
        solution_text.delete(1.0, tk.END)
        for step in solution_steps:
            solution_text.insert(tk.END, step + "\n")
        
        fig = plot_function(func, x, critical_points)
        
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    except Exception as e:
        messagebox.showerror("Ошибка", "Неверный ввод функции")

root = tk.Tk()
root.title("Калькулятор графиков функций")

frame_input = tk.Frame(root)
frame_input.pack(pady=10)

label = tk.Label(frame_input, text="Введите функцию:")
label.pack(side=tk.LEFT)

entry = tk.Entry(frame_input, width=40)
entry.pack(side=tk.LEFT)

button = tk.Button(frame_input, text="Рассчитать", command=calculate)
button.pack(side=tk.LEFT, padx=5)

frame_solution = tk.Frame(root)
frame_solution.pack(pady=10)

solution_label = tk.Label(frame_solution, text="Пошаговое решение:")
solution_label.pack()

solution_text = tk.Text(frame_solution, height=10, width=60)
solution_text.pack()

frame_graph = tk.Frame(root)
frame_graph.pack(pady=10)

root.mainloop()
