import 'dart:ui' as ui;

import 'package:flutter/material.dart';

import '../domain/pose_analysis.dart';

class ResultOverlayPainter extends CustomPainter {
  const ResultOverlayPainter({required this.image, this.result});

  final ui.Image image;
  final PoseAnalysisResult? result;

  @override
  void paint(Canvas canvas, Size size) {
    final source = Rect.fromLTWH(
      0,
      0,
      image.width.toDouble(),
      image.height.toDouble(),
    );
    final fitted = applyBoxFit(BoxFit.contain, source.size, size);
    final destination = Alignment.center.inscribe(
      fitted.destination,
      Offset.zero & size,
    );

    paintImage(
      canvas: canvas,
      rect: destination,
      image: image,
      fit: BoxFit.contain,
      filterQuality: FilterQuality.high,
    );

    final analysis = result;
    if (analysis == null) return;

    final statusColor = analysis.feedback.isInRange
        ? const Color(0xFF15803D)
        : const Color(0xFFCC2E2E);
    final points = [
      _mapPoint(analysis.landmarks.shoulder, source, destination),
      _mapPoint(analysis.landmarks.elbow, source, destination),
      _mapPoint(analysis.landmarks.wrist, source, destination),
    ];

    final shadowPaint = Paint()
      ..color = Colors.black.withValues(alpha: 0.52)
      ..strokeWidth = 9
      ..strokeCap = StrokeCap.round;
    final linePaint = Paint()
      ..color = statusColor
      ..strokeWidth = 5
      ..strokeCap = StrokeCap.round;

    canvas.drawLine(points[0], points[1], shadowPaint);
    canvas.drawLine(points[1], points[2], shadowPaint);
    canvas.drawLine(points[0], points[1], linePaint);
    canvas.drawLine(points[1], points[2], linePaint);

    for (final point in points) {
      canvas.drawCircle(point, 9, Paint()..color = Colors.white);
      canvas.drawCircle(point, 6, Paint()..color = statusColor);
    }

    _paintAngleLabel(
      canvas,
      points[1] + const Offset(14, -42),
      '${analysis.angleDegrees.toStringAsFixed(0)}°',
      statusColor,
      size,
    );
  }

  Offset _mapPoint(PosePoint point, Rect source, Rect destination) {
    return Offset(
      destination.left + point.x / source.width * destination.width,
      destination.top + point.y / source.height * destination.height,
    );
  }

  void _paintAngleLabel(
    Canvas canvas,
    Offset preferredOffset,
    String label,
    Color color,
    Size canvasSize,
  ) {
    final textPainter = TextPainter(
      text: TextSpan(
        text: label,
        style: const TextStyle(
          color: Colors.white,
          fontSize: 17,
          fontWeight: FontWeight.w800,
          fontFeatures: [ui.FontFeature.tabularFigures()],
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout();

    const padding = EdgeInsets.symmetric(horizontal: 11, vertical: 7);
    final labelSize = Size(
      textPainter.width + padding.horizontal,
      textPainter.height + padding.vertical,
    );
    final offset = Offset(
      preferredOffset.dx.clamp(8, canvasSize.width - labelSize.width - 8),
      preferredOffset.dy.clamp(8, canvasSize.height - labelSize.height - 8),
    );
    final rect = offset & labelSize;

    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, const Radius.circular(10)),
      Paint()..color = color,
    );
    textPainter.paint(canvas, offset + Offset(padding.left, padding.top));
  }

  @override
  bool shouldRepaint(covariant ResultOverlayPainter oldDelegate) {
    return oldDelegate.image != image || oldDelegate.result != result;
  }
}
