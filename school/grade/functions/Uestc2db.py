# -*- coding:UTF-8 -*-
__author__ = 'lc4t'

import sqlite3
import datetime


class DB_uestc:
    def __init__(self, belongs_id):
        self.cx = sqlite3.connect('data.db')
        self.cu = self.cx.cursor()
        self.table = 'grade_grades'
        self.belongs_id = belongs_id
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

    def add(self, li):#private
        for one in li:
            sql = "insert into "+self.table+" (belongs_id, academisc, semester, courseCode, number, courseName, courseType, credit, totalGrade, makeupGrade, finalGrade, gradePoint, updateTime) select "+str(self.belongs_id)+",'"+one[self.academisc]+"','"+one[self.semester]+"','"+one[self.courseCode]+"','"+one[self.number]+"','"+one[self.courseName]+"','"+one[self.courseType]+"','"+one[self.credit]+"','"+str(one[self.totalGrade])+"','"+one[self.makeupGrade]+"','"+str(one[self.finalGrade])+"','"+str(one[self.gradePoint])+"','"+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"' where not exists(select * from "+self.table+" where belongs_id="+str(self.belongs_id)+" and number='"+one[self.number]+"');"
            # print (sql)
            self.cu.execute(sql)
        self.cx.commit()
    def delete(self, li):#private
        for one in li:
            # delete if not equal

            sql = "delete from "+self.table+" where number='"+one[self.number]+"' and belongs_id="+str(self.belongs_id)+" and (makeupGrade<>'"+one[self.makeupGrade]+"' or finalGrade<>'"+str(one[self.finalGrade])+"')"

            self.cu.execute(sql)

        self.cx.commit()
    def sync(self, li):# exec this
        self.delete(li)
        self.add(li)




