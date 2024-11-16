@Managing Python Packages

A really simple and straight forard Python script that provieds Real-Time Weather Updates using Open Weather Map Services. Register for an API Key here: https://openweathermap.org/api . Requires the following python libraries to be installed Flask==3.0.3 and requests==2.32.3 
--------
1.) Create Python Environments
python -m venv .venv
--------
--------
On Windows run:
.venv\Scripts\activate
--------
--------
On MacOs run:
source .venv\Scripts\activate
--------
--------
2.) Install Python Packages
python -m pip install flask
#
python -m pip install request

3.) Backup your modules:
python -m pip freeze > requirements.txt

4.) List your applications
python -m pip list or 
cat requirements.txt (depending on terminal and os in use)
--------

