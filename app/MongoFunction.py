"""
# Project           : COMP9323
# Author            : Group 15
# Date created      : 25/10/2019
# Description       : Database operation functions
# Revision History  :
# Date              Author            Revision
# 31/10/2019        sherk             add a decoration to show db data
"""

from bson import ObjectId
import pymongo
from . import db

# control if show the data from mongodb
DEBUG = False


# decoration to show db data --------------------------------------------------------
def show_db_data(debug=DEBUG):
    def inner_data(func):
        def shower(*args, **kwargs):
            if debug:
                result = func(*args, **kwargs)
                if not isinstance(result, pymongo.cursor.Cursor):
                    print(f"\nDB_data: \n{result}\n")
                else:
                    print(f"\nDB_first_data: \n{result[0]}\n")
                return result
            else:
                return func(*args, **kwargs)
        return shower
    return inner_data


# personal profile --------------------------------------------------------
# course_id - string
@show_db_data()
def get_list_of_level_rank(course_id):
    result = db.users.aggregate(
        [{"$project": {
            "username": 1,
            "_id": 0,
            "rank": {
                "$filter": {
                    "input": "$levels",
                    "as": "x",
                    "cond": {
                        "$eq": ["$$x.course", ObjectId(course_id)]
                    }
                }
            }
        }}, {"$sort": {"rank.level": -1}}]
    )

    rank_result = []
    for key, value in enumerate(result):
        if value['rank']:
            rank_result.append([key+1, value['username'], int(value['rank'][0]['level'])])

    return rank_result


# get one course complete info. by user_id and course_id
@show_db_data()
def get_list_of_complete(user_id, course_id):
    result = db.users.aggregate(
        [{"$project": {
                "_id": 1,
                "complete": {
                    "$filter": {
                        "input": "$complete",
                        "as": "x",
                        "cond": {
                            "$eq": ["$$x.course", ObjectId(course_id)]
                        }
                    }
                }
            }}, {"$match": {"_id": ObjectId(user_id)}}]
        )

    return [i for i in result][0]


# get one course complete info. by username and course_id
@show_db_data()
def get_list_of_complete_username(username, course_id):
    result = db.users.aggregate(
        [{"$project": {
                "username": 1,
                "complete": {
                    "$filter": {
                        "input": "$complete",
                        "as": "x",
                        "cond": {
                            "$eq": ["$$x.course", course_id]
                        }
                    }
                }
            }}, {"$match": {"username": username}}]
        )

    return [i for i in result][0]

# get one course level info. by user_id and course_id
@show_db_data()
def get_list_of_levels(user_id, course_id):
    result = db.users.aggregate(
        [{"$project": {
                "_id": 1,
                "levels": {
                    "$filter": {
                        "input": "$levels",
                        "as": "x",
                        "cond": {
                            "$eq": ["$$x.course", ObjectId(course_id)]
                        }
                    }
                }
            }}, {"$match": {"_id": ObjectId(user_id)}}]
        )

    return [i for i in result][0]

# get one course pvp level info. by username and course_code
@show_db_data()
def get_list_of_pvplevels(username, course_code):
    print(username, course_code)
    result = db.users.aggregate(
        [{"$project": {
                "username": 1,
                "pvplevels": {
                    "$filter": {
                        "input": "$pvplevels",
                        "as": "x",
                        "cond": {
                            "$eq": ["$$x.course", course_code]
                        }
                    }
                }
            }}, {"$match": {"username": username}}]
        )

    return [i for i in result]

# personal profile --------------------------------------------------------
# game - question
# get all questions by node_id
@show_db_data()
def get_beginner_question(node_id):
    return db.question_set.find({"knowledge_node": ObjectId(node_id)})


# get all questions by chapter_id
@show_db_data()
def get_random_question(chapter_id):
    return db.question_set.find({"chapter": ObjectId(chapter_id)})


# get questions by question_id
@show_db_data()
def get_question(question_id):
    return db.question_set.find_one({"_id": ObjectId(question_id)})


# get user_id by username
@show_db_data()
def get_user_id(user_name):
    return db.users.find_one({"username": user_name})['_id']


@show_db_data()
def get_user_name(user_id):
    name_dic = db.users.find_one({'_id': ObjectId('{}'.format(user_id))}, {'username': 1, '_id': 0})
    name = name_dic['username']
    return name


@show_db_data()
def get_user_course_list(user_id):
    course_id_array = db.users.find_one({'_id': ObjectId('{}'.format(user_id))}, {'levels': 1, '_id': 0})
    course_id_list = []
    for each_course in course_id_array['levels']:
        course_id_list.append(each_course['course'])
    return course_id_list


@show_db_data()
def get_course_code_name_list(course_id_list):
    course_code_name_list = []
    for course_id in course_id_list:
        course_code_name = db.courses.find_one({'_id': ObjectId('{}'.format(course_id))},
                                               {'code': 1, 'name': 1, '_id': 0})
        course_code_name_list.append([course_code_name['code'], course_code_name['name']])

    return course_code_name_list
