import 'package:flutter/foundation.dart';

class UserData extends ChangeNotifier {
  late String _name;

  String get name => _name;

  void setName(String newName) {
    _name = newName;
    notifyListeners();
  }
}
