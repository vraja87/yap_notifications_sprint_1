# Проектная работа 10 спринта

https://github.com/kamartem/notifications_sprint_1

Для работы с mock апи надо будет указывать следующие заголовки: headers={'Cookie': f'access_token={os.environ['SERVICE_TOKEN']}; HttpOnly; Path=/', "X-Request-Id": "123"}

Сервис scheduler забирает расписание рассылок из базы notify_db и согласно указанным там правилам в виде cron строки производит вызовы notifications api.

# срочные сообщения
t = requests.post("http://127.0.0.1:8000/api/v1/publish_immediate/", json=data)
# обычные сообщения
t = requests.post("http://127.0.0.1:8000/api/v1/publish/", json=data)

data здесь - 
data = {"messages": [{"email_body": "txt", "subject": "huy", "newsletter_id": str(uuid.uuid4()), "worker_names": ["smtp"]}]}
data = {"messages": [{"template_id":str(uuid.uuid4()), "group_id": [str(uuid.uuid4()), str(uuid.uuid4())], "newsletter_id": str(uuid.uuid4()), "worker_names": ["smtp"]}]}