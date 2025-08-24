import 'client.dart';
import 'police.dart';

class Accident {
  final int id;
  final String addressMaps;
  final Client client;
  final Police police;

  Accident(
      {required this.id,
      required this.addressMaps,
      required this.client,
      required this.police});

  factory Accident.fromJson(Map<String, dynamic> json) {
    return Accident(
        id: json['id'],
        addressMaps: json['address_maps'],
        client: json['client'],
        police: json['police']);
  }
}
