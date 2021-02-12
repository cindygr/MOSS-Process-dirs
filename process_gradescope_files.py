#!/usr/bin/env python3

from os import system
import csv
import sys


class CompareHandins:
    lab_names = {0: "Lab0", 1: "Lab_1_Functions", 2: "Lab_2_Filter_PDF_and",
                 3: "Lab3", 4: "Lab4", 5: "Lab5", 6: "Lab6", 7:"Lab7", 8:"Lab8"}
    hwk_names = {1: "Homework_1_Data_analysis_PDF_and_code"}
class CompareHandins:
    lab_names = {0: "Lab0", 1: "Lab_1_Functions", 2: "Lab_2_Filter_PDF_and",
                 3: "Lab3", 4: "Lab4", 5: "Lab5", 6: "Lab6", 7:"Lab7", 8:"Lab8"}
    hwk_names = {0: "Homework1"}
    base_name = "Data"

    def __init__(self, term=""):
        """ Store term name"""
        self.term_name = term
        self.roster = self.build_roster()

    def build_dir_name(self):
        """Directory everything for this term is in"""
        return CompareHandins.base_name + "/" + self.term_name + "/"

    def build_lab_folder_name(self, lab=1):
        """Directory for student submisions
        :Param lab which lab to do"""
        return self.build_dir_name() + "Lab" + str(lab) + "/"

    def build_roster(self):
        """Read in the roster and build a name->id match"""
        fname = self.build_dir_name() + "ME_499_599_" + self.term_name + "_roster.csv"
        all_students = []
        try:
            with open(fname, "r") as f:
                roster_reader = csv.reader(f)
                for row in roster_reader:
                    student_data = [row[0], row[1], row[2]]
                    if row[4] is not "Student":
                        all_students.append(student_data)
        except FileNotFoundError:
            print("Please download gradescope roster and place in Data/{0}".format(self.term_name))
        return all_students

    def mv_submission_names(self, lab=-1, hwk=-1, print_only=True):
        """Process the csv file wiTrueth the submissions to get matching names/folders"""
        try:
            fname = self.build_dir_name() + "Lab" + str(lab) + "/" + CompareHandins.lab_names[lab] + "_Code__scores.csv"
            fname = self.build_dir_name() + "Lab" + str(lab) + "/" + CompareHandins.lab_names[lab] + "__scores.csv"
            folder_name = self.build_dir_name() + "Lab" + str(lab) + "/"
        except KeyError:
            fname = self.build_dir_name() + "Homework" + str(hwk) + "/" + CompareHandins.hwk_names[hwk] + "__scores.csv"
            folder_name = self.build_dir_name() + "Homework" + str(hwk) + "/"

        all_students = []

        to_remove = {' ', '-', "'"}
        try:
            with open(fname, "r") as f:
                submissions_reader = csv.reader(f)
                for row in submissions_reader:
                    first = row[0].strip("-, '")
                    last = row[1].strip("-, '")
                    for c in to_remove:
                        first = "".join(first.split(c))
                        last = "".join(last.split(c))
                    try:
                        submission_id = int(row[8])
                        old_name = "submission_{0}".format(submission_id)
                        new_name = "{0}_{1}_{2}".format(self.term_name, first, last)
                        system_call = "mv {0}{1} {0}{2}".format(folder_name, old_name, new_name)
                        print(system_call)
                        if not print_only:
                            system(system_call)
                    except ValueError:
                        pass
                    except IndexError:
                        print("Student missing code: {0} {1}".format(first, last))
        except FileNotFoundError:
            print("Make sure directory {0} exists and file {1} is in that directory.".format(folder_name, fname))
        return all_students


if __name__ == '__main__':
    """ Get setup
    From Gradescope: Select the assignment, then click on review grades (LHS)
    On the bottom: Download grades->Download csv and Export submissions
    move the zip file into Data/Term and then unzip. Rename the folder Data/Term/Lab? or Hwk?
    move the csv file into the Lab? or Hwk? directory
    In the code below, change the term to be the desired term and run mv_submissions.
        This should rename all of the submissions to term_first_last 
    Now you can run Moss
        cd Data/
        perl moss.perl -l python -d term/Lab?/*/*.py"""
    class_one = CompareHandins("Spring_2020")
    class_two = CompareHandins("Winter_2021")

    class_one.mv_submission_names(hwk=1, print_only=False)
    class_two.mv_submission_names(hwk=1, print_only=False)

    if len(sys.argv) < 3:
        print("Usage: Term [string] lab/hwk number")
        exit(1)

    print("Term {0} lab/hwk {1} number {2}".format(sys.argv[1], sys.argv[2], sys.argv[3]))
    class_one = CompareHandins(sys.argv[1])

    if sys.argv[2] == "lab":
        class_one.mv_submission_names(lab=int(sys.argv[3]), print_only=False)
    else:
        class_one.mv_submission_names(hwk=int(sys.argv[3]), print_only=False)

    print("perl moss.perl -l python -d {0}/Lab{1}/*/*.py".format(sys.argv[1], int(sys.argv[3])))
