import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class PredictService {
  static Future<String> sendAudio(File audioFile) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('token');

      var request = http.MultipartRequest(
        'POST',
        Uri.parse('http://192.168.1.5:5000/predict'),
      );

      // Set Authorization header
      if (token != null && token.isNotEmpty) {
        request.headers['Authorization'] = 'Bearer $token';
      }

      request.files.add(
        await http.MultipartFile.fromPath('file', audioFile.path),
      );

      var response = await request.send();

      if (response.statusCode == 200) {
        final responseBody = await response.stream.bytesToString();
        final jsonResponse = jsonDecode(responseBody);
        print(jsonResponse);
        return jsonResponse['predicted_class'].toString();
      } else {
        print('Error: ${response.statusCode}');
        return 'Error';
      }
    } catch (e) {
      print('Exception in sendAudio: $e');
      return 'Error';
    }
  }
}
