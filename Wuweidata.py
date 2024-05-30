#我们将使用 Python 的 json 库来处理 JSON 格式的数据，并使用 pandas 库来读取和处理数据集。假设数据集以 CSV 格式提供，我们将使用 pandas 读取 CSV 文件。
import pandas as pd
import json
import time
import uuid
import re
import requests
from bs4 import BeautifulSoup
start_time = time.time()

#假设数据集文件名为 finance_tasks.csv，读取数据集，我们使用 pandas 读取 CSV 文件。
data = pd.read_csv('AdaptLLM/finance-tasks/finance_tasks.csv')

#如果一开始没有数据集需要先到网页爬取
url = 'URL_OF_THE_WEBPAGE_WITH_DATASET'#网页url
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')#解析网页内容。


table = soup.find('table', {'id': 'dataset-table'})#结构化
rows = table.find_all('tr')

titles = []
#处理成列表的形式
for row in rows:
    cols = row.find_all('td')
    if cols:  # 
        title = cols[0].text.strip()  
        titles.append(title)
#每个条目包含多个“是”或“否”问题及其各自的答案。我们需要解析这些问题和答案，并将它们分离出来。
#如果问句不包含？做一个列表将疑问语气存取用于区分,简单示例，一些从句需要具体考虑。
question_list=["what","Who","Where","How"]
def parse_questions_answers(entry):
    qa_pairs = []
    questions_answers = entry.split(';')
    Flag=False
    for qa in questions_answers:
        Flag=contains_question_word(qa,question_list)
        if '?' in qa or Flag:
            question, answer = qa.split('?')
            question = question.strip() + '?'
            answer = answer.strip()
            qa_pairs.append({
                "id": str(uuid.uuid4()),#生成唯一id
                "Question": question,
                "Answer": answer,
                "Question_Length": len(question),
                "Answer_Length": len(answer)
            })
    return qa_pairs

def contains_question_word(sentence, question_list):
    # 创建一个正则表达式模式，不忽略大小写
    pattern = re.compile(r'\b(' + '|'.join(question_list) + r')\b')
    # 在句子中搜索模式
    match = pattern.search(sentence)
    if match:
        return True 
    return False

#

#如果有CSV文件转换对应格式
result = []
for entry in data['input_column']:  # 假设列名为 'input_column'
    result.extend(parse_questions_answers(entry))

#网页爬取转换对应格式
for entry in titles:
    result.extend(parse_questions_answers(entry))

#统计信息和性能指标

end_time = time.time()
total_time = end_time - start_time
total_qa_pairs = len(result)

print(f"Total QA pairs extracted: {total_qa_pairs}")
print(f"Time taken for processing: {total_time} seconds")

#处理完成示例：
# [
#     {
#         "id": "unique_identifier_1",
#         "Question": "What is the interest rate?",
#         "Answer": "The interest rate is 5%.",
#         "Question_Length": 26,
#         "Answer_Length": 24
#     },
#     {
#         "id": "unique_identifier_2",
#         "Question": "Is there a late fee?",
#         "Answer": "Yes, there is a late fee of $25."
#         "Question_Length": 19,
#         "Answer_Length": 31
#     },
#     ...
# ]


# 统计信息输出示例
print(f"Total QA pairs extracted: {total_qa_pairs}")
print(f"Time taken for processing: {total_time} seconds")

