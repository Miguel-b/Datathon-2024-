#This is the code we used to find the cordinates of some comunas to correlate them to some data we found so that it can be implemented in Arc GIS.
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Load your main dataset
df_main = pd.read_csv(r"Registro_Nacional_de_Turismo_-_RNT_20241109.csv")

# Initialize geolocator
geolocator = Nominatim(user_agent="geo_lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Define function to get lat/lon
def get_lat_long(row):
    location = geocode(f"{row['COMUNA']}, Medellín, Colombia")
    if location:
        return pd.Series([location.latitude, location.longitude])
    else:
        return pd.Series([None, None])

# Load the CSV file containing coordinates for Medellín's comunas
df_coords = pd.read_csv(r'medellin_comunas_coordinates.csv')

# Rename columns to match the ones in df_main if needed, for example:
# df_main.rename(columns={'Comuna_Name_In_Dataset': 'COMUNA'}, inplace=True)

# Merge the dataframes on the 'COMUNA' column
df_merged = pd.merge(df_main, df_coords, left_on='COMUNA', right_on='Comuna Name', how='left')

# Save the new dataset with coordinates
df_merged.to_csv('dataset_con_coordenadas.csv', index=False)
