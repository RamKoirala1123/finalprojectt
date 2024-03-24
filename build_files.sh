echo "BUILD START"
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
echo "BUILD END"