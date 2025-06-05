from budget import Budget


def main():
    budget = Budget()

    while True:
        print("==== 간단 가계부 ====")
        print("1. 지출 추가")
        print("2. 지출 목록 보기")
        print("3. 총 지출 보기")
        print("4. 정기지출 등록")
        print("5. 오늘 정기지출 자동 반영")
        print("6. 종료")
        choice = input("선택 > ")

        if choice == "1":
            category = input("카테고리 (예: 식비, 교통 등): ")
            description = input("설명: ")
            try:
                amount = int(input("금액(원): "))
            except ValueError:
                print("잘못된 금액입니다.\n")
                continue
            budget.add_expense(category, description, amount)

        elif choice == "2":
            budget.list_expenses()

        elif choice == "3":
            budget.total_spent()

        elif choice == "4":
            category = input("카테고리 (예 : 구독, 월세 등): ")
            description = input("설명 : ")
            try:
                amount = int(input("금액(원): "))
                # 29~31일은 월마다 없을 수 있으니 28일까지만 
                day = int(input("매월 며칠에 자동 추가(1~28): "))
                if not(1 <= day <= 28):
                    print("1~28 사이 숫자만 입력하세요.\n")
                    continue
            except ValueError:
                print("잘못된 입력입니다.\n")
                continue
            budget.add_recurring_expense(category, description, amount, day)

        elif choice == "5":
            budget.apply_recurring_expenses()
            
        elif choice == "6":
            print("가계부를 종료합니다.")
            break

        else:
            print("잘못된 선택입니다.\n")


if __name__ == "__main__":
    main()
