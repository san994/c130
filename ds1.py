import csv

rows = []

with open("main.csv","r") as f:
    csvreader = csv.reader(f)
    for row in csvreader:
        rows.append(row)

header = rows[0]
planet_data_rows = rows[1:]

header[0] = "row_num"
solars_system_planets_count = {}

for planet_data in planet_data_rows:
    if solars_system_planets_count.get(planet_data[11]):
        solars_system_planets_count[planet_data[11]]+=1
    else:
        solars_system_planets_count[planet_data[11]]=1

#print(len(planet_data_rows))


max_solar_system = max(solars_system_planets_count,key=solars_system_planets_count.get)
# print(max_solar_system,solars_system_planets_count[max_solar_system])
# print(solars_system_planets_count['HD 10180'])

koi_planets = []
for planet_data in planet_data_rows:
    if max_solar_system == planet_data[11]:
        koi_planets.append(planet_data)

# print(len(koi_planets),koi_planets)

temp_planet_data_rows = list(planet_data_rows)
for planet_data in temp_planet_data_rows:
    planet_mass = planet_data[3]
    if planet_mass.lower() == "unknown":
        planet_data_rows.remove(planet_data)
        continue
    else:
        planet_mass_value = planet_mass.split(" ")[0]
        planet_mass_ref = planet_mass.split(" ")[1]
        if planet_mass_ref == "Jupiters":
            planet_mass_value = float(planet_mass_value)*317.8
        
        planet_data[3] = planet_mass_value 

    planet_radius = planet_data[7]
    if planet_radius.lower() == 'unknown':
        planet_data_rows.remove(planet_data)
        continue
    else:
        planet_radius_value = planet_radius.split(" ")[0]
        planet_radius_ref = planet_radius.split(" ")[2]
        if planet_radius_ref == "Jupiter":
            planet_radius_value = float(planet_radius_value)*11.2

        planet_data[7] = planet_radius_value

#print(len(planet_data_rows))
koi_planets = []
for planet_data in planet_data_rows:
    if max_solar_system == planet_data[11]:
        koi_planets.append(planet_data)

#print(len(koi_planets),koi_planets)

import plotly.express as px

koi_planet_mass = []
koi_planet_names = []
for planet_data in koi_planets:
    koi_planet_mass.append(planet_data[3])
    koi_planet_names.append(planet_data[1])

koi_planet_mass.append(1)
koi_planet_names.append('earth')

# fig = px.bar(x=koi_planet_names,y=koi_planet_mass)
# fig.show()

temp_planet_data_rows = list(planet_data_rows) 
for planet_data in temp_planet_data_rows: 
    if planet_data[1].lower() == "hd 100546 b": 
        planet_data_rows.remove(planet_data)

planet_masses = [] 
planet_radiuses = [] 
planet_names = [] 
for planet_data in planet_data_rows: 
    planet_masses.append(planet_data[3]) 
    planet_radiuses.append(planet_data[7]) 
    planet_names.append(planet_data[1]) 
    planet_gravity = [] 

for index, name in enumerate(planet_names): 
    gravity = (float(planet_masses[index])*5.972e+24) / (float(planet_radiuses[index])*float(planet_radiuses[index])*6371000*6371000) * 6.674e-11 
    planet_gravity.append(gravity) 

#fig = px.scatter(x=planet_radiuses, y=planet_masses, size=planet_gravity, hover_data=[planet_names]) 
#fig.show()

low_gravity_planets = [] 
for index, gravity in enumerate(planet_gravity): 
    if gravity < 100: 
        low_gravity_planets.append(planet_data_rows[index]) 
        
#print(len(low_gravity_planets))

#ds2 c132

#print(header)
planet_type_values = []
for planet_data in planet_data_rows:
    planet_type_values.append(planet_data[6])

#print(list(set(planet_type_values)))

planet_masses=[]
planet_radius=[]
planet_types=[]
for planet_data in planet_data_rows:
    planet_masses.append(planet_data[3])
    planet_radius.append(planet_data[7])
    planet_types.append(planet_data[6])

# fig = px.scatter(x=planet_radius,y=planet_masses,color=planet_types)
# fig.show()

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

X = []
for index,planet_mass in enumerate(planet_masses):
    temp_list = [planet_radius[index],planet_mass]
    X.append(temp_list)

wcss = []
for i in range(1,11):
    kmeans = KMeans(n_clusters=i,init="k-means++",random_state=42)
    kmeans.fit(X)
    #inertia method returns wcss for that model
    wcss.append(kmeans.inertia_)

plt.figure(figsize=(10,5))
sns.lineplot(range(1,11),wcss,marker="o",color="red")

plt.title("the elbow method")
plt.xlabel("number of clusters")
plt.ylabel("wcss")

#plt.show()

#finding suitable planets
suitable_planets=[]
for planet_data in low_gravity_planets:
    if planet_data[6].lower() == 'terrestrial' or planet_data[6].lower() == "super earth":
        suitable_planets.append(planet_data)

#print(len(suitable_planets))

#class 133

#print(header)
temp_suitable_planets = list(suitable_planets)
for planet_data in temp_suitable_planets:
    if planet_data[8].lower()=="unknown":
        suitable_planets.remove(planet_data)

for planet_data in suitable_planets:
    if planet_data[9].split(" ")[1].lower()=="days":
        planet_data[9] = float(planet_data[9].split(" ")[0])
    else:
        planet_data[9]=float(planet_data[9].split(" ")[0])*365
    planet_data[8] = float(planet_data[8].split(" ")[0])

orbital_radius = []
orbital_period = []
for planet_data in suitable_planets:
    orbital_radius.append(planet_data[8])
    orbital_period.append(planet_data[9])

fig = px.scatter(x=orbital_radius,y=orbital_period)
# fig.show()

goldilock_planets = list(suitable_planets)
temp_goldilock_planets = list(suitable_planets)
for planet_data in temp_goldilock_planets:
    if planet_data[8] < 0.38 or planet_data[8] > 2:
        goldilock_planets.remove(planet_data)

# print(len(suitable_planets))
# print(len(goldilock_planets))

planets_speed = []
for planet_data in suitable_planets:
    distance = 2*3.14*(planet_data[8]*1.496e+9)
    time = planet_data[9]*86400
    speed = distance/time
    planets_speed.append(speed)

speed_supporting_planets = list(suitable_planets)
temp_speed_supporting_planets = list(suitable_planets)
for index,planets_data in enumerate(temp_speed_supporting_planets):
    if planets_speed[index] > 200:
        speed_supporting_planets.remove(planets_data)

#print(len(speed_supporting_planets))

#ds4

habitable_planets = []
for planets in speed_supporting_planets:
    if planets in goldilock_planets:
        habitable_planets.append(planets)

# print(habitable_planets,len(habitable_planets))

final_dict = {}
for index,planet_data in enumerate(planet_data_rows):
    features_list = []
    gravity = (float(planet_data[3])*5.972e+24)/(float(planet_data[7])*6371000*6371000)*6.674e-11
    try:
        if gravity<100:
            features_list.append("gravity")
    except:
        pass

    try:
        if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
            features_list.append("planettype")
    except:
        pass

    try:
        if planet_data[8]>0.38 or planet_data[8]<2:
            features_list.append("goldilock")
    except:
        pass

    try:
        distance = 2*3.14*(planet_data[8]*1.496e+9)
        time = planet_data[9]*86400
        speed = distance/time
        if speed < 200:
            features_list.append("speed")
    except:
        pass
    
    final_dict[index]=features_list
    
#print(final_dict)

#class 135

gravity_planet_count = 0
for key,value in final_dict.items():
    if "gravity" in value:
        gravity_planet_count+=1

#print(gravity_planet_count)

type_planet_count = 0
for key,value in final_dict.items():
    if "planettype" in value:
        type_planet_count+=1

#print(type_planet_count)

planet_not_gravity_support = []
for planet_data in planet_data_rows:
    if planet_data not in low_gravity_planets:
        planet_not_gravity_support.append(planet_data)

type_no_gravity_planet_count = 0
for planet_data in planet_not_gravity_support:
    if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
        type_no_gravity_planet_count+=1

# print(type_no_gravity_planet_count)
# print(type_planet_count-type_no_gravity_planet_count)

goldilock_planet_count = 0
for key,value in final_dict.items():
    if "goldilock" in value:
        goldilock_planet_count+=1

#print(goldilock_planet_count)

speed_planet_count = 0
for key,value in final_dict.items():
    if "speed" in value:
        speed_planet_count+=1

# print(speed_planet_count)

final_dict = {}
for index,planet_data in enumerate(planet_data_rows):
    features_list = []
    gravity = (float(planet_data[3])*5.972e+24)/(float(planet_data[7])*6371000*6371000)*6.674e-11
    try:
        if gravity<100:
            features_list.append("gravity")
    except:
        pass

    try:
        if planet_data[6].lower() == "terrestrial" or planet_data[6].lower() == "super earth":
            features_list.append("planettype")
    except:
        pass

    try:
        if  float(planet_data[8].split(" ")[0])>0.38 and float(planet_data[8].split(" ")[0])<2:
            features_list.append("goldilock")
    except:
        try:
            if planet_data[8]>0.38 and planet_data[8]<2:
                features_list.append("goldilock")
        except:
            pass

    try:
        try:
           distance = 2*3.14*(float(planet_data[8].split(" ")[0])*1.496e+9)
        except:
            try:
                diatance = 2*3.14*(float(planet_data[8])*1.496e+9)
            except:
                pass

        try:
            time,unit = planet_data[9].split(" ")[0],planet_data[9].split(" ")[1]
        
            if unit.lower()=="days":
                time = float(time)
            else:
                time = float(time)*365
            
        except:
            time = planet_data[9]

        time = time*86400

        speed = distance/time
        if speed < 200:
            features_list.append("speed")
    except:
        pass
    
    final_dict[planet_data[1]]=features_list
    
#print(final_dict)

goldilock_planet_count = 0
for key,value in final_dict.items():
    if "goldilock" in value:
        goldilock_planet_count+=1

#print(goldilock_planet_count)

speed_planet_count = 0
for key,value in final_dict.items():
    if "speed" in value:
        speed_planet_count+=1

#print(speed_planet_count)

goldilock_gravity_type_count = 0 
for key, value in final_dict.items(): 
    if "goldilock" in value and "planettype" in value and "gravity" in value: 
        goldilock_gravity_type_count += 1 
        

print(goldilock_gravity_type_count)

speed_goldilock_gravity_type_count = 0 
for key, value in final_dict.items(): 
    if "goldilock" in value and "planettype" in value and "gravity" in value and "speed" in value: 
        speed_goldilock_gravity_type_count += 1 
        
print(speed_goldilock_gravity_type_count)