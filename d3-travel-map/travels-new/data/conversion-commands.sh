ogr2ogr -f GeoJSON geoworld.json ne_50m_admin_0_countries.shp
geo2topo countries=geoworld.json > topoworld.json

# MAKE SURE YOU HAVE THE REST OF THE NATURALEARTH DOWNLOAD FILES IN THE SAME DIRECTORY
# i.e don't be a fool and copy over only the .shp file like I did.
# If you're curious, the error you'll get is:

# Unable to open datasource `ne_50m_admin_0_countries.shp' with the following drivers.