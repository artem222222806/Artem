import requests
from requests.packages.urllib3.util.retry import Retry 
from requests.adapters import HTTPAdapter
import random
import string
import os
from colorama import Fore, Style, init
import base64
init()
ban = """
  █████   ████  ███  ████  ████ 
░░███   ███░  ░░░  ░░███ ░░███ 
 ░███  ███    ████  ░███  ░███ 
 ░███████    ░░███  ░███  ░███ 
 ░███░░███    ░███  ░███  ░███ 
 ░███ ░░███   ░███  ░███  ░███ 
 █████ ░░████ █████ █████ █████
░░░░░   ░░░░ ░░░░░ ░░░░░ ░░░░░ 
  cоздатель: @EncryptionEnigma
"""                                        
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_phone():
    return f"+79{''.join(random.choice('0123456789') for _ in range(9))}"

def generate_random_email():
    domains = ["gmail.com", "mail.ru", "rambler.ru"]
    name_length = random.randint(5, 10)
    letters = "abcdefghijklmnopqrstuvwxyz1234567890"
    email_name = ''.join(random.choice(letters) for _ in range(name_length))
    return f"{email_name}@{random.choice(domains)}"

complaint_types = {
    "Спам": [
        "Пользователь {user} ID: {user_id} использует чат для рассылки рекламы и спама, что нарушает правила сообщества. Прошу удалить его сессию и заблокировать возможность отправки нежелательных сообщений.",
        "Здравствуйте, хочу пожаловаться на {user} ID: {user_id}, он использует спам для продвижения своего канала из-за чего невозможно общаться в группе, прошу принять меры по удалению аккаунта. Спасибо",
        "Доброго времени суток, прошу принять меры по рассылке спама. ID: {user_id} пользователя.",
        "Жалоба на рассылку рекламы. Пользователь {user} с ID: {user_id} спамит по группам, прошу принять меры",
        "Hello, I want to complain about ID: {user_id}, he uses spam to promote his channel, which makes it impossible to communicate in the group, please take steps to delete the account. Thank you",
        "Good day, I ask you to take measures to send spam. ID: {user_id} of the user.",
        "Complaint about sending advertisements. User with ID: {user_id} is spamming groups, please take action"
    ],
    "Порнография": [
        "Добрый день, прошу заблокировать доступ к порнографическому контенту. Акаунту {user} с  ID: {user_id}. Проблема в том что он занимается продажей детской порнографией",
        "Здравствуйте, хочу подать жалобу на порнографию.  Пользиватель {user} с  ID: {user_id} продает детскую порнографию, прошу принять меры по удалению акаунта. Спасибо",
        "Данный пользиватель {user} с ID: {user_id} растространяет запрешеный детский контент (дп,цп) прошу вас удалить данный акаунт. Спасибо",
        "Good afternoon, please block access to pornographic content. Account with ID: {user_id}. The problem is that it sells child pornography",
         "Hello, I want to file a complaint about pornography. User ID: {user_id} sells child pornography, please take steps to delete the account. Thank you",
         "This user with ID: {user_id} distributes prohibited children's content (dp, cp), I ask you to delete this account. Thank you",
         "Пользователь {user_id} распространяет порнографические материалы. Прошу заблокировать его аккаунт за нарушение правил платформы. Ссылка на материалы: {id}",
                "Обнаружено распространение порнографии пользователем {user_id}. Прошу принять меры. Ссылка на материалы: {id}",
                "Добрый день, прошу заблокировать аккаунт с  ID: {user_id}. Проблема в том,что он занимается продажей детской порнографией, вот ссылка на нарушение: {id}",
                "Здравствуйте, хочу подать жалобу на порнографию.  Пользователь с  ID: {user_id} продает детскую порнографию,вот ссылка на нарушение:{id},прошу принять меры по удалению акаунта. Спасибо",
                "Данный пользователь с ID: {user_id} растространяет запрещеный детский контент (дп,цп) прошу вас удалить данный акаунт.Также ссылка на нарушение:{id}.Спасибо",
                "Добрый день, прошу заблокировать аккунт с айди: {user_id} за распространение порнографии, точнее этот человек размещает порнографию, а также детскую порнографию в чатах ({id}) и так далее, что может повлиять на психику людей, которые находятся в этих чатах, а также это нарушает вашу политику, прошу заблокировать данного человека, также на момент жалобы у этого человека на аватарке было неприличное фото, поэтому прошу вас отреагировать на это быстро и четко. Заранее спасибо!",
                         "Hello, I want to file a complaint about pornography. User with ID: {user_id} sells child pornography,link to violation: {id},please take steps to delete the account. Thank you",
                "Good afternoon, please block the account with ID: {user_id}. The problem is that he is selling child pornography.Link to violation: {violation_link}.",
                "This user with ID: {user_id} distributes prohibited children's content (dp, cp),and link to violation: {id},I ask you to delete this account. Thank you",
                "Good afternoon, I ask you to block the account with ID: {user_id} for distributing pornography, more precisely, this person posts pornography, as well as child pornography in chats and so on,link to violation: {id},which can affect the psyche of people who are in these chats, and also violates your policy, I ask you to block this person, also at the time of the complaint this person had an indecent photo on his avatar, so I ask you to respond to this quickly and clearly. Thank you in advance!" 
    ],
    "Фишинг": [
       "Здравствуйте, сообщаю о подозрительной попытке фишинга. Акк: {user} ID: {user_id}.",
        "Добрый день, прошу обратить внимание на пользивателя {user} с ID: {user_id} он создает фишинг сылки, прошу принять меры по удалению данного акаунта",
        "Жалоба на фишинг. Пожалуйста, примите меры. {user} с ID: {user_id} использует фишинг для получения личных данных других пользывателей, прошу принять меры по удалению акаунта. Спасибо",
        "Hello, I'm reporting a suspicious phishing attempt. ID: {user_id}.",
         "Good afternoon, please pay attention to the user with ID: {user_id}, he creates phishing links, please take measures to delete this account",
         "Phishing complaint. Please take action. ID: {user_id} uses phishing to obtain personal information of other users, please take action to delete the account. Thank you"    
    ],
    "Дианон": [
       "Здравствуйте уважаемая поддержка телеграмм,хочу пожаловаться на пользователя {user} с ID:{user_id} дело в том что он нарушает правила телеграмм, он продает услули деанона, занимается терроризмом , а еще хочу сообщить что он оскорбляет чужие личности! ",
    "Здравствуйте уважаемая поддержка. Пользователь {user} вашей платформы Telegram с ID: {user_id}, угрожает дean0минuзациеё и свaтuнг0м. Требую удалить его аккаунт для безопасности других пользователей.",
    "Telegram, деактивируйте аккаунт {user} с ID: {user_id}, так как с него мне поступают многочисленные угрозы дean0н0м и сват0м, пугает также моих друзей, говорит, что сольёт их данные в сеть",
    "Данный пользователь {user} с ID: {user_id}, угрожает мне д0kсинг0м и свaтuнг0м. Он хочет слить мои данные в сеть. Просьба удалить его аккаунт для безопастности",
    "Telegram, деактивируйте аккаунт {user}, Id:  {user_id}, так как с него мне поступают многочисленные угрозы дean0н0м и сват0м, пугает также моих друзей, говорит, что сольёт их данные в сеть",
    "Данный пользователь {user}, id: {user_id}, угрожает мне     д0kсинг0м и свaтuнг0м. Он хочет слить мои данные в сеть. Просьба удалить его аккаунт для безопастности.",
       "Здравствуйте уважаемая поддержка. Пользователь {user} вашей платформы Telegram с id: {user_id}, угрожает дean0минuзациеё и свaтuнг0м. Требую удалить его аккаунт для безопасности других пользователей.",
       "Привествую Вас. Я являюсь родителем моего ребёнка и ему поступют угрозы об сливе данных с данного аккаунта {user}, id:{user_id}. Прошу удалить его аккаунт, так как теперь у моего ребёнка нарушена психика!",
       "Мне сказали, что телеграм самый безопасный мессенджер, только сейчас этот пользователь {user} id: {user_id} хочет слить мои данные.",
       "Hello, dear telegram moderator, I want to complain to you about a channel that sells doxing and swatting services ID: {user_id}, I ask you to take measures to delete the account.",
         "Good day, I ask you to take action on my complaint. The telegram user under ID: {id} is engaged in selling the services of Doxing and Swatting, I ask you to take action. Thank you.",
         "This account under ID: {user_id} is engaged in doxing and swatting, please take measures to delete the account."
    ],
    "Мошенничество": [
    "Уважаемая служба поддержки!Хочу сообщить о случае мошенничества. Пользователь {user} с ID: {user_id} пишет людям и предлагает услугу по выводу Notcoin на карту. После перевода Notcoin пользователь добавляет в черный список и отказывается переводить Notcoin. Прошу принять меры по удалению аккаунта. Спасибо!",
    "Добрый день!Прошу рассмотреть жалобу на мошенничество. Пользователь {user} с ID: {user_id} занимается мошенничеством, прошу принять меры по блокировке аккаунта.",
    "Обращаюсь к вам с жалобой на пользователя {user} с ID: {user_id}. Данный пользователь обманным путем получил от меня Notcoin, пообещав вывод на карту, но после получения средств заблокировал меня. Прошу принять меры и вернуть мои средства.",
    "Прошу обратить внимание на действия пользователя {user} с ID: {user_id}.Он предлагает услуги по выводу Notcoin, но после получения оплаты отказывается выполнять свои обязательства и блокирует пользователей. Это мошенник!",
    "ВНИМАНИЕ! Мошенник!Пользователь {user} с ID: {user_id} обманывает людей, предлагая несуществующие услуги. Будьте бдительны и не переводите ему свои средства!",
    "Я стал жертвой мошенничества со стороны пользователя {user} с ID: {user_id}.Прошу принять меры по блокировке его аккаунта и возврату моих средств.",
    "Требую наказать мошенника {user} с ID: {user_id}!Он обманул меня и многих других пользователей. Прошу принять меры!",
    "Обращаюсь к вам с просьбой о помощи.Пользователь {user} с ID: {user_id} обманным путем завладел моими средствами. Прошу вернуть мои Notcoin и заблокировать мошенника.",
    "Сколько можно терпеть мошенников на вашей платформе? Пользователь с ID: {user_id} продолжает обманывать людей. Прошу принять срочные меры!",
    "Dear support service, I want to report a case of fraud. A user with ID: {user_id} writes to people and offers a service to help them withdraw notcoin to a card. After transferring the notcoin, the user is blacklisted and refuses to transfer the notcoin, I ask you to take measures to delete the account.  Thank you",
         "Good afternoon, I ask you to consider a complaint about fraud. The user with ID: {user_id} is engaged in fraud, I ask you to take measures to assign the account.",
         "Fraud complaint against user ID: {user_id}. Please take action."
    ],
        "Премиум": [
        "Good afternoon Telegram support! Account ID: {user_id} purchased premium in your messenger to send spam messages and bypass Telegram restrictions. Please check this complaint and take action!"        
        ],
        "Домогательство": [
        "I ask you to delete user ID: {user_id}, he writes to my friends and asks them to send their intimate photos, please take action",
         "I ask you to delete user ID: {user_id}, he writes to my friend who is 15 years old and asks for intimate photos, I ask you to take punitive measures.  Thank you",
         "User ID: {user_id}, writes to minors and asks for intimate photographs, please take punitive measures.",
         "User ID: {user_id}, writes to my underage friends and asks for intimate photos, please take punitive measures.",
         "User ID: {user_id}, writes to my underage friends and asks them to send him intimate photos, I ask them to take punitive measures.",
         "User ID: {user_id}, writes to my friends and asks them to send him intimate photos, I ask them to take punitive measures.  Thank you"
            ],
            "Религия": [
            "User ID: {user_id} provokes people into conflicts, and also affects religion for the sake of conflict, I ask you to take action against this user",
         "User ID: {user_id} provokes people into conflicts, please take action.  Thank you",
         "User ID: {user_id} provokes people into conflicts by affecting religions, please take measures to remove this user",
         "I ask you to delete user {user} ID: {user_id}, he provokes other users into conflicts by touching on religions and this is obscene behavior. Please treat with understanding and take punitive measures"],
         "Канал": [
         "Hello, Telegram support! I want to file a complaint against the Telegram channel link: {id}, this channel distributes methods of doxing, hacking, and swatting. Please remove this channel. Thank you.",
        "Good afternoon, I want to complain about the telegram channel link: {id}, this channel publishes personal information of users, please take measures to delete the channel. Thanks.",
        "This channel: channel link {id} published my personal information without my consent. Please take action!",
        "I want to complain about the channel: channel link {id}. In the post from the date of publication, my photos and full name were published without my knowledge and consent. I ask you to remove the publication and take action against the channel that violates the confidentiality of users.",
        "Channel link {id} violates the rules of the Telegram platform by publishing personal information of users without their consent. I demand action!"],
        "Группа": [
        "Hello, Telegram Support, I want to file a complaint against the group with ID: {id} for the reason: distribution of prohibited content. Please take action to block the group!",
        "Good day, I ask you to take action on my complaint. Group ID: {id} is used to distribute illegal materials, please block the group. Thanks!"
        "I want to complain about group ID: {id} for violating community guidelines, please take action."
        ],
        "Вирт" : [
        "Good afternoon, Telegram support! Account {user} ID: {user_id} uses a virtual number purchased on the website for number activation. It has nothing to do with the number, the number has nothing to do with it. Please sort this out. Thanks in advance!",
        ],
        "Насилие": [        
        "Hello, Telegram support! I want to report a case of animal cruelty. User ID: {id} has shared content depicting animal abuse. I urge you to take immediate action and remove the content/block the user.",
        "I am writing to report a disturbing instance of animal abuse that I encountered on Telegram. User ID: {id} is responsible for sharing this content. I kindly request you to investigate this matter and take appropriate action to prevent further harm to animals."],
        "Сессия": [
        "Здраствуйте,меня взломали и выкинули с аккаунта {user}. Теперь Я не могу зайти на аккаунт так как мгновенно выкидывают меня с аккаунта. Прошу помогите, удалите аккаунт или обнулите сессии, там было очень много важной информации. Вот мой ID: {user_id}",
                "Здраствуйте, я попался на фишинг ссылку и меня как то взломали, на моем аккаунте {user} было очень много важных вещей, поэтому прошу вас обнулите пожалуйста сессию или же удалите аккаунт.Вот мой айди: {user_id}",
                "Здравствуйте, у меня украли аккаунт {user} с айди {user_id}, при попытке зайти на него, тот кто украл аккаунт не даёт мне зайти и отключает мою сессию, прошу вас пожалуйста отключить все сессии на данном аккаунте.",
                "Hello, I fell for a phishing link and somehow got hacked, there were a lot of important things on my account {user}, so I ask you to reset the session or delete the account. Here is my ID: {user_id}",
                "Hello, my account {user} with ID {user_id} was stolen, when I try to log into it, the one who stole the account does not allow me to log in and disables my session, I ask you to please disable all sessions on this account.",
                "Здраствуйте,меня взломали и выкинули с аккаунта {user}. Теперь Я не могу зайти на аккаунт так как мгновенно выкидывают меня с аккаунта. Прошу помогите, удалите аккаунт или обнулите сессии, там было очень много важной информации. Вот мой ID: {user_id}"
        ],
}

encoded_password = "S2lsbDoyMDI0"
correct_password = base64.b64decode(encoded_password).decode('utf-8')


while True:
    password_attempt = input("Введите пароль: ")
    if base64.b64decode(encoded_password).decode() == password_attempt:
        clear_screen()
        break
    else:
        print(Fore.RED + "Неверный пароль!" + Style.RESET_ALL)
        
        
def get_user_input():
    clear_screen()
    print(Fore.RED + ban + Style.RESET_ALL)
    user_id = input(Fore.CYAN + "   Введите ID: " + Style.RESET_ALL)
    user = input(Fore.CYAN + "   Введите @: " + Style.RESET_ALL) 
    id = input(Fore.CYAN + "   Введите cсылку на нарушение ( или для сноса канала/группы): " + Style.RESET_ALL)
    request_count = int(input(Fore.CYAN + "   Введите количество отправок: " + Style.RESET_ALL))
    print(Fore.CYAN + "   Выберите тип жалобы:" + Style.RESET_ALL)
    for i, complaint_type in enumerate(complaint_types.keys()):
        print(f"   {i+1}. {complaint_type}")
    choice = int(input(Fore.CYAN + "   Выберите номер типа жалобы: " + Style.RESET_ALL)) - 1 
    chosen_complaint_type = list(complaint_types.keys())[choice]
    return user_id, user, id, request_count, chosen_complaint_type 

RETRY_STRATEGY = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=1,
    respect_retry_after_header=True,
)

sites = [
    {
        'url': 'https://telegram.org/support?setln=ru',
        'data': {
            'tg_feedback_appeal': '...',  
            'tg_feedback_email': '...',
            'tg_feedback_phone': '...'
        }
    },
    {
        'url': 'https://telegram.org/support',
        'data': {
            'name': '...',
            'email': '...',
            'message': '...'
        }
    }       
]

def send_data_to_server(data, proxies, cause, email, phone):
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=RETRY_STRATEGY))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        proxy = random.choice(proxies)
        response = session.post(data['url'], headers=headers, data=data['data'], proxies=proxy, timeout=10)
        response.raise_for_status()
        phone_info = f", phone: {phone}" if phone else ""
        print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Запрос отправлен на {data['url']}  с причиной: {cause}, email: {email}{phone_info} отправлен через прокси {proxy}!")
    except requests.exceptions.RequestException as e:
        print(f"[{Fore.RED}-{Style.RESET_ALL}] Ошибка при отправке запроса на {data['url']} через прокси {proxy}: {e}")

def animate_sending(current, total):
    print(f"Идет отправка {current} из {total}", end="\r")

def main():
    user_id, user, id, request_count, chosen_complaint_type = get_user_input()
    proxies = [
     {"http": "http://185.221.160.123:80"},
    {"http": "http://45.8.211.90:80"},
    {"http": "http://62.182.204.81:88"},
    {"http": "http://178.218.44.79:3128"},
    {"http": "http://31.43.179.136:80"},
    {"http": "http://31.43.179.247:80"},
    {"http": "http://195.137.167.62:80"},
    {"http": "http://195.137.167.25:80"},
    {"http": "http://62.33.207.202:80"},
    {"http": "http://5.189.184.147:27191"},
    {"http": "http://50.221.74.130:80"},
    {"http": "http://172.67.43.209:80"},
    {"http": "http://178.48.68.61:18080"},
    {"http": "http://117.250.3.58:8080"},
    {"http": "http://172.67.181.106:80"},
    {"http": "http://172.67.181.108:80"},
    {"http": "http://172.67.181.150:80"},
    {"http": "http://172.67.182.159:80"},
    {"http": "http://172.67.3.64:80"},
    {"http": "http://185.162.228.223:80"},
    {"http": "http://172.67.177.157:80"},
    {"http": "http://45.12.30.1:80"},
    {"http": "http://185.162.229.78:80"},
    {"http": "http://31.43.179.237:80"},
    {"http": "http://172.67.172.174:80"},
    {"http": "http://172.67.0.21:80"},
    {"http": "http://172.67.73.212:80"},
    {"http": "http://172.67.75.187:80"},
    {"http": "http://172.67.43.190:80"},
    {"http": "http://172.67.192.8:80"},
    {"http": "http://31.43.179.83:80"},
    {"http": "http://172.67.201.224:80"},
    {"http": "http://172.67.24.126:80"},
    {"http": "http://63.141.128.17:80"},
    {"http": "http://67.201.33.10:25283"},
    {"http": "http://172.67.75.35:80"},
    {"http": "http://172.67.182.137:80"},
    {"http": "http://172.67.207.187:80"},
    {"http": "http://172.67.180.50:80"},
    {"http": "http://172.67.177.11:80"},
    {"http": "http://185.162.229.10:80"},
    {"http": "http://185.162.230.49:80"},
    {"http": "http://185.162.228.104:80"},
    {"http": "http://45.12.31.2:80"},
    {"http": "http://185.162.228.52:80"},
    {"http": "http://141.193.213.20:80"},
    {"http": "http://185.238.228.178:80"},
    {"http": "http://141.101.120.235:80"},
    {"http": "http://63.141.128.169:80"},
    {"http": "http://45.131.4.207:80"},
    {"http": "http://63.141.128.243:80"},
    {"http": "http://5.182.34.67:80"},
    {"http": "http://172.67.182.62:80"},
    {"http": "http://172.67.181.124:80"},
    {"http": "http://185.162.228.158:80"},
    {"http": "http://45.12.30.228:80"},
    {"http": "http://185.162.230.112:80"},
    {"http": "http://45.12.30.120:80"},
    {"http": "http://185.162.228.89:80"},
    {"http": "http://31.43.179.230:80"},
    {"http": "http://172.67.171.208:80"},
    {"http": "http://172.67.170.33:80"},
    {"http": "http://172.67.179.182:80"},
    {"http": "http://172.67.179.188:80"},
    {"http": "http://141.101.120.172:80"},
    {"http": "http://141.101.121.70:80"},
    {"http": "http://141.101.121.160:80"},
    {"http": "http://141.101.122.167:80"},
    {"http": "http://141.101.122.132:80"},
    {"http": "http://63.141.128.14:80"},
    {"http": "http://45.131.4.17:80"},
    {"http": "http://45.131.4.47:80"},
    {"http": "http://172.67.68.68:80"},
    {"http": "http://63.141.128.78:80"},
    {"http": "http://172.67.161.211:80"},
    {"http": "http://5.182.34.109:80"},
    {"http": "http://188.114.98.233:80"},
    {"http": "http://172.67.181.122:80"},
    {"http": "http://172.67.176.135:80"},
    {"http": "http://185.162.228.65:80"},
    {"http": "http://172.67.193.136:80"},
    {"http": "http://31.43.179.28:80"},
    {"http": "http://31.43.179.33:80"},
    {"http": "http://172.67.0.42:80"},
    {"http": "http://172.67.43.79:80"},
    {"http": "http://172.67.43.80:80"},
    {"http": "http://172.67.185.158:80"},
    {"http": "http://172.67.81.185:80"},
    {"http": "http://172.67.255.64:80"},
    {"http": "http://172.64.98.128:80"},
    {"http": "http://141.101.120.94:80"},
    {"http": "http://141.101.120.252:80"},
    {"http": "http://141.101.121.135:80"},
    {"http": "http://45.131.4.152:80"},
    {"http": "http://63.141.128.1:80"},
    {"http": "http://172.67.31.147:80"},
    {"http": "http://170.114.45.6:80"},
    {"http": "http://5.182.34.240:80"},
    {"http": "http://50.168.163.179:80"},
    {"http": "http://50.172.39.98:80"},
    {"http": "http://141.101.123.215:80"},
    {"http": "http://172.67.180.58:80"},
    {"http": "http://172.67.176.16:80"},
    {"http": "http://172.64.194.2:80"},
    {"http": "http://172.67.125.104:80"},
    {"http": "http://172.64.135.33:80"},
    {"http": "http://141.101.121.29:80"},
    {"http": "http://141.101.123.88:80"},
    {"http": "http://172.67.70.117:80"},
    {"http": "http://172.67.70.248:80"},
    {"http": "http://50.174.145.14:80"},
    {"http": "http://172.67.74.181:80"},
    {"http": "http://172.67.182.131:80"},
    {"http": "http://141.101.123.12:80"},
    {"http": "http://172.67.169.199:80"},
    {"http": "http://172.67.181.105:80"},
    {"http": "http://185.162.228.253:80"},
    {"http": "http://185.162.230.2:80"},
    {"http": "http://185.162.228.73:80"},
    {"http": "http://185.162.228.116:80"},
    {"http": "http://185.162.231.25:80"},
    {"http": "http://172.67.184.50:80"},
    {"http": "http://141.101.122.216:80"},
    {"http": "http://172.64.143.25:80"},
    {"http": "http://141.193.213.89:80"},
    {"http": "http://172.67.182.49:80"},
    {"http": "http://172.67.181.94:80"},
    {"http": "http://172.67.181.168:80"},
    {"http": "http://141.101.123.32:80"},
    {"http": "http://141.101.113.20:80"},
    {"http": "http://172.67.202.134:80"},
    {"http": "http://172.67.3.145:80"},
    {"http": "http://172.67.180.61:80"},
    {"http": "http://172.67.180.11:80"},
    {"http": "http://172.67.167.236:80"},
    {"http": "http://172.67.177.22:80"},
    {"http": "http://172.67.177.229:80"},
    {"http": "http://185.162.230.110:80"},
    {"http": "http://45.12.30.88:80"},
    {"http": "http://45.12.30.173:80"},
    {"http": "http://185.162.228.228:80"},
    {"http": "http://141.193.213.197:80"},
    {"http": "http://172.67.172.175:80"},
    {"http": "http://172.67.185.154:80"},
    {"http": "http://103.21.244.155:80"},
    {"http": "http://103.21.244.80:80"},
    {"http": "http://172.67.38.73:80"},
    {"http": "http://172.64.84.72:80"},
    {"http": "http://141.101.123.39:80"},
    {"http": "http://172.64.149.80:80"},
    {"http": "http://159.112.235.230:80"},
    {"http": "http://173.245.49.152:80"},
    {"http": "http://173.245.49.168:80"},
    {"http": "http://172.64.152.47:80"},
    {"http": "http://190.93.246.211:80"},
    {"http": "http://66.235.200.45:80"},
    {"http": "http://108.162.194.121:80"},
    {"http": "http://188.114.98.233:80"},
    {"http": "http://172.67.229.37:80"},
    {"http": "http://188.114.99.233:80"},
    {"http": "http://172.67.214.82:80"},
    {"http": "http://172.67.20.37:80"},
    {"http": "http://5.182.34.73:80"},
    {"http": "http://172.67.146.14:80"},
    {"http": "http://172.64.148.181:80"},
    {"http": "http://50.218.57.67:80"},
    {"http": "http://8.219.126.240:80"},
    {"http": "http://123.233.245.158:9080"},
    {"http": "http://172.67.182.116:80"},
    {"http": "http://172.67.70.109:80"},
    {"http": "http://172.67.176.13:80"},
    {"http": "http://172.67.167.139:80"},
    {"http": "http://185.162.231.139:80"},
    {"http": "http://185.162.229.219:80"},
    {"http": "http://185.162.228.208:80"},
    {"http": "http://31.43.179.125:80"},
    {"http": "http://31.43.179.18:80"},
    {"http": "http://172.67.192.20:80"},
    {"http": "http://103.21.244.223:80"},
    {"http": "http://103.21.244.42:80"},
    {"http": "http://103.21.244.65:80"},
    {"http": "http://103.21.244.97:80"},
    {"http": "http://172.64.159.199:80"},
    {"http": "http://172.67.238.67:80"},
    {"http": "http://141.101.120.110:80"},
    {"http": "http://63.141.128.149:80"},
    {"http": "http://66.235.200.153:80"},
    {"http": "http://45.131.4.77:80"},
    {"http": "http://45.85.119.253:80"},
    {"http": "http://159.112.235.214:80"},
    {"http": "http://173.245.49.130:80"},
    {"http": "http://173.245.49.209:80"},
    {"http": "http://173.245.49.238:80"},
    {"http": "http://141.101.113.17:80"},
    {"http": "http://66.235.200.157:80"},
    {"http": "http://188.114.98.233:80"},
    {"http": "http://188.114.98.233:80"},
    {"http": "http://188.114.99.233:80"},
    {"http": "http://172.67.23.144:80"},
    {"http": "http://172.67.161.194:80"},
    {"http": "http://172.64.144.177:80"},
    {"http": "http://172.64.149.213:80"},
    {"http": "http://198.74.51.79:8888"},
    {"http": "http://188.114.99.233:80"},
    {"http": "http://5.182.34.83:80"},
    {"http": "http://66.235.200.122:80"},
    {"http": "http://172.64.145.223:80"},
    {"http": "http://173.245.59.41:80"},
    {"http": "http://172.66.40.84:80"},
    {"http": "http://172.67.181.42:80"},
    {"http": "http://172.67.182.103:80"},
    {"http": "http://172.67.181.210:80"},
    {"http": "http://172.67.254.162:80"},
    {"http": "http://172.67.255.223:80"}  
]

    for i in range(request_count):
        random_site = random.choice(sites)
        if 'tg_feedback_appeal' in random_site['data']:
            random_site['data']['tg_feedback_appeal'] = random.choice(complaint_types[chosen_complaint_type]).format(user_id=user_id, user=user, id=id) 
            random_site['data']['tg_feedback_email'] = generate_random_email() 
            random_site['data']['tg_feedback_phone'] = generate_random_phone()
        else: 
            random_site['data']['name'] = user 
            random_site['data']['email'] = f"{user_id}@example.com" 
            random_site['data']['message'] = random.choice(complaint_types[chosen_complaint_type]).format(user_id=user_id, user=user, id=id)
        send_data_to_server(random_site, proxies, random_site['data'].get('tg_feedback_appeal') or random_site['data']['message'], random_site['data'].get('tg_feedback_email') or random_site['data']['email'], random_site['data'].get('tg_feedback_phone', ''))
        animate_sending(i + 1, request_count)
    input("Нажмите Enter для выхода...")    

if __name__ == "__main__":
    main()