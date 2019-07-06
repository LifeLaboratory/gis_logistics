from requests import post


def exec():
    data = {
        'sql': 'select * from bus'
    }
    print(post('http://83ca514e.ngrok.io/exec', json=data).text)


def insert_transaction():
    data = {
        "id_bus": 1,
        "id_route": 1,
        "input": 8,
        "output": 5
    }
    print(post('http://83ca514e.ngrok.io/transaction', json=data).text)
insert_transaction()