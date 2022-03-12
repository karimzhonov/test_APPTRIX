# test_APPTRIX
**Тестовое задание в компание APPTRIX**

Результат: [kht-test-apptrix.herokuapp.com](https://kht-test-apptrix.herokuapp.com/api/)

Используется:
![Python](https://img.shields.io/badge/-Python-black?style=flat-square&logo=Python)
![Postgresql](https://img.shields.io/badge/-Postgresql-%232c3e50?style=flat-square&logo=Postgresql)
![Docker](https://img.shields.io/badge/-Docker-46a2f1?style=flat-square&logo=docker&logoColor=white)

*Описание задачи*

> Разработка бэкенд для сайта знакомство
> 1.	Создать модель участников. У участника должна быть аватарка, пол, имя и фамилия, почта. 
> 2.	Создать эндпоинт регистрации нового участника: /api/clients/create (не забываем о пароле и совместимости с авторизацией модели участника). 
> 3.	При регистрации нового участника необходимо обработать его аватарку: наложить на него водяной знак (в качестве водяного знака можете взять любую картинку). 
> 4.	Создать эндпоинт оценивания участником другого участника: /api/clients/{id}/match. В случае, если возникает взаимная симпатия, то ответом выдаем почту клиенту и отправляем на почты участников: «Вы понравились <имя>! Почта участника: <почта>». 
> 5.	Создать эндпоинт списка участников: /api/list. Должна быть возможность фильтрации списка по полу, имени, фамилии. Советую использовать библиотеку Django-filters. 
> 6.	Реализовать определение дистанции между участниками. Добавить поля долготы и широты. В api списка добавить дополнительный фильтр, который показывает участников в пределах заданной дистанции относительно авторизованного пользователя. Не забывайте об оптимизации запросов к базе данных https://en.wikipedia.org/wiki/Great-circle_distance 
> 7.	Задеплоить проект на любом удобном для вас хостинге, сервисах PaaS (Heroku) и т.п. Должна быть возможность просмотреть реализацию всех задач. Если есть какие-то особенности по тестированию, написать в Readme. Там же оставить ссылку/ссылки на АПИ проекта

*Разработиние urls*(username: root, password: 9009 для админку)
> 1. Список Участников с фильтрами: [api/client/list/](https://kht-test-apptrix.herokuapp.com/api/client/list/)
> 2. Создается Участник, рефакторинг изображения и сохраните изображение: [api/client/create/](https://kht-test-apptrix.herokuapp.com/api/client/create/)
> 3. Аутентификация Участника: [api/client/auth/](https://kht-test-apptrix.herokuapp.com/api/client/auth/)
> 4. Координат Участника (get запрос для получение, post запрос для корректировки): [api/client/coordinates/](https://kht-test-apptrix.herokuapp.com/api/client/coordinates/)
> 5. Покажите одного из Участников (pk=5 для тестов по этой ссылке): [api/client/int:pk/](https://kht-test-apptrix.herokuapp.com/api/client/5/)
> 6. Подходящие Участники, если они оба совпадают, отправляется электронное письмо (pk=5 для тестов по этой ссылке): [api/client/int:pk/match/](https://kht-test-apptrix.herokuapp.com/api/client/5/match/)
> 7. Получение расстояние Участников (pk=5 для тестов по этой ссылке): [api/client/int:pk/distance/](https://kht-test-apptrix.herokuapp.com/api/client/5/distance/)

