import 'package:flutter/material.dart';

class WavePainter extends CustomPainter {
  final List<double> waveformData;
  final Color color;
  final double heightFactor;
  final bool isRecording;

  WavePainter({
    required this.waveformData,
    required this.color,
    this.heightFactor = 0.6,
    this.isRecording = true,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    final barWidth = size.width / waveformData.length;
    final centerY = size.height / 2;

    if (!isRecording) {
      final baselinePaint = Paint()
        ..color = color
        ..strokeWidth = 2;

      canvas.drawLine(
        Offset(0, centerY),
        Offset(size.width, centerY),
        baselinePaint,
      );

      // dotted baseline
      // double spacing = 10;
      // for (double x = 0; x < size.width; x += spacing) {
      //   canvas.drawCircle(Offset(x, centerY), 2, paint);
      // }
      return;
    }

    for (int i = 0; i < waveformData.length; i++) {
      final normalized = (waveformData[i] + 60) / 60;
      final barHeight = normalized * size.height * heightFactor;
      final dx = i * barWidth;
      canvas.drawRect(
        Rect.fromLTWH(dx, centerY - barHeight / 2, barWidth * 0.8, barHeight),
        paint,
      );
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
