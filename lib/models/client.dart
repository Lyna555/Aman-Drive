import 'accident.dart';
import 'insurance.dart';

class Client {
  final int id;
  final String address;
  final String? diseases;
  final String bloodType;
  final String insuranceNbr;
  final String insuranceType;
  final String vehicleType;
  final String vehicleBrand;
  final String vehicleYear;
  final String vehiclePlate;
  final String horses;
  final String price;
  final Insurance insurance;
  final List<Accident> accidents;

  Client(
      {required this.id,
      required this.address,
      required this.diseases,
      required this.bloodType,
      required this.insuranceNbr,
      required this.insuranceType,
      required this.vehicleType,
      required this.vehicleBrand,
      required this.vehicleYear,
      required this.vehiclePlate,
      required this.horses,
      required this.price,
      required this.insurance,
      required this.accidents});

  factory Client.fromJson(Map<String, dynamic> json) {
    return Client(
        id: json['id'],
        address: json['address'],
        diseases: json['diseases'],
        bloodType: json['blood_type'],
        insuranceNbr: json['insurance_nbr'],
        insuranceType: json['insurance_type'],
        vehicleType: json['vehicle_type'],
        vehicleBrand: json['vehicle_brand'],
        vehicleYear: json['vehicle_year'],
        vehiclePlate: json['vehicle_plate'],
        horses: json['horses'],
        price: json['price'],
        insurance: json['insurance'],
        accidents: json['accidents']);
  }
}
