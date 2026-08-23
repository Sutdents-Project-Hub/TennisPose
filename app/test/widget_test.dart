import 'package:flutter_test/flutter_test.dart';
import 'package:tennispose/features/pose_analysis/domain/pose_analysis.dart';
import 'package:tennispose/features/pose_analysis/presentation/pose_analysis_page.dart';
import 'package:tennispose/main.dart';

void main() {
  testWidgets('shows the focused idle flow and privacy boundary', (
    tester,
  ) async {
    final analyzer = _FakeAnalyzer();

    await tester.pumpWidget(
      TennisPoseApp(home: PoseAnalysisPage(analyzer: analyzer)),
    );

    expect(find.text('TennisPose'), findsOneWidget);
    expect(find.text('Start with one clear photo'), findsOneWidget);
    expect(find.text('Choose photo'), findsOneWidget);
    expect(find.text('Your photo stays on this device'), findsOneWidget);
    expect(find.text('Analyze elbow angle'), findsNothing);
  });
}

class _FakeAnalyzer implements PoseAnalyzer {
  @override
  Future<PoseAnalysisResult> analyze(String imagePath, ArmSide armSide) {
    throw UnimplementedError();
  }

  @override
  Future<void> close() async {}
}
