import csv


class Reader:
    
    @staticmethod
    def getReader(name, ) -> csv.DictReader:
        with open(name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            return reader