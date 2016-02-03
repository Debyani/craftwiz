__author__ = 'dghosh'
import dboperation

''' This programs takes 2 inputs :
    keyword to search : its a simple text search at this point
    result_num : number of results
'''

if __name__ == '__main__':
    key_search = raw_input('Enter the text to search :')
    num_results = raw_input('Enter how many max links do you want :')

    if not key_search :
        print "Error, search text cannot be null"
        exit()
    if not num_results:
        num_results = 10

    key_search_like = '%'+key_search+'%'
    project_path = '/Users/agoel/DataScience/projects/craftswiz/'

    db_conn = dboperation.DbOperation(dbPath=project_path+'data/craftdb.sqlite')
    craft_list = db_conn.executeSingleSQLfetchall(project_path+'sql/select_matching_craft.sql',(key_search_like,))
    craft_list = craft_list[:int(num_results)]
    for craft_url in craft_list:
        print "crafts matching" ,key_search,':', craft_url[0]