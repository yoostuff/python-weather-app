#Managing Python Packages
--------
A really simple and straight forward Python script that provieds Real-Time Weather Updates using Open Weather Map Services. Register for an API Key here: https://openweathermap.org/api. Requires the following python libraries to be installed, flask==3.0.3 and requests==2.32.3 

1.) Create Python Environments
python -m venv .venv

On Windows run:
.venv\Scripts\activate

On MacOs run:
source .venv\Scripts\activate

2.) Install Python Packages
python -m pip install flask
#
python -m pip install requests

3.) Backup your modules or python libraries:
python -m pip freeze > requirements.txt

4.) List your libraries or modules:
python -m pip list or 
cat requirements.txt (depending on terminal and os in use)

