import os
import folium
import geopandas as gpd
from geopy.geocoders import Nominatim

# Initialize the output counter
output_counter = 1
counter_file = 'output_counter.txt'

if os.path.exists(counter_file):
    with open(counter_file, 'r') as file:
        try:
            output_counter = int(file.read())
        except ValueError:
            pass

# Create a GeoDataFrame to store the missing persons' data
gdf = gpd.GeoDataFrame(columns=['name', 'latitude', 'longitude', 'place', 'country', 'postal_code', 'geometry'])

# Create a map centered at a default location (e.g., coordinates for South Africa).
map_center = [40.7128, -74.0060]
mymap = folium.Map(location=map_center, zoom_start=5)

geolocator = Nominatim(user_agent="missing_persons_tool")

# ANSI escape codes for color formatting
class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    END = '\033[0m'  # Reset color

# Colored question function
def colored_question(question, color):
    return f"{color}{question}{Color.END}"

# Add missing person data to the GeoDataFrame and create map markers
def add_missing_person(name, latitude, longitude, place, country, postal_code):
    gdf.loc[len(gdf)] = [name, latitude, longitude, place, country, postal_code, gpd.points_from_xy([longitude], [latitude])[0]]
    folium.Marker([latitude, longitude], tooltip=name).add_to(mymap)

# Add Street View and Real-Time View layers
folium.TileLayer('Stamen Terrain').add_to(mymap)  # Street View
folium.TileLayer('CartoDB positron', name='Real-Time View').add_to(mymap)  # Real-Time View

# Create a layer control for switching between the layers
folium.LayerControl().add_to(mymap)

# ASCII banner text with color
banner = f"""
{Color.GREEN}
 ______     __         ______     __   __     ______   __  __     ______     __   __    
/\  == \   /\ \       /\  __ \   /\ "-.\ \   /\  == \ /\ \_\ \   /\  ___\   /\ "-.\ \   
\ \  __<   \ \ \____  \ \  __ \  \ \ \-.  \  \ \  _-/ \ \  __ \  \ \  __\   \ \ \-.  \  
 \ \_____\  \ \_____\  \ \_\ \_\  \ \_\\"\_\  \ \_\    \ \_\ \_\  \ \_____\  \ \_\\"\_\ 
  \/_____/   \/_____/   \/_/\/_/   \/_/ \/_/   \/_/     \/_/\/_/   \/_____/   \/_/ \/_/ 

                                                                        Author: OFD5

                                  Safepayload.co.za                       
{Color.END}
"""

print(banner)

while True:
    name = input(colored_question("Enter the name of the missing person (or 'q' to quit): ", Color.CYAN))
    if name == 'q':
        break

    try:
        latitude = float(input(colored_question("Enter the latitude: ", Color.CYAN)))
        longitude = float(input(colored_question("Enter the longitude: ", Color.CYAN)))
    except ValueError:
        print(colored_question("Invalid latitude or longitude. Please enter numeric values.", Color.RED))
        continue

    postal_code = input(colored_question("Enter the postal code: ", Color.CYAN))
    place = input(colored_question("Enter the place: ", Color.CYAN))
    country = input(colored_question("Enter the country: ", Color.CYAN))

    # Add the missing person to the GeoDataFrame and create a map marker
    add_missing_person(name, latitude, longitude, place, country, postal_code)

if not gdf.empty:  # Check if the GeoDataFrame is not empty
    # Create a map with markers for all missing persons
    for index, row in gdf.iterrows():
        folium.Marker([row['latitude'], row['longitude']], tooltip=row['name']).add_to(mymap)

    # Save the map to an HTML file with the updated output counter.
    output_file = f'missing_persons_map_{output_counter}.html'
    mymap.save(output_file)

    print(colored_question(f'Map saved as {output_file}', Color.GREEN))
    output_counter += 1

    # Save the updated counter back to the file.
    with open(counter_file, 'w') as file:
        file.write(str(output_counter))
else:
    print(colored_question("No data provided, so the map was not saved.", Color.RED))
