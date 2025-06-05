import tkinter as tk


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("320x540")

        self.expression = ""
        self.memory = 0.0   # 메모리 값(float)

        # 입력창
        self.entry = tk.Entry(root, font=("Arial", 24), justify="right")
        self.entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

        # 버튼 정의 (마지막줄에 메모리 버튼 4개 추가)
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
            ['M+', 'M-', 'MR', 'MC'],
            ['=']
        ]

        for row in buttons:
            frame = tk.Frame(root)
            frame.pack(expand=True, fill="both")
            for char in row:
                btn = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 18),
                    command=lambda ch=char: self.on_click(ch)
                )
                btn.pack(side="left", expand=True, fill="both")

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception:
                self.expression = "에러"
        elif char == 'M+':
            self.memory_add()
        elif char == 'M-':
            self.memory_subtract()
        elif char == 'MR':
            self.memory_recall()
        elif char == 'MC':
            self.memory_clear()
        else:
            self.expression += str(char)

        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    # ------------- 메모리 기능 구현 ----------------
    def memory_add(self):
        # 현재 입력값(혹은 결과값)을 메모리에 더함
        try:
            val = float(self.entry.get())
            self.memory += val
        except Exception:
            pass    # 숫자가 아니면 무시

    def memory_subtract(self):
        # 현재 입력값(혹은 결과값)을 메모리에서 뺌
        try:
            val = float(self.entry.get())
            self.memory -= val
        except Exception:
            pass
    
    def memory_recall(self):
        # 메모리 값을 입력창에 출력
        self.expression = str(self.memory)

    def memory_clear(self):
        # 메모리 초기화
        self.memory = 0.0

