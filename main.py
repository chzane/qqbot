import qqbot
import time

if __name__ == "__main__":
    qqbot = qqbot.QQbot()
    groupid = 630283757

    message_list = {}

    count = 0

    while True:
        new_message_list = qqbot.get_group_message(0, 630283757) 

        if new_message_list != message_list:
            count += 1  
            message_list = new_message_list 
        else:
            count = count

        if count >= 5:
            print("消息已满5条")

            count = 0

            message_list = new_message_list

            gpt_input = "下面是代补全的聊天记录：\n"

            for mag in message_list["data"]["messages"][-5:]:
                nmag = f'{mag["sender"]["nickname"]}:{mag["message"]} \n'
                gpt_input += nmag

            print(gpt_input)

            gpt_response = qqbot.get_chatgpt_message(gpt_input)

            print(gpt_response)

            qqbot.send_group_message(groupid, gpt_response)

        time.sleep(0.5)
