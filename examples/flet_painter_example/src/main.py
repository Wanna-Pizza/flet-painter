import flet as ft

from flet_painter import FletPainter,TextWidget,ImageWidget

class ToolBarButton(ft.Container):
    def __init__(self,icon):
        super().__init__()
        self.border_radius = 10
        self.expand = True
        self.content = ft.Icon(icon, color='white,0.5',size=20)
        self.alignment = ft.alignment.center
        self.bgcolor = 'white,0.0'
        self.on_hover = self.__hover 
    
    def __hover(self,e):
        self.bgcolor = 'white,0.1' if self.bgcolor == 'white,0.0' else 'white,0.0'
        self.update()



class ToolBar(ft.Container):
    def __init__(self):
        super().__init__()
        self.width = 60
        self.height = 120
        self.padding = 5
        self.bgcolor = 'white,0.03'
        self.border_radius = 10
        self.border = ft.border.only(top=ft.BorderSide(1,'white,0.1'))
        self.shadow = ft.BoxShadow(spread_radius=5, blur_radius=10, color='black,0.02')
        self.content = self.__content()    
        self.alignment = ft.alignment.center
    def __content(self):
        return ft.Column([
            ToolBarButton(ft.Icons.TEXT_FIELDS),
            ToolBarButton(ft.Icons.IMAGE),
        ],alignment=ft.MainAxisAlignment.SPACE_EVENLY,spacing=10)

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
        self.painter = FletPainter(expand=True,layers=[TextWidget(text="Hello, World!",color=ft.Colors.WHITE)])
        

        return self.painter


class Designer(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.alignment = ft.alignment.center
        self.content = self.__content()
    
    def left_right_side(self):
        return ft.Container(
            bgcolor='white,0.03',
            border_radius=10,
            border=ft.border.all(1,'white,0.1'),
            content=ft.Text("Future content")
        )
    

    def __content(self):
        main_phone = ft.Row([Phone(),ToolBar()],alignment=ft.MainAxisAlignment.CENTER,spacing=20)
        return ft.Row([main_phone],alignment=ft.MainAxisAlignment.CENTER,spacing=20)

def main(page: ft.Page):
    page.add(Designer())

ft.run(main)