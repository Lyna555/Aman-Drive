class User {
  final int id;
  final String email;
  final String password;
  final String role;

  User(
      {required this.id,
      required this.email,
      required this.password,
      required this.role});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
        id: json['id'],
        email: json['email'],
        password: json['password'],
        role: json['role']);
  }
}
