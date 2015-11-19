# -*- coding:UTF-8 -*-
__author__ = 'lc4t'

import sqlite3



class DB_uestc:
    def __init__(self, li, belongs_id):
        self.cx = sqlite3.connect('../../data.db')
        self.cu = self.cx.cursor()
        self.table = 'grade_grades'
        self.academisc = 'academisc'
        self.number = 'number'
        self.makeupGrade = 'makeupGrade'
        self.finalGrade = 'finalGrade'
        self.gradePoint = 'gradePoint'
        self.courseType = 'courseType'
        self.courseCode = 'courseCode'
        self.courseName = 'courseName'
        self.credit = 'credit'
        self.semester = 'semester'
        self.totalGrade = 'totalGrade'
    def add(self):
        for one in self.li:
            # sql = print ("insert into %s (belongs_id, academisc, semester, courseCode, number, courseName, courseType, credit, totalGrade, makeupGrade, finalGrade, gradePoint) values(%d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (self.table, belongs_id,one[academisc], one[semester],one[courseCode],one[number],one[courseName],one[courseType],one[credit],str(one[totalGrade]),one[makeupGrade],str(one[finalGrade]),str(one[gradePoint])))            # print (s)
            sql = "insert into "+self.table+" (belongs_id, academisc, semester, courseCode, number, courseName, courseType, credit, totalGrade, makeupGrade, finalGrade, gradePoint) values("+str(self.belongs_id)+",'"+one[self.academisc]+"','"+one[self.semester]+"','"+one[self.courseCode]+"','"+one[self.number]+"','"+one[self.courseName]+"','"+one[self.courseType]+"','"+one[self.credit]+"','"+str(one[self.totalGrade])+"','"+one[self.makeupGrade]+"','"+str(one[self.finalGrade])+"','"+str(one[self.gradePoint])+"');"
            print (sql)
            self.cu.execute(sql)
        self.cx.commit()
    def delete(self):
        for one in self.li:
            sql = "delete from "+self.table+" where number='"+one[self.number]+"' and belongs_id="+str(self.belongs_id)+" and (makeupGrade<>'"+one[self.makeupGrade]+"' or finalGrade<>'"+str(one[self.finalGrade])+"')"
            self.cu.execute(sql)
            print (sql)
        self.cx.commit()






