# vehicle_charging_station_optimization

## Inspiration
One of the major reasons is to help improve the environment by replacing conventional vehicles with 
 zero-emission vehicles. Electric vehicles are known to reduce local emissions by approximately 34-98% and help improve air quality.

## What it does
Our web application takes the input of the number of charging stations from the user and displays a map with the existing stations and information of plug type and location coordinates along with newly suggested charging stations with only the coordinates

## How we built it
Firstly, we have extracted the data using overpassAPI and preprocessed that. Then, worked on location optimization of the vehicle's charging point. After all this work, we have deployed our work and made a web-app that takes the number of new charging points to be placed as an input and gives the output of the location of the new charging point on the map as well as a downloadable xlsx file format for the detailed location

## Challenges we ran into
Initially, Extraction the data from the OpenStreetMap was a big task. Then the data for charging points were also not available directly, we have to do that manually. In the end, we faced some challenges in deploying our work on heroku.


## Accomplishments that we're proud of
Everything about this challenge was new to us. We are glad to have put up a decent solution.

## What we learned
We learned how to work with APIs and geospatial data. Coming from a non-computer background, deployment was a good lesson as well.

## What's next for Optimization of Vehicle Charging Stations
This work can be replicated for several ways/streets provided in the OpenStreetMap data.
This can help further in improving functionality for better suggestions.
