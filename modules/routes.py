import random
import modules.repository
from modules.models import Accounts
from flask import jsonify, request, render_template, Blueprint


app = Blueprint('routes', __name__)


@app.route('/', methods=['GET'])
@app.route('/home/', methods=['GET'])
def index():
    return render_template("index.html"), 200


@app.route('/deleted_accounts/', methods=['GET'])
def get_all_deleted_accounts():
    # Получаем УДАЛЁННЫЕ счета всех Клиентов
    is_deleted = True
    accounts = modules.repository.get_all_accounts(is_deleted)
    if not accounts:
        return jsonify({'Message': 'No accounts found...'}), 404

    account_list = []
    for account in accounts:
        account_data = {
            'cust_id': account.cust_id,
            'id': account.id,
            'account_number': account.account_number,
            'is_deleted': account.is_deleted,
            'date_deleted': account.date_deleted,
            'amount': float(account.amount)
        }
        account_list.append(account_data)

    return jsonify({'accounts': account_list}), 200


@app.route('/accounts/', methods=['GET'])
@app.route('/acc/', methods=['GET'])
def get_all_accounts():
    # Получаем счета всех Клиентов
    accounts = modules.repository.get_all_accounts()
    if not accounts:
        return jsonify({'Message': 'No accounts found...'}), 404

    account_list = []
    for account in accounts:
        account_data = {
            'cust_id': account.cust_id,
            'id': account.id,
            'account_number': account.account_number,
            'is_deleted': account.is_deleted,
            'date_deleted': account.date_deleted,
            'amount': float(account.amount)
        }
        account_list.append(account_data)

    return jsonify({'accounts': account_list}), 200


@app.route('/customers/<int:id>/accounts/', methods=['GET'])
def get_customer_accounts(id):
    if not isinstance(id, int):
        return jsonify({'Error': 'Invalid customer ID format.'}), 400

    # Ищем Клиента по Id
    customer = modules.repository.get_customer_by_id(id)
    if not customer:
        return jsonify({'Error': 'Customer not found.'}), 404

    # Получаем все счета для данного Клиента
    accounts = modules.repository.get_accounts_by_cust_id(id)
    if not accounts:
        return jsonify({'Message': 'No accounts found for the customer.'}), 404

    account_list = []
    for account in accounts:
        account_data = {
            'id': account.id,
            'account_number': account.account_number,
            'is_deleted': account.is_deleted,
            'date_deleted': account.date_deleted,
            'amount': float(account.amount)
        }
        account_list.append(account_data)

    return jsonify({'customer_id': customer.id, 'accounts': account_list}), 200


@app.route('/customers/<int:id>/', methods=['POST'])
def add_customer_account(id):
    if not isinstance(id, int):
        return jsonify({'Error': 'Invalid customer ID format.'}), 400

    # Ищем Клиента по Id
    customer = modules.repository.get_customer_by_id(id)
    if not customer:
        return jsonify({'Error': 'Customer not found.'}), 404

    # Формируем данные для добавления счёта Клиенту
    max_account_number = modules.repository.get_max_account_number()
    if max_account_number is None:
        new_account_number = '7000000000000001'
    else:
        new_account_number = str(
            int(max_account_number) + random.randint(1, 57))
    account_add = Accounts(
        cust_id=id,
        account_number=new_account_number
    )
    modules.repository.add_accounts(account_add)

    return jsonify({'New account number created': new_account_number, 'customer_id': id}), 201


@app.route('/accounts/<string:account_number>/', methods=['DELETE'])
def del_account(account_number):
    # Ищем Клиента по Id
    account_number = str(account_number)
    account = modules.repository.get_account_by_number(account_number)
    if not account:
        return jsonify({'error': 'Account not found.'}), 404

    # Софт удаление счёта
    modules.repository.del_account(account_number)

    return '', 204


@app.route('/withdrawal/', methods=['PATCH'])
def withdrawal():
    req_data = request.get_json()
    if req_data:
        account_number = str(req_data.get('account_number'))
        sum = req_data.get('sum')
        if not isinstance(sum, int, float):
            return jsonify({'Error': 'Invalid sum format.'}), 400
    else:
        return 'Invalid JSON data', 400

    account = modules.repository.get_account_by_number(account_number)
    if not account:
        return jsonify({'Error': 'Account not found.'}), 404

    if account.amount >= sum:
        # Выполняем операцию снятия средств
        new_balance = account.amount - sum
        modules.repository.update_account_balance(account_number, new_balance)
        return jsonify({'Withdrawal successful on the account': account_number}), 200
    else:
        return jsonify({'Error': 'Insufficient funds.'}), 402


@app.route('/refill/', methods=['PATCH'])
def refill():
    req_data = request.get_json()
    if req_data:
        account_number = str(req_data.get('account_number'))
        sum = req_data.get('sum')
        if not isinstance(sum, int):
            return jsonify({'Error': 'Invalid sum format.'}), 400
    else:
        return 'Invalid JSON data', 400

    account = modules.repository.get_account_by_number(account_number)
    if not account:
        return jsonify({'Error': 'Account not found.'}), 404

    # Выполняем операцию начисления средств
    new_balance = account.amount + sum
    modules.repository.update_account_balance(account_number, new_balance)
    return jsonify({'Refill successful on the account': account_number}), 200


@app.route('/transfer/', methods=['PATCH'])
def transfer():
    req_data = request.get_json()
    if req_data:
        account_number_1 = str(req_data.get('account_number_1'))
        account_number_2 = str(req_data.get('account_number_2'))
        sum = req_data.get('sum')
        if not isinstance(sum, int):
            return jsonify({'Error': 'Invalid sum format.'}), 400
    else:
        return 'Invalid JSON data', 400

    account_1 = modules.repository.get_account_by_number(account_number_1)
    account_2 = modules.repository.get_account_by_number(account_number_2)
    if not account_1:
        return jsonify({'Error': 'Account_1 not found.'}), 404
    if not account_2:
        return jsonify({'Error': 'Account_1 not found.'}), 404

    if account_1.amount >= sum:
        # Выполняем операции снятия и пополнения средств на счетах
        new_balance_acc_1 = account_1.amount - sum
        new_balance_acc_2 = account_2.amount + sum
        modules.repository.update_account_balance(
            account_number_1, new_balance_acc_1)
        modules.repository.update_account_balance(
            account_number_2, new_balance_acc_2)
        return ('The transfer was successful'), 200
    else:
        return jsonify({'Error': 'Insufficient funds.'}), 400
