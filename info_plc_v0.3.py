import snap7
import struct
from SQLAIDA1600 import mysqlquery
from time import sleep

send_ReqVariable1 = 0
send_ReqVariable2 = 0
send_ReqVariable3 = 0
k = 0
DB_Number = 1000
START_ADDRESS = 0
SIZE = 546
IP = '10.18.20.133'
RACK = 0
SLOT = 2
plc = snap7.client.Client()
plc.connect(IP, RACK, SLOT)

while 1:

    if plc.get_connected() == False:
       #IP = '10.18.20.138'
       #RACK = 0
       #SLOT = 2
       plc = snap7.client.Client()
       plc.connect(IP, RACK, SLOT)
       print('not connected')
       time.sleep(1)

    else:
        #print('connected')
        #plc_info = plc.get_cpu_info()
        #print(f'Module Type: {plc_info.ModuleTypeName}')

        # state = plc.get_cpu_state()
        # print(f'State: {state}')

        db = plc.db_read(DB_Number, START_ADDRESS, SIZE)

        id = int.from_bytes(db[0:4], byteorder='big')
        #print(f'id: {id}')

        code = db[290:544].decode('UTF-8').strip('\x00')
        #print(f'code: {code}')

        namecardholder = db[6:260].decode('UTF-8').strip('\x00')
        #print(f'NameCardHolder: {namecardholder}')

        member = int.from_bytes(db[260:261], byteorder='big')
        #print(f'member: {member}')

        senssum = int.from_bytes(db[544:545], byteorder='big')
        #print(f'senssum: {senssum}')

        [Spm_set] = struct.unpack('>f', db[262:266])
        #print (f'Spm_set = {Spm_set}')

        [Spm_actual] = struct.unpack('>f', db[266:270])
        #print (f'Spm_actual = {Spm_actual}')

        [sAdj_set] = struct.unpack('>f', db[270:274])
        #print (f'sAdj_set = {sAdj_set}')

        [sAdj_actual] = struct.unpack('>f', db[274:278])
        #print (f'sAdj_actual = {sAdj_actual}')

        #sensor1state = bool(db[278])
        #print(f'sensor1state = {sensor1state}')

        [cpAdj_set] = struct.unpack('>f', db[280:284])
        #print (f'cpAdj_set = {cpAdj_set}')

        [cpAdj_actual] = struct.unpack('>f', db[284:288])
        #print (f'cpAdj_actual = {cpAdj_actual}')

        #plc.db_write(DB_Number, 288, b'1')

        # plc.disconnect()

        if (send_ReqVariable1 != member or send_ReqVariable2 != sAdj_set or send_ReqVariable3 != cpAdj_set) and member != 0:

            mysqlquery(code, id, namecardholder, sAdj_set, sAdj_actual, senssum, Spm_set, Spm_actual, cpAdj_set, cpAdj_actual)
            send_ReqVariable1 = member
            send_ReqVariable2 = sAdj_set
            send_ReqVariable3 = cpAdj_set
            #k = k + 1
            #print(k)
    sleep(3)