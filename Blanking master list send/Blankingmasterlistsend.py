import pypyodbc
import struct
import snap7
from time import sleep
#DB settings
DB_Number = 998
rubric_id = 1 # 1 - blanking, 2 - transfer, 3 - minitandem, 5 - big tandem
START_ADDRESS = 0
IP1 = '10.18.22.66' #Servo
IP2 = '192.168.3.101' #Blanking
IP3 = '192.168.99.55' #Progressive

SIZE = 15982
RACK = 0
SLOT = 2
y = 1
#SQL settings
conn = pypyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                             'Database=press_data_control;'
                             'uid=press_spvz; '
                             'pwd=admin100;')
while 1:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dbo.bboard_masters")
    result = cursor.fetchall()
    cardholderName = []
    cardNumber = []
    accessLevel = []
    i = 0
    for row in result:
        if row[5] == rubric_id or row[5] == 6:
            cardholderName.append(row[1])
            cardNumber.append(row[2])
            accessLevel.append(row[3])
            i = i + 1
    if y == 1:
        IP = IP1
        plc = snap7.client.Client()
        plc.connect(IP, RACK, SLOT)
        y = 2
    elif y == 2:
        IP = IP2
        plc = snap7.client.Client()
        plc.connect(IP, RACK, SLOT)
        y = 3
    elif y == 3:
        IP = IP3
        plc = snap7.client.Client()
        plc.connect(IP, RACK, SLOT)
        y = 1
    if plc.get_connected() == False:
        plc = snap7.client.Client()
        plc.connect(IP, RACK, SLOT)
        print('not connected')
        time.sleep(1)
    else:
        z = 0
        k = 0
        while i != 0:
            a = 0 + k
            b = 260 + k
            c = 6 + k
            if k < 15980:
                cardNumbertodb = struct.pack('>l', cardNumber[z])
                plc.db_write(DB_Number, a, cardNumbertodb)
                accessLeveltodb = struct.pack('<h', accessLevel[z])
                plc.db_write(DB_Number, b, accessLeveltodb)
                b = bytes(cardholderName[z], 'utf-8')
                cardholderNametodb = struct.pack('254s', b)
                plc.db_write(DB_Number, c, cardholderNametodb)
                k = k + 262
                i = i - 1
                z = z + 1
            else:
                break

    sleep(120)