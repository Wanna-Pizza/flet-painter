import flet as ft

from flet_painter import FletPainter, ImageWidget, TextWidget
from flet_painter.google_fonts import GoogleFont
from main import DropDownFonts



def rgb_to_hex(r, g, b):
    """
    Convert RGB color values to hexadecimal color code.
    
    Args:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)
        
    Returns:
        str: Hexadecimal color code in the format '#RRGGBB'
    """
    # Ensure the values are within valid range
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    # Convert to hex and format as #RRGGBB
    return f'#{r:02x}{g:02x}{b:02x}'


class ToolBarButton(ft.Container):
    def __init__(self,icon,on_click = None):
        super().__init__()
        self.border_radius = 10
        self.expand = True
        self.ink = True
        self.content = ft.Icon(icon, color='white,0.5',size=20)
        self.alignment = ft.Alignment.center()
        self.bgcolor = 'white,0.0'
        self.on_click = on_click
        self.on_hover = self.__hover 
    
    def __hover(self,e):
        self.bgcolor = 'white,0.1' if self.bgcolor == 'white,0.0' else 'white,0.0'
        self.update()

        

class SettingsField(ft.Container):
    def __init__(self,on_change_text = None,icon = ft.Icons.TEXT_FIELDS):
        super().__init__()
        self.border_radius = 10
        self.on_change = on_change_text
        self.padding = ft.Padding.only(left=10)
        self.bgcolor = 'white,0.03'
        self.__icon = icon
        self.alignment = ft.Alignment.center()
        self.content = self.__content()

    def __content(self):
        return ft.Row([
            ft.Row([ft.Icon(self.__icon, color='white,0.5'),ft.Text("Value:",color='white,0.5',size=15)]),
            ft.TextField(border_color='transparent',hint_style=ft.TextStyle(color='white,0.5'),hint_text="Change text here..",on_change=self.on_change)
        ],spacing=0)



class ToolBar(ft.Container):
    def __init__(self,on_text_created=None, on_image_created=None):
        super().__init__()
        self.width = 60
        self.height = 120
        self.padding = 5
        self.bgcolor = 'white,0.03'
        self.border_radius = 10
        self.border = ft.Border.only(top=ft.BorderSide(1,'white,0.1'))
        self.shadow = ft.BoxShadow(spread_radius=5, blur_radius=10, color='black,0.02')
        self.on_text_created = on_text_created
        self.on_image_created = on_image_created
        self.content = self.__content()    

        self.alignment = ft.Alignment.center()
    def __content(self):
        return ft.Column([
            ToolBarButton(ft.Icons.TEXT_FIELDS,on_click=self.on_text_created),
            ToolBarButton(ft.Icons.IMAGE,on_click=self.on_image_created),
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
        self.border = ft.Border.all(1,'white,0.1')
        
        self.layers = []
        self.selected_layer = None
        self.content = self.__content()

    def __content(self):
        self.painter = FletPainter(
            expand=True,
        )
        return ft.Stack([
            self.painter,
            ft.Row([
                ft.Container(width=100,height=30,border_radius=20,bgcolor='black',offset=[0,0.5]),
                
                ],alignment=ft.MainAxisAlignment.CENTER,spacing=0),
        ])

class Designer(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.content = self.__content()
    
    def __change_text(self,e):
        self.phone.painter.change_text(
            text=e.control.value)
        self.phone.painter.update()
    
    def __change_font(self,font):
        for _ in range(2):
            self.phone.painter.change_text(
                font_family=font)
            self.phone.painter.update()
        
    def __open_fonts(self,e):
        self.stack_settings.controls.append(
            ft.Row([
                DropDownFonts(on_click_font=self.__change_font)
            ],alignment=ft.MainAxisAlignment.END)
        )
        self.stack_settings.update()

    def __add_text(self,e):
        self.phone.painter.add_text(
            text="Hello World",
            font_size=20,
            color=rgb_to_hex(134,134,134),
            font_weight='bold'
        )
        self.phone.painter.update()
    
    def __add_image(self,e):
        self.phone.painter.add_image(
            path=r"C:\Users\MF\Downloads\CLOWN1.png",
        )
        self.phone.painter.update()
    
    def FontChangerWidget(self):
        return ft.Container(
            ft.Text("Change Font",color='white,0.5',size=15),
            bgcolor='white,0.03',
            border_radius=10,
            padding=10,
            ink=True,
            border=ft.border.only(
                top=ft.BorderSide(1,'white,0.1'),
            ),
            alignment=ft.Alignment.center(),
            on_click=self.__open_fonts,
        )
    
    def right_settings(self):
        self.stack_settings = ft.Stack([
            ft.Column([
                ft.Text("Style",color='white,0.5',size=15,offset=[0.1,0]),
                
                ft.Container(
                bgcolor='white,0.03',
                border_radius=10,
                expand=2,
                padding=10,
                alignment=ft.Alignment.center(),
                border=ft.Border.all(1,'white,0.1'),
                content=ft.Column([
                    SettingsField(on_change_text=self.__change_text),
                    self.FontChangerWidget()

                ])
            )
            
            ],expand=2)
        ],expand=2)
        return self.stack_settings

    def __save_image(self,e):
        print("Saving image...")
        self.phone.painter.save_image(
            path=r"C:\Users\MF\Downloads\test_save\test_save.png",
            scale=10.0,
        )
        self.phone.painter.update()
    
    
    def left_side(self):
        button = ft.ElevatedButton(
            content=ft.Text("Save",color='white,0.5'),
            on_click=self.__save_image
        )
        return ft.Container(
            bgcolor='white,0.03',
            border_radius=10,
            expand=2,
            alignment=ft.Alignment.center(),
            border=ft.Border.all(1,'white,0.1'),
            content=button
        )
    

    def __content(self):
        self.phone = Phone()
        main_phone = ft.Row([self.phone, ToolBar(
            on_text_created=self.__add_text,
            on_image_created=self.__add_image)],alignment=ft.MainAxisAlignment.CENTER,spacing=20)
        return ft.Row([
            self.left_side(),
            ft.Container(expand=1),
            main_phone,
            ft.Container(expand=1),
            self.right_settings()
        ],alignment=ft.MainAxisAlignment.CENTER,spacing=20)
def main(page: ft.Page):
    page.add(Designer())

ft.run(main)