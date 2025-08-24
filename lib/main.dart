import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'pages/login_page.dart';
import 'pages/client/home.dart';
import 'pages/police/home.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  final MaterialColor customColor = const MaterialColor(
    0xFF00B0EB,
    <int, Color>{
      50: Color(0xFFE1F5FE),
      100: Color(0xFFB3E5FC),
      200: Color(0xFF81D4FA),
      300: Color(0xFF4FC3F7),
      400: Color(0xFF29B6F6),
      500: Color(0xFF00B0EB),
      600: Color(0xFF00A5DF),
      700: Color(0xFF0095CF),
      800: Color(0xFF0085BF),
      900: Color(0xFF006DAA),
    },
  );

  Future<Widget> _getInitialScreen() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    final role = prefs.getString('role');

    if (token != null && role != null) {
      switch (role) {
        case 'client':
          return const ClientHome();
        case 'police':
          return const PoliceHome();
        default:
          return const LoginPage();
      }
    }
    return const LoginPage();
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Widget>(
      future: _getInitialScreen(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const MaterialApp(
            home: Scaffold(body: Center(child: CircularProgressIndicator())),
            debugShowCheckedModeBanner: false,
          );
        }

        return MaterialApp(
          title: 'Aman Drive',
          theme: ThemeData(
            primarySwatch: customColor,
            scaffoldBackgroundColor: Colors.white,
            inputDecorationTheme: const InputDecorationTheme(
              border: OutlineInputBorder(),
            ),
          ),
          home: snapshot.data,
          debugShowCheckedModeBanner: false,
          routes: {
            '/login': (context) => const LoginPage(),
            '/client': (context) => const ClientHome(),
            '/police': (context) => const PoliceHome()
          },
        );
      },
    );
  }
}
