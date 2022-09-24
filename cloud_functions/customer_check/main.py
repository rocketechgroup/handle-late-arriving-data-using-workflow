import flask
import logging
import functions_framework
import hashlib
import os

from flask import jsonify
from google.cloud import datastore

client = datastore.Client(project=os.environ.get('GCP_PROJECT'))
ds_namespace = 'customer_app'
ds_kind = 'Customer'


def fetch_customer(customer_id):
    str_customer_id = str(customer_id)
    key_customer_id = hashlib.md5(str_customer_id.encode('utf-8')).hexdigest() + "_" + str_customer_id
    logging.info(f"customer_id: {key_customer_id}")
    key = client.key(ds_kind, key_customer_id, namespace=ds_namespace)
    entity = client.get(key=key)

    print(entity)
    return entity


@functions_framework.http
def customer_check(request: flask.Request):
    content = request.get_json(silent=True)
    print(content)
    entity = fetch_customer(customer_id=content['customer_id'])

    if entity:
        return jsonify({'status': 'Customer found'})
    else:
        flask.abort(404, 'Customer not found')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    fetch_customer(1234)
