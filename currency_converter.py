import tkinter as tk
from tkinter import ttk, scrolledtext
import requests

# Formal Theme settings
LIGHT_THEME = {
    "bg": "#f5f7fa",          # very light gray-blue background
    "fg": "#1a1a1a",          # almost black text
    "entry_bg": "#ffffff",    # white entry backgrounds
    "button_bg": "#3b5998"    # formal navy blue buttons
}
DARK_THEME = {
    "bg": "#1f2937",          # dark slate gray background
    "fg": "#e4e6eb",          # very light gray text
    "entry_bg": "#374151",    # dark gray entry backgrounds
    "button_bg": "#2563eb"    # bright blue buttons for contrast
}
theme = LIGHT_THEME

def apply_theme():
    root.configure(bg=theme["bg"])
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, ttk.Combobox)):
            widget.configure(background=theme["bg"], foreground=theme["fg"])
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=theme["entry_bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Button):
            widget.configure(bg=theme["button_bg"], fg="white", activebackground=theme["entry_bg"])
    history_text.configure(bg=theme["entry_bg"], fg=theme["fg"])

def toggle_theme():
    global theme
    theme = DARK_THEME if theme == LIGHT_THEME else LIGHT_THEME
    apply_theme()

def fetch_currency_list():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    return list(data['rates'].keys())

def fetch_conversion_rate(from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    return data['rates'].get(to_currency, None)

def convert():
    try:
        amount = float(entry_amount.get())
        from_curr = combo_from.get()
        to_curr = combo_to.get()

        rate = fetch_conversion_rate(from_curr, to_curr)

        if rate is None:
            label_result.config(text="Currency not supported.")
            return

        result = amount * rate
        output = f"{amount:.2f} {from_curr} = {result:.2f} {to_curr}"
        label_result.config(text=output)
        history_text.insert(tk.END, output + "\n")
        history_text.yview(tk.END)
    except ValueError:
        label_result.config(text="Please enter a valid amount.")
    except:
        label_result.config(text="Error. Check internet or inputs.")

root = tk.Tk()
root.title("Advanced Currency Converter")
root.geometry("450x500")

# Currency list
currency_list = fetch_currency_list()

# Amount input
tk.Label(root, text="Amount:").pack(pady=5)
entry_amount = tk.Entry(root, font=("Arial", 12))
entry_amount.pack(pady=5)

# Currency dropdowns
tk.Label(root, text="From:").pack()
combo_from = ttk.Combobox(root, values=currency_list, state="readonly")
combo_from.set("USD")
combo_from.pack(pady=5)

tk.Label(root, text="To:").pack()
combo_to = ttk.Combobox(root, values=currency_list, state="readonly")
combo_to.set("INR")
combo_to.pack(pady=5)

# Convert button
tk.Button(root, text="Convert", command=convert, font=("Arial", 12)).pack(pady=10)

# Result label
label_result = tk.Label(root, text="Converted Amount: ", font=("Arial", 12))
label_result.pack(pady=10)

# History box
tk.Label(root, text="Conversion History:").pack()
history_text = scrolledtext.ScrolledText(root, height=8, width=50)
history_text.pack(pady=5)

# Dark mode toggle
tk.Button(root, text="Toggle Dark Mode", command=toggle_theme).pack(pady=10)

apply_theme()
root.mainloop()