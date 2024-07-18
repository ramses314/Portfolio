from datetime import datetime

from src.database.base import async_session_maker

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.database.models import model_namespace, related_field_id_mapper
from src.database.models.general.influencer import Influencer


class DataHub:
    def __init__(self, data: dict):
        """
        :param data: dict от сокета. Содержит
             - словарь полей influencer (от какого инфла пришел)
             - словарь fields (поля объекта на которого сработал триггер в бд)
             - model str модель
                 Пример:
                    {
                        'model': 'Lead',
                        'influencer': {'id': 1, 'title': 'Lara', 'is_active': True, ... },
                        'fields': {'username': 'lutellachris', 'tg_id': 4707114243, 'first_tourch': 'welcome_bot', ... }
                    }

        :param ids_field: list список полей, подразумевающих уникальность объекта (без дупликатов в бд). Служит
                 для их отлавливания (self.get_or_create_obj) и обнаружения в полях отношений (self.collect_fields).
        """
        self.data = data
        self.ids_field = ["tg_id", "telegram_id", "sub_id", "chat_id", "account_id_amo"]

    async def collect_fields(self):
        """
        Валидируем/преобразуем поля для CRUD в общую бд.
          Оссобенность работы заключается в невозможности опираться на id объектов отношений из-за их дубликатов и
        коллизий. РЕШЕНИЕ ПРОБЛЕМЫ на примере: н-р, имеем поле model.lead_id = 3, в таком случае при отправке сокета (InfluencerBot) мы заменяем
        id словарем относимого объекта (т.е. lead_id : {id:3, name: "some", ...}).
        ИТОГ: при отправке -  id заменяем словарем, при получении сокета - парсим поля относимого объекта (self.collect_fields), т.е. обратный процесс

        В данной ф-ии проходимся по всем полям и выполняем следущие операции:
           а) Если поле относиться к времени - преобразуем str -> datetime;
           б) Отлавливаем объекты внутри объектов, преобразуем словарь в объект модели SQLAlchemy ORM
           в) Отлавливаем поле в котором должно храниться id записи (но сокет отправляет словарь),
                преобразуем словарь в объект (self.get_or_create), по итогу помещаем в ключ необходимый id (уже нашей бд)
           г) Отлавливаем MtM поле influencers (для привязки объектов к тем инфлам от которых они пришли с сокетами)

        :return: dict
        """
        await self._infl_data_actualize()
        fields = await self._del_unneeded_fields(self.data.get("fields"))

        for key, value in fields.items():

            # в описании пункт а)
            try:
                date_format = '%Y-%m-%dT%H:%M:%S.%f'
                date_obj = datetime.strptime(value, date_format)
                fields[key] = date_obj
            except:
                pass

            # в описании пункт б)
            if isinstance(value, dict) and any(v in value for v in self.ids_field): # Парсинг объектов полей отношения
                model = model_namespace.get(value.get("model"))
                if model:
                    fields[key] = await self.get_or_create_obj(model, value)
            elif isinstance(value, list):  # Парсинг списка объектов полей отношения
                for i, item in enumerate(value):
                    if isinstance(value, dict) and any(v in value for v in self.ids_field):
                        model = model_namespace.get(item.get("model"))
                        if model:
                            fields[key][i] = await self.get_or_create_obj(model, item)

            # в описании пункт в)
            if str(key).endswith("_id") and value:
                model = related_field_id_mapper.get(key)
                if model:
                    obj = await self.get_or_create_obj(model, value)
                    fields[key] = obj.id

            # в описании пункт г)
            if key == "influencers":
                from_influencer = await self.get_or_create_obj(Influencer, self.data.get("influencer"))
                fields[key] = [] if None in fields[key] else fields[key]
                fields[key].append(from_influencer)
                fields[key] = list(set(fields[key]))
        print("FIELDS", fields)
        return fields

    async def get_or_create_obj(self, model, fields: dict = None):
        """
          Помимо классического get_or_create реализовано 1) проверка/отлавливание уникальных объектов по ключевым
          полям (tg_id, chat_id, ...). 2) Загрузка всех полей отношений.
        :param model: модель объекта
        :param fields: поля объекта
        :return: obj (of some model)
        """
        print("\nMODEL", model.__tablename__)
        fields = self.data.get("fields") if not fields else fields
        print("\nFIELDS",fields)
        async with async_session_maker() as session:
            statement = select(model)
            
            try:
                telegram_id = fields.get("telegram_id", 0)
            except AttributeError as e:
                print('not telegram_id ',e)
                telegram_id = None
            try:
                tg_id = fields.get("tg_id", 0)
            except AttributeError as e:
                print('not tg_id ',e)
                tg_id = None
            try:
                chat_id = fields.get("chat_id", 0)
            except AttributeError as e:
                print('not chat_d ',e)
                chat_id = None
            try:
                sub_id = fields.get("sub_id", 0)
            except AttributeError as e:
                print('not sub_id ',e)
                sub_id = None
            try:
                account_id_amo = fields.get("account_id_amo", 0)
            except AttributeError as e:
                print('account_id_amo',e)
                account_id_amo = None
            print("MODEL DICT",model.__dict__)
            if telegram_id:
                statement = statement.where(model.telegram_id == telegram_id)
            elif tg_id:
                statement = statement.where(model.tg_id == tg_id)
            elif chat_id:
                statement = statement.where(model.chat_id == chat_id)
            elif account_id_amo:
                statement = statement.where(model.account_id_amo == account_id_amo)
            elif sub_id:
                statement = statement.where(model.sub_id == sub_id)
            else:
                fields = await self._del_unneeded_fields(fields)
                new_obj = model(**fields)
                session.add(new_obj)
                await session.commit()
                return new_obj

            exist = (await session.execute(statement)).scalars().first()

            if not exist:
                fields = await self._del_unneeded_fields(fields)
                print("FIELDS",fields)
                
                new_obj = model(**fields)
                session.add(new_obj)
                await session.commit()
                # отсылаем ф-ию на саму себя, И в этот раз она пройдет проверку exist.
                return await self.get_or_create_obj(model, fields)

            # Проходим списком для всех полей отношений
            load_options = []
            for relation_column in model.__mapper__.relationships:
                load_options.append(selectinload(relation_column))
            statement = statement.options(*load_options)
            result = await session.execute(statement)
            return result.scalars().first()

    async def _infl_data_actualize(self):
        infl_fields = self.data.get("influencer")
        if infl_fields:
            await self.get_or_create_obj(Influencer, infl_fields)

    async def _del_unneeded_fields(self, fields):
        """
          Используем для удаления ненужных полей при записи в общую бд.
            - id : наличие может привести к коллизиям (из-за совпадений ids разных инфлов)
            - model : добавляется при отправке сокета, объявление несуществующего поля приведет к ошибке
            - created/updated : создается автоматически sqlalchemy orm

        :param fields: поля объекта для CRUD
        :return: fields
        """
        if "id" in fields:
            del fields["id"]
        if "model" in fields:
            del fields["model"]
        if "created" in fields:
            del fields["created"]
        if "updated" in fields:
            del fields["updated"]

        return fields


async def update_fields(obj, fields: dict) -> object:
    """
       Принимаем obj и провалидированный словарь полей.
       Обновляем/наполняем объект актуальными данными.
    :param obj:
    :param fields:
    :return: obj
    """
    for key, value in fields.items():
        setattr(obj, key, value)
    return obj
