# CQueue-OldjwQuickSearch

## Introduction
This is a python script used to get all scores from the [Old Educate System of Chongqing University](http://oldjw.cqu.edu.cn:8088).<br>
This website is often used as an official reference to students' GPA for it has its private source code, and is more stable and secure compared to the [New Educate System of Chongqing University](http://jxgl.cqu.edu.cn/) (Developed by Kingo, source can be found online).<br>
To make the old educate system more stable, the website is **NOT** open to the public. It is only available by using the network within Chongqing University, or using a VPN of Chongqing University with an account from the school.<br>
Many students are complaining about this website for it is unable to search his/her own score for there is no such button to choose. Here is the code segment in the [Score Management](http://oldjw.cqu.edu.cn:8088/score_zpy/index.asp) page:
```html
<table class="navLight" cellspacing="6" cellpadding="0" width="100%" border="0" style="background-color: #0082C6">
  <tbody>
    <tr>
      <td height="17">
        <font color="#ffffff">
          <!--  <a href="#:"  onMouseOver="expandMenu(null,'menu1',getPos(this,'Left'),getPos(this,'Top')+this.offsetHeight);" onmouseout="hideMe();" class="a" ><FONT color=#ffffff>重修考试</font></a> -->
          <a href="#;" onmouseover="expandMenu(null,'menu2',getPos(this,'Left'),getPos(this,'Top')+this.offsetHeight);" onmouseout="hideMe();" class="a">
            <font color="#ffffff">各种查询</font>
          </a>
        </font>
      </td>
    </tr>
  </tbody>
</table>
<!-- <div id="menu1" class="menu" onMouseOut="hideMe();"> -->
<!--  <a href="/score/others/reexam_app_select.asp" onMouseOver="expandMenu('menu1');">重修考试查询</a><br> -->
<!--  <a href="/score/others/reexam_app_end.asp" onMouseOver="expandMenu('menu1');">重修考试报名</a><br>  -->
<!--  <a href="/notices/reexam_manage_list.htm" onMouseOver="expandMenu('menu1');">查重考安排表</a><br> -->
<!-- </div> -->
<!-- 第一开始 -->
<div id="menu2" class="menu" onmouseout="hideMe();" style="">
<!--  <a href="/score/log_score/nolog_score_cour.asp" onMouseOver="expandMenu('menu2');">未提交成绩的课程</a><br> -->
  <a href="/score/sel_score/new_score_sel.asp" onmouseover="expandMenu('menu2');">学生最新成绩查询</a><br> 
  <a href="/score/sel_score/sum_score_sel.asp" onmouseover="expandMenu('menu2');">学生总成绩查询</a><br>
<!--  <a href="/score/sel_score/all_score_sel.asp" onMouseOver="expandMenu('menu2');">历史成绩记录查询</a><br> -->
<!--  <a href="/score/others/sele_delay_exam_stud.asp" onMouseOver="expandMenu('menu2');">学生缓考查询</a><br> -->
</div>
<!-- 第二开始 -->
```
We know why we cannot find the button. By capturing the code, we know the target address is http://oldjw.cqu.edu.cn:8088/score/sel_score/sum_score_sel.asp. Based on this, we write a script to log on it, get the score and analyze the text into an Excel file (.csv). 

## Resources to be imported
```Java
import requests
import time
import math
from bs4 import BeautifulSoup
```

BeautifulSoup needs to be installed before running this code.<br>
> [Download BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/download/4.6/)<br>

## Input
The input should be written in **input.txt**, with one line for username, one line for password (default password is the last 6 characters of the ID card). If more students' score is needed, you can add a line of username and a line of password after the first one. <br>
> Note that we should not input too many lines, for the website might block our request if we are doing too many login operations. Further more, Excel can only process 65536(.xls) or 1045876(.xlsx) lines of data if we need to make a further edition. We should NOT save too much data into this file.

## Output
The output is in **output.csv**, which can be directly opened by Microsoft Excel. Further edition can be done by saving the file as a normal excel file (.xlsx).
