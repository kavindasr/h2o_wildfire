# About deep-mind wildfire prediction app

![Cover](https://github.com/kavindasr/wildfire_images/blob/main/cover.jpg?raw=true)
## About h2o.ai wildfire-challange

Wildfires (aka bushfires) threaten lives, communities, wildlife, and forests every year, and with global climate change, it is getting worse.This problem is regional within countries, but it is a global issue and is considered one of the most dangerous disasters we face. While humans cause many fires, other factors, including wind, lightning, drought, and landscape, impact where fires occur and how they spread.

Wildfires present unique and severe forecasting challenges. Compared to storms, such as hurricanes, wildfires are ambiguous and hard to predict, especially when you start looking at large, intense wildfires. Those fires combine complex weather, different landscapes, fuel sources such as housing materials or dry forests, and more.

## Our mission
Our goal is to predict wildfires in Australia based on the location. We basically focus on the first responders(firefighters, or the firefighting command centers ). The basic functionalities of this application includes getting a summary dashboard with the Top 10 high fire alert regions for the last 24 hours and Top 4 frequent fire alert regions. This will inform the users about which areas they need to be aware of. Last 24 hour wildfires will be displayed on a map for a better understanding. Most importantly an intelligent ML model will predict the occuring of wildfires for the next 12 months. It includes the estimated risk and the estimated burning area which will helpful for the users to take precations prior to a wildfire occuring.

## How we predict wildfires
- We used Time Series Analysis to predict the future based on the past data upto last 24 hour.
- Last 24 data is retreived through a cron job which runs daily
- ([Prophet by facebook](https://facebook.github.io/prophet/)) is used to implement the time series model.
- Accuracy, Performance, Able to work with seasonality data are the main reason to choose Prophet
- This system is able to predict the future for selected location for next 12 month(This depend on the number of past data)
- Model training and the prediction is happenning real time.
- Currentl system is able to predict the estimated risk value and the estimated burned fire area
- Estimated values may vary between maximum and minimum threshold values.

## About dataset
FIRMS distributes Near Real-Time (NRT) active fire data within 3 hours of satellite observation from the Moderate Resolution Imaging Spectroradiometer ([MODIS](https://modis.gsfc.nasa.gov/)) aboard the Aqua and Terra satellites, and the Visible Infrared Imaging Radiometer Suite ([VIIRS](https://www.jpss.noaa.gov/viirs.html)) aboard S-NPP and NOAA 20.

![Dataset1](https://github.com/kavindasr/wildfire_images/blob/main/WhatsApp%20Image%202022-02-26%20at%201.13.18%20AM(1).jpeg?raw=true)

![Dataset2](https://github.com/kavindasr/wildfire_images/blob/main/WhatsApp%20Image%202022-02-26%20at%201.13.18%20AM.jpeg?raw=true)

## Features
### Dashboard
**High Fire Alert Regions for Last 24 Hours**

This will list the top 10 high estimated risk areas for last 24 hours, using the data captured by VIIRS satellite.
The estimated risk is calculated based on 
- Confidence Level 
- Total fire count per day 
- Total Burned Fire Area 
- Total Radiative Power emitted 
with different weights

![Dashboard](https://github.com/kavindasr/wildfire_images/blob/main/last24.png?raw=true)


**Top 4 Frequent Fire Ocurring Regions**

There are some regions where the occuring of wilfires are very frequent. This will displays the Top 4 areas where the number of fire occurences are very high. 

![top4](https://github.com/kavindasr/wildfire_images/blob/main/WhatsApp%20Image%202022-02-26%20at%201.50.26%20AM.jpeg?raw=true)

### Wildfire map

This Australia map displays the high risk areas for the last 24 hours.  

![map](https://github.com/kavindasr/wildfire_images/blob/main/map.png?raw=true)

### Predict

Most importantly an intelligent ML model will predict the occuring of wildfires for the next 12 months. It includes the estimated risk and the estimated burning area which will helpful for the users to take precations prior to a wildfire occuring. They can input the ocation they need to get the prediction and it will displays the prediction charts.


![predict](https://github.com/kavindasr/wildfire_images/blob/main/predict.png?raw=true)

### Third party APIs
- NASA firms modaps API to get latest data
- Openstreetmap nominatim to get location details


