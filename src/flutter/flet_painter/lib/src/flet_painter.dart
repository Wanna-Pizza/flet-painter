import 'dart:io';
import 'dart:ui' as ui;
import 'package:flet/flet.dart';
import 'package:google_fonts/google_fonts.dart';
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
  // Constants
  static const String _defaultText = "Text";
  static const double _defaultFontSize = 24.0;
  static const String _defaultFontFamily = 'Roboto';

  // Controllers and state
  late PainterController controller;
  final FocusNode _focusNode = FocusNode();
  Size? canvasSize;
  String defaultText = _defaultText;

  // Layer tracking
  final LayerManager _layerManager = LayerManager();

  @override
  void initState() {
    super.initState();
    _initController();
    _setupWidgets();
    widget.control.addInvokeMethodListener(_handleInvokeMethod);
  }

  void _initController() {
    controller = PainterController();
    controller.addListener(_handleControllerUpdate);

    // Initialize text settings
    controller.textSettings = TextSettings(
      textStyle: const TextStyle(
        fontWeight: FontWeight.bold,
        color: Colors.blue,
        fontSize: _defaultFontSize,
      ),
    );
  }

  void _handleControllerUpdate() {
    final sel = controller.selectedObjectDrawable;
    if (sel is TextDrawable) {
      _sendSelectedTextInfo();
    }
  }

  @override
  void dispose() {
    _focusNode.dispose();
    controller.dispose();
    widget.control.removeInvokeMethodListener(_handleInvokeMethod);
    super.dispose();
  }

  // ===== Event Methods =====

  void _sendEvent(String name, [dynamic data]) {
    widget.control.triggerEvent(name, data);
  }

  void _sendSelectedTextInfo() {
    final selectedDrawable = controller.selectedObjectDrawable;

    if (selectedDrawable is TextDrawable) {
      _sendEvent("on_selected_text", {
        "value": selectedDrawable.text,
        "style": selectedDrawable.style,
      });
    } else {
      _sendEvent("on_selected_text", {
        "value": null,
        "style": null,
      });
    }
  }

  // ===== Canvas Helper Methods =====

  Offset get _canvasCenter {
    if (canvasSize == null) return const Offset(100, 100);
    return Offset(canvasSize!.width / 2, canvasSize!.height / 2);
  }

  // ===== Text Handling Methods =====

  void addText({
    String? fontFamily,
    String? text,
    double? x,
    double? y,
    double? fontSize,
    Color? color,
    FontWeight? fontWeight,
  }) {
    final position = Offset(
      x ?? _canvasCenter.dx,
      y ?? _canvasCenter.dy,
    );

    final textDrawable = TextDrawable(
      position: position,
      text: text ?? defaultText,
      style: GoogleFonts.getFont(
        fontFamily ?? _defaultFontFamily,
        fontSize: fontSize ?? _defaultFontSize,
        color: color ?? Colors.black,
        fontWeight: fontWeight ?? FontWeight.normal,
      ),
    );

    controller.addDrawables([textDrawable]);
  }

  void updateTextDrawable({
    String? newText,
    String? newFontFamily,
    double? newFontSize,
    Color? newColor,
    FontWeight? newFontWeight,
    double? newRotation,
    double? newScale,
  }) {
    final selectedDrawable = controller.selectedObjectDrawable;

    if (selectedDrawable is TextDrawable) {
      final baseStyle = selectedDrawable.style;

      // Always preserve existing values when not explicitly set
      final updatedText = newText ?? selectedDrawable.text;
      final updatedRotation = newRotation ?? selectedDrawable.rotationAngle;
      final updatedScale = newScale ?? selectedDrawable.scale;

      TextStyle updatedStyle;
      if (newFontFamily != null) {
        // rebuild style with new font family
        updatedStyle = GoogleFonts.getFont(
          newFontFamily,
          fontSize: newFontSize ?? baseStyle.fontSize,
          color: newColor ?? baseStyle.color,
          fontWeight: newFontWeight ?? baseStyle.fontWeight,
        );
      } else {
        // preserve existing font family, apply other changes
        updatedStyle = baseStyle.copyWith(
          color: newColor,
          fontSize: newFontSize,
          fontWeight: newFontWeight,
        );
      }

      // Create updated drawable with all preserved properties
      final updatedDrawable = selectedDrawable.copyWith(
        text: updatedText,
        style: updatedStyle,
        rotation: updatedRotation,
        scale: updatedScale,
      );

      // Update immediately with setState to ensure UI refresh
      setState(() {
        controller.replaceDrawable(selectedDrawable, updatedDrawable);
      });
    } else {
      print("No TextDrawable selected or invalid drawable type.");
    }
  }

  // ===== Image Handling Methods =====

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
        x ?? _canvasCenter.dx,
        y ?? _canvasCenter.dy,
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

  // ===== Layer Management =====

  void _setupWidgets() {
    var layersData = widget.control.get("layers");
    if (layersData == null) return;

    _processLayers(layersData);
  }

  void _processLayers(dynamic layersData) {
    if (layersData is List) {
      _processLayersList(layersData);
    } else if (layersData is Map<String, dynamic>) {
      _processSingleLayer(layersData);
    }

    // Update tracking
    _layerManager.previousLayers = layersData;
  }

  void _processLayersList(List layers) {
    for (var layer in layers) {
      String id = layer["id"] ?? "${layer.hashCode}";
      if (_layerManager.isProcessed(id)) continue;

      _processSingleLayer(layer);
      _layerManager.markProcessed(id);
    }
  }

  void _processSingleLayer(Map<String, dynamic> layer) {
    String id = layer["id"] ?? "${layer.hashCode}";
    if (_layerManager.isProcessed(id)) return;

    String type = layer["type"] ?? "";

    if (type == "text") {
      defaultText = layer["text"] ?? defaultText;
      addText(
        text: defaultText,
        color: parseColor(layer["color"], Theme.of(context)),
        fontSize: parseDouble(layer["fontSize"]),
        fontWeight: getFontWeight(layer["fontWeight"]),
      );
    } else if (type == "image") {
      addImage(path: layer["path"] ?? "");
    }

    _layerManager.markProcessed(id);
  }

  // ===== Deletion Methods =====

  void deleteSelected() {
    final selectedDrawable = controller.selectedObjectDrawable;
    if (selectedDrawable != null) {
      setState(() {
        controller.removeDrawable(selectedDrawable);
      });
      // Restore focus after deletion
      _focusNode.requestFocus();
    }
  }

  // ===== Method Invocation Handling =====

  Future<dynamic> _handleInvokeMethod(String name, dynamic args) async {
    var theme = Theme.of(context);
    switch (name) {
      case "addText":
        addText(
          text: args["text"],
          fontFamily: args["fontFamily"],
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
          newFontFamily: args["fontFamily"],
          newFontSize: parseDouble(args["fontSize"]),
          newColor: parseColor(args["color"], theme),
          newFontWeight: getFontWeight(args["fontWeight"]),
          newRotation: parseDouble(args["rotation"]),
          newScale: parseDouble(args["scale"]),
        );
        break;
    }
  }

  // ===== Widget Building =====

  @override
  Widget build(BuildContext context) {
    return ConstrainedControl(
      control: widget.control,
      child: LayoutBuilder(
        builder: (context, constraints) {
          canvasSize = Size(constraints.maxWidth, constraints.maxHeight);
          return _buildKeyboardHandler();
        },
      ),
    );
  }

  Widget _buildKeyboardHandler() {
    return Focus(
      focusNode: _focusNode,
      autofocus: true,
      onKeyEvent: _handleKeyEvent,
      child: _buildShortcutsWrapper(),
    );
  }

  KeyEventResult _handleKeyEvent(FocusNode node, KeyEvent event) {
    if (event is KeyDownEvent &&
        event.logicalKey == LogicalKeyboardKey.keyX &&
        (HardwareKeyboard.instance.isControlPressed ||
            HardwareKeyboard.instance.isMetaPressed)) {
      deleteSelected();
      return KeyEventResult.handled;
    }
    return KeyEventResult.ignored;
  }

  Widget _buildShortcutsWrapper() {
    return Shortcuts(
      shortcuts: <ShortcutActivator, Intent>{
        LogicalKeySet(LogicalKeyboardKey.control, LogicalKeyboardKey.keyX):
            const DeleteIntent(),
        LogicalKeySet(LogicalKeyboardKey.meta, LogicalKeyboardKey.keyX):
            const DeleteIntent(),
      },
      child: _buildActionsWrapper(),
    );
  }

  Widget _buildActionsWrapper() {
    return Actions(
      actions: <Type, Action<Intent>>{
        DeleteIntent: CallbackAction<DeleteIntent>(
          onInvoke: (intent) {
            deleteSelected();
            return null;
          },
        ),
      },
      child: _buildPainter(),
    );
  }

  Widget _buildPainter() {
    return GestureDetector(
      onTap: () => _focusNode.requestFocus(),
      child: FlutterPainter(
        controller: controller,
        onSelectedObjectDrawableChanged: (drawable) {
          _sendSelectedTextInfo();
          _focusNode.requestFocus();
        },
      ),
    );
  }
}

// ===== Helper Classes =====

class LayerManager {
  dynamic previousLayers;
  final List<String> processedLayerIds = [];

  bool isProcessed(String id) => processedLayerIds.contains(id);

  void markProcessed(String id) {
    processedLayerIds.add(id);
  }
}

class DeleteIntent extends Intent {
  const DeleteIntent();
}
