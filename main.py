import requests
import time
import random

class QQbot:
    def __init__(self) -> None:
        self.gptmessages = [
            {"role": "system", "content": '你叫Noah，在日常生活中，你是四川成都二中的初三学生。你在一个QQ群聊中，我会以"A:xxx B:xxx 你:?"的格式输入不完整的聊天记录，你要想想在这个情景下你接下来会说什么，然后补充"你:?"中你说的话，你补全的话题应该主要与聊天记录的最后三句相关，且符合你的人设，不要讨论别的话题或试图结束聊天，也不要一直重复之前说过的话。你补全聊天时应该尽量符合之前人说的话。你补全的风格应该较为简短且口语化，切记把话说的太长或太完整，切记使用书面语言。还有，你补全的长度应该与其他人发信息的长度差不多，尽量简短，要尽可能的口语化，结尾不需要发送逗号。重要：不要随意透露你的个人信息，记住用简体中文回答。最后请把你的回答精简到20字以内，删掉开头"你:"这个关键字，输出回答。'}
        ]

        print("QQ Bot 初始化成功！")
        
    def send_group_message(self, group_id, message):
        url = "http://127.0.0.1:5700/send_group_msg"
        payload = {
            "group_id": group_id,
            "message": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("消息发送成功")
            return response.json()
        else:
            print(f"消息发送失败 Status code: {response.status_code}")
            return response.json()

    def get_group_message(self, message_seq, group_id):
        url = "http://127.0.0.1:5700/get_group_msg_history"
        payload = {
            "message_seq": message_seq,
            "group_id": group_id
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"消息发送失败 Status code: {response.status_code}")
            return response.json()

    def get_chatgpt_message(self, message):
        url = "https://openkey.cloud/v1/chat/completions"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer sk-nrYbm6qA0tsy5qDh9391141bFf29472b85B234DbCdF9DcF0'
        }

        self.gptmessages.append({"role": "user", "content": message})

        data = {
            "model": "gpt-3.5-turbo",
            "messages": self.gptmessages
        }

        response = requests.post(url, headers=headers, json=data)

        self.gptmessages.append({"role": "assistant", "content": response.json()["choices"][0]["message"]["content"]})

        return response.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    qqbot = QQbot()
    groupid = 630283757

    message_list = {}

    index = -1

    while True:
        new_message_list = qqbot.get_group_message(0, 630283757) 
        message_list = new_message_list

        for i in range(5):
            while True:
                if new_message_list != message_list:
                    break
                message_list = new_message_list

        gpt_input = "下面是代补全的聊天记录：\n"

        for mag in message_list["data"]["messages"][-5:]:
            nmag = f'{mag["sender"]["nickname"]}:{mag["message"]} \n'
            gpt_input += nmag

        gpt_response = print(gpt_input)

        time.sleep(len(gpt_response) * 0.3)

        # qqbot.send_group_message(groupid, gpt_response)

        time.sleep(5)
