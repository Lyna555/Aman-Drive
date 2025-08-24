import 'accident.dart';

class Police {
  final int id;
  final String addressMaps;
  final List<Accident> accidents;

  Police(
      {required this.id, required this.addressMaps, required this.accidents});

  factory Police.fromJson(Map<String, dynamic> json) {
    return Police(
        id: json['id'],
        addressMaps: json['address_maps'],
        accidents: json['accidents']);
  }
}
