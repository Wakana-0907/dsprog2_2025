import flet as ft
import math

class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=ft.padding.symmetric(vertical=10)
        )


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK

class ScientificActionButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.Colors.GREEN_400
        self.color = ft.Colors.WHITE


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=28) 
        self.width = 400 
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                # 結果表示
                ft.Row(controls=[self.result], alignment="end"),
                
                # 科学計算モードの行 1 (sin, cos, tan, pi)
                ft.Row(
                    controls=[
                        ScientificActionButton(text="sin", button_clicked=self.button_clicked),
                        ScientificActionButton(text="cos", button_clicked=self.button_clicked),
                        ScientificActionButton(text="tan", button_clicked=self.button_clicked),
                        ScientificActionButton(text="pi", button_clicked=self.button_clicked),
                    ]
                ),
                # 科学計算モードの行 2 (sqrt, x^2, e, log)
                ft.Row(
                    controls=[
                        ScientificActionButton(text="sqrt", button_clicked=self.button_clicked),
                        ScientificActionButton(text="x^2", button_clicked=self.button_clicked),
                        ScientificActionButton(text="e", button_clicked=self.button_clicked),
                        # ACからlogに変更
                        ScientificActionButton(text="log", button_clicked=self.button_clicked), 
                    ]
                ),

                # 標準電卓の行 1 (AC, +/-, %, /) 
                ft.Row(
                    controls=[
                        # logからACに変更
                        ExtraActionButton(text="AC", button_clicked=self.button_clicked),
                        ExtraActionButton(text="+/-", button_clicked=self.button_clicked),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                # 標準電卓の行 2 (7, 8, 9, *)
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                # 標準電卓の行 3 (4, 5, 6, -)
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                # 標準電卓の行 4 (1, 2, 3, +)
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                # 標準電卓の行 5 (0, ., =)
                ft.Row(
                    controls=[
                        DigitButton(text="0", expand=2, button_clicked=self.button_clicked),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.END 
        )

    def button_clicked(self, e):
        data = e.control.data
        current_value = self.result.value
        
        if current_value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()
        
        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if current_value == "0" or self.new_operand == True:
                if data == "." and current_value == "0":
                    self.result.value = "0."
                elif data == ".":
                     self.result.value = "0." if self.new_operand else current_value + data
                else:
                    self.result.value = data
                self.new_operand = False
            elif data == "." and "." in current_value:
                pass
            else:
                self.result.value = current_value + data
        
        elif data == "pi":
            self.result.value = str(math.pi)
            self.new_operand = True
        elif data == "e":
            self.result.value = str(math.e)
            self.new_operand = True

        elif data in ("sin", "cos", "tan", "sqrt", "x^2", "log"): 
            try:
                val = float(current_value)
                new_val = 0
                if data == "sin":
                    new_val = math.sin(val)
                elif data == "cos":
                    new_val = math.cos(val)
                elif data == "tan":
                    new_val = math.tan(val)
                elif data == "sqrt":
                    if val < 0:
                        raise ValueError("Cannot take square root of negative number")
                    new_val = math.sqrt(val)
                elif data == "x^2":
                    new_val = val * val
                elif data == "log": 
                    if val <= 0:
                        raise ValueError("Cannot take log of zero or negative number")
                    new_val = math.log10(val)
                
                self.result.value = str(self.format_number(new_val))
                self.new_operand = True 
            except ValueError:
                self.result.value = "Error"
            except Exception:
                self.result.value = "Error"

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(current_value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = 0
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(current_value), self.operator
            )
            self.reset()

        elif data in ("%"):
            try:
                self.result.value = str(self.format_number(float(current_value) / 100))
                self.new_operand = True 
            except ValueError:
                self.result.value = "Error"
        
        elif data in ("+/-"):
            try:
                val = float(current_value)
                self.result.value = str(self.format_number(-val))
            except ValueError:
                 self.result.value = "Error"

        self.update()

    def format_number(self, num):
        if abs(num - round(num)) < 1e-9:
            num = round(num)
        
        if num % 1 == 0 and abs(num) < 1e15: 
            return int(num)
        else:
            if len(str(num)) > 15:
                 return float(f"{num:.10f}") 
            return num

    def calculate(self, operand1, operand2, operator):
        try:
            if operator == "+":
                return self.format_number(operand1 + operand2)
            elif operator == "-":
                return self.format_number(operand1 - operand2)
            elif operator == "*":
                return self.format_number(operand1 * operand2)
            elif operator == "/":
                if operand2 == 0:
                    return "Error"
                else:
                    return self.format_number(operand1 / operand2)
        except OverflowError:
            return "Error"
        except Exception:
            return "Error"

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Scientific Calc App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.Colors.BLUE_GREY_900 

    calc = CalculatorApp()

    page.add(calc)


ft.app(target=main)