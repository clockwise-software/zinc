# CLOCKWISE-BOOTCAMP SimpleServer.py
# Based on Server from Dr. Ian Cooper @ Cardiff
# Updated by Dr. Mike Borowczak @ UWyo March 2021

import os
from flask import Flask, redirect, request, render_template
import sqlite3
from sqlite3 import Error

DATABASE = 'bootcamp.db'

app = Flask(__name__)


@app.route("/")
def basic():
    return render_template('EmployeeSearch.html')


@app.route("/Employee/AddEmployee", methods=['POST', 'GET'])
def studentAddDetails():

    if request.method == 'GET':
        print('returning a get')
        return render_template('EmployeeData.html')
    if request.method == 'POST':
        firstName = request.form.get('firstName', default="Error")
        lastName = request.form.get('lastName', default="Error")
        businessunit = request.form.get('bu', default="Error")
        state = request.form.get('state', default="Error")
        ftpt = request.form.get('FT/PT/.75', default="Error")
        city = request.form.get('city', default="Error")
        cmt = request.form.get('cmt', default="Error")
        totalYears = request.form.get('totalYears', default="Error")
        registeredLicenses = request.form.get(
            'registeredLicenses', default="Error")
        skill = request.form.get('skill', default="Error")
        skillLevel = request.form.get('skillLevel', default="Error")

        print("inserting employee"+firstName)
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()

            cur.execute("INSERT INTO EmployeeList ('FirstName', 'LastName', 'FT/PT/.75?', 'Business Unit', 'City', 'State/Province', 'Career Matrix Title', 'Total Years', 'Registered Licenses', 'Skill', 'Skill Level')\
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)", (firstName, lastName, ftpt, businessunit, city, state, cmt, totalYears, registeredLicenses, skill, skillLevel))
            conn.commit()
            msg = "Record successfully added"
        except:
            conn.rollback()
            msg = "error in insert operation"
        finally:
            conn.close()
            return msg


@app.route("/Employee/Search", methods=['GET', 'POST'])
def surnameSearch():
    if request.method == 'GET':
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT FirstName FROM EmployeeList")
            FirstName = cur.fetchall()
            print(FirstName)

            cur.execute("SELECT LastName from EmployeeList")
            LastName = cur.fetchall()
            print(LastName)

            cur.execute("SELECT DISTINCT [FT/PT/.75?] from EmployeeList")
            Time = cur.fetchall()

            cur.execute("SELECT DISTINCT [Business Unit] from EmployeeList")
            BU = cur.fetchall()

            cur.execute("SELECT DISTINCT City from EmployeeList")
            City = cur.fetchall()

            cur.execute("SELECT DISTINCT [State/Province] from EmployeeList")
            State = cur.fetchall()

            cur.execute("SELECT DISTINCT [Career Matrix Title] from EmployeeList")
            CMT = cur.fetchall()

            cur.execute("SELECT DISTINCT [Total Years] from EmployeeList")
            Years = cur.fetchall()

            cur.execute("SELECT DISTINCT [Registered Licenses] from EmployeeList")
            regLic = cur.fetchall()

            cur.execute("SELECT DISTINCT Skill from EmployeeList")
            Skill = cur.fetchall()

            cur.execute("SELECT DISTINCT [Skill Level] from EmployeeList")
            Level = cur.fetchall()

        except:
            print('there was an error')
            conn.close()
        finally:
            conn.close()
            # return str(data)
            return render_template('EmployeeSearch.html', FirstName=FirstName, LastName=LastName, Time=Time, BU=BU, City=City, State=State, CMT=CMT, Years=Years, regLic=regLic, Skill=Skill, Level=Level)
    if request.method == 'POST':
        try:
            # rem: args for get form for post
            #lastName = request.form.get('lastName', default="Error")
            firstName, lastName, ftpt, businessunit, city, state, cmt, totalYears, registeredLicenses, skill, skillLevel='Tim', '', '', '', '', '', '', '', '', '', '' 
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM 'EmployeeList' WHERE FirstName=? or LastName=? or [FT/PT/.75?]=? or [Business Unit]=? or [City]=? or [State/Province]=? or [Career Matrix Title]=? or [Total Years]=? or [Registered Licenses]=? or [Skill]=? or [Skill Level]=?", [firstName, lastName, ftpt, businessunit, city, state, cmt, totalYears, registeredLicenses, skill, skillLevel])

            data = cur.fetchall()
            print(data)
        except:
            print('there was an error', data)
            conn.close()
        finally:
            conn.close()
            return render_template('Employee.html', data=data)

@app.route("/Employee/Modify", methods=['GET', 'POST'])
def modifyEmployee():
    if request.method == 'GET':
        return render_template('EmployeeModify.html')
    if request.method == 'POST':
        firstName = request.form.get('fname', default="Error")
        lastName = request.form.get('lname', default="Error")
        businessunit = request.form.get('bu', default="Error")
        state = request.form.get('state', default="Error")
        ftpt = request.form.get('ftpt', default="Error")
        city = request.form.get('city', default="Error")
        cmt = request.form.get('cmt', default="Error")
        totalYears = request.form.get('totalYears', default="Error")
        registeredLicenses = request.form.get('Licenses', default="Error")
        skill = request.form.get('Skill', default="Error")
        skillLevel = request.form.get('skilllevel', default="Error")
        
        try:
            # rem: args for get form for post
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("UPDATE EmployeeList SET [FirstName] = ?, [LastName] = ?, [FT/PT/.75?] = ?, [Business Unit] = ?, [City] = ?, [State/Province] = ?, [Career Matrix Title] = ?, [Total Years] = ?, [Registered Licenses] = ?, [Skill] = ?, [Skill Level] = ? WHERE [LastName] = ?", (firstName, lastName, ftpt, businessunit, city, state, cmt, totalYears, registeredLicenses, skill, skillLevel, lastName))   
            conn.commit()
            if cur.rowcount < 1:
                msg = "Update failed"
            else:
                msg = "Record successfully updated"
        except Error as e:
            conn.rollback()
            msg = e
        finally:
            conn.close()
            print(msg)
            return msg


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
