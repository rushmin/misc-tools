import sys
import requests
import json
import time
import argparse

def main(argv):

     # Parse command line arguments
    parser = getArgParser()
    args = parser.parse_args()

    apiKey = args.apiKey
    startDate = args.startDate
    endDate = args.endDate
    teamId = args.teamId

    baseURL = "https://www.findmyshift.com/api/1.1/"

    response = requests.get(baseURL + "reports/shifts?teamId=" + teamId + "&apiKey=" + apiKey + "&from=" + startDate + "&to=" + endDate)

    staffIds = set()

    for shiftItem in response.json():
        staffIds.add(shiftItem['staffId']);

    # Need to rest a bit to avoid rate limiting.
    time.sleep(5)

    staffResponse = requests.get(baseURL + "staff/list?teamId=" + teamId + "&apiKey=" + apiKey)

    employees = {};

    for employee in staffResponse.json():
        employees[employee['staffId']] = employee

    for staffId in staffIds:
        print(employees[staffId]['emailAddress']);

def getArgParser():

    parser = argparse.ArgumentParser(description='FMS Client')
    parser.add_argument('--api-key', help='API Key', dest='apiKey', required=True)
    parser.add_argument('--team-id', help='Team Id', dest='teamId', required=True)
    parser.add_argument('--start-date', help='Shift start date. e.g. 2019-07-01', dest='startDate', required=True)
    parser.add_argument('--end-date', help='Shift end date. e.g. 2019-07-05', dest='endDate', required=True)

    return parser;

if __name__ == '__main__':
   main(sys.argv[1:])
