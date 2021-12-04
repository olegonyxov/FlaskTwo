from flask import Flask, render_template, request, make_response, session, g
from flask import current_app
from db import get_db
def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('app_config.cfg')
    with app.app_context():
        print(current_app.config['DATABASE'])
    return app

app = create_app()

#
#     В HTTP протоколе есть разные типы запросов
#     самые главные это GET и POST
#
#     Flask умеет принимать оба этих запроса
#     если вторым параметром в роуте указать
#     какие запросы мы ждем
#                     |
#                     |
@app.route('/row', methods=['GET', 'POST'])
def get_and_post_request():
    # узнать какой сейчас запрос прилетел можно через request.method
    #  он хранит в себе тип запросса
    #  и благодаря этой переменной можно делать разное поведение
    #  для разного типа запроса
    #
    if request.method == 'GET':
        # допустим если пользователь только открыл страничку
        # тоесть отправил гет запрос на сервер
        # можно просто отрисовать формочку, чтобы потом отправить
        # через неё пост запрос
        #
        cur = get_db()
        data = cur.execute('SELECT * FROM user')

        for value in data:
            print(tuple(value))
        # cur.commit()
        cur.close()

        return """
         <form action='http://localhost:5000/row', method='POST'>
             <input name="username">
             <input name="password">
             <input type="submit">
         </form>
        """

    elif request.method == 'POST':
        # В случае пост запроса
        username = request.form['username']
        password = request.form['password']
        cur = get_db()
        cur.execute(f'INSERT INTO user VALUES ("777","{username}","{password}")')
        data = cur.execute('SELECT * FROM user')

        for value in data:
            print(tuple(value))
        # cur.commit()
        cur.close()


        return f"You have written your username: <b>{username}</b> and password: <b>{password}</b> and sent it by POST request"


@app.route('/session')
def save_user_data_in_session():
    #
    # прежде всего для того чтобы начать работать с сессией
    # нужно указать секретный ключ как в начале файла
    #
    # далее работать с сессией можно просто заимпортив session
    #
    # session ведет себя как обычный словарь
    # можно проверять существует ли ключ через метод .get()
    #
    # или просто сохранять новое значение как в обычном словаре
    #

    # Как пример можно написать счетчик, сколько раз пользователь открывал эту страницу
    # для начала создадим переменную счетчика
    visit_counter = 0
    # Потом проверим существует ли уже счетчик посещений в сессии
    if session.get('visited'):
        # В случае если такой параметр есть перезаписываем переменную счетчик на этот параметр
        visit_counter = session['visited']
    else:
        # Если такой переменной нет, создаем счетчик в сессии
        session['visited'] = 0

    # Далее просто передадим этот счетчик в темлейт чтобы распечатать его
    response = make_response(render_template('index.html', visited=visit_counter))

    # Но и в конце инкрементим счетчик на один
    session['visited'] += 1
    return response


@app.route('/cookie')
def get_count_of_user_visits_by_cookie():
    # Как пример можно написать счетчик, сколько раз пользователь открывал эту страницу через cookie
    # для начала создадим переменную счетчика
    visited = 0
    # Потом проверим существует ли уже счетчик посещений в cookie переменной
    if request.cookies.get('visited'):
        # Если такой параметр есть в cookie, то можно взять его
        # поскольку все значения в cookie хранятся в виде строки
        # то надо транформировать в число через int()
        try:
            visited = int(request.cookies['visited'])
        except ValueError:
            return make_response(render_template('index.html', visited='Incorrect'))

    # Далее просто передадим этот счетчик в темлейт чтобы распечатать его
    response = make_response(render_template('index.html', visited=visited))

    # Но и в конце инкрементим счетчик на один
    response.set_cookie('visited', str(visited + 1))
    return response


def main():
    print('ALLOW IT')

"""
Лучше запуск сервера app.run(debug=True)
вставлять в условие if __name__ == '__main__':
это нужно для того чтобы этот файл не запустил сервер
если заимпортить этот файл из другого питоновского файла 
"""
if __name__ == '__main__':
    app.run()

