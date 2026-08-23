import 'dart:math' as math;

enum ArmSide {
  left('Left arm'),
  right('Right arm');

  const ArmSide(this.label);

  final String label;
}

class PosePoint {
  const PosePoint({required this.x, required this.y, required this.confidence});

  final double x;
  final double y;
  final double confidence;

  bool isReliable(double minimumConfidence) {
    return x.isFinite &&
        y.isFinite &&
        confidence.isFinite &&
        confidence >= minimumConfidence;
  }
}

class ArmLandmarks {
  const ArmLandmarks({
    required this.shoulder,
    required this.elbow,
    required this.wrist,
  });

  final PosePoint shoulder;
  final PosePoint elbow;
  final PosePoint wrist;

  double get minimumConfidence => math.min(
    shoulder.confidence,
    math.min(elbow.confidence, wrist.confidence),
  );
}

enum FeedbackKind { inRange, adjustmentSuggested }

class PoseFeedback {
  const PoseFeedback({
    required this.kind,
    required this.title,
    required this.message,
  });

  final FeedbackKind kind;
  final String title;
  final String message;

  bool get isInRange => kind == FeedbackKind.inRange;
}

class PoseAnalysisResult {
  const PoseAnalysisResult({
    required this.armSide,
    required this.landmarks,
    required this.angleDegrees,
    required this.feedback,
  });

  final ArmSide armSide;
  final ArmLandmarks landmarks;
  final double angleDegrees;
  final PoseFeedback feedback;
}

class PoseAnalysisFailure implements Exception {
  const PoseAnalysisFailure(this.message);

  final String message;

  @override
  String toString() => message;
}

abstract interface class PoseAnalyzer {
  Future<PoseAnalysisResult> analyze(String imagePath, ArmSide armSide);

  Future<void> close();
}

class ElbowAngleCalculator {
  const ElbowAngleCalculator();

  double calculate(ArmLandmarks landmarks) {
    final shoulderVectorX = landmarks.shoulder.x - landmarks.elbow.x;
    final shoulderVectorY = landmarks.shoulder.y - landmarks.elbow.y;
    final wristVectorX = landmarks.wrist.x - landmarks.elbow.x;
    final wristVectorY = landmarks.wrist.y - landmarks.elbow.y;

    final shoulderLength = math.sqrt(
      shoulderVectorX * shoulderVectorX + shoulderVectorY * shoulderVectorY,
    );
    final wristLength = math.sqrt(
      wristVectorX * wristVectorX + wristVectorY * wristVectorY,
    );

    if (!shoulderLength.isFinite ||
        !wristLength.isFinite ||
        shoulderLength == 0 ||
        wristLength == 0) {
      throw const PoseAnalysisFailure(
        'The arm landmarks do not form a measurable angle.',
      );
    }

    final dot = shoulderVectorX * wristVectorX + shoulderVectorY * wristVectorY;
    final cosine = (dot / (shoulderLength * wristLength)).clamp(-1.0, 1.0);
    final angle = math.acos(cosine) * 180 / math.pi;

    if (!angle.isFinite) {
      throw const PoseAnalysisFailure(
        'The arm landmarks do not form a measurable angle.',
      );
    }

    return angle;
  }
}

class TrophyPoseFeedbackRule {
  const TrophyPoseFeedbackRule({
    this.minimumDegrees = 90,
    this.maximumDegrees = 105,
  }) : assert(minimumDegrees < maximumDegrees);

  final double minimumDegrees;
  final double maximumDegrees;

  PoseFeedback evaluate(double angleDegrees) {
    if (angleDegrees >= minimumDegrees && angleDegrees <= maximumDegrees) {
      return const PoseFeedback(
        kind: FeedbackKind.inRange,
        title: 'In the demo range',
        message:
            'Your selected elbow is within the configured Trophy Pose range.',
      );
    }

    final direction = angleDegrees < minimumDegrees ? 'more open' : 'less open';
    return PoseFeedback(
      kind: FeedbackKind.adjustmentSuggested,
      title: 'Adjustment suggested',
      message:
          'Try a $direction elbow position, then compare another side-view photo.',
    );
  }
}
