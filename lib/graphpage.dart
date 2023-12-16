import 'dart:convert';

import 'package:flutter/material.dart';
import 'FeedBackPage_사막.dart';
import 'FeedBackPage_사막화.dart';
import 'FeedBackPage_숲.dart';
import 'FeedBackPage_초원.dart';
import 'dart:typed_data';
import 'package:http/http.dart' as http;


String url0 = 'http://172.20.23.208:5000/';


class GraphPage extends StatefulWidget {
  const GraphPage({super.key});

  @override
  State<GraphPage> createState() => _GraphPageState();
}

class _GraphPageState extends State<GraphPage> {
  int fetchedNumber = 0;

  @override
  void initState() {
    super.initState();
    // Flutter 앱이 시작될 때 Flask 서버에서 데이터를 가져오도록 함
    fetchData();
  }

  Future<void> fetchData() async {
    String url1 = url0+'get_number';
      final oldurl = Uri.parse(url1);
      
      final response = await http.get(oldurl);
    
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);
      setState(() {
        fetchedNumber = data['number'];
      });
    } else {
      throw Exception('Failed to load data');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            fit: BoxFit.cover,
              image: AssetImage('assets/images/graphpage.png'), // 배경 이미지
          ),
        ),
        child: Scaffold(
          backgroundColor: Colors.transparent,
          
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                 Column(
                  crossAxisAlignment: CrossAxisAlignment.center,
                   children: [
                    SizedBox(height: 30),
                     FutureBuilder(
                      future: fetchFFTPlot(),
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return CircularProgressIndicator();
                        } else if (snapshot.hasError) {
                          
                          print('에러: ${snapshot.error}');
                          return Text('에러: ${snapshot.error}');
                        } else {
                          return Image.memory(snapshot.data!);
                        }
                      },
                    ),
                  
                    SizedBox(height: 30),
                    FutureBuilder(
                      future: fetchFFTPlot2(),
                      builder: (context, snapshot) {
                        if (snapshot.connectionState == ConnectionState.waiting) {
                          return CircularProgressIndicator();
                        } else if (snapshot.hasError) {
                          
                          print('에러: ${snapshot.error}');
                          return Text('에러: ${snapshot.error}');
                        } else {
                          return Image.memory(snapshot.data!);
                        }
                      },
                    ),
                    SizedBox(height: 30),
                    Container(
                      width: 300,
                      height: 50,
                      decoration: ShapeDecoration(
                        color: Color(0xFFE6E6E6),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(25),
                        ),
                      ),
                      alignment: Alignment.center,
                      child: Text(
                          '분당 눈 깜빡임 횟수 : $fetchedNumber회',
                          textAlign: TextAlign.center,
                          style: TextStyle(
                            color: Color(0xFF494949),
                            fontSize: 17,
                            fontFamily: 'Poppins',
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                    ),
                        SizedBox(height: 30,),
                        ElevatedButton(
                      onPressed: () {

                  print('버튼눌림');
                  if (fetchedNumber >= 16 && fetchedNumber <= 20) {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => FeedBack_Soop()),
                    );
                  } else if (fetchedNumber >= 11 && fetchedNumber <= 15) {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (_) => FeedBack_Chowon()),
                    );
                  } else if (fetchedNumber >= 8 && fetchedNumber <= 10) {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (_) => FeedBack_Samakhwa()),
                    );
                  } else if (fetchedNumber < 7) {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => FeedBack_Samak()),
                    );
                  }

                      },
                      style: ElevatedButton.styleFrom(
                        minimumSize: Size(300, 50),
                        primary: Color(0xFF27AE61), // 버튼 배경색 설정
                        onPrimary: Colors.black, // 버튼 텍스트 색상 설정
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(25), // 버튼 모서리 둥글기 설정
                        ),
                        padding: EdgeInsets.all(5), // 버튼 내부 여백 설정
                      ),
                      child: Text(
                        '피드백 보러가기',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 18,
                          fontFamily: 'Inter',
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),
                   ],
                 ),
                 

              ],
            ),
          ),
        ),
    );
  }
  Future<Uint8List?> fetchFFTPlot() async {
      String url1 = url0+'plot';
      final oldurl = Uri.parse(url1);
      
      final response = await http.get(oldurl);

      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        throw Exception('Failed to load FFT plot image');
      }
    }

  Future<Uint8List?> fetchFFTPlot2() async {
      String url1 = url0+'get_eye';
      final oldurl = Uri.parse(url1);
      
      final response = await http.get(oldurl);

      if (response.statusCode == 200) {
        return response.bodyBytes;
      } else {
        throw Exception('Failed to load FFT plot image');
      }
    }
    
 }

