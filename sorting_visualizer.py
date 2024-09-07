import matplotlib.pyplot as plt
import numpy as np
import time
import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox

# Sorting algorithms
def bubble_sort(arr, draw_array, delay):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
            draw_array(arr, iteration=f'Iteration {i*n + j}')
            time.sleep(delay)

def insertion_sort(arr, draw_array, delay):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        draw_array(arr, iteration=f'Iteration {i}')
        time.sleep(delay)

def selection_sort(arr, draw_array, delay):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_array(arr, iteration=f'Iteration {i}')
        time.sleep(delay)

def merge_sort(arr, draw_array, delay):
    def merge_sort_recursive(arr, draw_array, delay):
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]
            merge_sort_recursive(L, draw_array, delay)
            merge_sort_recursive(R, draw_array, delay)
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
            draw_array(arr)
            time.sleep(delay)
    merge_sort_recursive(arr, draw_array, delay)

def quick_sort(arr, low, high, draw_array, delay):
    if low < high:
        pi = partition(arr, low, high, draw_array, delay)
        quick_sort(arr, low, pi - 1, draw_array, delay)
        quick_sort(arr, pi + 1, high, draw_array, delay)

def partition(arr, low, high, draw_array, delay):
    i = low - 1
    pivot = arr[high]
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        draw_array(arr, iteration=f'Partitioning: Pivot={pivot}')
        time.sleep(delay)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_array(arr, iteration=f'Pivot={pivot} Positioned')
    time.sleep(delay)
    return i + 1

# Visualization function
def draw_array(arr, color='blue', font_size=12, background_color='white', iteration=''):
    plt.clf()
    bars = plt.bar(range(len(arr)), arr, color=color)
    plt.xticks(range(len(arr)), [str(x) for x in arr], rotation=90, fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.title('Sorting Visualization', fontsize=font_size)
    plt.xlabel('Index', fontsize=font_size)
    plt.ylabel('Value', fontsize=font_size)
    plt.gca().set_facecolor(background_color)
    if iteration:
        plt.text(0.5, 1.05, iteration, transform=plt.gca().transAxes, ha='center', fontsize=font_size, color='black')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{height}', ha='center', va='bottom', fontsize=font_size, color='black')
    plt.pause(0.1)

def update_delay(val):
    global delay
    delay = float(val)

def main():
    global delay
    delay = 1.0  # Default delay

    root = tk.Tk()
    root.withdraw()

    # Get user inputs
    arr = list(map(int, simpledialog.askstring("Input", "Enter array elements separated by commas:").split(',')))
    font_size = int(simpledialog.askstring("Input", "Enter font size for labels:"))
    background_color = colorchooser.askcolor(title="Choose Background Color")[1]

    # Create a window for the speed slider
    slider_window = tk.Toplevel(root)
    slider_window.title("Speed Adjustment")

    tk.Label(slider_window, text="Adjust Delay (seconds):").pack()
    delay_slider = tk.Scale(slider_window, from_=0.1, to=2.0, resolution=0.1, orient='horizontal', command=update_delay)
    delay_slider.set(delay)
    delay_slider.pack()

    # Choose sorting algorithm
    algo_name = simpledialog.askstring("Input", "Enter sorting algorithm (Bubble, Insertion, Selection, Merge, Quick):").capitalize()

    algorithms = {
        'Bubble': bubble_sort,
        'Insertion': insertion_sort,
        'Selection': selection_sort,
        'Merge': merge_sort,
        'Quick': lambda arr, draw_array, delay: quick_sort(arr, 0, len(arr) - 1, draw_array, delay)
    }

    if algo_name in algorithms:
        plt.figure(figsize=(10, 6))
        draw_array(arr, font_size=font_size, background_color=background_color)
        plt.title(f'{algo_name} Sort Visualization')
        algo_func = algorithms[algo_name]
        algo_func(arr, lambda arr, iteration=None: draw_array(arr, font_size=font_size, background_color=background_color, iteration=iteration), delay)
        plt.show(block=False)
        plt.pause(60)  # Pause to allow viewing of the plot
        plt.close('all')  # Close the current figure
    else:
        messagebox.showerror("Error", "Invalid sorting algorithm selected.")

    slider_window.mainloop()

if __name__ == "__main__":
    main()
