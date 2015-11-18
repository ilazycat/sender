# -*- coding:UTF-8 -*-
__author__ = 'lc4t'
from Uestc import Exec
import sqlite3


li = [{'academisc': '2014-2015', 'number': 'B1300720.04', 'makeupGrade': '', 'finalGrade': 75, 'gradePoint': 3.0, 'courseType': 'A类语言技能类', 'semester': '2', 'credit': '2', 'courseCode': 'B1300720', 'totalGrade': 75, 'courseName': '高级英语听说'}, {'academisc': '2014-2015', 'number': 'I1009030.01', 'makeupGrade': '', 'finalGrade': 75, 'gradePoint': 3.0, 'courseType': '素质教育选修课（自然科学类）', 'semester': '2', 'credit': '3', 'courseCode': 'I1009030', 'totalGrade': 75, 'courseName': '算法分析与设计'}, {'academisc': '2014-2015', 'number': 'H1309320.02', 'makeupGrade': '', 'finalGrade': 83, 'gradePoint': 3.8, 'courseType': '本专业选修课', 'semester': '2', 'credit': '2', 'courseCode': 'H1309320', 'totalGrade': 83, 'courseName': '西方报刊选读'}, {'academisc': '2014-2015', 'number': 'E0600540.02', 'makeupGrade': '', 'finalGrade': 84, 'gradePoint': 3.9, 'courseType': '学科基础课程', 'semester': '2', 'credit': '4', 'courseCode': 'E0600540', 'totalGrade': 84, 'courseName': '离散数学'}, {'academisc': '2014-2015', 'number': 'D1000160.97', 'makeupGrade': '', 'finalGrade': 69, 'gradePoint': 2.4, 'courseType': '学科通识课程', 'semester': '1', 'credit': '6', 'courseCode': 'D1000160', 'totalGrade': 69, 'courseName': '微积分I'}, {'academisc': '2014-2015', 'number': 'L9800210.01', 'makeupGrade': '', 'finalGrade': 85, 'gradePoint': 4, 'courseType': '实践类核心课程', 'semester': '1', 'credit': '1', 'courseCode': 'L9800210', 'totalGrade': 85, 'courseName': '军事训练'}, {'academisc': '2014-2015', 'number': 'I9900120.02', 'makeupGrade': '', 'finalGrade': 82, 'gradePoint': 3.7, 'courseType': '素质教育选修课（艺体类）', 'semester': '2', 'credit': '2', 'courseCode': 'I9900120', 'totalGrade': 82, 'courseName': 'Flash动画设计'}, {'academisc': '2014-2015', 'number': 'D1000250.23', 'makeupGrade': '', 'finalGrade': 72, 'gradePoint': 2.7, 'courseType': '学科通识课程', 'semester': '2', 'credit': '5', 'courseCode': 'D1000250', 'totalGrade': 72, 'courseName': '微积分II'}, {'academisc': '2014-2015', 'number': 'G0601240.02', 'makeupGrade': '', 'finalGrade': 96, 'gradePoint': 4, 'courseType': '专业核心课程', 'semester': '2', 'credit': '4', 'courseCode': 'G0601240', 'totalGrade': 96, 'courseName': '程序设计（C与C++）'}, {'academisc': '2014-2015', 'number': 'B1400210.B4', 'makeupGrade': '', 'finalGrade': 100, 'gradePoint': 4, 'courseType': '军事理论、体育', 'semester': '2', 'credit': '1', 'courseCode': 'B1400210', 'totalGrade': 100, 'courseName': '大学体育II'}, {'academisc': '2014-2015', 'number': 'H0600310.02', 'makeupGrade': '', 'finalGrade': 81, 'gradePoint': 3.6, 'courseType': '本专业选修课', 'semester': '1', 'credit': '1', 'courseCode': 'H0600310', 'totalGrade': 81, 'courseName': '新生素质教育课'}, {'academisc': '2014-2015', 'number': 'F0600110.01', 'makeupGrade': '', 'finalGrade': 82, 'gradePoint': 3.7, 'courseType': '学科拓展课程', 'semester': '1', 'credit': '1', 'courseCode': 'F0600110', 'totalGrade': 82, 'courseName': '计算机导论'}, {'academisc': '2014-2015', 'number': 'B1600220.02', 'makeupGrade': '', 'finalGrade': 76, 'gradePoint': 3.1, 'courseType': '思想政治理论课', 'semester': '2', 'credit': '2', 'courseCode': 'B1600220', 'totalGrade': 76, 'courseName': '中国近现代史纲要'}, {'academisc': '2014-2015', 'number': 'B9800320.33', 'makeupGrade': '', 'finalGrade': 83, 'gradePoint': 3.8, 'courseType': '思想政治理论课', 'semester': '1', 'credit': '2', 'courseCode': 'B9800320', 'totalGrade': 83, 'courseName': '形势与政策'}, {'academisc': '2014-2015', 'number': 'B9800110.14', 'makeupGrade': '', 'finalGrade': 88, 'gradePoint': 4, 'courseType': '军事理论、体育', 'semester': '1', 'credit': '1', 'courseCode': 'B9800110', 'totalGrade': 88, 'courseName': '军事理论'}, {'academisc': '2014-2015', 'number': 'B1300140.28', 'makeupGrade': '', 'finalGrade': 69, 'gradePoint': 2.4, 'courseType': '外语', 'semester': '1', 'credit': '4', 'courseCode': 'B1300140', 'totalGrade': 69, 'courseName': '通用英语'}, {'academisc': '2014-2015', 'number': 'B1600130.03', 'makeupGrade': '', 'finalGrade': 88, 'gradePoint': 4, 'courseType': '思想政治理论课', 'semester': '1', 'credit': '3', 'courseCode': 'B1600130', 'totalGrade': 88, 'courseName': '思想道德修养与法律基础'}, {'academisc': '2014-2015', 'number': 'B1400110.17', 'makeupGrade': '', 'finalGrade': 79, 'gradePoint': 3.4, 'courseType': '军事理论、体育', 'semester': '1', 'credit': '1', 'courseCode': 'B1400110', 'totalGrade': 79, 'courseName': '大学体育I'}, {'academisc': '2014-2015', 'number': 'D1000540.94', 'makeupGrade': '', 'finalGrade': 67, 'gradePoint': 2.2, 'courseType': '学科通识课程', 'semester': '1', 'credit': '4', 'courseCode': 'D1000540', 'totalGrade': 67, 'courseName': '线性代数与空间解析几何I'}, {'academisc': '2014-2015', 'number': 'D0400340.21', 'makeupGrade': '', 'finalGrade': 77, 'gradePoint': 3.2, 'courseType': '学科通识课程', 'semester': '2', 'credit': '4', 'courseCode': 'D0400340', 'totalGrade': 77, 'courseName': '大学物理Ⅰ'}]

class DB_uestc:
    def __init__(self):
        self.cx = sqlite3.connect('../../data.db')
        self.cu = self.cx.cursor()
        self.table = 'grade_grades'
    def add(self,li, belongs_id):
        academisc = 'academisc'
        number = 'number'
        makeupGrade = 'makeupGrade'
        finalGrade = 'finalGrade'
        gradePoint = 'gradePoint'
        courseType = 'courseType'
        courseCode = 'courseCode'
        courseName = 'courseName'
        credit = 'credit'
        semester = 'semester'
        totalGrade = 'totalGrade'
        for one in li:
            # sql = print ("insert into %s (belongs_id, academisc, semester, courseCode, number, courseName, courseType, credit, totalGrade, makeupGrade, finalGrade, gradePoint) values(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (self.table, belongs_id,one[academisc], one[semester],one[courseCode],one[number],one[courseName],one[courseType],one[credit],str(one[totalGrade]),one[makeupGrade],str(one[finalGrade]),str(one[gradePoint])))            # print (s)
            sql = "insert into "+self.table+" (belongs_id, academisc, semester, courseCode, number, courseName, courseType, credit, totalGrade, makeupGrade, finalGrade, gradePoint) values("+str(belongs_id)+",'"+one[academisc]+"','"+one[semester]+"','"+one[courseCode]+"','"+one[number]+"','"+one[courseName]+"','"+one[courseType]+"','"+one[credit]+"','"+str(one[totalGrade])+"','"+one[makeupGrade]+"','"+str(one[finalGrade])+"','"+str(one[gradePoint])+"');"
            print (sql)
            self.cu.execute(sql)
        self.cx.commit()



db = DB_uestc()
db.add(li,1)

