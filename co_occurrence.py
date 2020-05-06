import pymysql, os, csv

tables = [
    "glaston29_BL",
    'glaston29_Extra',
    'glaston29_TF'
]

connection = pymysql.connect(
    host='localhost',
    user='root',
    password=os.environ.get('MYSQL_PWD'),
    db='ecs637u_digitalmedia',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    for table in tables:
        weighted_edge_list = dict()
        with connection.cursor() as cursor:
            sql = "SELECT `hashtags` FROM {}".format(table)
            cursor.execute(sql)
            results = cursor.fetchall()
            for result in results:
                hashtags = result.get('hashtags').split(' ')
                hashtags = hashtags[:len(hashtags)-1]
                hashtags = list(set(hashtags))
                if len(hashtags) > 1:
                    if weighted_edge_list.get(hashtags[0]) is None:
                        weighted_edge_list[hashtags[0]] = dict()
                    for tags in hashtags[1:]:
                        if weighted_edge_list[hashtags[0]].get(tags) is None:
                            weighted_edge_list[hashtags[0]][tags] = 1
                        else:
                            weighted_edge_list[hashtags[0]][tags] += 1

            with open('./edge_lists/{}_weighted.csv'.format(table), 'w') as f:
                writer = csv.writer(f,delimiter=";")
                #writer.writerow(["source", "target", "weight"])
                for src, dsts in weighted_edge_list.items():
                    for dst, weight in dsts.items():
                        writer.writerow([src,dst,weight])

finally:
    connection.close()
