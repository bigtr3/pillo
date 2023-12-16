import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'graphpage.dart';
import 'user_data.dart';




class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _nameController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Container(
        decoration: BoxDecoration(
          image: DecorationImage(
            fit: BoxFit.cover,
              image: AssetImage('assets/images/homepage.png'), // 배경 이미지
          ),
        ),
        child: Scaffold(
          resizeToAvoidBottomInset: false,
          backgroundColor: Colors.transparent,
           
          body: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              // 여백
              
              // 텍스트 상자 공간
              Container(
                width: 300,
                height: 60,
                child: Stack(
                  children: [
                    // 텍스트 상자 설정
                    Center(
                      child: Container(
                        width: 300,
                        height: 50,
                        decoration: ShapeDecoration(
                          shape: RoundedRectangleBorder(
                            side: BorderSide(width: 1, color: Color(0xFF27AE61)),
                            borderRadius: BorderRadius.circular(10),
                          ),
                        ),
                        // 텍스트 입력
                        padding: EdgeInsets.only(left: 10),
                        child: 
                          TextField(
                            controller: _nameController,
                            style: TextStyle(color: Colors.white, fontSize: 18, fontFamily: 'Inter',),
                            decoration: InputDecoration(
                              border: InputBorder.none,
                            ),
                          ),
                      ),
                    ),
                    // 텍스트 상자 글자 설정
                    Positioned(
                      left: 34,
                      top: -1,
                      child: Container(
                        padding: const EdgeInsets.all(2),
                        decoration: BoxDecoration(color: Colors.black),
                        child: Text(
                          'Enter your name',
                          style: TextStyle(
                            color: Color(0xFF27AE61),
                            fontSize: 11,
                            fontFamily: 'Inter',
                            fontWeight: FontWeight.w600,
                            height: 0,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              // 여백
              SizedBox(height: 200),
              // 버튼 설정
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  ElevatedButton(
                    onPressed: () {
                  // 버튼이 눌렸을 때 수행할 작업 추가
                        final userData = Provider.of<UserData>(context, listen: false);
                      userData.setName(_nameController.text);
                          Navigator.pushReplacement(
                        context,
                        MaterialPageRoute(builder: (context) => GraphPage()),
                      );
                    },
                    style: ElevatedButton.styleFrom(
                      minimumSize: Size(150, 50),
                      primary: Color(0xFF27AE61), // 버튼 배경색 설정
                      onPrimary: Colors.black, // 버튼 텍스트 색상 설정
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10), // 버튼 모서리 둥글기 설정
                      ),
                      padding: EdgeInsets.all(5), // 버튼 내부 여백 설정
                    ),
                    child: Text(
                      '분석 결과 보기',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.black,
                        fontSize: 18,
                        fontFamily: 'Inter',
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  
                  ElevatedButton(
                    onPressed: () {
                  // 버튼이 눌렸을 때 수행할 작업 추가
                    },
                    style: ElevatedButton.styleFrom(
                      minimumSize: Size(150, 50),
                      primary: Colors.transparent, // 버튼 배경색 설정
                      onPrimary: Color(0xFF115DA9), // 버튼 텍스트 색상 설정
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(10), // 버튼 모서리 둥글기 설정
                        side: BorderSide(width: 1, color: Color(0xFF115DA9)),
                      ),
                      padding: EdgeInsets.all(5), // 버튼 내부 여백 설정
                    ),
                    child: Text(
                      'QUIT',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Color(0xFF115DA9),
                        fontSize: 18,
                        fontFamily: 'Inter',
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ],
              ),
              SizedBox(height: 20,),
                
            ],
          ),
                        
        ),
      );
    }
}