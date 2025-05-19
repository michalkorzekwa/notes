Prosta aplikacja do zarządzania notatkami


### Backend

cd backend
python -m venv venv
source venv/bin/activate  
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

### Frontend

cd frontend
npm install
npm run serve