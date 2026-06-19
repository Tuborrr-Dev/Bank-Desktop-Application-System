from json import load, dump
import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")  # Set to Dark mode to let your colors pop beautifully

# Choose a Custom Palette Customization with thier Constants
COLOR_TAN = "#ecc19c"
COLOR_TURQUOISE = "#1e847f"
COLOR_BLACK = "#000000"
COLOR_SIDEBAR_BG = "#111111"  # Soft deep charcoal/black variant for layout separation


class Transaction:
    def __init__(self, frm, amount, transaction_type, to):
        self.frm = frm
        self.amount = amount
        self.transaction_type = transaction_type
        self.to = to

    def __str__(self):
        if self.transaction_type == "Transfer Out":
            return f"Sent ₦{self.amount} to {self.to}"

        elif self.transaction_type == "Transfer In":
            return f"Received ₦{self.amount} from {self.to}"

        elif self.transaction_type == "deposit":
            return f"Deposited ₦{self.amount}"

        elif self.transaction_type == "withdrawal":
            return f"Withdrew ₦{self.amount}"


class Bank:
    admin_pass = "admin"

    def __init__(self, bank_name, accounts=None):
        self.bank_name = bank_name
        if accounts == None:
            self.accounts = []
        else:
            self.accounts = accounts

    def add_account(self, account_object):
        if self.find_account(account_object.owner):
            return False
        else:
            self.accounts.append(account_object)
            self.save_accounts()
            return True

    def show_accounts(self):
        print(f"✅ {self.bank_name}")
        for account in self.accounts:
            print(f"- {account}")

    def find_account(self, owner):
        for account in self.accounts:
            if account.owner.lower() == owner.lower():
                return account
        return None

    def deposit_to_account(self, owner_account, amount):
        if amount <= 0:
            return "invalid_amount"
        else:
            account_to_deposit = self.find_account(owner_account)
            if account_to_deposit:
                account_to_deposit.deposit(amount)
                new_trans = Transaction(
                    owner_account, amount, "deposit", self.bank_name
                )
                account_to_deposit.transactions.append(new_trans)
                self.save_accounts()
                return "success"
            else:
                return "not_found"

    def withdraw_from_account(self, owner_account, amount):
        if amount <= 0:
            return "invalid_amount"
        else:
            account_to_withdraw = self.find_account(owner_account)
            if account_to_withdraw:
                if account_to_withdraw.withdraw(amount):
                    new_trans = Transaction(
                        owner_account, amount, "withdrawal", self.bank_name
                    )
                    account_to_withdraw.transactions.append(new_trans)
                    self.save_accounts()
                    return "success"
                else:
                    return "insufficient-funds"
            else:
                return "not_found"

    def transfer_money(self, send_acc, reciever_acc, amount):
        if amount <= 0:
            return "invalid_amount"
        if send_acc.withdraw(amount):
            new_trans1 = Transaction(
                send_acc.owner, amount, "Transfer Out", reciever_acc.owner
            )
            send_acc.transactions.append(new_trans1)
            reciever_acc.deposit(amount)
            new_trans2 = Transaction(
                send_acc.owner, amount, "Transfer In", reciever_acc.owner
            )
            reciever_acc.transactions.append(new_trans2)
            self.save_accounts()
            return "success"
        else:
            return "insufficient_funds"

    def show_transactions(self, acc_object):
        if not acc_object.transactions:
            print(" ❌ No transactions made yet !!!")
        else:
            for transaction in acc_object.transactions:
                print(f"✅ {transaction}")

    def total_bank_balance(self):
        return sum(account.balance for account in self.accounts)

    def save_accounts(self):
        data = []
        for account in self.accounts:
            present_info = {}
            present_info["account_name"] = account.owner
            present_info["balance"] = account.balance
            data_Tx = []
            for transact in account.transactions:
                data_Tx.append(
                    {
                        "from": transact.frm,
                        "transaction_type": transact.transaction_type,
                        "amount": transact.amount,
                        "to": transact.to,
                    }
                )
            present_info["transactions"] = data_Tx
            data.append(present_info)
        with open("accounts.json", "w") as file:
            dump(data, file, indent=4)
        print("Accounts have been saved")

    def load_accounts(self):
        json_dict = []
        account_name = ""
        balance = 0
        json_Tx = {}
        try:
            with open("accounts.json", "r") as file:
                json_dict = load(file)
        except FileNotFoundError:
            print("FileNotFoundError")
        if json_dict:
            for account_info in json_dict:
                json_Tx = account_info.get("transactions", [])
                transaction_objects = []
                for info in json_Tx:
                    frm = info["from"]
                    transaction_type = info["transaction_type"]
                    amount = info["amount"]
                    to = info["to"]
                    transaction_object = Transaction(frm, amount, transaction_type, to)
                    transaction_objects.append(transaction_object)
                account_name = account_info["account_name"]
                balance = account_info["balance"]
                account_object = BankAccount(account_name, balance, transaction_objects)
                self.add_account(account_object)


class BankAccount:
    def __init__(self, owner, balance, transactions=None):
        self.owner = owner
        self.balance = balance
        if transactions == None:
            self.transactions = []
        else:
            self.transactions = transactions

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Balance must be greater than 0.")
        self.__balance = amount

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        if amount > self.balance:
            return False

    def __str__(self):
        return f"{self.owner}: ₦{self.balance}"


# GUI interface created using Ctikinter
class BankGUI(ctk.CTk):
    def __init__(self, bank_system):
        super().__init__()
        self.bank = bank_system
        self.title(f"{self.bank.bank_name} Banking Hub")
        self.geometry("850x550")
        self.configure(fg_color=COLOR_BLACK)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_main_container()
        self.show_dashboard_view()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=220, corner_radius=0, fg_color=COLOR_SIDEBAR_BG
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        label = ctk.CTkLabel(
            self.sidebar,
            text=self.bank.bank_name,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COLOR_TAN,
        )
        label.pack(pady=20, padx=10)

        # Navigation Buttons Styled with the Deep Turquoise
        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            fg_color=COLOR_TURQUOISE,
            hover_color="#155d59",
            text_color="#ffffff",
            command=self.show_dashboard_view,
        ).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(
            self.sidebar,
            text="Open New Account",
            fg_color=COLOR_TURQUOISE,
            hover_color="#155d59",
            text_color="#ffffff",
            command=self.show_create_view,
        ).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(
            self.sidebar,
            text="Deposit / Withdraw",
            fg_color=COLOR_TURQUOISE,
            hover_color="#155d59",
            text_color="#ffffff",
            command=self.show_deposit_withdraw_view,
        ).pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(
            self.sidebar,
            text="Transfer Funds",
            fg_color=COLOR_TURQUOISE,
            hover_color="#155d59",
            text_color="#ffffff",
            command=self.show_transfer_view,
        ).pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            self.sidebar,
            text="── Admin Tools ──",
            font=ctk.CTkFont(size=12),
            text_color=COLOR_TAN,
        ).pack(pady=15)
        # Admin action styled with Tan accent highlighting
        ctk.CTkButton(
            self.sidebar,
            text="Admin Console",
            fg_color=COLOR_TAN,
            hover_color="#cca37e",
            text_color=COLOR_BLACK,
            font=ctk.CTkFont(weight="bold"),
            command=self.show_admin_view,
        ).pack(pady=5, padx=20, fill="x")

    def create_main_container(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_dashboard_view(self):
        self.clear_main_frame()

        lbl = ctk.CTkLabel(
            self.main_frame,
            text="Welcome to the Digital Banking Hub",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLOR_TAN,
        )
        lbl.pack(anchor="w", pady=(0, 20))

        search_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
            border_width=1,
        )
        search_frame.pack(fill="x", pady=10, ipady=10)

        ctk.CTkLabel(
            search_frame,
            text="Quick Account Lookup:",
            font=ctk.CTkFont(weight="bold"),
            text_color=COLOR_TAN,
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(5, 0), sticky="w")
        ctk.CTkLabel(
            search_frame, text="Search Account Name:", text_color="#ffffff"
        ).grid(row=1, column=0, padx=10, pady=10)

        search_entry = ctk.CTkEntry(
            search_frame,
            width=250,
            fg_color=COLOR_BLACK,
            border_color=COLOR_TAN,
            text_color="#ffffff",
        )
        search_entry.grid(row=1, column=1, padx=10, pady=10)

        display_box = ctk.CTkTextbox(
            self.main_frame,
            height=200,
            width=500,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
            border_width=1,
            text_color="#ffffff",
        )

        def do_search():
            search = search_entry.get().strip()
            found = self.bank.find_account(search)
            display_box.delete("1.0", "end")
            if found:
                display_box.insert(
                    "end", f"Account Detail: {found}\n\nRecent Ledger Records:\n"
                )
                if not found.transactions:
                    display_box.insert("end", " ❌ No transactions made yet !!!")
                for transaction in found.transactions:
                    display_box.insert("end", f"✅ {transaction}\n")
            else:
                messagebox.showerror("Error", "❌ Account does not Exist !!!")

        ctk.CTkButton(
            search_frame,
            text="Search",
            fg_color=COLOR_TURQUOISE,
            hover_color="#155d59",
            text_color="#ffffff",
            command=do_search,
        ).grid(row=1, column=2, padx=10, pady=10)
        display_box.pack(fill="both", expand=True, pady=10)

    def show_create_view(self):
        self.clear_main_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="Open a New Bank Account",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TAN,
        ).pack(anchor="w", pady=10)

        ctk.CTkLabel(
            self.main_frame, text="Please enter full name:", text_color="#ffffff"
        ).pack(anchor="w", pady=2)
        name_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
        )
        name_entry.pack(anchor="w", pady=10)

        ctk.CTkLabel(
            self.main_frame, text="Please enter Initial Balance:", text_color="#ffffff"
        ).pack(anchor="w", pady=2)
        bal_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
        )
        bal_entry.pack(anchor="w", pady=10)

        def save_action():
            user_name = name_entry.get().strip().lower()
            if not user_name:
                messagebox.showerror("Error", "❌ Name cannot be blank.")
                return
            try:
                user_init_bal = float(bal_entry.get())
                account = BankAccount(user_name, user_init_bal)
                if self.bank.add_account(account):
                    messagebox.showinfo("Success", "✅ Account Succesfully Created.")
                    self.show_dashboard_view()
                else:
                    messagebox.showerror("Error", "❌ Account already exists")
            except ValueError as e:
                if str(e) == "Balance must be greater than 0.":
                    messagebox.showerror("Error", f"❌ Error: {e}, Please try again")
                else:
                    messagebox.showerror(
                        "Error",
                        "❌ Error: Cannot set Initial balance with Text, please try again with Numbers",
                    )

        ctk.CTkButton(
            self.main_frame,
            text="Create Account",
            fg_color=COLOR_TAN,
            hover_color="#cca37e",
            text_color=COLOR_BLACK,
            font=ctk.CTkFont(weight="bold"),
            command=save_action,
        ).pack(anchor="w", pady=20)

    def show_deposit_withdraw_view(self):
        self.clear_main_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="Deposit / Withdraw Vault",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TAN,
        ).pack(anchor="w", pady=10)

        ctk.CTkLabel(
            self.main_frame, text="Please Enter Name of Account:", text_color="#ffffff"
        ).pack(anchor="w", pady=2)
        name_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
        )
        name_entry.pack(anchor="w", pady=10)

        ctk.CTkLabel(self.main_frame, text="Amount (₦):", text_color="#ffffff").pack(
            anchor="w", pady=2
        )
        amt_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
        )
        amt_entry.pack(anchor="w", pady=10)

        def handle_action(action_type):
            account_name = name_entry.get().strip().lower()
            try:
                amount = float(amt_entry.get())
                if action_type == "deposit":
                    status = self.bank.deposit_to_account(account_name, amount)
                    if status == "invalid_amount":
                        messagebox.showerror(
                            "Error", "❌ Amount must be greater than 0"
                        )
                    elif status == "success":
                        messagebox.showinfo(
                            "Success", f"✅ Deposit of ₦{amount} successfull"
                        )
                        self.show_dashboard_view()
                    elif status == "not_found":
                        messagebox.showerror(
                            "Error", f"❌ Account of {account_name} does not Exist !!!"
                        )
                else:
                    status = self.bank.withdraw_from_account(account_name, amount)
                    if status == "invalid_amount":
                        messagebox.showerror(
                            "Error", "❌ Amount must be greater than 0"
                        )
                    elif status == "success":
                        messagebox.showinfo(
                            "Success", f"✅ Withdrawal of ₦{amount} successfull"
                        )
                        self.show_dashboard_view()
                    elif status == "not_found":
                        messagebox.showerror(
                            "Error", f"❌ Account of {account_name} does not Exist !!!"
                        )
                    elif status == "insufficient-funds":
                        messagebox.showerror(
                            "Error",
                            f"❌ Insuffient Funds in {self.bank.find_account(account_name)}",
                        )
            except ValueError:
                if action_type == "deposit":
                    messagebox.showerror(
                        "Error",
                        "❌ Error: Cannot Deposit with Text, \nplease try again with Numbers",
                    )
                else:
                    messagebox.showerror(
                        "Error",
                        "❌ Error: Cannot Withdraw with Text, \nplease try again with Numbers",
                    )

        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(anchor="w", pady=20)
        ctk.CTkButton(
            btn_frame,
            text="Deposit",
            fg_color=COLOR_TURQUOISE,
            hover_color="#155d59",
            text_color="#ffffff",
            command=lambda: handle_action("deposit"),
        ).grid(row=0, column=0, padx=5)
        ctk.CTkButton(
            btn_frame,
            text="Withdraw",
            fg_color=COLOR_TAN,
            hover_color="#cca37e",
            text_color=COLOR_BLACK,
            font=ctk.CTkFont(weight="bold"),
            command=lambda: handle_action("withdraw"),
        ).grid(row=0, column=1, padx=5)

    def show_transfer_view(self):
        self.clear_main_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="Inter-Account Wire Transfer",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TAN,
        ).pack(anchor="w", pady=10)

        ctk.CTkLabel(
            self.main_frame,
            text="Please Enter Name of Sender Account:",
            text_color="#ffffff",
        ).pack(anchor="w", pady=2)
        sender_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
        )
        sender_entry.pack(anchor="w", pady=10)

        ctk.CTkLabel(
            self.main_frame,
            text="Please Enter Name of Reciever Account:",
            text_color="#ffffff",
        ).pack(anchor="w", pady=2)
        rec_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
        )
        rec_entry.pack(anchor="w", pady=10)

        ctk.CTkLabel(
            self.main_frame, text="Please Enter Amount to send:", text_color="#ffffff"
        ).pack(anchor="w", pady=2)
        amt_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TURQUOISE,
        )
        amt_entry.pack(anchor="w", pady=10)

        def execute_transfer():
            send_name = sender_entry.get().strip().lower()
            send_acc = self.bank.find_account(send_name)
            if send_acc == None:
                messagebox.showerror(
                    "Error", f"❌ Account named {send_name} does not Exist !!!"
                )
                return

            rcv_name = rec_entry.get().strip().lower()
            if send_name == rcv_name:
                messagebox.showerror(
                    "Error", "❌ You cannot transfer money to the same account!"
                )
                return

            rcv_acc = self.bank.find_account(rcv_name)
            if rcv_acc == None:
                messagebox.showerror(
                    "Error", f"❌ Account named {rcv_name} does not Exist !!!"
                )
                return

            try:
                amount = float(amt_entry.get())
                status = self.bank.transfer_money(send_acc, rcv_acc, amount)
                if status == "invalid_amount":
                    messagebox.showerror("Error", "❌ Amount must be greater than 0")
                elif status == "insufficient_funds":
                    messagebox.showerror("Error", f"❌ Insuffient Funds in {send_acc}")
                elif status == "success":
                    messagebox.showinfo(
                        "Success",
                        f"✅ Transfer of {amount} from {send_name} to {rcv_name} is Successfull",
                    )
                    self.show_dashboard_view()
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "❌ Error: Cannot Transfer with Text, \nplease try again with Numbers",
                )

        ctk.CTkButton(
            self.main_frame,
            text="Authorize Transfer",
            fg_color=COLOR_TURQUOISE,
            hover_color="#155d59",
            text_color="#ffffff",
            command=execute_transfer,
        ).pack(anchor="w", pady=20)

    def show_admin_view(self):
        self.clear_main_frame()

        dialog = ctk.CTkInputDialog(
            text="Please Input Admin Pass:", title="Security Check"
        )
        password = dialog.get_input()

        if password != Bank.admin_pass:
            messagebox.showerror(
                "Security Alert", "❌ Wrong-Pass, UnAuthorized !!! calls FBI"
            )
            self.show_dashboard_view()
            return

        ctk.CTkLabel(
            self.main_frame,
            text="Vault Master Console",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLOR_TAN,
        ).pack(anchor="w", pady=10)

        total_bal = self.bank.total_bank_balance()
        ctk.CTkLabel(
            self.main_frame,
            text=f"✅ Total balance of {self.bank.bank_name}: ₦{total_bal}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLOR_TAN,
        ).pack(anchor="w", pady=5)

        txt_box = ctk.CTkTextbox(
            self.main_frame,
            height=300,
            width=550,
            fg_color=COLOR_SIDEBAR_BG,
            border_color=COLOR_TAN,
            border_width=1,
            text_color="#ffffff",
        )
        txt_box.pack(pady=15, fill="both", expand=True)

        txt_box.insert(
            "end", f"✅ {self.bank.bank_name} - ACTIVE BANK ACCOUNTS LEDGER\n"
        )
        for account in self.bank.accounts:
            txt_box.insert("end", f"\n- {account}\n")
            if not account.transactions:
                txt_box.insert("end", "   └──  ❌ No transactions made yet !!!\n")
            for transaction in account.transactions:
                txt_box.insert("end", f"   └── ✅ {transaction}\n")


if __name__ == "__main__":
    bank = Bank("Tuborrr-Dev Bank")
    bank.load_accounts()
    app = BankGUI(bank)
    app.mainloop()
