############################################
#                                          #
#        TauraGameController 1.0.0        #
#        Author: Taura Bots                #
#        Date: 19/10/2015                  #
#                                          #
############################################

import socket, select, struct, time


# Dictionary that will contain the data from GameController
data = {"state":0, "version":0,"players":0,"state":0,"state":0,"firsthalf":0,"kickoff":0,"state2":0,"dropintime":0,"dropinteam":0,"time":0, "teamnumber0":0, "teamcolor0":0,"goalcolor0":0,"score0":0,
"t0p0penality":0 , "t0p0seconds":0,"t0p1penality":0 , "t0p1seconds":0,"t0p2penality":0 , "t0p2seconds":0,"t0p3penality":0 , "t0p3seconds":0,
"teamnumber1":0, "teamcolor1":0,"goalcolor1":0,"score1":0,
"t1p0penality":0 , "t1p0seconds":0,"t1p1penality":0 , "t1p1seconds":0,"t1p2penality":0 , "t1p2seconds":0,"t1p3penality":0 , "t1p3seconds":0}
# example of use: data_from_gamecontroller["time"] will return the time remaining

# socket listener
def socket_recieve():

    address=('',3838)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.bind(address)


    while True:
        result = select.select([s],[],[])
        msg = result[0][0].recv(5024)
        global data

        # Fills the dictionary
        # version
        data["version"] = struct.unpack("<I",msg[4:8])
        data["version"] = data["version"][0]
        # players
        data["players"] = struct.unpack("<B",msg[8:9])
        data["players"] = data["players"][0]
        # state
        data["state"] = struct.unpack("<B",msg[9:10])
        data["state"] = data["state"][0]
        # fristhalf => 1 if firsthalf 0 otherwise
        data["firsthalf"] = struct.unpack("<B",msg[10:11])
        data["firsthalf"] = data["firsthalf"][0]
        # kickoff
        data["kickoff"] = struct.unpack("<B",msg[11:12])
        data["kickoff"] = data["kickoff"][0]
        # state2
        data["state2"] = struct.unpack("<B",msg[12:13])
        data["state2"] = data["state2"][0]
        # dropinitem
        data["dropinteam"] = struct.unpack("<B",msg[13:14])
        data["dropinteam"] = data["dropinteam"][0]
        # dropintime
        data["dropintime"] = struct.unpack("<H",msg[14:16])
        data["dropintime"] = data["dropintime"][0]
        # time
        data["time"] = struct.unpack("<I",msg[16:20])
        data["time"] = data["time"][0]

        #team0 info
        data["teamnumber0"] = struct.unpack("<B", msg[20:21])
        data["teamnumber0"] = data["teamnumber0"][0]
        data["teamcolor0"] = struct.unpack("<B", msg[21:22])
        data["teamcolor0"] = data["teamcolor0"][0]
        data["goalcolor0"] = struct.unpack("<B", msg[22:23])
        data["goalcolor0"] = data["goalcolor0"][0]
        data["score0"] = struct.unpack("<B", msg[23:24])
        data["score0"] = data["score0"][0]
        #team0 player0 info
        data["t0p0penality"] = struct.unpack("<H", msg[24:26])
        data["t0p0penality"] = data["t0p0penality"][0]
        data["t0p0seconds"] = struct.unpack("<H", msg[26:28])
        data["t0p0seconds"] = data["t0p0seconds"][0]
        #team0 player1 info
        data["t0p1penality"] = struct.unpack("<H", msg[28:30])
        data["t0p1penality"] = data["t0p1penality"][0]
        data["t0p1seconds"] = struct.unpack("<H", msg[30:32])
        data["t0p1seconds"] = data["t0p1seconds"][0]
        #team0 player2 info
        data["t0p2penality"] = struct.unpack("<H", msg[32:34])
        data["t0p2penality"] = data["t0p2penality"][0]
        data["t0p2seconds"] = struct.unpack("<H", msg[34:36])
        data["t0p2seconds"] = data["t0p2seconds"][0]
        #team0 player3 info
        data["t0p3penality"] = struct.unpack("<H", msg[36:38])
        data["t0p3penality"] = data["t0p3penality"][0]
        data["t0p3seconds"] = struct.unpack("<H", msg[38:40])
        data["t0p3seconds"] = data["t0p3seconds"][0]
        #team1 info
        data["teamnumber1"] = struct.unpack("<B", msg[68:69])
        data["teamnumber1"] = data["teamnumber1"][0]
        data["teamcolor1"] = struct.unpack("<B", msg[69:70])
        data["teamcolor1"] = data["teamcolor1"][0]
        data["goalcolor1"] = struct.unpack("<B", msg[70:71])
        data["goalcolor1"] = data["goalcolor1"][0]
        data["score1"] = struct.unpack("<B", msg[71:72])
        data["score1"] = data["score1"][0]
        #team1 player0 info
        data["t1p0penality"] = struct.unpack("<H", msg[72:74])
        data["t1p0penality"] = data["t1p0penality"][0]
        data["t1p0seconds"] = struct.unpack("<H", msg[74:76])
        data["t1p0seconds"] = data["t1p0seconds"][0]
        #team1 player1 info
        data["t1p1penality"] = struct.unpack("<H", msg[76:78])
        data["t1p1penality"] = data["t1p1penality"][0]
        data["t1p1seconds"] = struct.unpack("<H", msg[78:80])
        data["t1p1seconds"] = data["t1p1seconds"][0]
        #team1 player2 info
        data["t1p2penality"] = struct.unpack("<H", msg[80:82])
        data["t1p2penality"] = data["t1p2penality"][0]
        data["t1p2seconds"] = struct.unpack("<H", msg[82:84])
        data["t1p2seconds"] = data["t1p2seconds"][0]
        #team1 player3 info
        data["t1p3penality"] = struct.unpack("<H", msg[84:86])
        data["t1p3penality"] = data["t1p3penality"][0]
        data["t1p3seconds"] = struct.unpack("<H", msg[86:88])
        data["t1p3seconds"] = data["t1p3seconds"][0]
        time.sleep(2/10)
