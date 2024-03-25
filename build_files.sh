echo "BUILD START"
python -m venv venv
venv\Scripts\activate 
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
echo "BUILD END"