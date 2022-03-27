# import module
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
from io import BytesIO

def main():
    st.set_page_config(page_title = 'EV charging station', 
                    layout = 'wide',
                    page_icon='🔌',
                    )

    st.title('Optimizing Vehicle Charging Station')

    st.sidebar.title('Enter the details of EV charging station')
    num_cs = st.sidebar.number_input('Number of charging stations', min_value=0, value=0)

    dist = pd.read_csv('data/distance_between_charging_stations.csv')
    df = pd.read_csv('data/ev_charging_station.csv')

    G = ox.graph_from_bbox(42.3567,41.9023,-82.4810,-83.1270, network_type='drive')

    geolocator = Nominatim(user_agent="geoapiExercises")

    loc = []
    address = []
    c,i = 0,0
    flag = False

    if num_cs>0:
        flag = True

    with st.spinner('Loading...'):   
        while flag:
            lat = (df.iloc[dist.st1.iloc[i]].lat + df.iloc[dist.st2.iloc[i]].lat )/2
            lon = (df.iloc[dist.st1.iloc[i]].lon + df.iloc[dist.st2.iloc[i]].lon )/2
            i+=1
            
            nearest_node = ox.distance.nearest_nodes(G, lon, lat)
            lat = G.nodes[nearest_node].get('y')
            lon = G.nodes[nearest_node].get('x')
            tmp = [lat,lon]
            
            if tmp in loc:
                continue
            d = []
            for j in range(len(df)):
                destination_node = ox.distance.nearest_nodes(G, df.lon[j], df.lat[j])
                distance_in_kilometers =  nx.shortest_path_length(G, nearest_node, destination_node, weight='length') / 1000
                d.append(distance_in_kilometers)
                
            if min(d)<5:
                continue 
            loc.append([lat,lon])
            address.append(geolocator.reverse(str(lat)+','+str(lon)).raw.get('address'))    
            c+=1
            if c==num_cs:
                break

        
        if flag:   
            address = pd.concat([pd.json_normalize(address),pd.DataFrame(loc,columns=['lat','lon'])],axis = 1)

            address['Status'] = 'New'

            df = df.append(address[['lat','lon','Status']]).reset_index(drop=True)
            



        m=folium.Map(
            location=[df['lat'].mean(), df['lon'].mean()],
            zoom_start=8)

        cluster = MarkerCluster(name="Electric Vehicle Charging Stations", options={"showCoverageOnHover": False})

        def get_icon(status):
            if status == "Existing":
                return folium.Icon(icon="bolt", prefix='fa',
                            color='black',
                            icon_color='#2ecc71'
                            )
            else:
                return folium.Icon(icon="glyphicon-time",
                            color='black',icon_color='yellow')
        df.apply(
            lambda row: folium.Marker(
                location=[row['lat'], row['lon']],
                popup=[row['lat'], row['lon']],
                tooltip=row['Plugtype'],
                icon=get_icon(row['Status']),
                ).add_to(cluster),
            axis=1)
        cluster.add_to(m)

        sw = df[['lat', 'lon']].min().values.tolist()
        ne = df[['lat', 'lon']].max().values.tolist()

        m.fit_bounds([sw,ne]) 
        m.add_child(folium.LatLngPopup())

        folium_static(m,width=1000, height=500)

        

        if flag:
            df_xlsx = to_excel(address.drop('house_number',axis =1))

            st.download_button(label=f'📥 Download detailed location information',
                                            data=df_xlsx ,
                                            file_name= f'location.xlsx')
            flag = False

    st.success('Done!')


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    
    return processed_data

if __name__ == '__main__':
    main()