import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';

import 'package:pillo/user_data.dart';
import 'package:provider/provider.dart';

String url0 = 'http://192.168.219.108:5000/';

class FeedBack_Chowon extends StatefulWidget {
  const FeedBack_Chowon({super.key});

  @override
  State<FeedBack_Chowon> createState() => _FeedBackState3();
}

class _FeedBackState3 extends State<FeedBack_Chowon> {
  int fetchedNumber = 0;
  int rate1=0;

  @override
  void initState() {
    super.initState();
    // Flutter 앱이 시작될 때 Flask 서버에서 데이터를 가져오도록 함
    fetchData();
    fetchRate();
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

  Future<void> fetchRate() async {
    String url1 = url0+'get_rate';
      final oldurl = Uri.parse(url1);
      
      final response = await http.get(oldurl);
    
    if (response.statusCode == 200) {
      final Map<String, dynamic> data = json.decode(response.body);
      setState(() {
        rate1 = data['rate'];
      });
    } else {
      throw Exception('Failed to load data');
    }
  }
  
  @override
  Widget build(BuildContext context) {
    final userData = Provider.of<UserData>(context);
    String trendText1 = rate1 >= 0 ? '상승했습니다. 휴식을 취해주세요!' : '감소했습니다. 지금 상태를 유지해주세요!';

    return Scaffold(
        backgroundColor: Colors.black,
        body: SingleChildScrollView(
            padding: EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                SizedBox(
                  height: 30,
                ),
                Image(image: AssetImage('assets/images/logo2.png')),
                SizedBox(height: 30),
                Text(
                  "당신은\n'초원' 단계\n입니다",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 48,
                    fontFamily: 'Space Grotesk',
                    fontWeight: FontWeight.w700,
                  ),
                ),
                SizedBox(
                  height: 30,
                ),
                Text(
                  "Hi, ${userData.name}!",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontFamily: 'Inter',
                    fontWeight: FontWeight.w500,
                  ),
                ),
                SizedBox(
                  height: 16,
                ),
                Text(
                  "분당 눈 깜빡임 횟수는 평균 $fetchedNumber회로, 정상입니다."+
                  "\n\n뇌파 분석 결과 뇌의 피로도가 ${rate1.abs()}% $trendText1",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontFamily: 'Inter',
                    fontWeight: FontWeight.w500,
                    height: 1.2,
                  ),
                ),
                SizedBox(
                  height: 20,
                ),
                Text(
                  "• 좋은 눈 깜빡임 습관을 가지고 계시네요 \n• 스마트폰 사용 시간을 조금 줄여보는 것은 어떨까요? \n• 스마트폰 사용 시 자주 눈을 쉬어주는 습관을 기르면 눈 건강에 도움이 될 거예요 ",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 16,
                    fontFamily: 'Inter',
                    fontWeight: FontWeight.w500,
                    height: 1.4,
                  ),
                ),
                SizedBox(
                  height: 16,
                ),
                Text(
                  "측정 시간이 적거나 측정 중 격한 움직임이 있으면 측정이 정확하지 않을 수도 있으니 주의하시기 바랍니다.",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 11,
                    fontFamily: 'Inter',
                    fontWeight: FontWeight.w500,
                    height: 1.2,
                  ),
                ),
              ],
            )));
  }
}