import datetime
import csv
from expense import Expense

class Budget:
    def __init__(self):
        self.expenses = []  # 일반 지출 내역 리스트
        self.recurring = [] # 정기지출 리스트 (딕셔너리의 리스트)

    # 일반 지출 추가
    def add_expense(self, category, description, amount):
        today = datetime.date.today().isoformat()
        expense = Expense(today, category, description, amount)
        self.expenses.append(expense)

    def list_expenses(self):
        return self.expenses

    def total_spent(self):
        return sum(e.amount for e in self.expenses)

    def category_totals(self):
        totals = {}
        for e in self.expenses:
            totals[e.category] = totals.get(e.category, 0) + e.amount
        return totals

    # ------------정기지출 관련 기능-----------

    def add_recurring_expense(self, category, description, amount, day):
        """
        정기지출 등록 (예 : 매일 5일, '월세', 40만원)
        day : 매월 며칠에 자동추가할지 (1~28 권장)
        """
        self.recurring.append({
            'category': category,
            'description': description,
            'amount': amount,
            'day': day  # int: 매월 며칠
        })

    def list_recurring_expenses(self):
        return self.recurring

    def apply_recurring_expenses(self):
        """
        오늘 날짜에 해당하는 정기지출을 실제 지출 내역에 반영
        (중복 방지는 실습을 위해 단순화, 실전 적용 시 추가 체크 필요)
        """
        today = datetime.date.today()
        for item in self.recurring:
            if today.day == item['day']:
                # 이미 오늘 해당 지출이 추가되었는지 간단히 중복 체크 (같은 카테고리 + 설명 + 금액 + 오늘날짜)
                already_added = any(
                    e.date == today.isoformat() and
                    e.category == item['category'] and
                    e.description == item['description'] and
                    e.amount == item['amount']
                    for e in self.expenses 
                )
                if not already_added:
                    self.add_expense(item['category'], item['description'], item['amount'])

    # ------ 확장 예시: 수입, 잔액, CSV 내보내기 ------

    def export_expenses_to_csv(self, filename):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'category', 'description', 'amount'])
            for e in self.expenses:
                writer.writerow([e.date, e.category, e.description, e.amount])
