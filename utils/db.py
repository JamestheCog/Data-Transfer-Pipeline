import turso.sync, random, string, time
from typing import Union
from etl import exceptions

def check_health(conn_url: str, conn_key: str) -> None:
    '''
    Given a connection URL and a connection string, try to connect to it and pull and insert data.  
    This function will raise if something goes awry; it ain't returning shit otherwise.  
    '''
    MAX_ATTMPTS, DELETE_DELAY = 5, 2
    try:
        db = turso.sync.connect(conn_url, conn_key) 
        table_cursor = db.execute("SELECT name FROM sqlite_schema WHERE type='table';")
        tables = table_cursor.fetchall()

        for _ in range(random.randint(MAX_ATTMPTS)):
            insert_table = random.choice(tables)
            insert_table_cols = [{'name': i[1], 'type': i[2]} for i in db.execute(f'PRAGMA table_info({insert_table});')]
            spoofed_data = _spoof_data(insert_table_cols)

            db.execute(f"INSERT INTO {insert_table} VALUES ({', '.join(['?'] * len(spoofed_data))});", spoofed_data.values())
            time.sleep(DELETE_DELAY * random.random())
            db.execute(f"DELETE FROM {insert_table} WHERE patient_id = ?;", spoofed_data.get('patient_id'))
            db.execute(F"SELECT * FROM {insert_table} LIMIT ?;", random.randint(1, MAX_ATTMPTS))
            db.commit()
        db.close()
    except Exception as e:
        raise exceptions.LoadException(message = f"Dee Bee is unwell.  It says: '{str(e)}'")


# --- PRIVATE FUNCTIONS ---

def _spoof_data(col_info: list[dict[str, str]]) -> dict[str, Union[str, int, float]]:
    '''
    Given the list object `insert_table_cols` in check_db, spoon data according 
    to the column type (either a string or a numeric value of sorts):
    '''
    MAX_SAMPLE_SIZE, BASE_RANDOM = 10, 1e3
    to_return = {}

    for col in col_info:
        col_key, col_type = col.get('name'), col.get('type', '').lower()
        val = None
        match col_type:
            case 'text' | 'string':
                val = ''.join(random.sample(string.ascii_letters))
            case 'integer':
                val = random.randint(1, MAX_SAMPLE_SIZE)
            case 'real':
                val = BASE_RANDOM + (random.random() * BASE_RANDOM)
        to_return[col_key] = val
    return to_return