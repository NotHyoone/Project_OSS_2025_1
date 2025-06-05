import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from budget import Budget

class BudgetApp:
    def __init__(self, root):
        self.budget = Budget()
        self.root = root
        self.root.title("간단 가계부")
        self.root.geometry("500x420")

        # 입력 프레임
        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="카테고리:").grid(row=0, column=0)
        self.category_entry = tk.Entry(entry_frame)
        self.category_entry.grid(row=0, column=1)

        tk.Label(entry_frame, text="설명:").grid(row=0, column=2)
        self.desc_entry = tk.Entry(entry_frame)
        self.desc_entry.grid(row=0, column=3)

        tk.Label(entry_frame, text="금액(원):").grid(row=0, column=4)
        self.amount_entry = tk.Entry(entry_frame, width=8)
        self.amount_entry.grid(row=0, column=5)

        tk.Button(entry_frame, text="지출 추가", command=self.add_expense).grid(row=0, column=6, padx=5)

        # 리스트박스
        self.listbox = tk.Listbox(root, width=70, height=10)
        self.listbox.pack(pady=10)

        # 버튼 프레임
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="지출 목록 보기", command=self.show_expenses).grid(row=0, column=0, padx=3)
        tk.Button(btn_frame, text="카테고리별 합계", command=self.show_category_totals).grid(row=0, column=1, padx=3)
        tk.Button(btn_frame, text="정기지출 등록", command=self.add_recurring_expense).grid(row=0, column=2, padx=3)
        tk.Button(btn_frame, text="정기지출 목록", command=self.show_recurring_expenses).grid(row=0, column=3, padx=3)
        tk.Button(btn_frame, text="오늘 정기지출 적용", command=self.apply_recurring_expenses).grid(row=0, column=4, padx=3)
        tk.Button(btn_frame, text="CSV 내보내기", command=self.export_csv).grid(row=0, column=5, padx=3)
        tk.Button(btn_frame, text="종료", command=root.quit).grid(row=0, column=6, padx=3)

        self.status = tk.Label(root, text="", fg="blue")
        self.status.pack(pady=5)

    def add_expense(self):
        cat = self.category_entry.get().strip()
        desc = self.desc_entry.get().strip()
        amt = self.amount_entry.get().strip()
        if not (cat and desc and amt.isdigit()):
            messagebox.showerror("입력 오류", "모든 정보를 올바르게 입력하세요.")
            return
        self.budget.add_expense(cat, desc, int(amt))
        self.status['text'] = "지출이 추가되었습니다."
        self.show_expenses()
        self.amount_entry.delete(0, tk.END)

    # ------ 정기지출 관련 GUI ------

    def add_recurring_expense(self):
        # 간단 입력 다이얼로그 사용
        cat = simpledialog.askstring("정기지출 카테고리", "카테고리 입력 (예: 월세, 구독 등):")
        if not cat:
            return
        desc = simpledialog.askstring("정기지출 설명", "설명 입력:")
        if not desc:
            return
        amt = simpledialog.askinteger("정기지출 금액", "금액 입력(원):")
        if not amt:
            return
        day = simpledialog.askinteger("매월 며칠?", "매월 몇일에 적용? (1~28):")
        if not day or not (1 <= day <= 28):
            messagebox.showerror("입력 오류", "1~28 사이의 숫자만 입력하세요.")
            return
        self.budget.add_recurring_expense(cat, desc, amt, day)
        self.status['text'] = "정기지출이 등록되었습니다."

    def show_recurring_expenses(self):
        self.listbox.delete(0, tk.END)
        lst = self.budget.list_recurring_expenses()
        if not lst:
            self.listbox.insert(tk.END, "정기지출 내역이 없습니다.")
            return
        for idx, r in enumerate(lst, 1):
            self.listbox.insert(
                tk.END,
                f"{idx}. [매월 {r['day']}일] {r['category']} - {r['description']}: {r['amount']}원"
            )
        self.status['text'] = "정기지출 목록 표시"

    def apply_recurring_expenses(self):
        self.budget.apply_recurring_expenses()
        self.status['text'] = "오늘 날짜의 정기지출이 반영되었습니다."
        self.show_expenses()

    # ------ 기존 기능 ------

    def show_expenses(self):
        self.listbox.delete(0, tk.END)
        for e in self.budget.list_expenses():
            self.listbox.insert(tk.END, str(e))
        self.status['text'] = f"총 지출: {self.budget.total_spent()}원"

    def show_category_totals(self):
        totals = self.budget.category_totals()
        self.listbox.delete(0, tk.END)
        if not totals:
            self.listbox.insert(tk.END, "지출 내역이 없습니다.")
            return
        for cat, amt in totals.items():
            self.listbox.insert(tk.END, f"{cat}: {amt}원")
        self.status['text'] = "카테고리별 합계 표시"

    def export_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            self.budget.export_expenses_to_csv(filename)
            self.status['text'] = "CSV 내보내기 완료"

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()

# def main():
#     budget = Budget()

#     while True:
#         print("==== 간단 가계부 ====")
#         print("1. 지출 추가")
#         print("2. 지출 목록 보기")
#         print("3. 총 지출 보기")
#         print("4. 정기지출 등록")
#         print("5. 오늘 정기지출 자동 반영")
#         print("6. 종료")
#         choice = input("선택 > ")

#         if choice == "1":
#             category = input("카테고리 (예: 식비, 교통 등): ")
#             description = input("설명: ")
#             try:
#                 amount = int(input("금액(원): "))
#             except ValueError:
#                 print("잘못된 금액입니다.\n")
#                 continue
#             budget.add_expense(category, description, amount)

#         elif choice == "2":
#             budget.list_expenses()

#         elif choice == "3":
#             budget.total_spent()

#         elif choice == "4":
#             category = input("카테고리 (예 : 구독, 월세 등): ")
#             description = input("설명 : ")
#             try:
#                 amount = int(input("금액(원): "))
#                 # 29~31일은 월마다 없을 수 있으니 28일까지만 
#                 day = int(input("매월 며칠에 자동 추가(1~28): "))
#                 if not(1 <= day <= 28):
#                     print("1~28 사이 숫자만 입력하세요.\n")
#                     continue
#             except ValueError:
#                 print("잘못된 입력입니다.\n")
#                 continue
#             budget.add_recurring_expense(category, description, amount, day)

#         elif choice == "5":
#             budget.apply_recurring_expenses()

#         elif choice == "6":
#             print("가계부를 종료합니다.")
#             break

#         else:
#             print("잘못된 선택입니다.\n")


# if __name__ == "__main__":
#     main()
