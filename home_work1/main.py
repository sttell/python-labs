import math

drone_list = ["DJI Mavic 2 Pro", "DJI Mavic 2 Zoom", "DJI Mavic 2 Enterprise Advanced", "AUTEL Evo II Pro", "DJI Mini 2", "Autel Evo Nano", "Autel Evo Lite Plus", "Parrot Anafi", "Dji Inspire 2", "DJI Mavic 3", "DJI Mavic Air2s", "Ryze Tello", "Eachine Trashcan"]

drone_weight_list = [903, 900, 920, 980, 249, 249, 600, 540, 1500, 1000, 570, 130, 110]

def print_separator(description: str='', sym: str='=', line_len: int=50):
    description_len = len(description) + 2 if len(description) else 0

    if description_len:    
        left_align  = int((line_len - description_len) / 2.0)
        right_align = math.ceil((line_len - description_len) / 2.0)

        print(sym * left_align, description, sym * right_align)
    else:
        print(sym * line_len)
    


#в drone по очереди попадает каждый дрон из списка drone_list
for drone in drone_list:
	print(drone)


# -------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------
#TODO1
#выведите все дроны производителя, название которого введет пользователь через input, и подсчитайте их количество. 
#учтите, что:
#1) DJI и Dji - это один и тот же производитель! такие случаи тоже должны обрабатываться
#2) при выводе исправьте название производителя, если допущена ошибка. правильный вариант названия: DJI, Autel
# Create manufacturers dict. Key - lower case names, Value - Correct names

print_separator('TODO 1')
#request = input("Enter the manufacture: ").lower()
request = "DJI"

founded_count = 0
print(f"Founded drones with {request} manufacture:")
for drone_name in drone_list:
  if request.lower() in drone_name.split(' ')[0].lower():
    founded_count += 1
    print('\t', drone_name)

if not founded_count:
  print("\tDrones of this manufacturer could not be found")

print_separator()

# -------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------
#TODO2
#подсчитайте количество моделей дронов каждого производителя из списка drone_list. производители: DJI, Autel, Parrot, Ryze, Eachine

print_separator('TODO 2')

print("The number of drones of each manufacturer:")
manufacturers_list = ["DJI", "Autel", "Parrot", "Ryze", "Eachine"]
manufacturers_stat = { name.lower() : 0 for name in manufacturers_list }
manufacturers_from_lowercase = { name.lower() : name for name in manufacturers_list }

# Count
for drone_name in drone_list:
  manufacture = drone_name.split(' ')[0].lower()
  manufacturers_stat[manufacture] += 1

# Show results
for name, count in manufacturers_stat.items():
  print("\t", manufacturers_from_lowercase[name], count)
  
print_separator()


# -------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------------------
#TODO3
#выведите все дроны из списка, которые нужно регистрировать (масса больше 150 г), и подсчитайте их количество. 
#сделайте то же самое для всех дронов, которые не нужно регистрировать
#для этого вам нужно параллельно обрабатывать два списка: drone_list и drone_weight_list:
#как работает zip, мы разберем на лекции про списки. пока что просто пользуйтесь
print_separator('TODO 3')
print("The number of drones of each manufacturer:")

count_with_registration = 0

print("Drones that need to be registered [Weight > 150 g]:")

for drone, weight in zip(drone_list,  drone_weight_list):
  if weight > 150:
    print(f'\t{drone} - Weight: {weight} g')
    count_with_registration += 1
    
print("Total:", count_with_registration)

print_separator()