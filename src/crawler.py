__author__ = 'dghosh'
# TODO : provide as a service start/stop with pid, write to a log
import optparse
import json
import urllib
import BeautifulSoup
import dboperation
import re
import exceptions

def read_config(name):
    if not name : name = 'config.json'
    config_file = '../config/'+name
    c_f = open(config_file).read()
    c_json = json.loads(c_f)
    return dict(c_json)

def get_links(url, max_urls,dic):
    url_list =[]
    try:
        url_data = urllib.urlopen(url).read()
        b_soup = BeautifulSoup.BeautifulSoup(url_data)
        #print b_soup
        for line in b_soup.findAll('a'):
            append = True
            valid = False
            for line_1 in list(dic['do_not_crawl']):
               # print line
                try:
                    if str(line_1)  in str(line['href']):
                     #   print 'donot crawl'
                        append = False
                except :
                  #  print line,line_1,line_2
                    None
            for line_2 in list(dic['valid_TLDs']):

                #print str(line_2),line
                try:
                    if str(line_2)  in str(line['href']):
                        valid = True
                except KeyError:
                    None
                except UnicodeEncodeError:
                    print 'Ignoring special characters in url'
                    None
                except :
                    raise
            try:
                if append and valid:
                   # print 'i am appending'
                    url_list.append(line['href'])
            except KeyError:
                    None
            except :
                    raise

    except IOError:
        None
    except UnicodeEncodeError:
        print 'Ignoring special characters in url'
        None
    except:
        raise
    return (list(set(url_list)))[:max_urls]
if __name__ == '__main__':
    project_path = '/Users/agoel/DataScience/projects/craftswiz/'
    dic = {}
    url_list = []
    depth = None

    dic = read_config('config.json')
    max_link = dic['max_link']
    db_conn = dboperation.DbOperation(dbPath=project_path+'data/craftdb.sqlite')

    print 'Creating Data Model , if not present ..'
    db_conn.executeFile(project_path+'sql/create_data_model.sql')

    # determine if this is a new crawling or existing one:
    try:

        url = db_conn.executeSingleSQL(project_path+'sql/select_unprocessed.sql')
        depth = db_conn.executeSingleSQL(project_path+'sql/select_depth.sql',(url,)) + 1

    except :
        url = dic['start_url']
        depth = 0

    print "i got here"
        #print url, max_depth


        # populate tables
  #  print 'Inserting into URL table ..'
    db_conn.executeSingleDML(project_path+'sql/insert_records_url.sql',(url,depth))
    url_id = db_conn.executeSingleSQL(project_path+'sql/get_url_id.sql',(url,))

    base_url = re.findall('^([^.]+[^/]+)',url)
    print url,base_url
   # print 'Inserting into URL_base table ..'
    db_conn.executeSingleDML(project_path+'sql/insert_records_url_base.sql',(base_url[0],))
    base_url_id = db_conn.executeSingleSQL(project_path+'sql/get_url_base_id.sql',(base_url[0],))

    print "i got here too"
    while url and (depth < int(dic['max_depth'])):
        try:
    # now dig deeper:
            print 'url',url
            depth = int(db_conn.executeSingleSQL(project_path+'sql/select_depth.sql',(url,))) + 1
            print "got depth"
            url_list = get_links(url,max_link,dic)
            print 'got links'
            for row in url_list:
                try:
                    #print 'Inserting into URL table ..'
                    db_conn.executeSingleDML(project_path+'sql/insert_records_url.sql',(row,depth))
                    row_url_id = db_conn.executeSingleSQL(project_path+'sql/get_url_id.sql',(row,))
                    #print 'inserted urls'
                    base_row = re.findall('^([^.]+[^/]+)',row)

                  #  print 'Inserting into URL_base table ..'
                    db_conn.executeSingleDML(project_path+'sql/insert_records_url_base.sql',(base_row[0],))
                    row_base_id = db_conn.executeSingleSQL(project_path+'sql/get_url_base_id.sql',(base_row[0],))

                   # print 'Insert into association table'
                    db_conn.executeSingleDML(project_path+'sql/insert_record_url_association.sql',(url_id,row_url_id))

                   # print 'Insert into url_popularity'
                except IndexError:
                    None
                except :
                    raise

           # print 'Update Parent flag'
            #print str(url)
            db_conn.executeSingleDML(project_path+'sql/update_processed_flag.sql',(str(url),))

            #select next item if exists:
            try:
                url = db_conn.executeSingleSQL(project_path+'sql/select_unprocessed.sql')
                #print url
            except:
                break
        except KeyboardInterrupt:
            break


    print 'Inserting into URL_popularity table ..'
    db_conn.executeFile(project_path+'sql/insert_records_url_popularity.sql')


    #print 'Inserting into url_association table ..'

    db_conn.close()

