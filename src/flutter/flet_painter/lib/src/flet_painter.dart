import 'dart:io';
import 'dart:ui' as ui;
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flet_painter/src/flutter_painter_v2/flutter_painter.dart';

class FletPainterControl extends StatefulWidget {
  final Control control;

  const FletPainterControl({
    super.key,
    required this.control,
  });

  @override
  _FletPainterControlState createState() => _FletPainterControlState();
}

class _FletPainterControlState extends State<FletPainterControl> {
  late PainterController controller;
  Size? canvasSize;
  final FocusNode _focusNode = FocusNode();
  String defaultText = "Text"; // Default text value
  dynamic previousLayers; // Track previously processed layers
  List<String> processedLayerIds = []; // Track processed layer IDs

  void sendEvent(String name, [dynamic data]) {
    widget.control.triggerEvent(name, data);
  }

  @override
  void initState() {
    super.initState();
    controller = PainterController();
    controller.addListener(() {
      final sel = controller.selectedObjectDrawable;
      if (sel is TextDrawable) {
        sendSelectedTextInfo();
      }
    });
    _setupWidgets();
    widget.control.addInvokeMethodListener(_invokeMethod);

    // Initialize with text settings
    controller.textSettings = TextSettings(
      textStyle: const TextStyle(
        fontWeight: FontWeight.bold,
        color: Colors.blue,
        fontSize: 24,
      ),
    );
  }

  void updateTextDrawable({
    String? newText,
    double? newFontSize,
    Color? newColor,
    FontWeight? newFontWeight,
  }) {
    final selectedDrawable = controller.selectedObjectDrawable;

    if (selectedDrawable is TextDrawable) {
      final updatedDrawable = TextDrawable(
        position: selectedDrawable.position,
        text: newText ?? selectedDrawable.text,
        style: TextStyle(
          color: newColor ?? selectedDrawable.style.color,
          fontSize: newFontSize ?? selectedDrawable.style.fontSize,
          fontWeight: newFontWeight ?? selectedDrawable.style.fontWeight,
        ),
      );

      // Replace the old drawable with the updated one
      controller.replaceDrawable(selectedDrawable, updatedDrawable);
    } else {
      print("No TextDrawable selected or invalid drawable type.");
    }
  }

  void sendSelectedTextInfo() {
    final selectedDrawable = controller.selectedObjectDrawable;

    if (selectedDrawable is TextDrawable) {
      sendEvent("on_selected_text", {
        "value": selectedDrawable.text,
        "style": selectedDrawable.style,
      });
    } else {
      sendEvent("on_selected_text", {
        "value": null,
        "style": null,
      });
    }
  }

  void _setupWidgets() {
    var layersData = widget.control.get("layers");

    if (layersData == null) return;

    if (layersData is List) {
      for (var layer in layersData) {
        String id = layer["id"] ??
            "${layer.hashCode}"; // Generate id from hashcode if not provided
        if (processedLayerIds.contains(id)) continue;

        String type = layer["type"] ?? "";

        if (type == "text") {
          defaultText = layer["text"] ?? defaultText;
          addText(
              text: defaultText,
              color: parseColor(layer["color"], Theme.of(context)),
              fontSize: parseDouble(layer["fontSize"]),
              fontWeight: getFontWeight(layer["fontWeight"]));
        } else if (type == "image") {
          addImage(
            path: layer["path"] ?? "",
          );
        }

        processedLayerIds.add(id); // Mark layer as processed
      }
    } else if (layersData is Map<String, dynamic>) {
      String id = layersData["id"] ??
          "${layersData.hashCode}"; // Generate id from hashcode if not provided
      if (processedLayerIds.contains(id))
        return; // Skip already processed layer

      String type = layersData["type"] ?? "";

      if (type == "text") {
        defaultText = layersData["text"] ?? defaultText;
        addText(text: defaultText);
      } else if (type == "image") {
        addImage(path: layersData["path"] ?? "");
      }

      processedLayerIds.add(id); // Mark layer as processed
    }

    // Update previousLayers to track what has been processed
    previousLayers = layersData;
  }

  @override
  void dispose() {
    _focusNode.dispose();
    controller.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  // Helper method to get the center of the canvas
  Offset get canvasCenter {
    if (canvasSize == null) return const Offset(100, 100);
    return Offset(canvasSize!.width / 2, canvasSize!.height / 2);
  }

  // Function to add text to the canvas
  void addText({
    String? text,
    double? x,
    double? y,
    double? fontSize,
    Color? color,
    FontWeight? fontWeight,
  }) {
    final position = Offset(
      x ?? canvasCenter.dx, // Default to center if x is null
      y ?? canvasCenter.dy, // Default to center if y is null
    );

    final textDrawable = TextDrawable(
      position: position,
      text: text ?? defaultText, // Use default text if no text is provided
      style: TextStyle(
        color: color ?? Colors.red, // Default color
        fontSize: fontSize ?? 30, // Default font size
        fontWeight: fontWeight ?? FontWeight.bold, // Default font weight
      ),
    );

    controller.addDrawables([textDrawable]);
  }

  // Function to add image to the canvas
  Future<void> addImage({
    required String path,
    double? x,
    double? y,
  }) async {
    try {
      final file = File(path);
      if (!file.existsSync()) {
        print('Image file not found: $path');
        return;
      }

      final bytes = await file.readAsBytes();
      final codecData = await ui.instantiateImageCodec(bytes);
      final frame = await codecData.getNextFrame();
      final uiImage = frame.image;

      final position = Offset(
        x ?? canvasCenter.dx,
        y ?? canvasCenter.dy,
      );

      final imageDrawable = ImageDrawable(
        position: position,
        image: uiImage,
      );

      controller.addDrawables([imageDrawable]);
    } catch (e) {
      print('Error adding image: $e');
    }
  }

  // Helper method to delete selected drawable
  void deleteSelected() {
    final selectedDrawable = controller.selectedObjectDrawable;
    if (selectedDrawable != null) {
      controller.removeDrawable(selectedDrawable);
    }
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    var theme = Theme.of(context);
    switch (name) {
      case "addText":
        addText(
          text: args["text"],
          x: parseDouble(args["x"]),
          y: parseDouble(args["y"]),
          fontSize: parseDouble(args["fontSize"]),
          color: parseColor(args["color"], theme),
          fontWeight: getFontWeight(args["fontWeight"]),
        );
        break;
      case "addImage":
        addImage(
          path: args["path"],
          x: parseDouble(args["x"]),
          y: parseDouble(args["y"]),
        );
        break;
      case "changeText":
        updateTextDrawable(
          newText: args["text"],
          newFontSize: parseDouble(args["fontSize"]),
          newColor: parseColor(args["color"], theme),
          newFontWeight: getFontWeight(args["fontWeight"]),
        );
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return ConstrainedControl(
      control: widget.control,
      child: LayoutBuilder(
        builder: (context, constraints) {
          canvasSize = Size(constraints.maxWidth, constraints.maxHeight);

          return KeyboardListener(
            focusNode: _focusNode,
            autofocus: true,
            onKeyEvent: (KeyEvent event) {
              if (event is KeyDownEvent &&
                  event.logicalKey == LogicalKeyboardKey.keyX &&
                  (HardwareKeyboard.instance.isControlPressed ||
                      HardwareKeyboard.instance.isMetaPressed)) {
                deleteSelected();
              }
            },
            child: GestureDetector(
              child: FlutterPainter(
                controller: controller,
                onSelectedObjectDrawableChanged: (drawable) {
                  sendSelectedTextInfo();
                },
              ),
            ),
          );
        },
      ),
    );
  }
}
