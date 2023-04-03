from datetime import date, timedelta, datetime
import decimal
import xml.etree.ElementTree as ET

from apps.scrapers.scraper_base import ScraperBase
from datetime import datetime, timezone

from .models import market_source_data_ats

class ScraperATS(ScraperBase):

    column_names_mapping = {
        "DAT": "observation_date",
        "PRICE_ZONE_CODE": "price_zone_code",
        "CONSUMER_PRICE": "consumer_price",
        "CONSUMER_VOLUME": "consumer_volume",
        "THERMAL_VOLUME": "thermal_volume",
        "HYDRO_VOLUME": "hydro_volume",
        "ATOMIC_VOLUME": "atomic_volume",
        "RENEWABLE_VOLUME": "renewable_volume"    
    }

    column_types_mapping = {
        "DAT": datetime,
        "PRICE_ZONE_CODE": int,
        "CONSUMER_PRICE": decimal,
        "CONSUMER_VOLUME": decimal,
        "THERMAL_VOLUME": decimal,
        "HYDRO_VOLUME": decimal,
        "ATOMIC_VOLUME": decimal,
        "RENEWABLE_VOLUME": decimal    
    }    

    async def scrape(self):

        # типы загрузки со страницы:
        # 0. если статическая загрузка - парсинг полностью загруженной страницы
        # 1. при наличии ajax - эмулировать ajax call, ответственный за загрузку данных, далее парсинг 
        # 2. selenium/web driver если ajax недоступен. 

        # Для АТС - вариант 1:

        # перезагрузка последнх 10 дней, проверяем обновление за этот перод.
        # при наличии обновления - обновляем значения и publication_date.
        today = date.today
        start_date = await self.most_recent_observation_date() - timedelta(10)
        end_date = date.today() + timedelta(1)
        start_date = f'{start_date:%Y%m%d}'
        end_date = f'{end_date:%Y%m%d}'        
        url = f"https://www.atsenergo.ru/market/stats.xml?date1={start_date}&date2={end_date}&period=1"        

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Connection": "keep-alive",
            "Cookie": "has_js=1",
            "Host": "www.atsenergo.ru",
            "Referer": "https://www.atsenergo.ru/results/rsv/statistics",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Microsoft Edge\";v=\"110\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Linux"
        }

        xml = await self.fetch_url(url, headers)
        root = ET.fromstring(xml)

        columns = root.findall("./columns/name")
        rows = root.findall("./row")

        column_tag_names = list()

        for column in columns:
            column_tag_names.append(column.text)

        for child in rows:
            source_column_values = child.findall("./col")
            values = {}
            for (column_index, column_value) in enumerate(source_column_values):
                source_column_name = column_tag_names[column_index]
                column_name = self.column_names_mapping[source_column_name]        
                column_type = self.column_types_mapping[source_column_name]          
                values[column_name] = self.format_property_value(column_value.text, column_type)
            create_values = dict(values)
            create_values["publication_date"] = today
            
            model, created = await market_source_data_ats.objects.aget_or_create(observation_date = values["observation_date"], 
                                                                                    price_zone_code = values["price_zone_code"], 
                                                                                    defaults = create_values)
            
            # вызов ниже можно удалить, если не предполагаем обновление исторических данных.
            #
            # В текущей DJango DEV branch версии уже ввели метод update_or_create и аргументы defaults и create_defaults
            # После обновления можно будет убрать этот if с заменой aget_or_create на  update_or_create   
            if (not created):
                self.update_model_properties(model, values)


    async def most_recent_observation_date(self):

        try:
            max_existing_model = await market_source_data_ats.objects.alatest('observation_date')
        except market_source_data_ats.DoesNotExist:
            return date.fromisocalendar(2023, 1, 1)
        return max_existing_model.observation_date
    
  
    def update_model_properties(self, model: market_source_data_ats, props: set):

        if (self.update_object_from_dictionary(model, props)):
            model.publication_date = date.today()
            model.save


    def format_property_value(self, value, column_type):

        if column_type == datetime:
            dt = datetime.strptime(value, '%d.%m.%Y')
            return datetime(dt.year, dt.month, dt.day, tzinfo = timezone.utc)
        elif column_type == int:
            return int(value)  
        elif column_type == decimal:
            return decimal.Decimal(value)    
              
        return value
    
    def update_object_from_dictionary(self, my_object, my_dict):

        modified = False
        for key, value in my_dict.items():
            attr = getattr(my_object, key)
            if (attr != value):
                setattr(my_object, key, value)    
                modified = True 
        
        return modified
