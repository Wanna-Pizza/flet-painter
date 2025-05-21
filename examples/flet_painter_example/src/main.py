import asyncio
import flet as ft
from flet_painter.google_fonts import GoogleFont



class TextPreviewFont(ft.Container):
    def __init__(self,on_click: callable = None,font: str = None):
        super().__init__()
        self.callback_on_click = on_click
        self.content=ft.Text(
                value=str(font),
                size=15,
                color='white,0.5',
                text_align=ft.TextAlign.CENTER,
            )
        self.padding=10
        self.border=ft.border.only(
            top=ft.BorderSide(1, 'white,0.1')
        )
        self.alignment=ft.Alignment.center()
        self.bgcolor='white,0.03'
        self.border_radius=10
        self.on_click=lambda e: self.__on__click(font)
        self.expand = True
    
    def __on__click(self,font):
        self.callback_on_click(font)



class DropDownFonts(ft.Container):
    def __init__(self,on_click_font: callable = None):
        super().__init__()
        self.border_radius = 10
        self.expand = 2
        self.blur = 10
        self.offset = [1.1,0.0]
        self.animate_offset = ft.Animation(
            duration=300,
            curve=ft.AnimationCurve.LINEAR_TO_EASE_OUT
        )
        # Add default callback if none is provided
        self.on_click_font = on_click_font if on_click_font else lambda font: print(f"Selected font: {font}")
        self.bgcolor = 'white,0.03'
        self.alignment = ft.Alignment.center()
        self.padding = 10
        self.content = self.__content()
    

    def text_field(self):
        return ft.TextField(
            label="Search font",
            on_change=self.__on_change,
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
            border_color='white,0.1',
            border_width=1,
            label_style=ft.TextStyle(color='white,0.5'),
            cursor_color='white,0.5',
        )
    
    def __on_change(self, e):
        self.content.value = e.control.value
        self.update()
        matching_fonts = [font for font in self.font_list if e.control.value.lower() in font.lower()]
        self.grid.controls.clear()
        self.grid.update()

        if e.control.value.strip() == "":
            pass
        else:
            for i in matching_fonts:
                self.grid.controls.append(
                    TextPreviewFont(on_click=self.on_click_font, font=i)
                )
            self.grid.update()


    def close_dropdown(self,e):
        async def animate_off():
            self.offset = [1.1,0.0]
            self.update()
            await asyncio.sleep(0.3)
            self.parent.controls.remove(self)
            self.parent.update()
        self.page.run_task(animate_off)


    def __content(self):
        self.button_back = ft.Container(
            content=ft.Text("Back",color='white,0.5'),
            bgcolor='white,0.03',
            padding=10,
            border=ft.border.only(
                top=ft.BorderSide(1, 'white,0.1'),
            ),
            alignment=ft.Alignment.center(),
            on_click=self.close_dropdown,
            border_radius=10)

        self.font_list = [
            v for v in GoogleFont.__dict__.values()
            if isinstance(v, str)
        ]
        self.grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.7,
            spacing=5,
            run_spacing=5,
            controls=[
                # Use actual font names from font_list instead of numbers
                TextPreviewFont(on_click=self.on_click_font, font=self.font_list[i] if i < len(self.font_list) else f"Font {i}")
                for i in range(0, 20)
            ]
        )

        return ft.Column([
            self.text_field(),
            self.grid,
            self.button_back
        ],expand=True)
    
    def __animate_on(self):
        async def animate_on():
            await asyncio.sleep(0.1)
            self.offset = [0.0,0.0]
            self.update()
        self.page.run_task(animate_on)

    def did_mount(self):
        self.__animate_on()
        return super().did_mount()

# def main(page: ft.Page):
#     # Add a callback function to demonstrate the click is working
#     def on_font_selected(font):
#         print("FUUUCK")
        
#     # Pass the callback to DropDownFonts
#     page.add(DropDownFonts(on_click_font=on_font_selected))

# ft.run(main)