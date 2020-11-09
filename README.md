# UKS
Project repository for subject "Software Configuration Management" - 2019./2020.

Open command prompt in the root directory of the application:

<b>1. <i> Start application locally </b></i>
  - run: python manage.py runserver 
  
<b>2. <i> Deploy application on heroku server </i> </b>
  - run: heroku open
  
<b>3. <i> Deploy application using Docker </i></b>
  - build docker image from Dockerfile: docker build .
  - build docker-compose (using image from DockerHub): docker-compose build 
  - start application: docker-compose up
  - browser: http://localhost:5000
