import psycopg2
import psycopg2.extras
import json
from jsonmerge import merge

from config_db import dbuser, dbname

privacy_server = "dbname=%s user=%s" % (dbname, dbuser)

INSERT = "INSERT INTO privacy_server (patient_id, policy, last_modified) VALUES (%s, %s, %s)"
DELETE = "DELETE FROM privacy_server WHERE patient_id = %s"
SELECT = "SELECT FROM privacy_server WHERE patient_id = %s"
UPDATE = "UPDATE privacy_server set policy=%s, last_modified=%s WHERE id=%s"



def search_record(patient_id):
    """
    This function search for the record of the given patient.
    :param patient_id:  the patient's id
    :return:            return 1 if the record exists
                        return 0 if the record doesn't exist
    """
    conn = psycopg2.connect(privacy_server)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT, (patient_id,))
            result = curs.fetchone()

    if result is not None:
        return 1
    else:
        return 0

def insert_record(patient_id, policy, time):
    """
    :param patient_id:  patient id that identifies the patient
    :param policy:      patient's privacy policy
    :param time:        time that the policy is inserted
    :return:            return 1  if inserted successfully
                        return 0  if the patient's policy already exists
                        return -1 if the type of parameter is wrong
    """
    conn = psycopg2.connect(privacy_server)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT, (patient_id,))
            result = curs.fetchone()

    if result is None:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            with curs:
                if type(policy) == dict or list:
                    dumped_policy = json.dumps(policy, sort_keys=True)
                elif type(policy) == str:
                    dumped_policy = json.dumps(json.loads(policy))
                else:
                    conn.close()
                    return -1
                curs.execute(INSERT, (patient_id, dumped_policy, time))
    else:
        return 0

    conn.commit()
    conn.close()
    return 1


def delete_record(patient_id):
    """
    :delete the record of the patient identified by the given id

    :param patient_id: the patient's id whose record will be deleted
    """
    conn = psycopg2.connect(privacy_server)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(DELETE, (patient_id,))


def add_policy(patient_id, added_policy, time):
    """
    This function add added_policy into a patient existing privacy policy.
    If the patient is not in the database, then create a new record with added_policy.
    :param patient_id:      the patient id
    :param added_policy:    the additional privacy policy that will be added
    :param time:            the time that the record is modified
    :return:                return 1 if policy added successfully
    """
    conn = psycopg2.connect(privacy_server)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT, (patient_id,))
            result = curs.fetchone()

    if result is not None:
        merged_policy = merge(result['policy'], added_policy)
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            with curs:
                curs.execute(UPDATE, (merged_policy, time, patient_id))
    else:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
            with curs:
                curs.execute(INSERT, (patient_id, added_policy, time))

    return 1


"""
def delete_policy(patient_id):
    conn = psycopg2.connect(privacy_server)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute()
"""


def select_policy(patient_id):
    """
    This function select the record of the assumed patient and return the patient's privacy record
    :param patient_id:  the patient id
    :return:            return the privacy policy
                        return 0 if the patient is not in the database
    """
    conn = psycopg2.connect(privacy_server)

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as curs:
        with curs:
            curs.execute(SELECT, (patient_id,))
            result = curs.fetchone()

    if result is not None:
        return result
    else:
        return 0
