import os
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

console = Console()
client = OpenAI(
    api_key='DEEPSEEK-API-KEY',
    base_url="https://api.deepseek.com")

def ai(message):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": message}
        ],
        stream=False
    )
    return response.choices[0].message.content

# print(ai("deepseek-chat",'你好'))
# 第一次输出
user = input("user:")
first_answer = ai(user)
# 检查
ai_check = "你是一名AI，现在你需要根据这个用户输入：“{}”，和这个AI的回答：“{}”，检查这个回答是否有逻辑性和条理性，是否有无关的内容，是否有不妥的或错误之处，如果有请修改，修改后的内容要有逻辑性和条理性，不能有无关的内容，直接输出修改后的内容来回答用户的原始需求即可".format(user,first_answer)
answer_ai_check = ai(ai_check)
# 补充
ai_supplement = "你是一名AI，现在你需要根据这个用户输入：“{}”，和这个AI的回答：“{}”，想一些补充内容，直接输出补充内容来回答用户的原始需求即可".format(user,answer_ai_check)
answer_ai_supplement = ai(ai_supplement)
# 最终答案
final_answer = "你是一名AI，现在你需要根据这个用户输入：“{}”，和这个AI的回答：“{}”，和这个补充内容：“{}”，给出一个最终的答案，直接输出最终的答案来回答用户的原始需求即可".format(user,answer_ai_check,answer_ai_supplement)
answer_final = ai(final_answer)
# print("最终答案:"+answer_final)
console.print(Markdown(answer_final))