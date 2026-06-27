import random
import json 

consumptionperperson = {
    "potatoes": {"max": 11.61},
    "tomatoes": {"max": 3.3},
    "orange": {"max": 3.4},
    "apple": {"max": 8.0},
    "peach": {"max": 4.5},
    "olives": {"max": 1.2},
    "zucchini": {"max": 5.0}
}

totalPopulation = 34080030

populationperwillaya = {
    "Algiers": 2988145,
    "Oran": 1584607,
    "Setif": 1496150,
    "Djelfa": 1223223,
    "Batna": 1128030,
    "Tizi Ouzou": 1127608,
    "Chlef": 1013718,
    "Blida": 1009892,
    "M'Sila": 991846,
    "Tlemcen": 949135,
    "Tiaret": 946823,
    "Constantine": 943112,
    "Bejaia": 915835,
    "Skikda": 904195,
    "Medea": 830943,
    "Boumerdes": 802943,
    "Mascara": 784073,
    "Ain Defla": 771890,
    "Mila": 766886,
    "Mostaganem": 746947,
    "Relizane": 733060,
    "Biskra": 730262,
    "Bordj Bou Arreridj": 716432,
    "Bouira": 695583,
    "El Oued": 673934,
    "Tebessa": 657227,
    "Oum El Bouaghi": 644364,
    "Annaba": 640050,
    "Jijel": 636948,
    "Tipaza": 617661,
    "Sidi Bel Abbes": 604744,
    "Ouargla": 558558,
    "Guelma": 482430,
    "Laghouat": 477328,
    "Souk Ahras": 440299,
    "Adrar": 439693,
    "El Tarf": 411783,
    "Khenchela": 386683,
    "Ain Temouchent": 384565,
    "Ghradaia": 375988,
    "Saida": 330641,
    "Tissemsilt": 296336,
    "Bechar": 274866,
    "El Bayadh": 262187,
    "Naama": 209470,
    "Tamanrasset": 198691,
    "Tindouf": 159898,
    "Illizi": 54490
}




    
def generateConsumption () : 
    yearlyConsumption = {}

    for state in populationperwillaya:
        willay = []
        for product in consumptionperperson:
            min_val = consumptionperperson[product]["max"]
            needs = populationperwillaya[state] * min_val * 12
            productss = {
                "product": product,
                "needs": needs
            }
            willay.append(productss)
        yearlyConsumption[state] = willay

    import os

    file_path = './consumption.json'

    if os.path.exists(file_path):
        with open(file_path, "r") as myfile:
            file_content = myfile.read()
    else:
        file_content = "File doesn't exist."

    json_file_path = './consumption.json'

    with open(json_file_path, "w") as json_file:
        json.dump(yearlyConsumption, json_file)

generateConsumption()
