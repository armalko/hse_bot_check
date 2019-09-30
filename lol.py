import json
import requests
import time
import urllib

TOKEN = "873341609:AAEqb3Wp1R2SfB04ZBxk4wN6u6Y3_5IoC6Q"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def check_hse():
    r = requests.get("https://ba.hse.ru/bolimp2020")
    if "Документ не найден, Not Found." in r.text:
        return False
    return True


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        chat = update["message"]["chat"]["id"]
        try:
            text = update["message"]["text"]
        except:
            send_message("Будешь стикеры слать, выебу и забаню нахуй.", chat)
            continue

        if text == "/start":
            send_message(
                "Привет, я ХУЙ. Напиши чекай, чтобы я вручную проверил",
                chat)
        elif text == 'чекай':
            send_message("Я и так проверяю, умник хуев. Ну ладно, еще разок.", chat)

            if check_hse():
                send_message("Ааааа, выложили, пиздуй чекать срочно! https://ba.hse.ru/bolimp2020", chat)
                send_message("Ааааа, выложили, пиздуй чекать срочно! https://ba.hse.ru/bolimp2020", chat_id="284545845")
                send_message("Ааааа, выложили, пиздуй чекать срочно! https://ba.hse.ru/bolimp2020", chat_id="267399865")
            else:
                send_message("Бля, нихуя нет еще. Не спами, я и так раз в 3 минуты чекаю", chat)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text, chat_id


def get_keyboard(items):
    reply_markup = {"keyboard": items, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)


def main():
    last_update_id = None
    st = time.time()
    while True:
        if time.time() - st > 120:
            if check_hse():
                send_message("Ааааа, выложили, пиздуй чекать срочно! https://ba.hse.ru/bolimp2020", chat_id="284545845")
                send_message("Ааааа, выложили, пиздуй чекать срочно! https://ba.hse.ru/bolimp2020", chat_id="267399865")
            st = time.time()
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.3)


if __name__ == '__main__':
    main()
