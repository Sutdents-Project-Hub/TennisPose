import 'package:google_mlkit_pose_detection/google_mlkit_pose_detection.dart';

import '../domain/pose_analysis.dart';

class MlKitPoseAnalyzer implements PoseAnalyzer {
  MlKitPoseAnalyzer({
    ElbowAngleCalculator angleCalculator = const ElbowAngleCalculator(),
    TrophyPoseFeedbackRule feedbackRule = const TrophyPoseFeedbackRule(),
    this.minimumLandmarkConfidence = 0.55,
  }) : _angleCalculator = angleCalculator,
       _feedbackRule = feedbackRule,
       _detector = PoseDetector(
         options: PoseDetectorOptions(
           model: PoseDetectionModel.accurate,
           mode: PoseDetectionMode.single,
         ),
       );

  final PoseDetector _detector;
  final ElbowAngleCalculator _angleCalculator;
  final TrophyPoseFeedbackRule _feedbackRule;
  final double minimumLandmarkConfidence;
  bool _closed = false;

  @override
  Future<PoseAnalysisResult> analyze(String imagePath, ArmSide armSide) async {
    if (_closed) {
      throw const PoseAnalysisFailure('The pose analyzer is unavailable.');
    }

    final poses = await _detector.processImage(
      InputImage.fromFilePath(imagePath),
    );
    if (poses.isEmpty) {
      throw const PoseAnalysisFailure(
        'No person was detected. Try a clear, full upper-body side-view photo.',
      );
    }

    ArmLandmarks? bestLandmarks;
    for (final pose in poses) {
      final candidate = _readArm(pose, armSide);
      if (candidate == null ||
          !candidate.shoulder.isReliable(minimumLandmarkConfidence) ||
          !candidate.elbow.isReliable(minimumLandmarkConfidence) ||
          !candidate.wrist.isReliable(minimumLandmarkConfidence)) {
        continue;
      }
      if (bestLandmarks == null ||
          candidate.minimumConfidence > bestLandmarks.minimumConfidence) {
        bestLandmarks = candidate;
      }
    }

    if (bestLandmarks == null) {
      throw PoseAnalysisFailure(
        'The ${armSide.label.toLowerCase()} is not clear enough. Keep the shoulder, elbow, and wrist visible.',
      );
    }

    final angle = _angleCalculator.calculate(bestLandmarks);
    return PoseAnalysisResult(
      armSide: armSide,
      landmarks: bestLandmarks,
      angleDegrees: angle,
      feedback: _feedbackRule.evaluate(angle),
    );
  }

  ArmLandmarks? _readArm(Pose pose, ArmSide side) {
    final shoulder =
        pose.landmarks[side == ArmSide.left
            ? PoseLandmarkType.leftShoulder
            : PoseLandmarkType.rightShoulder];
    final elbow =
        pose.landmarks[side == ArmSide.left
            ? PoseLandmarkType.leftElbow
            : PoseLandmarkType.rightElbow];
    final wrist =
        pose.landmarks[side == ArmSide.left
            ? PoseLandmarkType.leftWrist
            : PoseLandmarkType.rightWrist];

    if (shoulder == null || elbow == null || wrist == null) {
      return null;
    }

    return ArmLandmarks(
      shoulder: _toPoint(shoulder),
      elbow: _toPoint(elbow),
      wrist: _toPoint(wrist),
    );
  }

  PosePoint _toPoint(PoseLandmark landmark) {
    return PosePoint(
      x: landmark.x,
      y: landmark.y,
      confidence: landmark.likelihood,
    );
  }

  @override
  Future<void> close() async {
    if (_closed) return;
    _closed = true;
    await _detector.close();
  }
}
