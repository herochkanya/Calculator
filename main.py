import flet as ft
import re

def main(page: ft.Page):
    page.title = "Калькулятор"
    page.window_width = 270
    page.window_height = 450
    page.bgcolor = ft.Colors.GREY_900
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.update()

    result = ft.TextField(
        label="Результат",
        value="0",
        read_only=True,
        text_align=ft.TextAlign.RIGHT,
        text_size=36,
        bgcolor=ft.Colors.GREY_800,
        color=ft.Colors.WHITE,
        height=70,
    )

    def format_numbers(expression):
        """ Форматує числа у виразі, не чіпаючи оператори. """
        tokens = re.split(r'([\+\-\×\÷])', expression)
        formatted_tokens = []

        for token in tokens:
            if re.match(r'^\d+(\.\d+)?$', token.replace(",", "")):  # Число з можливим десятковим дробом
                num_without_commas = token.replace(",", "")
                if "." in num_without_commas:
                    int_part, dec_part = num_without_commas.split(".")
                    formatted_number = f"{int(int_part):,}.{dec_part}"  # Форматування тільки цілої частини
                else:
                    formatted_number = f"{int(num_without_commas):,}"
                formatted_tokens.append(formatted_number)
            else:
                formatted_tokens.append(token)  

        return "".join(formatted_tokens)

    def button_click(e):
        button_data = e.control.data
        current_value = result.value

        if button_data is None or button_data == " ":
            return  # Ігноруємо пусту кнопку

        if current_value == "Помилка":
            current_value = "0"  # Якщо була помилка, замінюємо на "0"

        if button_data == "C":
            result.value = "0"
        elif button_data == "=":
            try:
                calc_value = current_value.replace("÷", "/").replace("×", "*")
                calc_value_no_commas = calc_value.replace(",", "")
                result_value = str(eval(calc_value_no_commas))
                result.value = format_numbers(result_value)
            except Exception:
                result.value = "Помилка"
        elif button_data == "⌫":
            result.value = current_value[:-1] if len(current_value) > 1 else "0"
        elif button_data == "%":
            tokens = re.split(r'([\+\-\×\÷])', current_value)
            if tokens:
                # Якщо останній символ — оператор, видаляємо його (імітуємо "⌫")
                while tokens and tokens[-1] in "+-×÷":
                    tokens.pop(-1)

                if tokens:
                    last_number = tokens[-1].replace(",", "")
                    if re.match(r'^\d+(\.\d+)?$', last_number):  # Якщо останній токен - число
                        new_number = str(float(last_number) / 100)  # Ділимо на 100
                        tokens[-1] = new_number  # Замінюємо останнє число
                        result.value = format_numbers("".join(tokens))  
        elif button_data == ".":
            tokens = re.split(r'([\+\-\×\÷])', current_value)
            last_number = tokens[-1]
            if "." not in last_number:  # Не дозволяємо другу крапку
                if last_number == "" or last_number in "+-×÷":
                    tokens.append("0.")  # Додаємо "0." якщо число відсутнє
                else:
                    tokens[-1] += "."  # Додаємо крапку до останнього числа
                result.value = "".join(tokens)
        elif button_data in "+-×÷":
            if current_value[-1] in "+-×÷":
                result.value = current_value[:-1] + button_data  # Замінюємо попередній оператор
            else:
                result.value += button_data
        elif current_value == "0" and button_data not in "0123456789":
            pass  # Не дозволяємо починати з оператора
        else:
            result.value = current_value + button_data

        result.value = format_numbers(result.value)
        page.update()

    page.on_key_down = lambda e: button_click(ft.Control(data=e.key))

    buttons = [
        ["C", "⌫", "%", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        [" ", "0", ".", "="],
    ]

    button_controls = []
    for row in buttons:
        button_row = []
        for button in row:
            button_row.append(
                ft.ElevatedButton(
                    button, 
                    data=button, 
                    on_click=button_click, 
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=36),
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.GREY_700,
                    ),
                    width=70,
                    height=70,
                )
            )
        button_controls.append(ft.Row(button_row, alignment=ft.MainAxisAlignment.CENTER))

    page.add(result, *button_controls)

ft.app(target=main)
