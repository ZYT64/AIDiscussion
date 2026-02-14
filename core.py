import os
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

console = Console()
client = OpenAI(
    api_key='DEEPSEEK_API_KEY',
    base_url="https://api.deepseek.com")

# 讨论列表
discussions = []

def ai(model, message):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": message}
        ],
        stream=False
    )
    return response.choices[0].message.content

# print(ai("deepseek-chat",'你好'))
# 制定任务
message_user = input("输入你的消息: ")
to_manager = "你是一群ai的管理者，现在你需要一群AI讨论这个问题：“{}”，请你制作一个讨论方向明细，只能包含文字和具体的讨论方向（每个用小标题概括即可），不要有其他的话，每一条之间用‘;’分隔开".format(message_user)
answer_manager = ai("deepseek-chat",to_manager)
tasks = answer_manager.split(";")
print(tasks)
# 对话文件
with open("discussion.txt", "w", encoding="utf-8") as f:
    f.write("")
# 讨论
for task in tasks:
    # 第一次讨论
    to_ai = "你是一名AI，现在你需要根据这个讨论主题：“{}”、讨论方向（用户需要你回答）：“{}”，和其他AI进行讨论其中的要点和怎么回答用户，讨论内容要有逻辑性和条理性，不能有无关的内容，你是讨论的参与者，只讲你的内容".format(message_user,task)
    answer_ai = ai("deepseek-chat",to_ai)
    print("第一次讨论输出:"+answer_ai)
    with open ("discussion.txt","a",encoding="utf-8") as f:
        f.write("\n\n\n讨论方向：“{}”，第一次讨论内容：“{}”\n".format(task,answer_ai))

    # 给建议
    advise_ai = "你是一名AI，现在你需要根据这个讨论主题：“{}”、讨论内容：“{}”，想一些建议，并且直接修改，修改后的讨论内容要有逻辑性和条理性，不能有无关的内容，你是讨论的参与者，只讲你的修改后内容".format(message_user,answer_ai)
    answer_advise = ai("deepseek-chat",advise_ai)
    # print("建议:"+answer_advise)
    # with open("discussion.txt","a",encoding="utf-8") as f:
    #     f.write("\n\n\n讨论方向：“{}”，关于第一次讨论内容给出建议：“{}”\n".format(task,answer_advise))

    # 根据建议改答案
    # to_ai_modify = "你是一名AI，现在你需要根据这个，讨论主题：“{}”，讨论内容：“{}”，和这个建议：“{}”，给出一个修改后的讨论内容，修改后的讨论内容要有逻辑性和条理性，不能有无关的内容，你是讨论的参与者，只讲你的内容".format(message_user,answer_ai,answer_advise)
    # answer_ai_modify = ai("deepseek-chat",to_ai_modify)
    # print("讨论输出:"+answer_ai_modify)
    print("讨论输出:"+answer_advise)
    # discussions.append(answer_ai_modify)
    discussions.append(answer_advise)
    with open("discussion.txt","a",encoding="utf-8") as f:
        # f.write("\n\n\n讨论方向：“{}”，最终讨论内容：“{}”\n".format(task,answer_ai_modify))
        f.write("\n\n\n讨论方向：“{}”，最终讨论内容：“{}”\n".format(task,answer_advise))

# 初步最终答案
with open ("discussion.txt","r",encoding="utf-8") as f:
    discussion_total = f.read()
to_answer = "你是一名AI，现在你需要根据这个讨论主题：“{}”，和这个讨论内容：“{}”，给出一个回答，要求回答要有逻辑性和条理性，不能有无关的内容".format(message_user,discussion_total)
answer = ai("deepseek-chat",to_answer)
print("初步最终回答:\n",answer)

# 给初步最终答案提建议
i=0
for discussion in discussions:
    to_advise_final = "你是一名AI，现在你需要根据这个讨论主题：“{}”，和根据讨论内容输出的讨论答案：“{}”，根据“{}”方面的讨论内容：“{}”，直接修改讨论答案的那一部分，要求建议要有逻辑性和条理性，不能有无关的内容，输出完整答案（包括其他不改的部分）".format(message_user,answer,tasks[i],discussion)
    answer = ai("deepseek-chat",to_advise_final)
    i += 1
print("最终回答:\n",answer)
