import datetime
from expense import Expense

class Budget:
    def __init__(self):
        self.expenses = []
        self.recurring = [] # 정기지출 목록 저장용 리스트 추가

    def add_expense(self, category, description, amount):
        today = datetime.date.today().isoformat()
        expense = Expense(today, category, description, amount)
        self.expenses.append(expense)
        print("지출이 추가되었습니다.\n")

    def list_expenses(self):
        if not self.expenses:
            print("지출 내역이 없습니다.\n")
            return
        print("\n[지출 목록]")
        for idx, e in enumerate(self.expenses, 1):
            print(f"{idx}. {e}")
        print()

    def total_spent(self):
        total = sum(e.amount for e in self.expenses)
        print(f"총 지출: {total}원\n")

    # 정기지출 등록 메서드
    def add_recurring_expense(self, category, description, amount, day):
        self.recurring.append({
            'category': category,
            'description': description,
            'amount': amount,
            'day': day  # int: 매월 며칠
        })
        print(f"정기지출로 등록됨: [{category}] {description} {amount}원, 매월 {day}일\n")

    # 오늘 날짜에 맞는 정기지출 자동추가
    def apply_recurring_expenses(self):
        import datetime
        today = datetime.date.today()
        for item in self.recurring:
            if today.day == item['day']:
                self.add_expense(item['category'], item['description'], item['amount'])
