import mariadb
import sys

err_codes = {
    'UAN_CLIENTS': 'Username not alfanumeric', 
    'PAN_CLIENTS': 'Password not alfanumeric',
    'EM_CONTACTS': 'Email missing or wrong',
    'PN_CONTACTS': 'Phone Number missing or wrong',
    'DF_GAMES': 'Wrong data format',
    'Incorrect date' : 'Not a valid date',
    'PID' : 'Publisher Unknown',
    'UC_USRNME' : 'Username already used',
    'UC_GAME_NAME' : 'Game already exists',
    'UC_PUBLISHER_NAME': 'Publisher already exists',
    'UQ_EMAIL': 'Email already used'
}

def connect():
    try:
        conn = mariadb.connect(
            user="user",
            password="user",
            host="localhost",
            database="TEMA_BD"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    
    return conn

def try_log(cur, username, passwrd, isADM):
    cur.execute(
        "SELECT CID FROM CLIENTS WHERE USRNME = ? AND PASSWRD = ? AND isADM = ?", 
        (username, passwrd, isADM)
    )

    result = cur.fetchone()

    if result is None:
        return False  
    else:
        return True
    
def get_games_details(cur, game_name):
    gme_tup = (game_name,)
    query = """SELECT PRICE, STOCK, RELEASE_DATE, GAME_DESCRIPTION 
    FROM GAMES 
    WHERE GAME_NAME = (?)"""
    cur.execute(
        query, (gme_tup)
    )

    result = cur.fetchone()
    price        = result[0]
    stock        = result[1]
    release_date = result[2]
    game_desc    = result[3]
    #print(result)
    #print(price, stock, release_date, game_desc )
    return price, stock, release_date, game_desc 

def get_publisher(cur, game_name):
    gme_tup = (game_name,)
    query = """SELECT PID 
    FROM GAMES 
    WHERE GAME_NAME = (?)"""
    cur.execute(
        query, (gme_tup)
    )

    temp = cur.fetchone()
    query = """SELECT PUBLISHER_NAME
    FROM PUBLISH 
    WHERE PID = (?)"""
    cur.execute(
        query, (temp)
    )

    result = cur.fetchall()
    print(result)
    return result[0][0]

def buy_item(cur, game_name, cid):
    stock = get_game_stock(cur, game_name)
    gid = get_gid(cur, game_name)
    if(int(stock) > 0):
        cur.execute(
            "START TRANSACTION"
        )    

        query = """UPDATE GAMES 
        SET STOCK = (?) 
        WHERE GAME_NAME = (?)"""
        cur.execute(
            query, (stock - 1, game_name)
        )

        query = """INSERT INTO 
        ORDERS(CID, GID)
        VALUES (?, ?)"""
        cur.execute(
            query, (cid, gid)
        )

        cur.execute(
            "COMMIT"
        )
        return True
    else:
        return False

def get_game_stock(cur, game_name):
    gme_tup = (game_name,)
    cur.execute(
        "SELECT STOCK FROM GAMES WHERE GAME_NAME = ?",
        (gme_tup)
    )
    data = cur.fetchall()
    #print(data)
    return data[0][0]

def get_cid(cur, username, passwrd):
    cur.execute(
        "SELECT CID FROM CLIENTS WHERE USRNME = ? AND PASSWRD = ?",
        (username, passwrd)
    )
    data = cur.fetchall()
    #print(data)
    return data[0][0]

def get_pid(cur, publisher):
    cur.execute(
        "SELECT PID FROM PUBLISH WHERE PUBLISHER_NAME = ?",
        ((publisher,))
    )
    data = cur.fetchone()
    print(data)
    if data is None:
        return -1  
    else:
        return data

def new_user(cur, username, email, pnumber, passwrd):
    try:
        cur.execute(
        "INSERT INTO CLIENTS (USRNME, PASSWRD) VALUES (?, ?)", 
        (username, passwrd)
        )

        cur.execute(
        "INSERT INTO CONTACT (CID, EMAIL, PNUMBER) VALUES (" +
        "(SELECT max(CID) FROM CLIENTS)" +
        ",?, ?)", 
        (email, pnumber)
        )

        return True, None
    except mariadb.Error as err:
        print(f"MySQL/MariaDB error: {err}")
        error_message = str(err)
        for code in err_codes.keys():
            if code in error_message[: len(error_message)//2]:
                return False, err_codes.get(code)
        
        return False, error_message

    
def new_game(cur, game_name, publisher, price, stock, release_date, game_desc):
    try:
        pid = get_pid(cur, publisher)
        if(pid != -1):
            print("aidci")
            cur.execute(
            """INSERT INTO GAMES (GAME_NAME, PRICE, STOCK, RELEASE_DATE, GAME_DESCRIPTION, PID) 
            VALUES (?,?,?,?,?,?)""", 
            (game_name, price, stock, release_date, game_desc, pid[0])
            )
        else:
            print("aici")

            cur.execute(
            "INSERT INTO PUBLISH (PUBLISHER_NAME) VALUES (?)", 
            ((publisher,))
            )

            cur.execute(
            """INSERT INTO GAMES (GAME_NAME, PRICE, STOCK, RELEASE_DATE, GAME_DESCRIPTION, PID) 
            VALUES (?,?,?,?,?,(SELECT max(PID) FROM PUBLISH))""", 
            ((game_name, price, stock, release_date, game_desc))
            )
       
        return True, None
    except mariadb.Error as err:
        print(f"MySQL/MariaDB error: {err}")
        error_message = str(err)
        for code in err_codes.keys():
            if code in error_message:
                return False, err_codes.get(code)
        
        return False, error_message
    
def get_games_name(cur):
    cur.execute(
        "SELECT GAME_NAME FROM GAMES"
    )
    data = cur.fetchall()
    data = [item for tpl in data for item in tpl]
    #print(data)
    return data

def get_gid(cur, game_name):
    cur.execute(
        "SELECT GID FROM GAMES WHERE GAME_NAME = ?",
        ((game_name,))
    )
    data = cur.fetchall()
    data = data[0][0]
    print(data)
    return data

def delete_game(cur, game_name):
    gid = get_gid(cur, game_name)
    cur.execute(
        """
        DELETE FROM ORDERS 
        WHERE GID = (?) 
        """,
        ((gid,))
    )

    cur.execute(
        """
        DELETE FROM GAMES WHERE GAME_NAME = ?
        """,
        ((game_name,))
    )

def get_games_data(cur):
    cur.execute(
        """SELECT GID, GAME_NAME, PRICE, STOCK, RELEASE_DATE, GAME_DESCRIPTION, PUBLISHER_NAME
           FROM GAMES JOIN PUBLISH ON GAMES.PID = PUBLISH.PID""",
    )
    data = cur.fetchall()
    print(data)
    return data

def update_games_data(cur, data):
    try:
        cur.execute(
        """ Update GAMES SET
        GAME_NAME = ?,
        PRICE = ?, 
        STOCK = ?, 
        RELEASE_DATE = ?,
        GAME_DESCRIPTION = ?, 
        PID = (SELECT PID FROM PUBLISH WHERE PUBLISHER_NAME = ?)
        WHERE GID = ? """,
        (data)
        )
        return True, None
    except mariadb.Error as err:
        print(f"MySQL/MariaDB error: {err}")
        error_message = str(err)
        for code in err_codes.keys():
            if code in error_message:
                return False, err_codes.get(code)
        
        return False, error_message