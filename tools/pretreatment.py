import json
# 对字符串进行清洗
def pretreatment(file_name):
    with open(file_name,'r') as input_file:
        input_dict_list = json.load(input_file)
        for input_dict in input_dict_list:
            input_dict['title'] = input_dict['title'].strip(' \n\t')
            input_dict['desc'] = input_dict['desc'].strip(' \n\t')
            while '' in input_dict['tags']:
                input_dict['tags'].remove('')
            input_dict['answer_best'] = input_dict['answer_best'].strip(' \n\t')
            for i in range(len(input_dict['answers_other'])):
                input_dict['answers_other'][i] = input_dict['answers_other'][i].strip(' \n\t')
        with open(file_name.split('.')[0]+'_new.json','w') as output_file:
            output_data = json.dumps(input_dict_list)
            output_file.write(output_data)
        
                
if __name__ == "__main__":
    pretreatment("data3.json")
