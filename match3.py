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

"""EMPLOYER CHOOSING EQUAL TO APPLICANT"""
from numpy import *


# from Marriage.Graph import Graph


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
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        Person.__init__(self, name, priorities)
        self.proposalIndex = 0  # next person in our list to whom we might propose

    def nextProposal(self):
        if self.proposalIndex >= len(self.priorities):
            print('returned None')
            return None
        goal = self.priorities[self.proposalIndex]
        self.proposalIndex += 1
        return goal

    def __repr__(self):
        return Person.__repr__(self) + '\n' + \
            'next proposal would be to person at position ' + str(self.proposalIndex)


class Applicant(Person):

    def __init__(self, name, priorities):
        """
        name is a string which uniquely identifies this person

        priorities is a list of strings which specifies a ranking of all
          potential partners, from best to worst
        """
        Person.__init__(self, name, priorities)

        self.ranking = {}
        for rank in range(len(priorities)):
            self.ranking[priorities[rank]] = rank

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
    hr_list = parseFile(fileTuple[0])
    hr = dict()
    # each item in hr_list is a person and their priority list
    for person in hr_list:
        hr[person[0]] = Employer(person[0], person[1])
    unmatched = list(hr.keys())

    # initialize dictionary of appllicants
    applicant_list = parseFile(fileTuple[1])
    applicants = dict()
    # each item in applicant_list is a person and their priority list
    for person in applicant_list:
        applicants[person[0]] = Applicant(person[0], person[1])

    ############################### the real algorithm ##################################
    while len(unmatched) > 0:
        print("Unmatched employers ", unmatched)
        m = hr[unmatched[0]]  # pick arbitrary unmatched employer
        n = m.nextProposal()
        if n is None:
            print('No more options ' + str(m))
            unmatched.pop(0)
            continue
        who = applicants[n]
        verbose = fileTuple[2]
        if verbose: print(m.name, 'proposes to', who.name)

        if who.evaluateProposal(m.name):
            if verbose: print('  ', who.name, 'accepts the proposal')

            if who.partner:
                # prev partner dumped
                mOld = hr[who.partner]
                mOld.partner = None
                mOld.rank = 0
                unmatched.append(mOld.name)

            unmatched.pop(0)
            who.partner = m.name
            m.partner = who.name
            m.rank = m.proposalIndex
        else:
            if verbose:
                print('  ', who.name, 'rejects the proposal')

        if verbose:
            print("Tentative Pairings are as follows:")
            printPairings(hr, applicants)

    # we should be done
    print("Final Pairings are as follows:")
    printPairings(hr, applicants)

    print("Sum of preferences for employers:", calculate_preference_sum(hr))
    print("Sum of preferences for applicants:", calculate_preference_sum(applicants))


files = [("EmployersEX.txt", "ApplicantsEX.txt", True)]
for fileTuple in files:
    doMatch(fileTuple)
