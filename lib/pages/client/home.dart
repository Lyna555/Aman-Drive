import 'dart:async';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_sound/flutter_sound.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';
import '/services/audio_service.dart';
import 'wave_painter.dart';

class ClientHome extends StatefulWidget {
  const ClientHome({super.key});

  @override
  State<ClientHome> createState() => _ClientHomePageState();
}

class _ClientHomePageState extends State<ClientHome>
    with SingleTickerProviderStateMixin {
  final FlutterSoundRecorder _recorder = FlutterSoundRecorder();
  bool _isRecording = false;
  bool _isCrashDetected = false;
  String _username = "";
  String _email = "";
  Timer? _timer;
  Timer? _recordingTimer;
  Duration _elapsed = Duration.zero;

  final int _waveSamples = 60;
  late List<double> _waveformData;

  @override
  void initState() {
    super.initState();
    _waveformData = List.filled(_waveSamples, -60.0, growable: true);
    _initRecorder();
    _loadUserInfo();
  }

  Future<void> _loadUserInfo() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _username = prefs.getString('username') ?? '';
      _email = prefs.getString('email') ?? '';
    });
  }

  Future<void> _initRecorder() async {
    await Permission.microphone.request();
    await _recorder.openRecorder();
  }

  void _startRecordingLoop() async {
    final dir = await getTemporaryDirectory();

    await _recorder.startRecorder(
      codec: Codec.pcm16WAV,
      numChannels: 1,
      sampleRate: 16000,
      toFile: p.join(dir.path, 'current.wav'),
    );

    _recorder.setSubscriptionDuration(const Duration(milliseconds: 60));
    _recorder.onProgress?.listen((event) {
      if (event.decibels != null) {
        final db = event.decibels!;
        setState(() {
          if (_waveformData.length >= _waveSamples) {
            _waveformData.removeAt(0);
          }
          _waveformData.add(db);
        });
      }
    });

    _timer = Timer.periodic(const Duration(seconds: 5), (_) async {
      final timestamp = DateTime.now().millisecondsSinceEpoch;
      final clipPath = p.join(dir.path, 'audio_$timestamp.wav');

      await _recorder.stopRecorder();
      final currentPath = p.join(dir.path, 'current.wav');
      File(currentPath).copySync(clipPath);

      await _recorder.startRecorder(
        codec: Codec.pcm16WAV,
        numChannels: 1,
        sampleRate: 16000,
        toFile: currentPath,
      );

      try {
        String result = await PredictService.sendAudio(File(clipPath));
        if (!mounted) return;
        setState(() {
          _isCrashDetected = result == "1";
        });
      } catch (e) {
        debugPrint("Error sending audio: $e");
      } finally {
        File(clipPath).deleteSync();
      }
    });

    setState(() {
      _isRecording = true;
      _isCrashDetected = false;
      _elapsed = Duration.zero;
    });

    _recordingTimer = Timer.periodic(const Duration(milliseconds: 50), (_) {
      setState(() {
        _elapsed += const Duration(milliseconds: 50);
      });
    });
  }

  void _stopRecordingLoop() {
    _timer?.cancel();
    _recordingTimer?.cancel();
    try {
      _recorder.stopRecorder();
    } catch (_) {}
    setState(() {
      _isRecording = false;
      _isCrashDetected = false;
      _elapsed = Duration.zero;
      _waveformData = List.filled(_waveSamples, -60.0, growable: true);
    });
  }

  Color get _micColor {
    if (_isCrashDetected) return Colors.red;
    if (_isRecording) return const Color(0xff1fa5e7);
    return const Color(0xff1fa5e7);
  }

  String _formatDuration(Duration duration) {
    String twoDigits(int n) => n.toString().padLeft(2, '0');
    return "${twoDigits(duration.inHours)}:"
        "${twoDigits(duration.inMinutes.remainder(60))}:"
        "${twoDigits(duration.inSeconds.remainder(60))}";
  }

  @override
  void dispose() {
    _recorder.closeRecorder();
    _timer?.cancel();
    _recordingTimer?.cancel();
    super.dispose();
  }

  void _launchEmail() async {
    final Uri emailLaunchUri = Uri(
      scheme: 'mailto',
      path: 'bouglina3@gmail.com',
      query: Uri.encodeFull(
          'subject=Support Request Aman Drive&body=Hello, I need help with...'),
    );

    if (await canLaunchUrl(emailLaunchUri)) {
      await launchUrl(emailLaunchUri);
    } else if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Could not open email app')),
      );
    }
  }

  void _showAboutUsDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('About Us'),
          content: const Text(
            'Aman Drive is a smart safety app that detects car crashes in real-time using audio signals. '
            'It helps enhance road safety and provide instant response options.\n\n'
            'Developed for a safer future.',
          ),
          actions: [
            TextButton(
              child: const Text('Close'),
              onPressed: () => Navigator.of(context).pop(),
            ),
          ],
        );
      },
    );
  }

  void _toggleRecording() {
    if (_isRecording) {
      _stopRecordingLoop();
    } else {
      _startRecordingLoop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        surfaceTintColor: Colors.transparent,
        shadowColor: Colors.transparent,
        elevation: 0,
        iconTheme: const IconThemeData(
          color: Color(0xff1b93ce),
          size: 35,
        ),
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: <Widget>[
            UserAccountsDrawerHeader(
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  colors: [Colors.blue, Colors.lightBlueAccent],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              accountName: Text(
                _username,
                style: const TextStyle(color: Colors.white),
              ),
              accountEmail: Text(
                _email,
                style: const TextStyle(color: Colors.white),
              ),
              currentAccountPicture: const CircleAvatar(
                backgroundImage: AssetImage('assets/images/user.png'),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('Home Page'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.contact_mail),
              title: const Text('Contact Us'),
              onTap: () {
                Navigator.pop(context);
                _launchEmail();
              },
            ),
            ListTile(
              leading: const Icon(Icons.info),
              title: const Text('About Us'),
              onTap: () {
                Navigator.pop(context);
                _showAboutUsDialog();
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.logout),
              title: const Text('Logout'),
              onTap: () async {
                final prefs = await SharedPreferences.getInstance();
                await prefs.clear();
                if (!mounted) return;
                Navigator.of(context)
                    .pushNamedAndRemoveUntil('/login', (route) => false);
              },
            ),
          ],
        ),
      ),
      body: Stack(
        children: [
          Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 90),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(
                        vertical: 30, horizontal: 40),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(20),
                      gradient: const LinearGradient(
                        colors: [
                          Color(0xffffffff),
                          Color(0xffb3e5fa),
                          Color(0xff9eddf2),
                          Color(0xfffeeffa),
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.2),
                          spreadRadius: 2,
                          blurRadius: 5,
                          offset: const Offset(2, 4),
                        ),
                      ],
                    ),
                    child: Column(
                      children: [
                        const Text(
                          "Listening Duration",
                          style: TextStyle(fontSize: 16, color: Colors.black54),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          _formatDuration(_elapsed),
                          style: const TextStyle(
                            fontSize: 48,
                            fontWeight: FontWeight.bold,
                            color: Colors.black87,
                          ),
                        ),
                      ],
                    ),
                  ),
                  CustomPaint(
                    painter: WavePainter(
                      waveformData: _waveformData,
                      color: _micColor,
                      isRecording: _isRecording,
                    ),
                    size: const Size(400, 60),
                  ),
                  Column(
                    children: [
                      GestureDetector(
                        onTap: _toggleRecording,
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          width: 160,
                          height: 160,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            gradient: const RadialGradient(
                              colors: [
                                Color.fromRGBO(255, 255, 255, 1.0),
                                Color.fromRGBO(255, 255, 255, 1.0)
                              ],
                              radius: 0.85,
                              focal: Alignment.center,
                              focalRadius: 0.1,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: _micColor.withOpacity(0.4),
                                blurRadius: 25,
                                spreadRadius: 6,
                              )
                            ],
                          ),
                          child: Icon(
                            _isRecording ? Icons.stop : Icons.mic,
                            size: 72,
                            color: _micColor,
                          ),
                        ),
                      ),
                      const SizedBox(height: 20),
                      Text(
                        _isCrashDetected
                            ? '🚨 Crash Detected!'
                            : _isRecording
                                ? 'Listening...'
                                : 'Tap to Start',
                        style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w600,
                            color: _micColor),
                      ),
                    ],
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
