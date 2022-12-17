# В ЭТОМ ДЗ ВЫ БУДЕТЕ АНАЛИЗИРОВАТЬ ДАННЫЕ ОБ АВИАПРОИСШЕСТВИЯХ С УЧАСТИЕМ МОДЕЛЕЙ ДРОНОВ ИЗ ВАШИХ ИСХОДНЫХ ДАННЫХ В .JSON

# =====================================
# ЗАДАНИЕ 1: Классы - декораторы
# =====================================
# TODO 1-1 - Добавить атрибут incidents типа список
# Возьмите код из предыдущего ДЗ
# Добавьте в класс MultirotorUAV атрибут incidents и внесите туда информацию обо всех найденных происшествиях для этой модели
# Не забудьте, что атрибут добавляется при помощи декоратора

# ВАШ КОД (дополните то, что нужно в классах):
import json

class Aircraft:
    def __init__(self, weight):
        self._weight = weight


class UAV:
    def __init__(self):
        self._has_autopilot = True
        self.__missions = []

    # напишите код для декоратора атрибута _missions
    @property
    def missions(self):
        return self.__missions

    @missions.setter
    def missions(self, missions):
        self.__missions = missions

    # напишите публичный метод count_missions
    def count_missions(self):
        return len(self.__missions)


class MultirotorUAV(Aircraft, UAV):
    def __init__(self, weight, model, brand):
        super().__init__(weight)
        UAV.__init__(self)
        self.__weight = weight
        self.__model = model
        self.__brand = brand
        self.__incidents = []

    # напишите публичный метод get_info
    def get_info(self):
        return f"Информация о дроне {self.__model}: масса {self.__weight}, производитель {self.__brand}, " \
               f"количество миссий {self.count_missions()}"

    # напишите публичный метод get_model
    def get_model(self):
        return self.__model

    # напишите код декоратора для атрибута incidents. Не забудьте сначала добавить приватный атрибут в класс
    @property
    def incidents(self):
        return self.__incidents

    # напишите публичный метод add_incident, который добавляет инцидент в список инцидентов для данной модели дрона
    def add_incident(self, incident):
        self.__incidents.append(incident)

    # напишите публичный метод save_data, который сохраняет информацию о дроне в файл json
    def save_data(self):
        data = {
            "model": self.__model,
            "weight": self.__weight,
            "brand": self.__brand,
            "missions": self.missions,
            "incidents": self.__incidents
        }

        output_filename = 'saved_data/' + str(self.__class__.__name__) + '_' + str(self.__model) + ".json"
        with open(output_filename, 'w') as fp:
            json.dump(data, fp, indent=2)


# ВАШ КОД из предыдущего ДЗ, необходимый для решения этого ДЗ (чтение данных о пилотах, сбор информации о дронах и пр.):

data = {}
with open('pilot_path.json', 'r') as fp:
    data = json.load(fp)

# каталог дронов уже готов для вас:
drone_catalog = {
    "DJI Mavic 2 Pro": {"weight": 903, "brand": "DJI"},
    "DJI Mavic 2 Zoom": {"weight": 900, "brand": "DJI"},
    "DJI Mavic 2 Enterprise Advanced": {"weight": 920, "brand": "DJI"},
    "DJI Inspire 2": {"weight": 1500, "brand": "DJI"},
    "DJI Mavic 3": {"weight": 1000, "brand": "DJI"}
}

# ВАШ КОД:
drone_to_multirotor = {}

for pilot, pilot_data in data.items():
    for mission in pilot_data['missions']:
        drone = mission['drone']

        catalog_info = drone_catalog[drone]
        weight = drone_catalog[drone]['weight']
        brand = drone_catalog[drone]['brand']

        if drone in drone_to_multirotor:
            drone_to_multirotor[drone].missions.append(mission['mission'])
        else:
            drone_to_multirotor[drone] = MultirotorUAV(catalog_info['weight'], drone, catalog_info['brand'])
            drone_to_multirotor[drone].missions.append(mission['mission'])

drones_cls_list = [x for _, x in drone_to_multirotor.items()]


# =====================================
# ЗАДАНИЕ 2: Файлы - CSV
# =====================================
# TODO 2-1 - Загрузите информацию об авиапроисшествиях из файла csv
# Проверьте по моделям (названия моделей возьмите из экземпляров класса MultirotorUAV), какие из них участвовали в авиапроисшествиях

# ВАШ КОД чтения данных из файла:
import csv

incidents_details = []
with open("faa_incidents.csv") as f:
    reader = csv.reader(f)
    lines = list(reader)
    incidents_details = [line[-1] for line in lines[1:]]

# =====================================
# ЗАДАНИЕ 3: Классы
# =====================================
# TODO 3-1 - Для каждой модели дрона добавьте в экземпляр класса информацию об авиапроисшествиях, в которых участвовала эта модель
# Информацию сохраните в атрибут incidents (используйте декораторы)
# Подсказка: вот так вы получаете названия модели для каждого экземпляра класса MultirotorUAV
# Экземпляры все так же находятся в списке (например, drones_cls_list)

for drone_cls in drones_cls_list:
    drone = drone_cls.get_model()
    drone_name = ' '.join(drone.split(' ')[1:]).lower()

    for incident in incidents_details:
        if drone_name in incident.lower():
            drone_cls.add_incident(incident)

# TODO 3-2 - Добавьте в класс MultirotorUAV публичный метод save_data, который сохраняет статистику по дрону в файл
# Внимание! Метод save_data не принимает параметры. Название файла сформируйте как: название класса + название модели + расширение .json
# например: "MultirotorUAV_DJI Mavic 2 Pro.json"
# Подсказка: название класса вы можете получить вот так: self.__class__.__name__
# используйте ключи: "model", "weight", "brand", "missions", "incidents"
# например: {"model":"DJI Inspire 2", "weight": 1500, "info": "...", "manufacturer": "DJI", "missions": [], "incidents": []}

# ВАШ КОД - допишите код в объявлении класса
# Сохранение идет в папку saved_data.

# =====================================
# ЗАДАНИЕ 4: Регулярные выражения
# =====================================
# TODO 4-1 - Выведите на экран собранную информацию по инцидентам по каждому дрону в таком виде:
# модель: инцидентов - количество
# 1 - краткий текст инцидента*
# полный текст инцидента
# * - краткий текст инцидента получайте следующим образом: в исходном тексте инцидента найдите модель, например, INSPIRE 2,
# и выведите все предложения, в которых встречается упоминание этой модели
# Подсказка 1: Полностью готовый код есть в лекции про регулярные выражения (пример про перелетных птиц).
# Ваши изменения: а) вставить вместо "зим" название модели дрона, б) поменять язык поиска на английский
# Подсказка 2: не забывайте использовать флаг re.I для игнорирования регистра символов
# Подсказка 3: перед тем, как искать, уберите из названия модели название производителя
# Подсказка 4: лучше не используйте re.compile. Для этого случая работает не очень

# РЕЗУЛЬТАТ:
# mavic 2 enterprise advanced: инцидентов - 0
# mavic 2 pro: инцидентов - 0
# mavic 3: инцидентов - 0
# mavic 2 zoom: инцидентов - 1
# 1 - ON JULY 15, 2020 AT 1050 EDT, A DJI, MAVIC 2 ZOOM L1Z UAS, SERIAL # 0M6TG85R0A04ZP, UA FA REGISTRATION # FA3RE7RNWP, REGISTERED TO ^PRIVACY DATA OMITTED^ (PIC), REMOTE PILOT CERTIFICATE ^PRIVACY DATA OMITTED^, LOST CONTROLLED FLIGHT IN THE AREA OF ^PRIVACY DATA OMITTED^ AND HIT A BLACK NISSAN PICKUP TRUCK BEARING ^PRIVACY DATA OMITTED^ TRAVELING ALONG TAMIAMI TRAIL IN NORTH PORT CAUSING PROPERTY DAMAGE.
# ON JULY 15, 2020 AT 1050 EDT, A DJI, MAVIC 2 ZOOM L1Z UAS, SERIAL # 0M6TG85R0A04ZP, UA FA REGISTRATION # FA3RE7RNWP, REGISTERED TO ^PRIVACY DATA OMITTED^ (PIC), REMOTE PILOT CERTIFICATE ^PRIVACY DATA OMITTED^, LOST CONTROLLED FLIGHT IN THE AREA OF ^PRIVACY DATA OMITTED^ AND HIT A BLACK NISSAN PICKUP TRUCK BEARING ^PRIVACY DATA OMITTED^ TRAVELING ALONG TAMIAMI TRAIL IN NORTH PORT CAUSING PROPERTY DAMAGE. THE UAS WAS FLOWN ON A RECREATIONAL FLIGHT OVER A CONSTRUCTION SITE AT ^PRIVACY DATA OMITTED^, USING AN AUTOMATIC FREQUENCY SELECTION FEATURE THAT RANGED FROM 2.400 - 2.4835 GHZ; 5.725 - 5.850 GHZ. WEATHER CONDITIONS WERE CLEAR AND ARE NOT CONSIDERED A FACTOR. THE UAS WAS DESTROYED AND THE PROPERTY DAMAGE WAS GREATER THAN $500. THERE WERE NO PERSONAL INJURIES. THE FLIGHT ORIGINATED FROM ^PRIVACY DATA OMITTED^, EARLIER THAT DAY. WHILE THIS INCIDENT MEETS FAA UAS ACCIDENT CRITERIA, IT DOES NOT MEET THE NTSB?S UAS ACCIDENT CRITERIA. THE NTSB WOULD NOT ISSUE A NTSB ACCIDENT NUMBER FOR THIS EVENT. THEREFORE, THIS EVENT WILL BE CLASSIFIED AN INCIDENT.
# inspire 2: инцидентов - 3
# 1 - RPIC WAS OPERATING A DJI INSPIRE 2 WITH A CAMERA/GIMBLE COMBINATION SET UP. DJI INSPIRE 2 (SN 09YDDCQL040384) CURRENT FAA SUAS REGISTRATION NUMBER FA343FTPWM.
# ON MAY 25, 2020, MOJAVE AIR AND SPACE PORT (KMHV) AIR TRAFFIC CONTROL TOWER (ATCT) PROVIDED VERBAL AUTHORIZATION TO ^PRIVACY DATA OMITTED^ TO PERFORM SUAS OPERATIONS IN KMHV CLASS D AIRSPACE. WIND SPEED WAS 7 KNOTS WITH GUSTS AT 14 KNOTS. WIND DIRECTION 060. ^PRIVACY DATA OMITTED^. AND KMHV HAVE A LETTER OF AGREEMENT (LOA) EFFECTIVE JANUARY 28, 2020 FOR SUAS OPERATIONS IN KMHV CLASS D AIRSPACE. ^PRIVACY DATA OMITTED^ HOLDS A CURRENT CERTIFICATE OF WAIVER OR AUTHORIZATION EFFECTIVE FROM JANUARY 31, 2019 TO SEPTEMBER 30, 2020 TO PERFORM SMALL UNMANNED AIRCRAFT SYTEM (SUAS) OPERATIONS IN CLASS D AIRSPACE AT KMHV. ^PRIVACY DATA OMITTED^ HOLDS A CURRENT REMOTE PILOT CERTIFICATE WITH A SUAS RATING ^PRIVACY DATA OMITTED^. REMOTE PILOT IN COMMAND (RPIC), ^PRIVACY DATA OMITTED^ WAS OPERATING UNDER PART 107 AT KMHV COVERING SURVEILLANCE OF THE VIRGIN ORBIT LAUNCHER ONE MISSION. RPIC WAS OPERATING A DJI INSPIRE 2 WITH A CAMERA/GIMBLE COMBINATION SET UP. DJI INSPIRE 2 (SN 09YDDCQL040384) CURRENT FAA SUAS REGISTRATION NUMBER FA343FTPWM. REGISTERED TO ^PRIVACY DATA OMITTED^. RPIC WAS OPERATING WITH ONE INEXPERIENCED VISUAL OBSERVER (VO). RPIC WAS NOT ACCUSTOMED TO OPERATING THE SMALL UNMANNED AIRCRAFT CONTROLS, MANIPULATING THE CAMERA/GIMBLE COMBINATION SET UP, AND COMMUNICATING TO ATCT VIA RADIO SIMULTANEOUSLY. RPIC WAS ALSO WORKING WITH AN INEXPERIENCED VO. RPIC BECAME TASK SATURATED AND LOST SIGHT OF THE SMALL UNMANNED AIRCRAFT. AT 1208 LOCAL TIME, THE SMALL UNMANNED AIRCRAFT STRUCK THE WEST SIDE OF KMHV ATCT. ^PRIVACY DATA OMITTED^ SUSTAINED A SUPERFICIAL HORIZONTAL LACERATION TO HIS RIGHT LOWER, INSIDE FOREARM. HE WAS TREATED ON-SCENE WITH BANDAGE AND GAUZE WRAP.
# 2 - USED RENTED DJI INSPIRE 2 DRONE.
# UAS PILOT ^PRIVACY DATA OMITTED^ REMOTE CERTIFICATE #^PRIVACY DATA OMITTED^ WAS HIRED BY PRODUCER ^PRIVACY DATA OMITTED^ TO DO SOME AERIAL SHOTS OF EL MORRO FOR A DOCUMENTARY ABOUT THE 500 YEARS OF THE CITY OF SAN JUAN ON SEPTEMBER 3RD. USED RENTED DJI INSPIRE 2 DRONE. LOST CONTROL LINK WITH DRONE ON WAY BACK CRASHED INTO EL MORRO FORT IN OLD SAN JUAN.
# 3 - AIRCRAFT IS A DJI T650A INSPIRE 2 SUAS, SERIAL # 0A0LG2J107005, REGISTRATION # FA3FTYCLFE.
# AIRCRAFT IS A DJI T650A INSPIRE 2 SUAS, SERIAL # 0A0LG2J107005, REGISTRATION # FA3FTYCLFE. FREQUENCY USED IS UNKNOWN. THE AIRCRAFT HAS TWO FREQUENCIES AVAILABLE, 2.4 AND 5.8 GHZ, BUT THE PIC DOESN'T REMEMBER WHICH ONE WAS IN USE DURING THE FLIGHT. PIC IS ^PRIVACY DATA OMITTED^, CERTIFICATE ^PRIVACY DATA OMITTED^. ^PRIVACY DATA OMITTED^ SAID THAT THE UAS EXPERIENCED AN ERROR ON ITS FIRST CALIBRATION ATTEMPT PRIOR TO LAUNCH BUT CALIBRATED CORRECTLY ON THE SECOND ATTEMPT AND THE FLIGHT CONTINUED AFTER RECORDING THE HOME POINT AT THE LAUNCH POSITION. HE SAID THE UAS WAS IN POSITIONING MODE (P-MODE) FOR THE ENTIRE FLIGHT. THE LANDING SEQUENCE WAS INITIATED MANUALLY (I.E. THE AUTOLAND FEATURE WAS NOT USED). ^PRIVACY DATA OMITTED^ SAID THAT THE UAS "TOOK OFF" WHEN IT GOT DOWN TO ABOUT 5' AGL AND FLEW INSIDE THE CPD HANGAR WHERE IT STRUCK A CPD HELICOPTER. HE SAID THAT THE UAS ACTED AS IF IT WAS "PRE-PROGRAMMED" TO FLY INTO THE HANGAR ONCE IT GOT AWAY FROM HIM.

# ВАШ КОД:
import re

regex_pattern_fmt = r'[A-Z][^\.!?]+({})(?(1)[^\.!?]+[\.!?])'
drones_cls_list = sorted(drones_cls_list, key=lambda item: len(item.incidents))
for drone_cls in drones_cls_list:
    drone_name = ' '.join(drone_cls.get_model().lower().split(' ')[1:]).strip()
    incidents_count = len(drone_cls.incidents)

    print(f"{drone_name}: инцидентов - {incidents_count}")
    if incidents_count == 0:
        continue

    pattern = regex_pattern_fmt.format(drone_name)
    for incident_idx, incident in enumerate(drone_cls.incidents):
        print(f'{incident_idx + 1} - ', end='')
        result = re.search(pattern, incident, flags=re.IGNORECASE)
        print(result.group())
        print(incident)

# TODO 4-2 - После вывода информации об инциденте сохраните всю информацию о дроне в файл .json при помощи метода save_data
# ВАШ КОД:
for drone_cls in drones_cls_list:
    drone_cls.save_data()

# РЕЗУЛЬТАТ:
# см. приложенные файлы в папке samples