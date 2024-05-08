# hdb-better-map
A cleaner visualization of block ages and resale prices, compared to HDB's official map (https://services2.hdb.gov.sg/web/fi10/emap.html), based on Python, and Plotly on Dash

Data for transactions up to 22 Apr 2024 has been included, for trying out this map. It has been preprocessed to fit the requirements of the mapping app. To include newer transactions in the app, newer data will need to be downloaded from HDB, preprocessed and referenced to by the code.

Running instructions:
1. Download this repo locally into a single folder
2. Install all required packages (requirements.txt file will be included in the future)
3. Optional: if you want to use Mapbox maps, add a file named mapbox_token.txt to this same folder with your Mapbox access token inside
4. In a command prompt window, navigate to the folder where you downloaded everything to, and run "python scatter-map-app.py"
