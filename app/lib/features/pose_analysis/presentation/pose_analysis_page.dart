import 'dart:io';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../data/ml_kit_pose_analyzer.dart';
import '../domain/pose_analysis.dart';
import 'result_overlay_painter.dart';

class PoseAnalysisPage extends StatefulWidget {
  const PoseAnalysisPage({super.key, this.analyzer, this.imagePicker});

  final PoseAnalyzer? analyzer;
  final ImagePicker? imagePicker;

  @override
  State<PoseAnalysisPage> createState() => _PoseAnalysisPageState();
}

class _PoseAnalysisPageState extends State<PoseAnalysisPage> {
  late final PoseAnalyzer _analyzer;
  late final ImagePicker _imagePicker;
  _SelectedPhoto? _photo;
  ArmSide _armSide = ArmSide.right;
  PoseAnalysisResult? _result;
  String? _message;
  bool _isAnalyzing = false;

  @override
  void initState() {
    super.initState();
    _analyzer = widget.analyzer ?? MlKitPoseAnalyzer();
    _imagePicker = widget.imagePicker ?? ImagePicker();
  }

  @override
  void dispose() {
    _photo?.image.dispose();
    _analyzer.close();
    super.dispose();
  }

  Future<void> _selectPhoto() async {
    if (_isAnalyzing) return;

    try {
      final selection = await _imagePicker.pickImage(
        source: ImageSource.gallery,
        maxWidth: 2400,
        imageQuality: 94,
        requestFullMetadata: false,
      );
      if (!mounted) return;
      if (selection == null) {
        setState(() => _message = 'No photo was selected.');
        return;
      }

      final decodedImage = await _decodeImage(selection.path);
      if (!mounted) {
        decodedImage.dispose();
        return;
      }

      final oldImage = _photo?.image;
      setState(() {
        _photo = _SelectedPhoto(file: selection, image: decodedImage);
        _result = null;
        _message = null;
      });
      oldImage?.dispose();
    } on PlatformException catch (error) {
      if (!mounted) return;
      setState(() {
        _message = error.code == 'photo_access_denied'
            ? 'Photo access was denied. Allow gallery access in device settings and try again.'
            : 'The gallery could not be opened. Please try again.';
      });
    } on FileSystemException {
      if (!mounted) return;
      setState(() {
        _message = 'That photo could not be read. Choose another JPEG or PNG.';
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _message = 'That photo could not be opened. Choose another image.';
      });
    }
  }

  Future<ui.Image> _decodeImage(String path) async {
    final bytes = await File(path).readAsBytes();
    final codec = await ui.instantiateImageCodec(bytes);
    try {
      final frame = await codec.getNextFrame();
      return frame.image;
    } finally {
      codec.dispose();
    }
  }

  Future<void> _analyzePhoto() async {
    final photo = _photo;
    if (photo == null || _isAnalyzing) return;

    setState(() {
      _isAnalyzing = true;
      _result = null;
      _message = null;
    });

    try {
      final result = await _analyzer.analyze(photo.file.path, _armSide);
      if (!mounted) return;
      setState(() => _result = result);
    } on PoseAnalysisFailure catch (error) {
      if (!mounted) return;
      setState(() => _message = error.message);
    } on PlatformException {
      if (!mounted) return;
      setState(() {
        _message =
            'On-device pose detection is unavailable for this photo. Try another clear image.';
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        _message =
            'The photo could not be analyzed. Try a clear side-view image with one person.';
      });
    } finally {
      if (mounted) setState(() => _isAnalyzing = false);
    }
  }

  void _selectArm(ArmSide side) {
    if (_isAnalyzing || side == _armSide) return;
    setState(() {
      _armSide = side;
      _result = null;
      _message = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: CustomScrollView(
          slivers: [
            SliverToBoxAdapter(child: _buildHeader(context)),
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(18, 8, 18, 40),
              sliver: SliverToBoxAdapter(
                child: Center(
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 760),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        _buildHero(context),
                        const SizedBox(height: 22),
                        _buildPhotoCard(context),
                        if (_photo != null) ...[
                          const SizedBox(height: 16),
                          _buildControlsCard(context),
                        ],
                        if (_message != null) ...[
                          const SizedBox(height: 16),
                          _InlineMessage(message: _message!),
                        ],
                        if (_result != null) ...[
                          const SizedBox(height: 16),
                          _buildResultCard(context, _result!),
                        ],
                        const SizedBox(height: 16),
                        const _PrivacyCard(),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 18, 20, 10),
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 760),
          child: Row(
            children: [
              Container(
                width: 38,
                height: 38,
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.secondary,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.sports_tennis, size: 21),
              ),
              const SizedBox(width: 11),
              const Expanded(
                child: Text(
                  'TennisPose',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 10,
                  vertical: 6,
                ),
                decoration: BoxDecoration(
                  border: Border.all(color: const Color(0xFFCBD2C3)),
                  borderRadius: BorderRadius.circular(999),
                ),
                child: const Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.phonelink_lock_outlined, size: 15),
                    SizedBox(width: 5),
                    Text(
                      'ON-DEVICE',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHero(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 18),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'ONE PHOTO · ONE ANGLE',
            style: TextStyle(
              color: Theme.of(context).colorScheme.primary,
              fontSize: 12,
              fontWeight: FontWeight.w800,
            ),
          ),
          const SizedBox(height: 10),
          Text(
            'Check the moment.\nUnderstand the angle.',
            style: Theme.of(context).textTheme.displaySmall,
          ),
          const SizedBox(height: 12),
          Text(
            'Choose a side-view Trophy Pose photo. TennisPose finds your selected arm and explains its elbow angle.',
            style: Theme.of(context).textTheme.bodyLarge,
          ),
        ],
      ),
    );
  }

  Widget _buildPhotoCard(BuildContext context) {
    final photo = _photo;
    return Card(
      clipBehavior: Clip.antiAlias,
      child: Padding(
        padding: const EdgeInsets.all(14),
        child: photo == null
            ? _EmptyPhotoState(onSelect: _selectPhoto)
            : Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(14),
                    child: AspectRatio(
                      aspectRatio: photo.image.width / photo.image.height,
                      child: ColoredBox(
                        color: const Color(0xFF11150F),
                        child: CustomPaint(
                          painter: ResultOverlayPainter(
                            image: photo.image,
                            result: _result,
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  OutlinedButton.icon(
                    onPressed: _isAnalyzing ? null : _selectPhoto,
                    icon: const Icon(Icons.photo_library_outlined, size: 19),
                    label: const Text('Choose a different photo'),
                  ),
                ],
              ),
      ),
    );
  }

  Widget _buildControlsCard(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Select the arm to inspect',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 6),
            Text(
              'Choose the arm that is most visible in the photo.',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 14),
            SegmentedButton<ArmSide>(
              segments: ArmSide.values
                  .map(
                    (side) => ButtonSegment<ArmSide>(
                      value: side,
                      label: Text(side.label),
                      icon: Icon(
                        side == ArmSide.left
                            ? Icons.keyboard_double_arrow_left
                            : Icons.keyboard_double_arrow_right,
                      ),
                    ),
                  )
                  .toList(),
              selected: {_armSide},
              onSelectionChanged: _isAnalyzing
                  ? null
                  : (selection) => _selectArm(selection.first),
              showSelectedIcon: false,
            ),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: _isAnalyzing ? null : _analyzePhoto,
              icon: _isAnalyzing
                  ? const SizedBox.square(
                      dimension: 18,
                      child: CircularProgressIndicator(strokeWidth: 2.4),
                    )
                  : const Icon(Icons.auto_awesome_outlined, size: 20),
              label: Text(
                _isAnalyzing ? 'Analyzing on device…' : 'Analyze elbow angle',
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildResultCard(BuildContext context, PoseAnalysisResult result) {
    final isInRange = result.feedback.isInRange;
    final statusColor = isInRange
        ? const Color(0xFF15803D)
        : const Color(0xFFB42318);
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  width: 44,
                  height: 44,
                  decoration: BoxDecoration(
                    color: statusColor.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(13),
                  ),
                  child: Icon(
                    isInRange ? Icons.check_circle_outline : Icons.tune,
                    color: statusColor,
                  ),
                ),
                const SizedBox(width: 13),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        result.feedback.title,
                        style: Theme.of(
                          context,
                        ).textTheme.titleLarge?.copyWith(color: statusColor),
                      ),
                      const SizedBox(height: 3),
                      Text(result.feedback.message),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFFF0F2EB),
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: _Metric(
                      label: '${result.armSide.label} angle',
                      value: '${result.angleDegrees.toStringAsFixed(0)}°',
                    ),
                  ),
                  Container(
                    width: 1,
                    height: 48,
                    color: const Color(0xFFD3D9CE),
                  ),
                  const Expanded(
                    child: _Metric(label: 'Demo range', value: '90–105°'),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 12),
            Text(
              'This range is a configurable demonstration rule, not medical or professional coaching advice.',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
          ],
        ),
      ),
    );
  }
}

class _SelectedPhoto {
  const _SelectedPhoto({required this.file, required this.image});

  final XFile file;
  final ui.Image image;
}

class _EmptyPhotoState extends StatelessWidget {
  const _EmptyPhotoState({required this.onSelect});

  final VoidCallback onSelect;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(22, 38, 22, 28),
      decoration: BoxDecoration(
        color: const Color(0xFFF7F8F3),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(
        children: [
          Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              color: Theme.of(
                context,
              ).colorScheme.secondary.withValues(alpha: 0.18),
              shape: BoxShape.circle,
            ),
            child: const Icon(Icons.add_photo_alternate_outlined, size: 28),
          ),
          const SizedBox(height: 18),
          Text(
            'Start with one clear photo',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 7),
          Text(
            'Use a side-view image with one person and the shoulder, elbow, and wrist visible.',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 20),
          FilledButton.icon(
            onPressed: onSelect,
            icon: const Icon(Icons.photo_library_outlined, size: 20),
            label: const Text('Choose photo'),
          ),
        ],
      ),
    );
  }
}

class _InlineMessage extends StatelessWidget {
  const _InlineMessage({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFFFFF1EF),
        border: Border.all(color: const Color(0xFFF3C7C1)),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(Icons.info_outline, color: Theme.of(context).colorScheme.error),
          const SizedBox(width: 10),
          Expanded(child: Text(message)),
        ],
      ),
    );
  }
}

class _PrivacyCard extends StatelessWidget {
  const _PrivacyCard();

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Icon(Icons.lock_outline, size: 22),
            const SizedBox(width: 11),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Your photo stays on this device',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 5),
                  Text(
                    'TennisPose does not create an account, upload the photo, or save an analysis history.',
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _Metric extends StatelessWidget {
  const _Metric({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: Theme.of(context).textTheme.bodyMedium),
        const SizedBox(height: 2),
        Text(
          value,
          style: const TextStyle(
            fontSize: 24,
            height: 1.2,
            fontWeight: FontWeight.w800,
            fontFeatures: [ui.FontFeature.tabularFigures()],
          ),
        ),
      ],
    );
  }
}
