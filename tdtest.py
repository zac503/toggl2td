from TdApi import TdApi

user_config = {}

with open('config.txt','r') as f:
    for line in f:
        user_config[line.split('=')[0]] = line.split("=")[1].rstrip()

team_dynamix_api = TdApi(user_config['td_api_BEID'],
                      user_config['td_api_Key'])

team_dynamix_api.authenticate()
user_id = team_dynamix_api.get_user('Zach Phillips')
team_dynamix_api.set_default_user(user_id)
project_list = team_dynamix_api.get_project_list()

cleaned_project_list = [obj for obj in project_list if(obj['Name'] != 'Private Team')]

team_dynamix_api.write_project_file(cleaned_project_list)

#for item in cleaned_project_list:
#    print('Project Name:{} Project ID:{}'.format(item['Name'],item['ID']))


