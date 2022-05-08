# Works Single View Backend Challenge
```NOTE:``` 
- Backend project implemented in **Python and Django Rest Framework**
- The ```.env``` file was pushed to this repository on purpose.
- The answers to the questions asked for this backend challenge are provided at the end of this README document.

## STEPS TO RUN THIS PROJECT ON YOUR MACHINE
```NOTE:``` You need to have docker installed locally to complete the steps below.
- Clone the project to your local machine by opening your terminal and type:
```python
git clone https://github.com/dev-jochland/music-task.git
``` 
- ```OPTIONAL``` If you are on a MacOS or Ubuntu and your docker was not running before cloning the project, type the 
  following command in that same terminal and provide your admin password to grant permission to run the project:
```python
sudo chmod 666 /var/run/docker.sock
```

- While still in your terminal where you originally cloned the project, navigate into the cloned project folder by 
  typing the following:
```python
cd music-task/
```

- Next run the following command after navigating into the project as described above:
```python
docker-compose up
```
```NOTE```: The command above would take time to complete as it would try to build the docker image, so ensure you have 
a fast internet, also, you may have a "timeout error" or "HTTPconnection" error, this is as a result of your internet. 
Be patient as it would eventually build.

- Once the build is completed and successful, you would see the message below on your terminal: Ensure port ```3030``` 
  is available on your local machine, to avoid port collision.
```python
web_1  | System check identified no issues (0 silenced).
web_1  | May 08, 2022 - 17:00:50
web_1  | Django version 4.0.4, using settings 'music_meta.settings.dev'
web_1  | Starting development server at http://0.0.0.0:3030/
web_1  | Quit the server with CONTROL-C.
```

- Press ```ctrl + c``` on your keyboard to stop the server. Note that this command is OS dependent, so be sure to read 
  the displayed terminal message above for your specific terminal and follow the displayed command to quit the server.

- Next step is to run the script to migrate the migration files, so run the command below in your terminal
```python
docker-compose run --rm web python manage.py migrate
```

- Then run the command below to create superuser, this command would allow you to access the admin dashboard of the app. 
  Fill in the required fields and try to remember your credentials
```python
docker-compose run --rm web python manage.py createsuperuser
```
- To load the ```works-metadata.csv``` file, run the command script below. If the script is successful, you should get 
  the following message printed to the terminal: **Music data loaded successfully**
```python
docker-compose run --rm web python manage.py load_works_metadata
```
- To confirm that the data from the csv loaded correctly, you need to start the server again by typing the command below:
```python
docker-compose up
```
- Then go to the admin dashboard [here](http://0.0.0.0:3030/admin) or http://0.0.0.0:3030/admin and sign in with the 
  credentials you created when you were creating the superuser above.
- After you have successfully logged in, you should navigate to the ```musics``` table and click into it to see the csv 
  data loaded successfully. You should see 4 rows of music metadata.

## RUNNING THE TEST
- Press ```ctrl + c``` on your keyboard to stop the server. Note this command is OS dependent, so be sure to read the 
  displayed terminal message when you started the server and follow the displayed command to quit the server.
- To run the test script, type the command below while still in the music-task folder terminal
```python
docker-compose run --rm web python manage.py test
```
- You should see the image below after the test script runs
  
```python
Found 11 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 0.077s

OK
Destroying test database for alias 'default'...
```

## Testing on Postman
```NOTE``` You need to have Postman installed locally to try out this next step.
- Now start the server again by typing the command below:
```python
docker-compose up
```
- To try out the available endpoint, you can access the [postman](https://documenter.getpostman.com/view/11396719/UyxdLpVd) 
  documentation [here](https://documenter.getpostman.com/view/11396719/UyxdLpVd).
=======================================================================================

## ANSWERS TO QUESTIONS ASKED FOR THIS BACKEND CHALLENGE
**PART ONE** <br>
```Question 1```Describe brieﬂy the matching and reconciling method chosen.
- ```Answer```  I wrote a method called **clean_csv_data** that takes the **works_metadata.csv** file as an argument. 
  The **works_metadata.csv** is passed into another method called **read_csv_file**, this method read in the provided 
  csv file and process it into a list of dictionaries, with each dictionary element representing a row of data from the 
  csv file. I have a **unique_dict** variable which initially points to an empty dictionary to help me store the cleaned 
  data I would be processing. So I iterate over the earlier list of dictionaries and save the **music title**
  as a key in the **unique_dict** dictionary, provided that's the first time the **music title** is being saved as a 
  key in the **unique_dict** dictionary, I get to also save the corresponding entire row as a value of type ```dict``` 
  to this first time **music title** key. Now if the **music title** already exists in the **unique_dict** dictionary, 
  I get the **music contributors** from the current iteration and split by ```|``` and save it to a variable. I also get 
  the **music contributors** from the existing **music title** in the **unique_dict** dictionary and split by ```|``` 
  while saving the resultant split action into another variable. I repeat the same action for the **music iswc**, 
  except that I split with an empty space for the **music iswc**, and save the result from both **music iswc** split 
  action into two different variables. I now make a unique union of the both **music contributors** variable into a new 
  variable holding the new combined unique **music contributors** data. I repeat same for the **music iswc** and save 
  it into a new variable too, holding the unique combined **music iswc** data. I now update the dictionary value for the 
  already existing **music title** key in the **unique_dict** with the new unique **music contributors** and **music 
  iswc** data. This way no data is lost and existing data keeps getting updated with the new data till the end of the 
  iteration.
  
```Question 2```We constantly receive metadata from our providers, how would
you automatize the process?
- ```Answer``` I would provide an endpoint for metadata uploads and use pandas python package toolkit to perform the 
  necessary data manipulation.<br>

**PART TWO** <br>
```Question 1```Imagine that the Single View has 20 million musical works, do
you think your solution would have a similar response time?
- ```Answer```  No

```Question 2```If not, what would you do to improve it?
- ```Answer```  I would integrate ElasticSearch to index the musical works. This would greatly improve the search 
  response time and  enrich the user experience on the platform.
