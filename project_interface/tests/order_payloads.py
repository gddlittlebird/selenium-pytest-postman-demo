# order_payloads.py

base_order_payload = {
        "productsId": 97,
        "countryId": 233,
        "userId": 8065,
        "packageTypeId": 1,
        "goodsNumber": 2,
        "receiveInfo": {
            "address": "9850 Mississippi Street",
            "provinceId": 0,
            "cityId": 0,
            "districtId": 0,
            "provinceName": "IN",
            "cityName": "MERRILLVILLE",
            "countryId": 233,
            "mobile": "000",
            "name": "ONT8",
            "phoneNumber": "000",
            "zipCode": "46410"
        },
        "storehouseId": 1,
        "reserveOrderDetailList": [
            {
                "height": 40,
                "length": 40,
                "weight": 12,
                "width": 40
            },
            {
                "height": 40,
                "length": 40,
                "weight": 12,
                "width": 40
            }
        ],
        "customsInfoList": [
            {
                "amount": 48,
                "ctns": 2,
                "hsCode": "83061000",
                "englishName": "铃铛",
                "shipmentTrackingId": "",
                "fbaNumber": "",
                "remark": "",
                "material": "铁",
                "name": "铃铛",
                "singleWeight": 12,
                "specification": "无",
                "totalValue": 288,
                "unitPrice": 3,
                "unitTypeId": 0,
                "uses": "铃铛",
                "picUrl": "http://tianmubms.oss-cn-shenzhen.aliyuncs.com/1752718461039_GkN1.png",
                "brand": "无",
                "volume": "40*40*40"
            }
        ]
    }

def get_order_payload_by_index(idx):
    import copy
    order=copy.deepcopy(base_order_payload)
    #动态该产品ID
    order["productsId"] += idx
    order["countryId"] += idx
    order["userId"] += idx

    return order



