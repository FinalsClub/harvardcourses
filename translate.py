#!/usr/bin/python

import datetime
import csv

import pymongo

def init_mongo(dbname):
    conn = pymongo.Connection() # put db info here
    fc = conn[dbname]
    t = fc.test_collection
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
    dates = [x['meetings'] for x in courses]
    dates.sort()
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

        time = d[1].split('-') # split the time segment to get the start time

        # one for each of the days of the week a course is held
        for day in weekly_classes:
            event = course # an event is a weekly instance of a course
            event['weekday'] = day
            event['time_start'] = time[0] # the starting time of the course
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
    thing = []
    for lecture in weekly:
        weekday = lecture['weekday']
        for week in range(1,3):
            thing.append( iso_to_gregorian(2012, week, weekday) )
    return thing

def main():
    file = './courses_2012_spring.csv'
    courses = read_csv(file)
    t = init_mongo('fc')
    #insert_courses(t, courses)
    weekly_courses = week_parse(courses)
    return semester_parse(weekly_courses, t)

if __name__ == '__main__':
    e = main()
