from dataclasses import dataclass, field
from typing import Optional, Callable, Any

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.colors import Colors
from flet.controls.text_style import TextStyle,FontWeight
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.base_control import control
from flet.controls.alignment import Alignment
from flet.controls.control_event import ControlEvent
from flet.controls.control_event import (
    OptionalControlEventHandler,
    OptionalEventHandler,
)
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
    color: Optional[Colors] = None
    font_weight: Optional[FontWeight] = None

@dataclass
class TextEvent(ControlEvent):
    value: Optional[str] = field(metadata={"data_field": "value"})
    style: Optional[TextStyle] = field(metadata={"data_field": "style"})






@control("FletPainter")
class FletPainter(ConstrainedControl, AdaptiveControl):
    """
    A control that allows dropping files.
    """
    # Modify the layers type to accept any dict or list objects, not just specific classes
    layers: Optional[list] = field(default_factory=list)
    on_selected_text: OptionalEventHandler["TextEvent"] = None

    async def async_save_image(self, **args) -> None:
        await self._invoke_method_async(
            "saveImage",
            {
                "path": args.get("path"),
                "scale": args.get("scale"),
            }
        )

    async def async_add_text(self, **args) -> None:
        
        await self._invoke_method_async(
            "addText",
            {
                "font_family": args.get("font_family"),
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
                "fontFamily": args.get("font_family"),
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
                font_family: Optional[str] = None,
                x: Optional[float] = None,
                y: Optional[float] = None,
                font_size: Optional[float] = None,
                color: Optional[Colors] = None,
                font_weight: Optional[str] = None) -> None:
        asyncio.create_task(
            self.async_add_text(
                text=text,
                font_family=font_family,
                x=x,
                y=y,
                font_size=font_size,
                color=color,
                font_weight=font_weight
            )
        )
    
    def save_image(self, path: str = None,scale: float = None) -> None:
        asyncio.create_task(
            self.async_save_image(
                path=path,
                scale=scale
            )
        )


    def change_text(self,
                text: str = None,
                font_family: Optional[str] = None,
                x: Optional[float] = None,
                y: Optional[float] = None,
                font_size: Optional[float] = None,
                color: Optional[Colors] = None) -> None:
        print(font_family)
        asyncio.create_task(
            self.async_change_text(
                text=text,
                font_family=font_family,
                x=x,
                y=y,
                font_size=font_size,
                color=color,
            )
        )