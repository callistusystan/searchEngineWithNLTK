from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk.wsd import lesk
from nltk import word_tokenize
from collections import defaultdict
from career_parser import CareerParser, ID, NAME, DESC, INTERESTS
from nltk.stem.wordnet import WordNetLemmatizer

INTEREST_CONTEXT_FILE_RAW = "interest_context_raw.csv"
INTEREST_CONTEXT_FILE_PROCESSED = "interest_context_processed.csv"

class InterestCareerMapper:
    def __init__(self):
        cp = CareerParser()
        self.careers = cp.careers

        # get interest context
        # see if we should recompute interestContext or not
        choice = None
        while choice not in ["y","n"]:
            choice = input("Should we recompute interest context? (y/n) ")
        if choice == "y":
            self.interestContext = self.computerInterestContext(self.careers)
            self.writeToInterestContextFile(INTEREST_CONTEXT_FILE_RAW)
            self.processInterestContext()
            self.writeToInterestContextFile(INTEREST_CONTEXT_FILE_PROCESSED)
        else:
            self.interestContext = self.getInterestContext(INTEREST_CONTEXT_FILE_PROCESSED)

        # loop through interest context, and create a mapping
        self.interestContextToCareer = self.getInterestContextToCareer()

        # loop through interest context, and map hypernyms and hyponyms to interest context

    def computerInterestContext(self, careers):
        """
        Computes a dictionary mapping interest to the NLTK synset name with
        same context (not 100%)
        1. loop through each career
        2. get interests of each career
        3. make a sentence in the format:
            A <career_name> should like <interest1> and <interest2> and ...
        4. Pass it to NLTK lesk to determine context
            (Of course, this isnt 100%, but a good approximate)
        """
        interestContext = {}
        # loop each career
        for career in self.careers.values():
            print("Looking at {}".format(career[NAME]))
            N = len(career[INTERESTS])
            interestList = list(career[INTERESTS])
            interestList.sort()

            # make the sentence
            sentence = "A {} should like ".format(career[NAME])
            for i in range(N):
                interest = interestList[i]
                verbForm = WordNetLemmatizer().lemmatize(interest,'v')
                sentence += verbForm + [" and ", "."][i==N-1]
            print("Sentence:",sentence,"\n")

            # determine context of each interest
            splitSentence = sentence.split()
            for interest in career[INTERESTS]:
                if interest in interestContext:
                    continue
                print(" Determining the context of {}".format(interest))
                ss = lesk(splitSentence, interest)
                interestContext[interest] = (ss, "n")
                if ss is not None:
                    print(" - {}".format(ss.definition()))
                else:
                    print(" - UNABLE TO DETERMINE")
                print()
            # uncomment following if you want to view one at a time
            # input("Press enter to continue...")
            # print("\n"*4)
        return interestContext

    def writeToInterestContextFile(self, filename):
        with open(filename, "w") as f:
            for interest in self.interestContext.keys():
                ss = self.interestContext[interest][0]
                flag = self.interestContext[interest][1]
                f.write("{},{},{}\n".format(interest, (ss.name() if ss is not None else None), flag))

    def processInterestContext(self):
        interests = self.interestContext.keys()
        print("We need your help to confirm the contexts")
        input("Press Enter to continue")
        for interest in interests:
            print("Looking at '{}'".format(interest))
            if self.interestContext[interest][0] is None:
                continue
            print("\t- {}".format(self.interestContext[interest][0].definition()))
            choice = None
            while choice not in ["y","n"]:
                choice = input("Is this correct? (y/n) ")
            print()
            if choice == "y":
                self.interestContext[interest] = (self.interestContext[interest][0], "y")
            else:
                for ss in wn.synsets(interest):
                    print("\t{}".format(ss.definition()))
                    choice = None
                    while choice not in ["y","n"]:
                        choice = input("Is this correct? (y/n) ")
                    if choice == "y":
                        self.interestContext[interest] = (ss, "y")
                        break

    def getInterestContext(self, filename):
        interestContext = {}
        with open(filename, "r") as f:
            lines = [line.strip() for line in f]
            for line in lines:
                print(line)
                interest, ssName, flag = line.split(",")
                if flag == "y":
                    interestContext[interest] = (wn.synset(ssName), flag)
        return interestContext

    def getInterestContextToCareer(self):
        interestContextToCareer = defaultdict(set)
        for career in self.careers.values():
            print(career)
            if len(career[INTERESTS]) > 0:
                for interest in career[INTERESTS]:
                    if interest in self.interestContext:
                        ssName = self.interestContext[interest][0].name()
                        interestContextToCareer[ssName].add(career[ID])
        return interestContextToCareer

def main():
    icm = InterestCareerMapper()

if __name__ == "__main__":
    main()
