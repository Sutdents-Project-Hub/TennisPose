import 'package:flutter_test/flutter_test.dart';
import 'package:tennispose/features/pose_analysis/domain/pose_analysis.dart';

void main() {
  const calculator = ElbowAngleCalculator();

  group('ElbowAngleCalculator', () {
    test('calculates a right angle', () {
      final angle = calculator.calculate(
        const ArmLandmarks(
          shoulder: PosePoint(x: 0, y: 1, confidence: 1),
          elbow: PosePoint(x: 0, y: 0, confidence: 1),
          wrist: PosePoint(x: 1, y: 0, confidence: 1),
        ),
      );

      expect(angle, closeTo(90, 0.0001));
    });

    test('calculates a straight angle', () {
      final angle = calculator.calculate(
        const ArmLandmarks(
          shoulder: PosePoint(x: -1, y: 0, confidence: 1),
          elbow: PosePoint(x: 0, y: 0, confidence: 1),
          wrist: PosePoint(x: 1, y: 0, confidence: 1),
        ),
      );

      expect(angle, closeTo(180, 0.0001));
    });

    test('rejects duplicate points instead of fabricating an angle', () {
      expect(
        () => calculator.calculate(
          const ArmLandmarks(
            shoulder: PosePoint(x: 0, y: 0, confidence: 1),
            elbow: PosePoint(x: 0, y: 0, confidence: 1),
            wrist: PosePoint(x: 1, y: 0, confidence: 1),
          ),
        ),
        throwsA(isA<PoseAnalysisFailure>()),
      );
    });

    test('rejects non-finite geometry', () {
      expect(
        () => calculator.calculate(
          const ArmLandmarks(
            shoulder: PosePoint(x: double.nan, y: 0, confidence: 1),
            elbow: PosePoint(x: 0, y: 0, confidence: 1),
            wrist: PosePoint(x: 1, y: 0, confidence: 1),
          ),
        ),
        throwsA(isA<PoseAnalysisFailure>()),
      );
    });
  });

  group('TrophyPoseFeedbackRule', () {
    const rule = TrophyPoseFeedbackRule();

    test('includes both configured range boundaries', () {
      expect(rule.evaluate(90).isInRange, isTrue);
      expect(rule.evaluate(105).isInRange, isTrue);
    });

    test('suggests adjustment outside the configured range', () {
      expect(rule.evaluate(89.9).kind, FeedbackKind.adjustmentSuggested);
      expect(rule.evaluate(105.1).kind, FeedbackKind.adjustmentSuggested);
    });
  });

  test('PosePoint requires finite coordinates and sufficient confidence', () {
    expect(
      const PosePoint(x: 10, y: 20, confidence: 0.55).isReliable(0.55),
      isTrue,
    );
    expect(
      const PosePoint(x: 10, y: 20, confidence: 0.54).isReliable(0.55),
      isFalse,
    );
    expect(
      const PosePoint(
        x: double.infinity,
        y: 20,
        confidence: 1,
      ).isReliable(0.55),
      isFalse,
    );
  });
}
