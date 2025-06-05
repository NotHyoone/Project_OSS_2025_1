
class Expense:
    def __init__(self, date, category, description, amount):
        self.date = date                # 날짜 (문자열)
        self.category = category        # 카테고리 (예 : 식비, 교통)
        self.description = description  # 지출 설명
        self.amount = amount            # 금액 (int)

    def __str__(self):
        # 지출 내역을 보기 좋게 문자열로 반환
        return f"[{self.date}] {self.category} - {self.description}: {self.amount}원"