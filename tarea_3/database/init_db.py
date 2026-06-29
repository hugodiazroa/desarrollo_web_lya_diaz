from db import engine
from sqlalchemy import text
import os

def execute_sql_file(file_path):
    """Execute SQL commands from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        sql_content = file.read()
    
    # Split by semicolon and execute each statement
    statements = sql_content.split(';')
    with engine.connect() as connection:
        for statement in statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                try:
                    connection.execute(text(statement))
                    connection.commit()
                except Exception as e:
                    print(f"Error executing statement: {statement[:50]}... Error: {e}")
                    # Continue with next statement

if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Execute SQL files in order
    sql_files = [
        os.path.join(script_dir, 'tarea3.sql'),
        os.path.join(script_dir, 'region-comuna.sql'),
        os.path.join(script_dir, 'miembros-actividades.sql')
    ]
    
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            print(f"Executing {os.path.basename(sql_file)}...")
            execute_sql_file(sql_file)
            print(f"Finished executing {os.path.basename(sql_file)}")
        else:
            print(f"SQL file not found: {sql_file}")
    
    print("¡Base de datos inicializada y datos cargados!")