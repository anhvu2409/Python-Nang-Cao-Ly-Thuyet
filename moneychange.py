import tkinter as tk
from tkinter import messagebox

# Lớp CurrencyConverterApp quản lý giao diện và các chức năng chuyển đổi
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Chuyển Đổi Tiền Tệ")

        # Tỷ giá có thể cập nhật theo nhu cầu
        self.exchange_rates = {
            "USD": 25280,  # 1 USD = 24000 VND
            "EUR": 27475,  # 1 EUR = 28000 VND
            "CHF": 29268   # 1 CHF = 25000 VND
        }

        # Tạo các thành phần giao diện
        self.create_widgets()

    def create_widgets(self):
        # Nhập số tiền và đơn vị
        tk.Label(self.root, text="Số tiền:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_amount = tk.Entry(self.root)
        self.entry_amount.grid(row=0, column=1, padx=10, pady=10)

        # Đơn vị tiền tệ nguồn (đổi từ)
        tk.Label(self.root, text="Đổi từ:").grid(row=1, column=0, padx=10, pady=10)
        self.from_currency = tk.StringVar(self.root)
        self.from_currency.set("VND")  # mặc định là VND
        from_currency_menu = tk.OptionMenu(self.root, self.from_currency, "VND", "USD", "EUR", "CHF")
        from_currency_menu.grid(row=1, column=1, padx=10, pady=10)

        # Đơn vị tiền tệ đích (đổi sang)
        tk.Label(self.root, text="Đổi sang:").grid(row=2, column=0, padx=10, pady=10)
        self.to_currency = tk.StringVar(self.root)
        self.to_currency.set("USD")  # mặc định là USD
        to_currency_menu = tk.OptionMenu(self.root, self.to_currency, "VND", "USD", "EUR", "CHF")
        to_currency_menu.grid(row=2, column=1, padx=10, pady=10)

        # Nút chuyển đổi
        convert_button = tk.Button(self.root, text="Chuyển Đổi", command=self.convert)
        convert_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Hiển thị kết quả
        tk.Label(self.root, text="Kết quả:").grid(row=4, column=0, padx=10, pady=10)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.grid(row=4, column=1, padx=10, pady=10)

    def convert(self):
        try:
            amount = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số tiền hợp lệ!")
            return

        from_currency = self.from_currency.get()
        to_currency = self.to_currency.get()

        # Nếu hai loại tiền giống nhau
        if from_currency == to_currency:
            self.result_label.config(text=f"{amount:,.2f} {to_currency}")
            return

        # Đổi từ VND sang ngoại tệ
        if from_currency == "VND":
            rate = self.exchange_rates.get(to_currency)
            if rate:
                result = amount / rate
                self.result_label.config(text=f"{result:,.2f} {to_currency}")
            else:
                messagebox.showerror("Lỗi", f"Tỷ giá không khả dụng cho {to_currency}")
        
        # Đổi từ ngoại tệ sang VND
        elif to_currency == "VND":
            rate = self.exchange_rates.get(from_currency)
            if rate:
                result = amount * rate
                self.result_label.config(text=f"{result:,.2f} {to_currency}")
            else:
                messagebox.showerror("Lỗi", f"Tỷ giá không khả dụng cho {from_currency}")

        # Đổi từ một ngoại tệ sang một ngoại tệ khác
        else:
            from_rate = self.exchange_rates.get(from_currency)
            to_rate = self.exchange_rates.get(to_currency)
            if from_rate and to_rate:
                vnd_amount = amount * from_rate
                result = vnd_amount / to_rate
                self.result_label.config(text=f"{result:,.2f} {to_currency}")
            else:
                messagebox.showerror("Lỗi", f"Tỷ giá không khả dụng cho {from_currency} hoặc {to_currency}")

# Chạy ứng dụng
root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()
