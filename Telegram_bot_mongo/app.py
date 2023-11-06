from pymongo import MongoClient
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pprint import pprint
import config


# Making Connection
# myclient = MongoClient("mongodb://localhost:27017/")
myclient = MongoClient(f"mongodb://{config.DB_HOST}:{config.DB_PORT}/")


# database
db = myclient["GFG"]

Collection = db["data"]
log_col = db["log"]

def log_request(chat_id,request,answer):
    log_col.insert_one({'chat_id':chat_id, 'dt':datetime.now(), 'request':request, 'answer':answer})


def error_format():
    return 'Невалидный запос. Пример запроса: {"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", ' \
           '"group_type": "month"} '


def convert(data):
    try:
        return check_data(eval(data))
    except:
        return error_format()


def check_data(input_data):
    if type(input_data) is not dict:
        return error_format()

    dt_from_str = input_data.get('dt_from')
    dt_upto_str = input_data.get('dt_upto')

    try:
        dt_from = datetime.strptime(dt_from_str, '%Y-%m-%dT%H:%M:%S')
    except:
        return (error_format())

    try:
        dt_upto = datetime.strptime(dt_upto_str, '%Y-%m-%dT%H:%M:%S')
    except:
        return (error_format())

    group_type = input_data.get('group_type')
    if group_type not in ['hour', 'day', 'month']:
        return (error_format())
    return data_set(dt_from=dt_from, dt_upto=dt_upto, unit=group_type)


# словарь для склейки с нулевыми значениями
def time_interval_range(dt_from, dt_upto, unit):
    if unit == 'hour':
        delta = relativedelta(hours=+1)
        dt_from = datetime(dt_from.year, dt_from.month, dt_from.day, dt_from.hour)
    if unit == 'day':
        delta = relativedelta(days=+1)
        dt_from = datetime(dt_from.year, dt_from.month, dt_from.day)
    if unit == 'month':
        delta = relativedelta(months=+1)
        dt_from = datetime(dt_from.year, dt_from.month, day=1)
    ar_time = {}
    while dt_from <= dt_upto:
        ar_time[dt_from] = 0
        dt_from += delta
    return ar_time


def data_set(dt_from, dt_upto, unit):
    data = Collection.aggregate([
        {"$match": {"dt": {"$gte": dt_from}}},
        {"$match": {"dt": {"$lte": dt_upto}}},
        {"$project":
             {"value": "$value",
              "truncatedDate": {
                  "$dateTrunc": {
                      "date": "$dt", "unit": unit
                  }
              }
              }
         },
        {"$group":
             {"_id": "$truncatedDate", "count": {"$sum": "$value"}}
         },
        {"$sort":
             {"_id": 1}
         }
    ])

    dc_data = {dat['_id']: dat['count'] for dat in data}
    # добавление в итог диапазонов с нулевыми суммами
    data_total = (time_interval_range(dt_from, dt_upto, unit) | dc_data)

    dataset = []
    labels = []
    for key, value in data_total.items():
        dataset.append(value)
        labels.append(key.strftime("%Y-%m-%dT%H:%M:%S"))
    return {"dataset": dataset, "labels": labels}


if __name__ == '__main__':
    ans = check_data({
        "dt_from": "2022-10-01T00:00:00",
        "dt_upto": "2022-11-30T23:59:00",
        "group_type": "day"
    })
    pprint(ans)
    log_request('вопрос',"ответ")
