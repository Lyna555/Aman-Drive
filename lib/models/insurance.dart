import 'client.dart';

class Insurance {
  final int id;
  final String address;
  final List<Client> clients;

  Insurance({required this.id, required this.address, required this.clients});

  factory Insurance.fromJson(Map<String, dynamic> json) {
    return Insurance(
        id: json['id'], address: json['address'], clients: json['clients']);
  }
}
