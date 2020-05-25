# testList = ['T336F_艳阳花开', 'T338F_芭蕾元素', 'T341F_仙人掌']
# for i in testList:
#     print(i)


# import re
# # test = "T336F_yanyanghuakai666.jpg"
# #
# # mm = re.search(r"616",test)
# # if mm:
# #     print(test)

# import os
# path = "D:\learn\AutoUpLoad\data\特辑套图\T336F_艳阳花开"
# test_list = ['T336F_01.jpg', 'T336F_02.jpg', 'T336F_03.jpg', 'T336F_04.jpg']
# myTest = [path+os.sep+x for x in test_list]
# print(myTest)

# from fileUpload.single import single
#

# from jsonpath import jsonpath
# mm = {
# 	'stateCode': 200,
# 	'stateMsg': 'OK',
# 	'currentPage': 1,
# 	'pageSize': 1000,
# 	'totalNum': 1,
# 	'totalPage': 1,
# 	'data': [{
# 		'id': 'efbc88c058dc412e97790f60dd38ba57',
# 		'uid': 90001399,
# 		'username': 'oFZ0f1LJfAtkKyVkJw_hmg3YyQ2U',
# 		'nickname': 'YaDAn7',
# 		'email': None,
# 		'mobile': None,
# 		'lastName': '',
# 		'firstName': '',
# 		'headPortrait': '/tutu/anjou/headportrait/20200313100252016_247023.jpeg',
# 		'headPortraitThumbnail': '/tutu/anjou/headportrait/20200313101000620_427919.png',
# 		'sex': 0,
# 		'userStatus': '0',
# 		'creatorId': 'efbc88c058dc412e97790f60dd38ba57',
# 		'creatorName': 'YaDAn7',
# 		'createTime': '2020-03-13 10:02:52',
# 		'modifierId': '',
# 		'modifierName': '',
# 		'modifyTime': None,
# 		'recordState': 0,
# 		'productLineId': '46981435671117824',
# 		'clientId': 'f9c8218ff78a4e8daa6f014b20c61be2',
# 		'tenantId': '61bf9fc4a862452c8e7f09ef0b4e9a42',
# 		'birthday': '',
# 		'country': '',
# 		'province': '',
# 		'area': '',
# 		'city': '',
# 		'address': '',
# 		'industry': ''
# 	}]
# }
#
# test = jsonpath(mm,'$..id')
# print(test)


# a = ()


from queue import Queue, LifoQueue, PriorityQueue

# 先进先出队列
q = Queue(maxsize=5)
# 后进先出队列
lq = LifoQueue(maxsize=6)
# 优先级队列
pq = PriorityQueue(maxsize=5)

for i in range(5):
    q.put(i)
    lq.put(i)
    pq.put(i)

print("先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" % (q.queue, q.empty(), q.qsize(), q.full()))

print("后进先出队列：%s;是否为空：%s;多大,%s;是否满,%s" % (lq.queue, lq.empty(), lq.qsize(), lq.full()))

print("优先级队列：%s;是否为空：%s,多大,%s;是否满,%s" % (pq.queue, pq.empty(), pq.qsize(), pq.full()))


print(q.get(), lq.get(), pq.get())

print("先进先出队列：%s;是否为空：%s；多大,%s;是否满,%s" % (q.queue, q.empty(), q.qsize(), q.full()))

print("后进先出队列：%s;是否为空：%s;多大,%s;是否满,%s" % (lq.queue, lq.empty(), lq.qsize(), lq.full()))



