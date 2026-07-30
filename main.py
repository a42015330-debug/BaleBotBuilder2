import os
import time
import requests


TOKEN = os.getenv("BALE_TOKEN")


if not TOKEN:
    print("توکن ربات وارد نشده است")
    exit()


API = f"https://tapi.bale.ai/bot{TOKEN}"


def send_message(chat_id, text):
    url = API + "/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    requests.post(url, json=data)


def get_updates(offset=None):

    url = API + "/getUpdates"

    params = {}

    if offset:
        params["offset"] = offset

    response = requests.get(url, params=params)

    return response.json()


def main():

    print("ربات بله روشن شد")

    offset = None

    while True:

        try:
            updates = get_updates(offset)

            if "result" in updates:

                for update in updates["result"]:

                    offset = update["update_id"] + 1

                    message = update.get("message")

                    if message:

                        chat_id = message["chat"]["id"]

                        text = message.get("text", "")

                        if text == "/start":

                            send_message(
                                chat_id,
                                "سلام 👋\n"
                                "به ربات ساز بله خوش آمدید.\n"
                                "به زودی می‌توانید ربات خودتان را بسازید."
                            )

                        else:

                            send_message(
                                chat_id,
                                "پیام شما دریافت شد."
                            )


            time.sleep(2)

        except Exception as e:

            print(e)
            time.sleep(5)



main()
