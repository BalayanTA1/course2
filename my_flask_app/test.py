from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

# Пример данных администратора
admin_data = {
    'users': ['user1', 'user2'],
    'settings': 'Some admin settings'
}

@app.route('/login', methods=['POST'])
def login():
    # Здесь должна быть ваша логика авторизации
    # Если пользователь авторизован как администратор:
    response = make_response(redirect(url_for('admin_panel')))
    response.set_cookie('is_admin', 'true')  # Устанавливаем куку
    return response

@app.route('/admin_panel')
def admin_panel():
    # Проверяем куку
    is_admin = request.cookies.get('is_admin')
    if is_admin == 'true':
        return render_template('admin_panel.html', admin_data=admin_data)
    else:
        return "Доступ запрещен", 403  # Возвращаем ошибку доступа

@app.route('/cookie/')
def cookie():
    res = make_response("Setting a cookie")
    res.set_cookie('is_admin', 'true', max_age=60*60*24*365*2)
    return res

if __name__ == '__main__':
    app.run(debug=True)
