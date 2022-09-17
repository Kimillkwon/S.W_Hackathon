#### 동기식

import re
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import unbrella_data

# <add_uri_and_key>
endpoint = "https://ksh0522.documents.azure.com:443/"
key = "zjoM5ek2Ux4af9zHiMi1fPPR0aOv7dd4tkkrdAmGivqulAu7kO2LEPU0FHP6Gq8s8j1Q1zNz0SKjpIUGIFcKgg=="

database_name = 'test_base'
container_name = 'user_set'


def create_items(container, email, name, pw):
    print('Creating Items')
    print('\n1.1 Create Item\n')

    # Create a SalesOrder object. This object has nested properties and various types including numbers, DateTimes and strings.
    # This can be saved as JSON as is without converting into rows/columns.
    sales_order = get_sales_order(email, name, pw)
    container.create_item(body=sales_order)

    # As your app evolves, let's say your object has a new schema. You can insert SalesOrderV2 objects without any
    # changes to the database tier.

    # container.create_item(body=sales_order2)


def get_sales_order(email, name, pw):
    order1 = {'id': email,
              'name': name,
              'pw': pw,
              'rent_num': '0'
              }

    return order1


def read_item(container, id, ub_name):
    print('\n1.2 Reading Item by Id\n')

    # Note that Reads require a partition key to be specified.
    response = container.read_item(item=id, partition_key=ub_name)

    print('Item read by Id {0}'.format(id))
    return response


def read_items(container):
    print('\n1.3 - Reading all items in a container\n')

    # NOTE: Use MaxItemCount on Options to control how many items come back per trip to the server
    #       Important to handle throttles whenever you are doing operations such as this that might
    #       result in a 429 (throttled request)
    item_list = list(container.read_all_items(max_item_count=10))

    print('Found {0} items'.format(item_list.__len__()))

    for doc in item_list:
        print('Item Id: {0}'.format(doc.get('id')))
        print('pw: {0}'.format(doc.get('pw')))

    return item_list


def query_items(container, doc_id):
    print('\n1.4 Querying for an  Item by Id\n')

    # enable_cross_partition_query should be set to True as the container is partitioned
    items = list(container.query_items(
        query="SELECT * FROM r WHERE r.id=@id",
        parameters=[
            {"name": "@id", "value": doc_id}
        ],
        enable_cross_partition_query=True
    ))

    print('Item queried by Id {0}'.format(items[0].get("id")))


def replace_item(container, id, ub_name, state, on_off):
    print('\n1.5 Replace an Item\n')

    read_item = container.read_item(item=id, partition_key=ub_name)
    read_item[state] = on_off
    # response = container.replace_item(item=read_item, body=read_item)
    response = container.upsert_item(read_item)

    print('Replaced Item\'s Id is {0}'.format(response['id']))


def replace_item2(container, id, ub_name):
    print('\n1.5 Replace an Item\n')

    read_item = container.read_item(item=id, partition_key=ub_name)
    # response = container.replace_item(item=read_item, body=read_item)
    response = container.upsert_item(read_item)

    print('Replaced Item\'s Id is {0}'.format(response['id']))


def upsert_item(container, doc_id):
    print('\n1.6 Upserting an item\n')

    read_item = container.read_item(item=doc_id, partition_key=doc_id)
    read_item['subtotal'] = read_item['subtotal'] + 1
    response = container.upsert_item(body=read_item)

    print('Upserted Item\'s Id is {0}, new subtotal={1}'.format(response['id'], response['subtotal']))


def delete_item(container, doc_id):
    print('\n1.7 Deleting Item by Id\n')

    response = container.delete_item(item=doc_id, partition_key=doc_id)

    print('Deleted item\'s Id is {0}'.format(doc_id))



def run_sample():
    client = cosmos_client.CosmosClient(endpoint, {'masterKey': key})
    try:
        # setup database for this sample
        db = client.create_database_if_not_exists(id=database_name)
        # setup container for this sample
        container = db.create_container_if_not_exists(id=container_name, partition_key=PartitionKey(path='/ub_name'))

        # read_item(container, "unb_1")
        temp = read_items(container)[0]['location']
        print(temp)
        # query_items(container, 'SalesOrder1')
        # replace_item(container, 'SalesOrder1')
        # upsert_item(container, 'SalesOrder1')
        # delete_item(container, 'SalesOrder1')

        # cleanup database after sample

    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))

    finally:
        print("\nrun_sample done")


if __name__ == '__main__':
    run_sample()
