import os
import sqlite3

class QuestionModel: 
    def __init__(self, database_file):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    # Select all questions with questions with special characters from db
    def getAllSpecialCharacters(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f'SELECT * FROM vragen WHERE vraag LIKE "%<br>%" OR vraag LIKE "%&nbsp;%" OR vraag LIKE "%<p>%" OR vraag LIKE "%<script>%" OR vraag LIKE "%<a>%";')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    # Edit special characters
    def editSpecialCharacters(self, id, question):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE vragen SET vraag = ? WHERE id = ?', (question, id))
        conn.commit()

    # Get question with specific id from db
    def getSpecificQuestion(self, id):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, vraag FROM vragen WHERE id = ?', (id,))
        result = cursor.fetchone()

        return result

    # Get all null values from db
    def getAllNullValues(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f'SELECT id, leerdoel, vraag, auteur FROM vragen WHERE vraag IS NULL OR auteur IS NULL OR leerdoel IS NULL;')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    # Get question row with specific id from db
    def getSpecificQuestionRow(self, id):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, leerdoel, vraag, auteur FROM vragen WHERE id = ?', (id,))
        result = cursor.fetchone()

        return result

    # Edit null values
    def editNullValues(self, id, learningGoal, question, author):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE vragen SET leerdoel = ?, vraag = ?, auteur = ? WHERE id = ?', (learningGoal, question, author, id))
        conn.commit()

    # Get all columns from db
    def getAuthors(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f'SELECT * FROM `auteurs`')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    # Edit collaborator in author table
    def editAuthor(self, id, collaborator):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE auteurs SET medewerker = ? WHERE id = ?', (collaborator, id))
        conn.commit()

    # Get all faulty goals from db
    def getWrongGoals(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f'SELECT * FROM vragen WHERE leerdoel NOT IN (SELECT id FROM leerdoelen);')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    # Edit faulty goal
    def editWrongGoals(self, id, collaborator):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'UPDATE vragen SET leerdoel = ? WHERE id = ?;', (collaborator, id))
        conn.commit()

    # Get goal IDs
    def getAllGoalID(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cur_ex = cursor.execute(f'SELECT * FROM leerdoelen;')
        empty_list = []
        for x in cur_ex:
            empty_list.append(x)
        return empty_list


    def allid(self):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, vraag FROM vragen;')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    def specifiedid1(self):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vragen WHERE id BETWEEN 1 and 35;')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    def specifiedid2(self):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vragen WHERE id BETWEEN 35 and 70;')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers

    def specifiedid3(self):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM vragen WHERE id BETWEEN 70 and 95;')
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        return table_content, table_headers