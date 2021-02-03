from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database_connection
from datetime import datetime

@database_connection.connection_handler
def list_all_questions(cursor: RealDictCursor, order_by, order_direction):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {order_direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_one_by_id(cursor: RealDictCursor, data_table, id):
    query = f"""
        SELECT *
        FROM {data_table}
        WHERE id = {id}
    """
    cursor.execute(query)
    return cursor.fetchone()


@database_connection.connection_handler
def get_many_by_id(cursor: RealDictCursor, data_table, column_name, id):
    query = f"""
        SELECT *
        FROM {data_table}
        WHERE {column_name} = {id}
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def increase_view_number(cursor: RealDictCursor, id):
    query = f"""
        UPDATE question
        SET view_number = view_number + 1
        WHERE id = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def list_answer_for_question(cursor: RealDictCursor, id):
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = {id}
        ORDER BY vote_number DESC
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def edit_question(cursor: RealDictCursor, question_id, title, message):
    query = """
        UPDATE question
        SET title = %(title)s, message = %(message)s
        WHERE id = %(id)s
    """
    cursor.execute(query, {'title': title, 'message': message, 'id': question_id})


@database_connection.connection_handler
def edit_comment(cursor: RealDictCursor, comment_id, message):
    query = """
        UPDATE comment
        SET message = %(message)s
        WHERE id = %(id)s
    """
    cursor.execute(query, {'message': message, 'id': comment_id})


@database_connection.connection_handler
def edit_answer(cursor: RealDictCursor, answer_id, message):
    query = """
        UPDATE answer
        SET message = %(message)s
        WHERE id = %(id)s
    """
    cursor.execute(query, {'message': message, 'id': answer_id})


@database_connection.connection_handler
def new_question(cursor: RealDictCursor, form):
    date = datetime.now()
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message)
        VALUES ('{date}', 0, 0, '{form['title']}', '{form['message']}')
    """
    cursor.execute(query)
    cursor.execute('SELECT LASTVAL()')
    return cursor.fetchone()['lastval']


@database_connection.connection_handler
def new_answer(cursor: RealDictCursor, question_id, form):
    date = datetime.now()
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message)
        VALUES ('{date}', 0, {question_id}, '{form['message']}')
    """
    cursor.execute(query)
    cursor.execute('SELECT LASTVAL()')
    return cursor.fetchone()['lastval']


@database_connection.connection_handler
def insert_picture(cursor: RealDictCursor, data_table, id, pic_name):
    query = f"""
        UPDATE {data_table}
        SET image = '{pic_name}'
        WHERE id = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def delete_record(cursor: RealDictCursor, data_table, column_name, id):
    query = f"""
        DELETE FROM {data_table}
        WHERE {column_name} = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def vote(cursor: RealDictCursor, vote, data_table, id):
    number = 1 if vote == "upvote" else -1
    query = f"""
        UPDATE {data_table}
        SET vote_number = vote_number + {number}
        WHERE id = {id}
    """
    cursor.execute(query)


@database_connection.connection_handler
def new_comment(cursor: RealDictCursor, message, question_id=None, answer_id=None):
    date = datetime.now()
    column = 'question_id' if question_id else 'answer_id'
    id = question_id if question_id else answer_id
    query = f"""
        INSERT INTO comment ({column}, message, submission_time)
        VALUES ({id}, '{message}', '{date}')
    """
    cursor.execute(query)
    # cursor.execute('SELECT LASTVAL()')
    # return cursor.fetchone()['lastval']


@database_connection.connection_handler
def search(cursor: RealDictCursor, search_phrase):
    query = f"""
        SELECT question.id, question.submission_time, question.view_number,
            question.vote_number, question.title, question.message, question.image
        FROM question
        LEFT JOIN answer
        ON question.id = answer.question_id
        WHERE UPPER(CONCAT(title, question.message, answer.message)) LIKE UPPER('%{search_phrase}%')
        GROUP BY question.id
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def increase_comment_edit(cursor: RealDictCursor, comment_id):
    date = datetime.now()
    cursor.execute(f"SELECT edited_count FROM comment WHERE id = {comment_id}")
    if cursor.fetchone()['edited_count'] == None:
        query = f"""
            UPDATE comment
            SET edited_count = 1, submission_time = '{date}'
            WHERE id = {comment_id}
        """
    else:
        query = f"""
            UPDATE comment
            SET edited_count = edited_count + 1, submission_time = '{date}'
            WHERE id = {comment_id}
        """
    cursor.execute(query)