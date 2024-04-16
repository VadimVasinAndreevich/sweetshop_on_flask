from flask import Flask, request, render_template, redirect, url_for, session, flash
from sweetshop.models import db, Buyer, Address, Typesweets, Sweets, Order, Product
from sweetshop.forms import RegistrationForm, LoginForm, ChangeNumber, ChangeAddress, ChangeCount
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)
app.secret_key = 'bdfd4abee1bdec8a459c7e50f8c97dea1300aab823dfcb366265013a62e149eb'
app.config['SECRET_KEY'] = 'e511faf185d536df046464f80dc645d0c8166ca25f5c634eaf4b89c6ba344142'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
csrf = CSRFProtect(app)
db.init_app(app)


@app.route('/')
def index():
    """Главная страница"""
    # db.create_all()
    sweets = Sweets.query.all()
    return render_template('index.html', sweets=sweets)


@app.route('/my_profile/')
def my_profile():
    """Мой профиль"""
    buyer = Buyer.query.filter_by(name=session['name']).first()
    address = Address.query.filter_by(buyer_id=buyer.id).all()
    return render_template('my_profile.html', buyer=buyer, address=address)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    """Регистрация пользователя"""
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        try:
            name = form.name.data
            email = form.email.data
            password = form.password.data
            buyer = Buyer(name=f'{name}', email=f'{email}',
                        password=f'{generate_password_hash(password)}')
            db.session.add(buyer)
            db.session.commit()
            session['mess'] = 'Регистрация прошла успешно!'
            return render_template('registration.html', form=form)
        except:
            session['mess_one'] = 'Учётная запись уже существует'
            return render_template('registration.html', form=form)
    session.pop('mess', None)
    session.pop('mess_one', None)
    return render_template('registration.html', form=form)


@app.route('/change_information/', methods=['GET', 'POST'])
def change_information():
    """Изменение номера"""
    form = ChangeNumber()
    if request.method == 'POST' and form.validate():
        contact_number = form.contact_number.data
        buyer = Buyer.query.filter_by(name=session['name']).first()
        buyer.contact_number = contact_number
        db.session.commit()
        session['mess'] = 'Номер изменён!'
        return render_template('index.html')
    session.pop('mess', None)
    session.pop('mess_one', None)
    return render_template('my_form.html', form=form)


@app.route('/change_address/', methods=['GET', 'POST'])
def change_address():
    """Создание адреса"""
    form = ChangeAddress()
    if request.method == 'POST' and form.validate():
        address_name = form.address.data
        buyer = Buyer.query.filter_by(name=session['name']).first()
        address = Address(address=f'{address_name}', buyer_id=buyer.id)
        db.session.add(address)
        db.session.commit()
        session['mess'] = 'Адрес добавлен!'
        return render_template('index.html')
    session.pop('mess', None)
    session.pop('mess_one', None)
    return render_template('address.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login_form():
    """Авторизация"""
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = request.form.get('email')
        password = request.form.get('password')
        buyer = Buyer.query.filter_by(email=email).first()
        if check_password_hash(buyer.password, password):
            session['name'] = buyer.name
            return render_template('index.html')
        session['message'] = 'Учётная запись не существует, проверьте почту и пароль, или зарегистрируйтесь'
        return render_template('login.html', form=form)
    session.pop('message', None)
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    """Выход из учётной записи"""
    session.pop('name', None)
    return render_template('index.html')


@app.route('/del_buyer/')
def del_buyer():
    """Удаление учётной записи"""
    buyer = Buyer.query.filter_by(name=session['name']).first()
    address = Address.query.filter_by(buyer_id=buyer.id).all()
    for line in address:
        db.session.delete(line)
    db.session.delete(buyer)
    db.session.commit()
    session.pop('name', None)
    return render_template('index.html')


@app.route('/del_product/<sweet_id>')
def del_product(sweet_id):
    """Удаление товара из корзины"""
    product = Product.query.filter_by(sweet_id=sweet_id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('shopping_cart'))


@app.route('/add_sweets/')
def add_sweets():
    # Код для этапа разработки
    """Добавление сладостей"""
    for i in range(1, 10):
        typesweets = Typesweets(name=f'sweet{i}')
        db.session.add(typesweets)
    db.session.commit()
    typesweets = Typesweets.query.all()
    i = 1
    x = 20
    for el in typesweets:
        for num in range(i, x):
            sweets = Sweets(name=f'candy{num}', description=f'description{num}',
                          price=randint(50, 1000), typesweets_id=el.id)
            db.session.add(sweets)
            db.session.commit()
        i = x
        x = x + 20
    return render_template('index.html')


@app.route('/product/<sweet_id>')
def product(sweet_id):
    """Формирование каталога"""
    buyer = Buyer.query.filter_by(name=session['name']).first()
    product = Product(sweet_id=sweet_id, buyer_id=buyer.id, count=0, price=0)
    db.session.add(product)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/shopping_cart/', methods=['GET', 'POST'])
def shopping_cart():
    """Корзина"""
    form = ChangeCount()
    buyer = Buyer.query.filter_by(name=session['name']).first()
    product = Product.query.filter_by(buyer_id=buyer.id, status='Не подтверждён').all()
    sweets = [Sweets.query.filter_by(id=el.sweet_id).first() for el in product]
    address = Address.query.filter_by(buyer_id=buyer.id).all()
    streets = [street.address for street in address]
    if request.method == 'POST':
        counts = request.form.getlist('count')
        session['street'] = request.form['street']
        i = 0
        total_price = 0
        for elem in counts:
            product[i].count = int(elem)
            product[i].price = sweets[i].price * int(elem)
            total_price += product[i].price
            db.session.commit()
            i += 1
        return render_template('order.html', buyer=buyer, product=product, sweets=sweets,
                               total_price=total_price, street=session['street'])
    return render_template('shopping_cart.html', buyer=buyer, product=product, sweets=sweets,
                           streets=streets, form=form)


@app.route('/order/')
def order():
    """Заказ"""
    buyer = Buyer.query.filter_by(name=session['name']).first()
    products = Product.query.filter_by(buyer_id=buyer.id, status='Не подтверждён').all()
    total_price = 0
    for product in products:
        total_price += product.price
        product.status = 'Принят в работу'
    order = Order(buyer_id=buyer.id, total_price=total_price, address=session['street'],
                  email=buyer.email, contact_number=buyer.contact_number)
    session.pop('street')
    db.session.add(order)
    db.session.commit()
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
