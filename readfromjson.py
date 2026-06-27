import json

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def structure_data():
    filenames = ['orange.json','olives.json','peach.json', 'tomato_data.json', 'potato_data.json', 'zucchini.json', 'apple.json']
    structured_data = []
    for filename in filenames:
        crop_data = read_json(filename)
        for record in crop_data:
            wilaya_name = record.get("Wilaya Name")
            for crop_type, crops in record.items():
                if crop_type not in ["Wilaya Number", "Wilaya Name"]:
                    for crop_name, crop_info in crops.items():
                        structured_data.append({
                            "name": crop_name,
                            "wilaya_name": wilaya_name,
                            "production": crop_info.get("Production (qx)", 0),
                            "land_size": crop_info.get("Superficie (ha)", 0),
                            "type": crop_type
                        })
                   
    return structured_data

def wilaya_land_size():
    # Dictionary containing the data
    data = {
        "Algeria": {
            "wilayas": [
    {"name": "ADRAR", "size": 575551},
    {"name": "CHLEF", "size": 262511},
    {"name": "LAGHOUAT", "size": 2008706},
    {"name": "O.E.BOUAGHI", "size": 360885},
    {"name": "BATNA", "size": 422677},
    {"name": "BEJAIA", "size": 130917},
    {"name": "BISKRA", "size": 473185},
    {"name": "BECHAR", "size": 1424998},
    {"name": "BLIDA", "size": 55780},
    {"name": "BOUIRA", "size": 293544},
    {"name": "TAMANRASSET", "size": 263543},
    {"name": "TEBESSA", "size": 175312},
    {"name": "TLEMCEN", "size": 537274},
    {"name": "TIARET", "size": 707622},
    {"name": "TIZI-OUZOU", "size": 98842},
    {"name": "ALGER", "size": 28870},
    {"name": "DJELFA", "size": 665378},
    {"name": "JIJEL", "size": 44967},
    {"name": "SETIF", "size": 364870},
    {"name": "SAIDA", "size": 308206},
    {"name": "SKIKDA", "size": 131829},
    {"name": "S.B.ABBES", "size": 363420},
    {"name": "ANNABA", "size": 47448},
    {"name": "GUELMA", "size": 187338},
    {"name": "CONSTANTINE", "size": 125010},
    {"name": "MEDEA", "size": 338359},
    {"name": "MOSTAGANEM", "size": 144778},
    {"name": "M'SILA", "size": 277592},
    {"name": "MASCARA", "size": 312787},
    {"name": "OUARGLA", "size": 50421},
    {"name": "ORAN", "size": 86757.39},
    {"name": "EL-BAYADH", "size": 239.574},
    {"name": "ILLIZI", "size": 2725.0},
    {"name": "B.B.ARRERIDJ", "size": 186600},
    {"name": "BOUMERDES", "size": 26817},
    {"name": "EL-TARF", "size": 74173},
    {"name": "TINDOUF", "size": 872},
    {"name": "TISSEMSILT", "size": 145456},
    {"name": "EL-OUED", "size": 105500},
    {"name": "KHENCHELA", "size": 257426},
    {"name": "SOUK-AHRAS", "size": 253606},
    {"name": "TIPAZA", "size": 61799.79},
    {"name": "MILA", "size": 237557},
    {"name": "AIN-DEFLA", "size": 181676},
    {"name": "NAAMA", "size": 28283},
    {"name": "A.TEMOUCHENT", "size": 180994},
    {"name": "GHARDAIA", "size": 72491},
    {"name": "RELIZANE", "size": 281875}
]

        }
    }

    # Extract wilayas data from the dictionary
    wilayas = data["Algeria"]["wilayas"]
    land_size = [{"name": wilaya["name"], "size": wilaya["size"]} for wilaya in wilayas]
    return land_size

if __name__ == '__main__':
    structured_data = structure_data()
    print(structured_data)