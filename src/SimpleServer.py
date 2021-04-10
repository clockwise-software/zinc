# CLOCKWISE-BOOTCAMP SimpleServer.py
# Based on Server from Dr. Ian Cooper @ Cardiff
# Updated by Dr. Mike Borowczak @ UWyo March 2021

import os
from flask import Flask, redirect, request, render_template
import sqlite3

DATABASE = 'bootcamp.db'

app = Flask(__name__)


@app.route("/")
def basic():
    return render_template('Employee.html')


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
        return render_template('EmployeeSearch.html')
    if request.method == 'POST':
        try:
            # rem: args for get form for post 
            lastName=request.form.get('lastName', default="Error")
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT * FROM 'EmployeeList' WHERE LastName=?", [lastName])
            data = cur.fetchall()
            print(data)
        except:
            print('there was an error', data)
            conn.close()
        finally:
            conn.close()
            return render_template('Employee.html', data=data)


# The name says it...
# @app.route("/Employee/VulnerableSearch", methods=['GET', 'POST'])
# def surnameInjectionSearch():
#     if request.method == 'GET':
#         return render_template('EmployeeSQLInjection.html')
#     if request.method == 'POST':
#         # rem: args for get form for post
#         lastName = request.form.get('lastName', default="Error")
#         conn = sqlite3.connect(DATABASE)
#         cur = conn.cursor()

#         # VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD
#         query = "SELECT * FROM EmployeeList WHERE lastname= '%s' " % (
#             lastName,)
#         print(query)
#         cur.execute(query)
#         # VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD VERY BAD

#         data = cur.fetchall()
#         print(data)
#         print(lastName)
#         conn.close()
#         return render_template('Employee.html', data=data)


@app.route("/Employee/Modify", methods=['GET', 'POST'])
def modifyEmployee():
    if request.method == 'GET':
        return render_template('EmployeeModify.html')
    if request.method == 'POST':
        firstName = request.form.get('firstName', default="Error")
        lastName = request.form.get('lastName', default="Error")
        businessunit = request.form.get('bu', default="Error")
        state = request.form.get('state', default="Error")
        ftpt = request.form.get('FT/PT/.75', default="Error")
        city = request.form.get('city', default="Error")
        cmt = request.form.get('cmt', default="Error")
        totalYears = request.form.get('totalYears', default="Error")
        registeredLicenses = request.form.get('registeredLicenses', default="Error")
        skill = request.form.get('skill', default="Error")
        skillLevel = request.form.get('skillLevel', default="Error")
        try:
            # rem: args for get form for post
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("UPDATE EmployeeList SET ('FirstName', 'LastName', 'FT/PT/.75?', 'Business Unit', 'City', 'State/Province', 'Career Matrix Title', 'Total Years', 'Registered Licenses', 'Skill', 'Skill Level') VALUES (?,?,?,?,?,?,?,?,?,?,?) WHERE ('LastName') VALUES (?)", (firstName, lastName, ftpt, businessunit, city, state, cmt, totalYears, registeredLicenses, skill, skillLevel), (lastName))   
            # "UPDATE EmployeeList SET ('FirstName', 'LastName', 'FT/PT/.75?', 'Business Unit', 'City', 'State/Province', 'Career Matrix Title', 'Total Years', 'Registered Licenses', 'Skill', 'Skill Level') VALUES (?,?,?,?,?,?,?,?,?,?,?) WHERE ('LastName') VALUES (?)", (firstName, lastName, ftpt, businessunit, city, state, cmt, totalYears, registeredLicenses, skill, skillLevel), (lastName)) 
            # "UPDATE EmployeeList SET 'FirstName'=%s, 'FT/PT/.75'=%s, 'Business Unit'=%s, 'City'=%s, 'State/Province'=%s, 'Career Matrix Title'=%s, 'Total Years'=%s, 'Registered Licenses'=%s, 'Skill'=%s, 'Skill Level'=%s WHERE 'LastName'=%s" %(firstName, ftpt, businessunit, city, state, cmt, totalYears, registeredLicenses, skill, skillLevel, lastName))
            conn.commit()
            msg = "Record successfully updated"
        except:
            conn.rollback()
            msg = "error in modification operation"
        finally:
            conn.close()
            return msg


@app.route("/Employee/Main", methods=['GET', 'POST'])
def mainFunctionality():
    if request.method == 'GET':
        return render_template('Main.html')
    if request.method == 'POST':
        # Queries and such here, also functionality for filters once they appear
        return render_template('Main.html')  # Might need to rename this


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
