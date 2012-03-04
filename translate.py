#!/usr/bin/python

import csv

def read_csv(file):
    # make csvreader
    csvreader = csv.reader(open(file))
    for line in csvreader:
        # Field,Number,Title,Meetings,n (Past Enrollment)
        # print the course name and time
        print line[2], line[-1]

if __name__ == '__main__':
    read_csv('./courses_2012_spring.csv')
