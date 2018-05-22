import flask
import pymysql
import random

survey_blueprint = Blueprint('survey', __name__)

class GrabSurvey:
    # Define an object for records in the "questions" table.
    def __init__(self, id, createdBy, groupName, numMembers, dateCreated, members):
        self.text = text
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.r4 = r4
        self.id = id

    def serialize(self):
        return {
            'text': self.text,
            'r1': self.r1,
            'r2': self.r2,
            'r3': self.r3,
            'r4': self.r4,
            'id' = self.id,
            # required by Ember
            'type': 'survey'
        }

    def randQuest(self):
        # The following are IDs for questions that examine adherence 
        # to certain qualities identified by Meyers-Briggs.
        eori = [1, 8, 15, 22, 29, 36, 43, 50, 57, 64, 2, 9, 16, 23, 30, 37, 44, 51, 58, 65]
        sorn = [3, 4, 10, 11, 17, 18, 24, 25, 31, 32, 38, 39, 45, 46, 52, 53, 59, 60, 66, 67]
        torf = [5, 6, 12, 13, 19, 20, 26, 27, 33, 34, 40, 41, 47, 48, 54, 55, 61, 62, 68, 69]
        jorp = [7, 14, 21, 28, 35, 42, 35, 42, 49, 56, 63, 70]
        
        ids = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # test w/ 12 questions
        
        for i in range(len(ids) - 1):
            if(i < 3):
                ids[i] = random.sample(eori, 1)
            if(i < 6 and i > 2):
                ids[i] = random.sample(sorn, 1)
            if(i < 9 and i > 5):
                ids[i] = random.sample(torf, 1)
            if(i < 12 and i > 8):
                ids[i] = random.sample(jorp, 1)
            
        return ids

def grabQuestion(id, cursor):
	questions = []
	cursor.execute('SELECT id FROM survey where id=%s', id)
	results = cursor.fetchall()
	for result in results:
		questions.append(result[0])
	return quesions
		
def grabRandQuests():
    ids = self.ids      # IDs for questions we want
    quest4user = []     # what goes on the survey page
    
    for i in range(len(ids) - 1):
        # grab records for quesstions with IDs in ids