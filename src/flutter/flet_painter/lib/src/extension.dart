import 'package:flet/flet.dart';
import 'package:flutter/cupertino.dart';
import 'flet_painter.dart';

class Extension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "FletPainter":
        return FletPainterControl(control: control);
      default:
        return null;
    }
  }
}
