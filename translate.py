#!/usr/bin/python

import datetime
import csv
import time

import pymongo

def init_mongo(dbname, collection):
    conn = pymongo.Connection() # put db info here
    db = conn[dbname]
    t = db[collection]
    return t

def read_csv(file):
    # make csvreader
    csvreader = csv.reader(open(file))
    courses = []
    for line in csvreader:
        # Field,Number,Title,Meetings,n (Past Enrollment)
        # print the course name and time
        course = {}
        course['field'] = line[0]
        course['number'] = line[1]
        course['title'] = line[2]
        course['meetings'] = line[3]
        course['enrollment'] = line[4]
        courses.append(course)
    return courses

def insert_courses(collection, courses):
    for c in courses:
        collection.insert(c)

def week_parse(courses):
    days = {
        'TuTh': [1,3],
         'W': [2],
         'Tu': [1],
         'M': [0],
         'MW': [0,2],
         'MWF': [0,2,5],
         'Th': [3]
         }

    weekly_events = []
    for course in courses:
        date = course['meetings']

        d = date.split(' ') # split the date after the first or each space
        weekly_classes = days[d[0]]

        ntime = d[1].split('-') # split the time segment to get the start time

        # one for each of the days of the week a course is held
        for day in weekly_classes:
            event = course # an event is a weekly instance of a course
            event['weekday'] = day
            event['time_start'] = ntime[0] # the starting time of the course
            weekly_events.append(event)

    return weekly_events


def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta

def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day-1, weeks=iso_week-1)

def semester_parse(weekly, t):
    lectures = []
    for weekly_lecture in weekly:
        weekday = weekly_lecture['weekday']
        print weekday
        # Turn lecture['time_start'] into a time object
        timey = time.strptime(weekly_lecture['time_start'], '%H:%M%p')
        # make a datetime.time object to combine later
        dtime = datetime.time(timey.tm_hour, timey.tm_min)
        # for week in first week of semester to finals week @ harvard
        # may 4th is the last possible class date before may 5th finals
        # http://webdocs.registrar.fas.harvard.edu/general_docs/final_exams.html
        # > datetime.date(2012, 5, 4).isocalendar() >> (2012, 18, 5)
        for week in range(1,18):
            event = {}
            event['title'] = weekly_lecture['title']
            event['number'] = weekly_lecture['number']
            event['field'] = weekly_lecture['field']

            # from the week information, make a date element
            date = iso_to_gregorian(2012, week, weekday)
            # save this new datetime object of the class start into lect
            event['date'] = datetime.datetime.combine(date, dtime)
            # save lect in a new list of all lecture_events
            lectures.append(event)
    return lectures

def main():
    file = './courses_2012_spring.csv'
    courses = read_csv(file)
    t = init_mongo('fc', 'LiveCourses')
    weekly_courses = week_parse(courses)
    weekly_lectures = semester_parse(weekly_courses, t)
    insert_courses(t, weekly_lectures)

if __name__ == '__main__':
    e = main()
