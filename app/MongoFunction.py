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
# 获取用户的关于course_id的用户名和level -> [tuple,...]
# 问题: 这里如何数据库没有level项，在做聚合的时候无法返回正确值，会导致ranking页面加载失败
@show_db_data()
def get_list_of_level_rank(course_id):
    result = db.users.aggregate(
        [{"$project": {
                "username": 1,
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

    return [(i['username'], i['rank'][0]['level']) for i in result]


# 获取用户的关于course_id的用户名和complete
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


# 获取关于course_id和user_id的levels
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


# personal profile --------------------------------------------------------
# game - question
# node_id - string
# 获取基于node_id的知识节点的题目
# 返回mongodb command cursor, 可迭代
@show_db_data()
def get_beginner_question(node_id):
    return db.question_set.find({"knowledge_node": ObjectId(node_id)})


# 获取基于chapter_id的随机题目
# 返回mongodb command cursor, 可迭代
@show_db_data()
def get_random_question(chapter_id):
    return db.question_set.find({"chapter": ObjectId(chapter_id)})


# 获取基于question_id的question object - 可用于solution搜索
# 返回一条数据
@show_db_data()
def get_question(question_id):
    return db.question_set.find_one({"_id": ObjectId(question_id)})


# profile
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
