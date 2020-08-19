# Attendence Management System

This is python project to manage attendence for any orgainization.  
Backend of Project is available here, Frontend will be developed in future.  

# Features

1)Admin can add subject, students, professor, subjects and various departments.  
2)professor can take attendence of the students of his/her subjects.  
3)Attendece can be viewed in different sorted forms like professor wise, subject wise, class wise, department wise etc.

# Technologies

1)python3  
2)Django Rest Framework  
3)MySql database  

## Installation

This application is containerized using Docker.
if you have docker-compose installed on your machine. below command will start project on your machine by hadling all the dependencies.  
Run this command in root directory of project.

```bash
docker-compose up
```
if you don't have docker-compose installed on your machine. then you can start project with below process
1)install python3 dependencies using requirements.txt  

```bash
pip3 install -r requirements.txt
```
2)install mysql database on your machine and provide username and password of your database in settings.py file of project  
 
 ```bash
 DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'databaseName',
        'USER': 'databaseUserName',
        'PASSWORD': 'databasePassword',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.  
dilipjoshis98@gmail.com  
8975427620  

## License
[MIT](https://choosealicense.com/licenses/mit/)





