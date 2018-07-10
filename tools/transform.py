# -*- coding: utf-8 -*-
import json
# 转换json格式的函数
def transform(file_name):
    with open(file_name+'.json') as rawlines:
        QA_list = []
        data = json.load(rawlines, encoding='UTF-8')
        for (key, val) in data.items():
            cur_QA = dict()
            cur_QA['question'] = val['question']
            cnt = 0
            for (key,val) in val['evidences'].items():
                ans_key = 'answer_best'
                if cnt > 0:
                    ans_key = 'answer_%d'%cnt
                cnt += 1 
                cur_QA[ans_key] = ','.join(val['answer'])+"."+val['evidence']
            QA_list.append(cur_QA)

        with open(file_name+'_transformed.json','w') as out:
            json_file = json.dumps(QA_list)
            out.write(json_file)

if __name__ == '__main__':
    file_name = "WebQA/me_validation.ann"
    transform(file_name)
    