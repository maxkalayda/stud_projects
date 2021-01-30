from flask import render_template, jsonify, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from sv_packages import app, db
from sv_packages.classes import User, MainDBForwarder

from sv_packages.logistician_funcs import postHandlerLogisticianByBank, postHandlerLogisticianByMaterial, \
    postHandlerLogisticianAdd, postHandlerLogisticianDelete
from sv_packages.admin_funcs import adminDeleteFunc, adminEditFunc, adminViewFunc


@app.route('/')
def index():
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('inputEmail')
    password = request.form.get('inputPassword')
    print(f"login = {login}; password = {password}")
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.passwd, password):
            login_user(user)
            print('User is correct!')
            # savepage = request.args.get('redirect')
            if login == 'forwarder':
                # redirect(savepage)
                return redirect('forwarder')
            elif login == 'logistician':
                return redirect('logistician')
            elif login == 'admin':
                return redirect('admin')
            else:
                pass  # TODO
        else:
            flash('Неверный логин или пароль!')

    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('inputEmail')
    password = request.form.get('inputPassword')
    print(f"login = {login}; password = {password}")

    if request.method == 'POST':
        userExists = User.query.filter_by(login=login).first()
        if userExists:
            flash('Пользователь с таким именем уже существует!')
        else:
            hash_password = generate_password_hash(password)
            new_user = User(login=login, passwd=hash_password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('index.html')

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/404', methods=['GET', 'POST'])
@login_required
def code404():
    return render_template('404.html')


@app.after_request  # редирект на логинизацию, если пытаешься попасть в профиль не авторизованным. 401 - неавторизован
def redirect_after_login(response):
    if response.status_code == 401:
        return redirect(url_for('login_page'))
    elif response.status_code == 404:
        return redirect(url_for('code404'))

    return response


@app.route('/forwarder', methods=['GET'])
@login_required
def forwarder():
    page = request.args.get('page')
    codename_input = request.args.get('codename_input')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if codename_input:
        search = MainDBForwarder.query.filter(
            MainDBForwarder.product_name.contains(codename_input) | MainDBForwarder.material_code.contains(
                codename_input))
        page_list = search.paginate(page=page, per_page=10, error_out=True)
        select_list = MainDBForwarder.query.group_by(MainDBForwarder.material_code).distinct()
    else:
        search = MainDBForwarder.query.order_by(MainDBForwarder.order_num)
        page_list = search.paginate(page=page, per_page=10, error_out=True)
        select_list = MainDBForwarder.query.group_by(MainDBForwarder.material_code).distinct()
        print(select_list)

    return render_template('forwarder.html', data=search, page_list=page_list, codename_input=codename_input, select_list=select_list)


@app.route('/forwarder', methods=['POST', 'GET'])
@login_required
def addData():
    sup_code = request.form.get('sup_code')
    balance_acc = request.form.get('balance_acc')
    code_of_dir = request.form.get('code_of_dir_of_documents')
    product_name = request.form.get('product_name')
    num_of_document = request.form.get('num_of_document')
    material_code = request.form.get('material_code')
    material_acc = request.form.get('material_acc')
    measure_unit_code = request.form.get('measure_unit_code')
    amount_of_material = request.form.get('amount_of_material')
    unit_price = request.form.get('unit_price')
    data_row = MainDBForwarder(sup_code=sup_code, balance_acc=balance_acc, code_of_dir=code_of_dir,
                               product_name=product_name, num_of_document=num_of_document, material_code=material_code,
                               material_acc=material_acc, measure_unit_code=measure_unit_code,
                               amount_of_material=amount_of_material, unit_price=unit_price)
    if (data_row.sup_code != '' and data_row.sup_code.isdigit()) and (
            data_row.balance_acc != '' and data_row.balance_acc.isdigit()) and (
            data_row.code_of_dir != '' and data_row.code_of_dir.isdigit()) and data_row.product_name != '' and (
            data_row.num_of_document != '' and data_row.num_of_document.isdigit()) and (
            data_row.material_code != '' and data_row.material_code.isdigit()) and (
            data_row.material_acc != '' and data_row.material_acc.isdigit()) and (
            data_row.measure_unit_code != '' and data_row.measure_unit_code.isdigit()) and (
            data_row.amount_of_material != '' and data_row.amount_of_material.isdigit()) and (
            data_row.unit_price != '' and data_row.unit_price.isdigit()):
        db.session.add(data_row)
        db.session.commit()
        flash('Запись успешно добавлена!', 'error_add')
        return redirect('forwarder')
    else:
        flash('Не все поля заполнены или заполнены некорректно', 'error_add')
    return redirect('forwarder')


@app.route('/logistician', methods=['GET'])
@login_required
def logistician():
    return render_template('logistician.html')


@app.route('/logistician/SearchByMaterial', methods=['POST'])
def logisticianSearchByMaterial():
    return jsonify(postHandlerLogisticianByMaterial(request.json))


@app.route('/logistician/SearchByBank', methods=['POST'])
def logisticianSearchByBank():
    return jsonify(postHandlerLogisticianByBank(request.json))


@app.route('/logistician/Add', methods=['POST'])
def logisticianAdd():
    return jsonify(postHandlerLogisticianAdd(request.json))


@app.route('/logistician/Delete', methods=['POST'])
def logisticianDelete():
    return jsonify(postHandlerLogisticianDelete(request.json))


@app.route('/admin', methods=['GET'])
@login_required
def admin():
    return render_template('admin.html')


@app.route('/admin/Delete', methods=['POST'])
def adminDelete():
    return jsonify(adminDeleteFunc(request.json))


@app.route('/admin/Edit', methods=['POST'])
def adminEdit():
    return jsonify(adminEditFunc(request.json))


@app.route('/admin/View', methods=['POST'])
def adminView():
    return jsonify(adminViewFunc(request.json))
