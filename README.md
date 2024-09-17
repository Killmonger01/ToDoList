# ToDoList

# Как запустить
- создаете и активтруйте вертуальное окружение
```
python3 -m venv venv
source venv/bin/activate
or
python -m venv venv
source venv/Scripts\activate
```
- переходим в директерию с manage.py и делаем миграции
```
cd todolist
python manage.py makemigrations
python manage.py migrate
```
- в текущей версии проекта нужно создать суперпользователя и через админку созать категории
```
python manage.py createsuperuser
```
- запускаем джанго приложение
```
python manage.py runserver
```
- с нового терминала нужно активировать вертуальное окружение в корне проекта затем перейти в директерию с manage.py и запустить celery
```
celery -A todolist.celery_app worker --loglevel=info
```
- делаем тоже самое с нового терминала но уже прописываем эту команду
```
celery -A todolist.celery_app beat --loglevel=info
```
- затем с нового терминала в корне проекта включаем вертуальное окружение и включаем бота
```
python bot.py
```
- вот username бота @todolistforchatlabsbot, также сейчас бот работает так что после каждого выключения и включения бота необходимо удалить юезра с бд что иначе нынешнея версия не узнает id пользователя 

