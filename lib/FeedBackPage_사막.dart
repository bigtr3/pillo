import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:pillo/user_data.dart';
import 'package:provider/provider.dart';

String url0 = 'http://172.20.23.208:5000/';

class FeedBack_Samak extends StatefulWidget {
  const FeedBack_Samak({super.key});

  @override
  State<FeedBack_Samak> createState() => _FeedBackState2();
}

class _FeedBackState2 extends State<FeedBack_Samak> {
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
                Image(image: AssetImage('assets/images/logo4.png')),
                SizedBox(height: 30),
                Text(
                  "당신은\n'사막' 단계\n입니다",
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
                  "분당 눈 깜빡임 횟수는 평균 $fetchedNumber회로, 안구건조증이 의심됩니다."+
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
                  "• 평소보다 눈을 자주 깜빡이셔야 해요 \n• 가까운 안과에 내원하여 의사에게 상담받아보세요 \n• 스마트폰을 사용하는 중간중간 적절한 휴식을 취해주세요 \n• 외부자극을 줄이기 위한 안경을 착용해주세요 ",
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