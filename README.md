<div align="center">
  <h2>Personalized News Aggregator</h2>
</div>


## Technical Requirements
 * **Backend**
●​ Framework: Python 3.12, Django, Django REST Framework​
●​ Database: PostgreSQL​
●​ Scheduler: Celery
●​ News API: Integrated with NewsAPI.org free plan 

 * **​Frontend**
●​ Framework: Vue 3​
●​ Styling: Tailwind CSS
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

### Project Structure