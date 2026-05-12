instructions to run the application:

in the terminal, navigate to /tarea_2/ (this folder) and run:
```bash
pip install -r requirements.txt
```

sudo mysql -u root


CREATE DATABASE IF NOT EXISTS tarea2;
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;
EXIT;


sudo mysql -u cc5002 -pprogramacionweb -h localhost -P 3306 tarea2 < /path/to/tarea2.sql


sudo mysql -u cc5002 -pprogramacionweb -h localhost -P 3306 tarea2 < region-comuna.sql

python init_db.py

then run the application with:
```bash
python app.py
```

to see the application, open http://127.0.0.1:5000
