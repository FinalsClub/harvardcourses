#!/usr/bin/python

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

def main():
    file = './courses_2012_spring.csv'
    courses = read_csv(file)
    t = init_mongo('fc')
    insert_courses(t, courses)

if __name__ == '__main__':
    main()
