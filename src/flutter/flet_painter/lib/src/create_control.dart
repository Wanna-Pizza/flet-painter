import 'package:flet/flet.dart';

import 'flet_painter.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "flet_painter":
      return FletPainterControl(
        parent: args.parent,
        control: args.control,
        backend: args.backend,
        key: args.key,
        children: args.children,
        parentAdaptive: args.parentAdaptive,
        parentDisabled: args.parentDisabled,
      );
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
