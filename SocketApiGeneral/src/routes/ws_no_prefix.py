from src.core.socket_io import sio
from src.database.base import async_session_maker
from src.database.models import *
from src.utils.general import update_fields, DataHub


@sio.on('connect')
def test_connect(*args, **kwargs):
    print('Client connected')


@sio.on('create', namespace='*')
async def my_create_event(namespace, sid, data):
    print(f"for create : {data}")
    model = model_namespace.get(data.get("model"))
    fields = await DataHub(data).collect_fields()
    if fields:
        await DataHub(data).get_or_create_obj(model, fields)


@sio.on('update', namespace='*')
async def my_update_event(namespace, sid, data: dict):
    print(f"for update : {data}")
    async with async_session_maker() as session:
        model = model_namespace.get(data.get("model"))
        fields = await DataHub(data).collect_fields()
        obj = await DataHub(data).get_or_create_obj(model)
        session.add(obj)
        await update_fields(obj, fields)
        await session.commit()


@sio.on('delete', namespace='*')
async def my_delete_event(namespace, sid, data):
    print(f"for delete : {data}")
    async with async_session_maker() as session:
        model = model_namespace.get(data.get("model"))
        obj = await DataHub(data).get_or_create_obj(model)
        await session.delete(obj)
        await session.commit()
