from cosmos_lib import *

async def run_data():
    # <create_cosmos_client>
    async with cosmos_client(endpoint, credential = key) as client:
    # </create_cosmos_client>
        try:
            # create a database
            database_obj = await get_or_create_db(client, database_name)
            # create a container
            container_obj = await get_or_create_container(database_obj, container_name)
            # generate some family items to test create, read, delete operations
            family_items_to_create = [unbrella_data.get_ub_data_1(), unbrella_data.get_ub_data_2(), unbrella_data.get_ub_data_3()]
            # populate the family items in container
            await populate_container_items(container_obj, family_items_to_create)  
            # read the just populated items using their id and partition key
            # await read_items(container_obj, family_items_to_create)
            total_lst = await read_items(container_obj, family_items_to_create)
            # print(total_lst[0]['location'])
            print(total_lst)
            
            # await update_item(container_obj,unbrella_data.get_ub_data_1(),'location', 'honolulu')
            
            # total_lst = await read_items(container_obj, family_items_to_create)
            # print(total_lst[0]['location'])
            
            # Query these items using the SQL query syntax. 
            # Specifying the partition key value in the query allows Cosmos DB to retrieve data only from the relevant partitions, which improves performance
            # query = "SELECT * FROM c WHERE c.ub_name IN ('unb_1')"
            # temp_lst = await query_read(container_obj, ['unb_1'])

            # print(temp_lst)
            # print(temp_lst[0]['location'])            
            
            
            
            
            # print("\nupdate item")
            # query = "UPDATE unb_1 SET location = honolulu"
            # temp_lst = await query_items(container_obj, query)

            # query = "SELECT * FROM c WHERE c.ub_name IN ('unb_1')"
            # temp_lst = await query_items(container_obj, query)
            # print(temp_lst)
            # print(temp_lst[0]['location'])            
        except exceptions.CosmosHttpResponseError as e:
            print('\nrun_sample has caught an error. {0}'.format(e.message))
        finally:
            print("\nQuickstart complete")
            
            
            
# </run_sample>

if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_data())
