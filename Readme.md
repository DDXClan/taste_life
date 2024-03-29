В каждый powershell всего их 3

$ENV:database_url = 'login:password@host:port/db_name' ваши данные

cd backend

|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|<br />
|         pip install -r req.txt Это один раз           |<br />
|_______________________________________________________|


Это в терминалах по очереди в каждом одну из 3 команд 

uvicorn app.auth:app —reload

uvicorn app.client.main:app —reload —port 8001

uvicorn app.admin.main:app —reload —port 8002

![alt text](https://sun9-50.userapi.com/impg/lhGDOYlV9p6hktVPKE44iIgxj06DVfAQOTJjcQ/7_AzdWSc7Dc.jpg?size=620x437&quality=96&sign=459ad155478687dbaf4cf7b1f6f63a5d&type=album)
