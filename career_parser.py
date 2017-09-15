import csv
from collections import defaultdict

CSV_FILE = "myFuture Dataset.csv"
ID = "id"
NAME = "name"
DESC = "description"
INTERESTS = "interests"

class CareerParser:
    def __init__(self):
        # get all careers
        data = self.parseCSV(CSV_FILE)
        self.careers = self.getCareers(data)

    def parseCSV(self, filename):
        with open(filename, "r") as f:
            reader = csv.reader(f)
            return list(reader)

    def getCareers(self, data):
        careers = {}
        for careerLine in data:
            # create career object
            career = {}
            career[ID] = careerLine[0]
            career[NAME] = careerLine[1]
            career[DESC] = careerLine[3]
            career[INTERESTS] = [interest.strip() for interest in careerLine[4].split(",")]

            # check if there are interests
            if (career[INTERESTS] == [""]):
                career[INTERESTS] = []

            careers[career[ID]] = career

        return careers

    def isSynset(self, word):
        return word.count(".") == 2
