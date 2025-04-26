from dataclasses import dataclass, field
from typing import Optional, Callable, Any
import asyncio

import flet as ft

__all__ = ["FletPainter","ImageWidget","TextWidget","TextEvent"]


@dataclass
class ImageWidget:
    type: str = "image" # DONT CHANGE THIS
    path: str = None
    x: Optional[float] = None
    y: Optional[float] = None

@dataclass
class TextWidget:
    type: str = "text" # DONT CHANGE THIS
    text: str = None
    x: Optional[float] = None
    y: Optional[float] = None
    font_size: Optional[float] = None
    color: Optional[ft.Colors] = None
    font_weight: Optional[ft.FontWeight] = None

@dataclass
class TextEvent(ft.ControlEvent):
    value: Optional[str] = field(metadata={"data_field": "value"})
    style: Optional[ft.TextStyle] = field(metadata={"data_field": "style"})






@ft.control("FletPainter")
class FletPainter(ft.ConstrainedControl, ft.AdaptiveControl):
    """
    A control that allows dropping files.
    """
    layers: Optional[list[ImageWidget | TextWidget]] = field(default_factory=list)
    on_selected_text: ft.OptionalEventCallable["TextEvent"] = None
    








    async def async_add_text(self, **args) -> None:
        
        await self._invoke_method_async(
            "addText",
            {
                "text": args.get("text"),
                "x": args.get("x"),
                "y": args.get("y"),
                "font_size": args.get("font_size"),
                "color": args.get("color"),
                "font_weight": args.get("font_weight"),
            }
        )
    async def async_change_text(self, **args) -> None:
        
        await self._invoke_method_async(
            "changeText",
            {
                "text": args.get("text"),
                "x": args.get("x"),
                "y": args.get("y"),
                "font_size": args.get("font_size"),
                "color": args.get("color"),
                "font_weight": args.get("font_weight"),
            }
        )
    async def async_add_image(self,**args):
        await self._invoke_method_async(
            "addImage",
            {
                "path": args.get("path"),
                "x": args.get("x"),
                "y": args.get("y"),
            }
        )
    def add_image(self,
                  path: str = None,
                x: Optional[float] = None,
                y: Optional[float] = None) -> None:
        asyncio.create_task(
            self.async_add_image(
                path=path,
                x=x,
                y=y
            )
        )
    def add_text(self,
                text: str = None,
                x: Optional[float] = None,
                y: Optional[float] = None,
                font_size: Optional[float] = None,
                color: Optional[ft.Colors] = None,
                font_weight: Optional[str] = None) -> None:
        asyncio.create_task(
            self.async_add_text(
                text=text,
                x=x,
                y=y,
                font_size=font_size,
                color=color,
                font_weight=font_weight
            )
        )
    def change_text(self,
                text: str = None,
                x: Optional[float] = None,
                y: Optional[float] = None,
                font_size: Optional[float] = None,
                color: Optional[ft.Colors] = None,
                font_weight: Optional[str] = None) -> None:
        asyncio.create_task(
            self.async_change_text(
                text=text,
                x=x,
                y=y,
                font_size=font_size,
                color=color,
                font_weight=font_weight
            )
        )