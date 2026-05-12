instructions to run the application:

in the terminal, navigate to /tarea_2/ (this folder) and run:
```bash
python3 -m venv venv
source venv/bin/activate  # on Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

if you don't have a password for your root user, you can enter mysql with:
```bash
sudo mysql -u root
```
otherwise, use:
```bash
sudo mysql -u root -pPASSWORD
```

then, in the mysql prompt, run:
```sql
CREATE DATABASE IF NOT EXISTS tarea2;
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

to initialize the database and load the data, run the following commands in the terminal:
```bash
sudo mysql -u cc5002 -pprogramacionweb -h localhost -P 3306 tarea2 < database/tarea2.sql
sudo mysql -u cc5002 -pprogramacionweb -h localhost -P 3306 tarea2 < database/region-comuna.sql
sudo mysql -u cc5002 -pprogramacionweb -h localhost -P 3306 tarea2 < database/miembros-actividades.sql
```

# todo: hadle this initialization with python script, so we can run it with: python init_db.py

then run the application with:
```bash
python app.py
```

to see the application, open http://127.0.0.1:5000
