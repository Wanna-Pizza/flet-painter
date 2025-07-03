import time
import flet as ft

from flet_painter import FletPainter, ImageWidget, TextWidget


class Phone(ft.Container):
    def __init__(self):
        super().__init__()
        self.__phone_width = 2.72 
        self.__phone_height = 5.67
        self.scale_factor = 120

        self.phone_height = self.__phone_height * self.scale_factor
        self.phone_width = self.__phone_width * self.scale_factor

        self.width = self.phone_width
        self.height = self.phone_height
        self.bgcolor = 'white,0.03'
        self.border_radius = 30
        self.border = ft.border.all(1,'white,0.1')
        
        self.layers = []
        self.selected_layer = None
        self.content = self.__content()

    def __content(self):
        self.painter = FletPainter(
            expand=True
        )
        return ft.Stack([
            self.painter,
            ft.Row([
                ft.Container(width=100,height=30,border_radius=20,bgcolor='black',offset=[0,0.5]),
                
                ],alignment=ft.MainAxisAlignment.CENTER,spacing=0),
        ])
        self.painter.add_text

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    phone = Phone()
    def add_image(e):
        phone.painter.add_image(
            path=r"G:\Albert_Designer\Albert_Designer\src\assets\logos\MLB\MLB-ARI01.png",
            scale=0.05
        )
        phone.painter.update()
    button = ft.ElevatedButton(
        text="Add Image",
            on_click=add_image)
    page.add(
        phone,
        button
    )

    page.update()

ft.app(main)
