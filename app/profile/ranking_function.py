from bson import ObjectId
import pymongo


# update from the sherk's file
# connect to the pymongo
client = pymongo.MongoClient("mongodb+srv://public:1234567890unsw@devdb-30fsv."
                             "mongodb.net/test?retryWrites=true&w=majority")
db = client.main

# get the ranks
def get_list_of_level_rank(course_id):
    '''
    this function returns the list of level and rank
    :param course_id: course object id
    :type course_id: pymongo object id
    :return: a list of [rank, username, level]
    :rtype: list
    '''

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

    # the sample result is 1 => {'username': 'xinyuan',
    #                               'rank': [{'course': ObjectId('5db18c70c10657b763c513d5'), 'level': 4}]}
    # deal with rank: [] or rank: None

    # return a list of list: [[rank, username, level], [], []]
    rank_result = []
    for key, value in enumerate(result):
        if value['rank']:
            rank_result.append([key+1, value['username'], int(value['rank'][0]['level'])])

    return rank_result


def get_user_course_list(username):
    '''

    :param user_id: user object id
    :type user_id: object id
    :return: empty list if the person does not have 'levels' field
             course_id_list: list with course object id if this person has 'levels' field
    :rtype: list
    '''

    # check if the user has levels in the document
    check_level_exist = db.users.find_one({'username': username, 'levels': {'$exists': True, '$ne': False}})

    if check_level_exist:
        # this user has levels in the document
        course_id_array = db.users.find_one({'username': username},
                                            {'levels':1, '_id': 0}
                                            )
        course_id_list = []
        for each_course in course_id_array['levels']:
            course_id_list.append(each_course['course'])
        return course_id_list

    else:
        # if the user has no 'levels' in the document, return empty
        return []


def get_course_code_name_list(course_id_list):
    '''

    :param course_id_list: course object id list
    :type course_id_list: list
    :return: course code name list, cannot be empty since field 'levels' is checked
    :rtype: list
    '''
    course_code_name_list = []
    for course_id in course_id_list:
        course_code_name = db.courses.find_one({'_id':ObjectId('{}'.format(course_id))},
                                               {'code':1, 'name':1, '_id':0})
        course_code_name_list.append([course_code_name['code'], course_code_name['name']])

    return course_code_name_list


def get_position_list(username, total_rank_list):
    '''

    :param username: username of the current user
    :type username: string
    :param total_rank_list: descending rank list of all coursers this user taken
    :type total_rank_list: list
    :return: position list: you have beaten xx% users !!
    :rtype: list of float
    '''
    position_list = []
    for course_rank in total_rank_list:
        num_people = len(course_rank)
        for index, person in enumerate(course_rank):
            if person[1] == username:
                position_list.append(round(float(1 - (index + 1) / num_people)*100))

    return position_list

def get_question_correct_answer(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['correct_answer']

def get_question_option(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['option']

def get_user_info(user_name):
    result = db.users.find_one({"username": user_name})
    return result


def get_course_name(course_id):
    course = db.courses.find_one({"_id": course_id})
    if course:
        return course['name']


def get_course_code(course_id):
    course = db.courses.find_one({"_id": course_id})
    if course:
        return course['code']


def get_chapter_name(chapter_id):
    chapter = db.chapters.find_one({"_id": chapter_id})
    if chapter:
        return chapter['name']


def get_question_content(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['content']


def get_question_course(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['course']


def get_question_chapter(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['chapter']

def get_question_knowledge_node(question_id):
    question = db.question_set.find_one({"_id": question_id})
    if question:
        return question['knowledge_node']

def get_node_name(node_id):
    node = db.knowledge_nodes.find_one({"_id": node_id})
    if node:
        return node['name']
def correct_answer(str):
    if str == '1':
        return 'A'
    elif str == '2':
        return 'B'
    elif str == '3':
        return 'C'
    elif str == '4':
        return 'D'

if __name__ == '__main__':
    pass