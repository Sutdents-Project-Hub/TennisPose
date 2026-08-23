import 'package:flutter/material.dart';

import 'features/pose_analysis/presentation/pose_analysis_page.dart';

void main() {
  runApp(const TennisPoseApp());
}

class TennisPoseApp extends StatelessWidget {
  const TennisPoseApp({super.key, this.home});

  final Widget? home;

  @override
  Widget build(BuildContext context) {
    const seed = Color(0xFF87B522);
    final colorScheme =
        ColorScheme.fromSeed(
          seedColor: seed,
          brightness: Brightness.light,
          surface: const Color(0xFFF7F8F3),
        ).copyWith(
          primary: const Color(0xFF24351F),
          onPrimary: Colors.white,
          secondary: seed,
          onSecondary: const Color(0xFF16220F),
          outline: const Color(0xFFCBD2C3),
          error: const Color(0xFFB42318),
        );

    return MaterialApp(
      title: 'TennisPose',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: colorScheme,
        scaffoldBackgroundColor: const Color(0xFFF1F3EC),
        useMaterial3: true,
        textTheme: const TextTheme(
          displaySmall: TextStyle(
            fontSize: 38,
            height: 1.08,
            fontWeight: FontWeight.w800,
            color: Color(0xFF172016),
          ),
          headlineSmall: TextStyle(
            fontSize: 24,
            height: 1.2,
            fontWeight: FontWeight.w700,
            color: Color(0xFF172016),
          ),
          titleLarge: TextStyle(
            fontSize: 19,
            height: 1.3,
            fontWeight: FontWeight.w700,
            color: Color(0xFF172016),
          ),
          bodyLarge: TextStyle(
            fontSize: 16,
            height: 1.5,
            color: Color(0xFF465143),
          ),
          bodyMedium: TextStyle(
            fontSize: 14,
            height: 1.45,
            color: Color(0xFF5A6556),
          ),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            minimumSize: const Size(0, 52),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
            textStyle: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
        cardTheme: CardThemeData(
          elevation: 0,
          color: const Color(0xFFFDFEF9),
          shape: RoundedRectangleBorder(
            side: const BorderSide(color: Color(0xFFDDE2D7)),
            borderRadius: BorderRadius.circular(22),
          ),
        ),
      ),
      home: home ?? const PoseAnalysisPage(),
    );
  }
}
