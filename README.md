## Turfcoach challenge

### Prerequisites
  - docker
  - docker-compose


### How to set up and run
```shell
# Spin up the services
docker-compose up --build

# Create django-admin user
docker-compose run backendserver python manage.py createsuperuser

# You can access django admin dashboard at http://localhost:8000/admin
```

### How to retrieve and store weather forcasting data from external API
I used the API from https://www.weatherapi.com/ which is free, it still requires signing up in order
to be able to call APIs, after doing signup you can use your own API key. Put it in the docker-compose file
replace it with environment `WEATHER_API_KEY`

### Import weather forcasting data
This command would import the data of Berlin for the next 14 day (today included)   
`docker-compose run backendserver python manage.py update_weather_forecast Berlin 14`


### Import weather forcasting data of the past
This command will import the forcasting data of Berlin for the specified period, you can tune the dates as you wish,
so you can have all days in a row (future, which has been retrieved previously and also the data of the past accordingly)
`docker-compose run backendserver python manage.py update_weather_forecast_history Berlin 2024-01-18 2024-01-29`

### Then you can use admin dashboard in order to create new Pitch records
Note: To prevent issues, Please be careful to use the same characters as they exist in the table WeatherForecast


### Find the next maintenance day
This command will find the next maintenance day for the given pitch (with ID equals to 1)
`docker-compose run backendserver python manage.py find_next_maintenance_date 1`

### Updating current condition of a pitch
This command will update the current condition for the given pitch (with ID equals to 1)
(Note: The related pitch should have a valid value on field `last_maintenance_date` which is probably in the past)
`docker-compose run backendserver python manage.py update_current_condition 1`

### Finally to remove services (and related volumes)
`docker-compose down -v`

#### You can also visit API-docs on http://localhost:8000/swagger to explore the endpoints


### Regarding deploying application on the cloud and making sure that the system can scale
For production level deployment k8s and helm charts can be used. It can be used with the help of features of cloud providers
such as GCP or Azure (Google Kubernetes Engine (GKE) or Azure Kubernetes Service (AKS)) or just using cloud
cheaper cloud providers like Hetzener cloud.
Some other important steps about safe and scalable deployments that should be taken into account:
Set Up Load Balancing, Configure Horizontal Pod Autoscaler, Implement Monitoring, Logging
Optimize Resource Utilization of pods, developing robust CICD pipelines and also best practices for
IaC(infrastructure as code).