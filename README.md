<div align="center">
  <h2>Personalized News Aggregator</h2>
</div>

### Project Features:
* Implemented the project using django vite plugin to execute both frontend and backend within a single server.
* Frontend and backend within one server. So no need different server for frontend and backend.
* Register and securely log in.​
* Customize news settings: country, sources, and keywords (using user profile).
* Browse, search, and filter their news feed.
* Access original articles via source links.​
* Background scheduler integration using celery for periodic news updates.​
* Fetch the latest articles from NewsAPI.org based on all users’ preferences.​
* Store matching articles in the database linked to each user.
* Deliver a paginated news feed tailored to the authenticated user’s preferences.


## Technical Requirements
 * ***Backend***
 * ​ Framework: Python 3.12, Django, Django REST Framework​
 * ​ Database: PostgreSQL​ 
 * ​ Scheduler: Celery
 * ​ News API: Integrated with NewsAPI.org free plan 

 * ***​Frontend***
  * ​ Framework: Vue 3​
  * ​ Styling: Tailwind CSS
---

<div align="center">
  <h3>Setup guide.</h3>
</div>

## Getting Started

To start using Personalized News Aggregator:

1. **Clone the Repository**:
 ```shell
git clone git@github.com:rakibulislam8226/Personalized-news.git
  ```
* cd Personalized-news/

---
**Create virtual environment based on your operating system**
 * **For ubuntu**
 ```shell
python3.12 -m venv venv
  ```

  ###### Activate the virtual environment
 ```shell
source venv/bin/activate
  ```
 * **For windows**
 ```shell
python -m venv venv
  ```

---
**Copy .example.env file to .env:**

  * For linux
    ```shell
    cp .example.env .env
    ```
  * For windows
    ```shell
    copy .example.env .env
    ```
    ##### Fill the .env with proper data

---
### Install the requirements file.
```
pip install -r requirements.txt
```

  ###### Migrate the project
 ```shell
python manage.py migrate
  ```
  ###### If needed create superuser with proper data
  ```
  python manage.py createsuperuser
  ```
  ###### Run the python server
 ```shell
python manage.py runserver
  ```
---
### Install the requirements file for vue.js.
```
npm install
```
  ###### Run the frontend server
 ```shell
npm run dev
  ```
---
### To execute celery worker and beat for periodic news updates based on users
```
celery -A config worker --loglevel=info
```
```
celery -A config beat --loglevel=info
```
---
