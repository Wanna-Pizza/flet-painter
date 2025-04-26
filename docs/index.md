# Introduction

FletPainter for Flet.

## Examples

```
import flet as ft

from flet_painter import FletPainter


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(

                ft.Container(height=150, width=300, alignment = ft.alignment.center, bgcolor=ft.Colors.PURPLE_200, content=FletPainter(
                    tooltip="My new FletPainter Control tooltip",
                    value = "My new FletPainter Flet Control", 
                ),),

    )


ft.app(main)
```

## Classes

[FletPainter](FletPainter.md)


