import flet as ft

# カウンター表示用のテキスト
def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)
# ボタンが押し下げられた時に呼び出される関数
    def decrement_click(e):
        counter.data -= 1
        counter.value = str(counter.data)
        counter.update()

# ボタンが押し下げられた時に呼び出される関数
    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()    

# カウンターを増やすボタンを追加
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=increment_click
    )

# SafeAraaで囲んで、中央にカウンターを配置
    page.add(
        ft.SafeArea(
            ft.Container(
                content=ft.Column(controls=[counter, hoge]),
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
