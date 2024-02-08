"""
Demo of Gale-Shapley stable matching algorithm.
Written by Michael Goldwasser
Modified by Vicki Allan

For simplicity, the file format is assumed (without checking) to match
the following format:

  bob:     alice,carol
  david:   carol,alice

and likewise for the applicant file,  and the identifiers should be
self-consistent between the two files.
If a match is unacceptable, it is not listed in the preferences.

"""
from numpy import *


# from Marriage.Graph import Graph
"""APPLICANTS CHOOSING"""

class Person:
    """
    Represent a generic person
    """

    def __init__(self, name, priorities):
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        self.name = name
        self.priorities = priorities
        self.partner = None
        self.rank = None

    def __repr__(self):
        return 'Name is ' + self.name + '\n' + \
            'Partner is currently ' + str(self.partner) + str(self.rank) + '\n' + \
            'priority list is ' + str(self.priorities)


class Employer(Person):
    def __init__(self, name, priorities):
        super().__init__(name, priorities)
        self.ranking = {}
        for rank in range(len(priorities)):
            self.ranking[priorities[rank]] = rank

    def evaluateProposal(self, suitor):
        if suitor in self.ranking:
            if self.partner == None or self.ranking[suitor] < self.ranking[self.partner]:
                self.rank = self.ranking[suitor] + 1
                return True
            else:
                return False
        else:
            return False


class Applicant(Person):

    def __init__(self, name, priorities):
        super().__init__(name, priorities)
        self.proposalIndex = 0

    def nextProposal(self):
        if self.proposalIndex >= len(self.priorities):
            return None
        goal = self.priorities[self.proposalIndex]
        self.proposalIndex += 1
        return goal

    def evaluateProposal(self, suitor):
        """
        Evaluates a proposal, though does not enact it.

        suitor is the string identifier for the employer who is proposing

        returns True if proposal should be accepted, False otherwise
        """
        if suitor in self.ranking:
            if self.partner == None or self.ranking[suitor] < self.ranking[self.partner]:
                self.rank = self.ranking[suitor] + 1
                return True
            else:
                return False
        else:
            return False


def parseFile(filename):
    """
    Returns a list of (name,priority) pairs.
    """
    people = []
    # f = file(filename)
    with open(filename) as f:
        for line in f:
            pieces = line.split(':')
            name = pieces[0].strip()
            if name:
                priorities = pieces[1].strip().split(',')
                for i in range(len(priorities)):
                    priorities[i] = priorities[i].strip()
                people.append((name, priorities))
        f.close()
    return people


def printPairings(employer, applicant):
    for empl in employer.values():
        if empl.partner:
            print(empl.name, empl.rank, 'is paired with', str(empl.partner), applicant[str(empl.partner)].rank)
        else:
            print(empl.name, 'is NOT paired')


def calculate_preference_sum(person_dict):
    sum_of_preferences = 0
    for person in person_dict.values():
        if person.partner:
            sum_of_preferences += person.rank
    return sum_of_preferences


def doMatch(fileTuple):
    print("working with files ", fileTuple)
    employer_list = parseFile(fileTuple[0])
    employers = dict()
    for person in employer_list:
        employers[person[0]] = Employer(person[0], person[1])

    applicant_list = parseFile(fileTuple[1])
    applicants = dict()
    for person in applicant_list:
        applicants[person[0]] = Applicant(person[0], person[1])

    unmatched = list(applicants.keys())

    while len(unmatched) > 0:
        print("Unmatched applicants ", unmatched)
        a = applicants[unmatched[0]]
        e_name = a.nextProposal()
        if e_name is None:
            print('No more options for ' + str(a))
            unmatched.pop(0)
            continue
        employer = employers[e_name]
        verbose = fileTuple[2]
        if verbose: print(a.name, 'proposes to', employer.name)

        if employer.evaluateProposal(a.name):
            if verbose: print('  ', employer.name, 'accepts the proposal')

            if employer.partner:
                aOld = applicants[employer.partner]
                aOld.partner = None
                aOld.rank = 0
                unmatched.append(aOld.name)

            unmatched.pop(0)
            employer.partner = a.name
            a.partner = employer.name
            a.rank = a.proposalIndex
        else:
            if verbose:
                print('  ', employer.name, 'rejects the proposal')

        if verbose:
            print("Tentative Pairings are as follows:")
            printPairings(employers, applicants)

    # we should be done
    print("Final Pairings are as follows:")
    printPairings(employers, applicants)
    print("Sum of preferences for employers:", calculate_preference_sum(employers))
    print("Sum of preferences for applicants:", calculate_preference_sum(applicants))


files = [("Employers.txt", "Applicants.txt", True)]
for fileTuple in files:
    doMatch(fileTuple)
