import random
import string
import json
import os
from tkinter import *
from tkinter import ttk, messagebox

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Файл истории
        self.history_file = "history.json"
        self.history = self.load_history()
        
        # Переменные
        self.password_length = IntVar(value=12)
        self.use_digits = BooleanVar(value=True)
        self.use_letters = BooleanVar(value=True)
        self.use_symbols = BooleanVar(value=False)
        
        self.create_widgets()
        self.update_history_table()
    
    def create_widgets(self):
        # Рамка настроек
        settings_frame = LabelFrame(self.root, text="Настройки пароля", padx=10, pady=10)
        settings_frame.pack(pady=10, padx=10, fill="x")
        
        # Ползунок длины
        Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
        self.length_scale = Scale(settings_frame, from_=4, to=32, orient=HORIZONTAL,
                                  variable=self.password_length, length=300)
        self.length_scale.grid(row=0, column=1, padx=10)
        self.length_label = Label(settings_frame, text="12")
        self.length_label.grid(row=0, column=2)
        self.length_scale.config(command=lambda x: self.length_label.config(text=str(int(float(x)))))
        
        # Чекбоксы
        Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky="w")
        Checkbutton(settings_frame, text="Буквы (A-Z, a-z)", variable=self.use_letters).grid(row=2, column=0, sticky="w")
        Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&* etc)", variable=self.use_symbols).grid(row=3, column=0, sticky="w")
        
        # Кнопка генерации
        Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password,
               bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=3, pady=10)
        
        # Поле для отображения пароля
        self.password_var = StringVar()
        password_frame = LabelFrame(self.root, text="Сгенерированный пароль", padx=10, pady=10)
        password_frame.pack(pady=10, padx=10, fill="x")
        
        self.password_entry = Entry(password_frame, textvariable=self.password_var, font=("Courier", 12),
                                    state="readonly", readonlybackground="white")
        self.password_entry.pack(side=LEFT, fill="x", expand=True)
        
        Button(password_frame, text="Копировать", command=self.copy_to_clipboard,
               bg="#2196F3", fg="white").pack(side=RIGHT, padx=5)
        
        # Таблица истории
        history_frame = LabelFrame(self.root, text="История паролей", padx=10, pady=10)
        history_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        columns = ("#", "Пароль", "Длина", "Цифры", "Буквы", "Спецсимволы", "Дата")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
        
        # Настройка колонок
        self.tree.heading("#", text="#")
        self.tree.heading("Пароль", text="Пароль")
        self.tree.heading("Длина", text="Длина")
        self.tree.heading("Цифры", text="Цифры")
        self.tree.heading("Буквы", text="Буквы")
        self.tree.heading("Спецсимволы", text="Спецсимволы")
        self.tree.heading("Дата", text="Дата")
        
        self.tree.column("#", width=30)
        self.tree.column("Пароль", width=180)
        self.tree.column("Длина", width=50)
        self.tree.column("Цифры", width=60)
        self.tree.column("Буквы", width=60)
        self.tree.column("Спецсимволы", width=80)
        self.tree.column("Дата", width=120)
        
        scrollbar = Scrollbar(history_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=LEFT, fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill="y")
        
        # Кнопки управления историей
        btn_frame = Frame(self.root)
        btn_frame.pack(pady=5)
        Button(btn_frame, text="Очистить историю", command=self.clear_history,
               bg="#f44336", fg="white").pack(side=LEFT, padx=5)
        Button(btn_frame, text="Сохранить историю", command=self.save_history_to_file,
               bg="#FF9800", fg="white").pack(side=LEFT, padx=5)
    
    def generate_password(self):
        """Генерация пароля на основе выбранных параметров"""
        length = self.password_length.get()
        
        # Проверка корректности длины
        if length < 4:
            messagebox.showerror("Ошибка", "Минимальная длина пароля - 4 символа")
            return
        if length > 32:
            messagebox.showerror("Ошибка", "Максимальная длина пароля - 32 символа")
            return
        
        # Проверка, что выбран хотя бы один тип символов
        if not (self.use_digits.get() or self.use_letters.get() or self.use_symbols.get()):
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
            return
        
        # Формирование набора символов
        characters = ""
        if self.use_digits.get():
            characters += string.digits
        if self.use_letters.get():
            characters += string.ascii_letters
        if self.use_symbols.get():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Генерация пароля
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)
        
        # Сохранение в историю
        from datetime import datetime
        history_entry = {
            "password": password,
            "length": length,
            "digits": self.use_digits.get(),
            "letters": self.use_letters.get(),
            "symbols": self.use_symbols.get(),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(history_entry)
        self.save_history()
        self.update_history_table()
    
    def copy_to_clipboard(self):
        """Копирование пароля в буфер обмена"""
        if self.password_var.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.password_var.get())
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Внимание", "Нет пароля для копирования")
    
    def load_history(self):
        """Загрузка истории из JSON файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Сохранение истории в JSON файл"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)
    
    def save_history_to_file(self):
        """Принудительное сохранение истории (уже автосохраняется)"""
        self.save_history()
        messagebox.showinfo("Успех", "История сохранена в файл")
    
    def update_history_table(self):
        """Обновление таблицы истории"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление записей
        for idx, entry in enumerate(self.history, 1):
            self.tree.insert("", "end", values=(
                idx,
                entry["password"],
                entry["length"],
                "Да" if entry["digits"] else "Нет",
                "Да" if entry["letters"] else "Нет",
                "Да" if entry["symbols"] else "Нет",
                entry["date"]
            ))
    
    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_table()
            messagebox.showinfo("Успех", "История очищена")

if __name__ == "__main__":
    root = Tk()
    app = PasswordGenerator(root)
    root.mainloop()
