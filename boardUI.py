"""UI module for player1/2.py. Use for connection + board interaction/display."""
import tkinter as tk
import socket
from gameboard import BoardClass


#--------------------------------------------------------------------
# Socket functions
def tryConnection(hostTuple:tuple) -> bool:
    """Attempt to connect to server."""
    try:
        self.socket.connect(hostTuple)
        connection = True
    except:
        return connection
    return connection


def sendInfo(socket, info:str) -> None:
    """Send information.

    Parameters:
    socket (socket) = socket for info to be sent through.
    info (str): info to be sent.

    """
    info = bytes(info,encoding='utf8')
    socket.send(info)


def receiveInfo(socket) -> str:
    """Returns info received from other end of socket.

    Parameters:
    socket (socket) = socket for info to be sent through.

    """
    socketData = socket.recv(1024)
    return socketData.decode('ascii')


#--------------------------------------------------------------------
# GUI (Tkinter) Class...
# hi TA grading this, i got pretty lazy with annotations so hopefully this is enough :)
class BoardUIGrid():
    """UI for connection between boards.
    Handles display and interaction with BoardClass objects.
    """
    # Methods
#--------INITIALIZING WINDOW--------------------------------------------------------
    def __init__(self, player):
        """Initializes GUI
        Parameters:
        player (boolean) - True if P1, False if P2
        """
        # Create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = player
        # Create window
        self.windowStart()
        if player:
            self.connectFrame()
        else:
            self.hostFrame()
        

    def windowStart(self):
        """Initialize TK window and loop.
        root = main Tk widget, main window of application
        """
        # Set up root widget
        self.root = tk.Tk()
        self.root.title('Multiplayer Tic-Tac-Toe')
        self.root.geometry('400x400')
        self.root.configure(bg='green')
        self.root.resizable(0,0)
        self.root.grid()
        self.root.columnconfigure(2,weight=1)
        self.root.rowconfigure(2, weight=1)

#---CONNECTION FUNCTIONS--------------------------------------------------------------------------------------
    def __connect__(self):
        """Attempt to connect to server. Start game once connected."""
        #Try connecting to server, tell if connected
        connection = False
        try:
            hostTuple = (self.host.get(), int(self.port.get()))
            self.socket.connect(hostTuple)
            connection = True
        except:
            """Do nothing."""
    
        if connection: # If connected, say so and destroy connection frame
            self.cfrm.destroy()
            self.connected = tk.Label(self.root, text=f'Connected to ({self.host.get()}, {self.port.get()}).', width=30).grid(row=3,column=0,sticky='sw')
            #Start sending/receiving name process after connection
            self.nameFrame()
        else: # Ask for reinput if not connected
            self.host.set('Try again?')
            self.port.set('Must be a #.')
            self.connectionStatus.set('Reinput info.') 
            self.quitButton = tk.Button(self.cfrm, text='Or quit', command=self.root.destroy).grid(row=1,column=2)


    def connectFrame(self):
        """Initialize connection widget."""
        # Initialize TK variables
        self.host = tk.StringVar()
        self.host.set('Hostname')
        self.port = tk.StringVar()
        self.port.set('Port #')
        self.connectionStatus = tk.StringVar()
        self.connectionStatus.set('Connection in progress...')
        
        # Set up connection frame
        self.cfrm = tk.Frame(self.root, width=100, relief='raised',highlightbackground="grey",highlightthickness=2)
        self.cfrm.grid(row=2,rowspan=1,column=0,columnspan=2,sticky='sesw')

        # Widgets within frame
        self.hostEntry = tk.Entry(master=self.cfrm, textvariable=self.host).grid(row=0,column=0,padx=0,sticky='ew')
        self.portEntry = tk.Entry(master=self.cfrm, textvariable=self.port).grid(row=0,column=1,sticky='w')
        self.submit = tk.Button(self.cfrm, text='Connect', command=self.__connect__).grid(row=0,column=2)
        self.connectLabel = tk.Label(self.cfrm, textvariable=self.connectionStatus, width=30).grid(row=1,column=0,sticky='w',pady=0,ipady=0)


    def hostFrame(self):
        """Initialize host widget."""
        # Initialize TK variables
        self.host = tk.StringVar()
        self.host.set('Enter IP to host with.')
        self.port = tk.StringVar()
        self.port.set('Port #')

        # Set up hosting frame
        self.hfrm = tk.Frame(self.root, width=100, relief='raised',highlightbackground="grey",highlightthickness=2)
        self.hfrm.grid(row=2,rowspan=1,column=0,columnspan=2,sticky='sesw')

        # Widgets within frame
        self.hostEntry = tk.Entry(master=self.hfrm, textvariable=self.host).grid(row=0,column=0,padx=0,sticky='ew')
        self.portEntry = tk.Entry(self.hfrm, textvariable=self.port).grid(row=0,column=1,sticky='w')
        self.submit = tk.Button(self.hfrm, text='Host', command=self.__host__).grid(row=0,column=2)
    

    def __host__(self):
        """Host server and create client socket"""
        try:
            serverInfo = (self.host.get(), int(self.port.get()))
            self.hfrm.update()
            self.socket.bind(serverInfo)
            self.socket.listen(1)
        except:
            self.host.set('Error, try reinputing info.')
            self.port.set('Must be a #.')
        self.clientSock, self.clientAddress = self.socket.accept()
        self.hfrm.destroy()
        self.connected = tk.Label(self.root, text=f'Connected to {self.clientAddress}', width=30).grid(row=3,column=0,sticky='sw')
        #Start sending/receiving name process after connection
        self.nameFrame()


#---NAME/TURN FUNCTIONS--------------------------------------------------------------------------------------
    def sendName(self):
        """Function to send name for send button"""
        # Send name to client or host depending on who sends
        self.nframe.update()
        if self.player: # Client
            sendInfo(self.socket,self.name.get())
        else: # Host
            sendInfo(self.clientSock,self.name.get())
        # Destroy name frame and start board
        self.nframe.destroy()
        self.boardFrame()
        self.miscFrame()


    def nameFrame(self):
        """Initialize widget for name"""
        # Make name frame
        self.nframe = tk.Frame(self.root, width=200, height=200, relief='raised',highlightbackground="grey",highlightthickness=2)
        self.nframe.grid(row=2,rowspan=2,columnspan=2,sticky="ew")

        # Make input to send name with variable
        self.name = tk.StringVar()
        self.name.set('Enter name')
        self.nameBox = tk.Entry(self.nframe, textvariable=self.name).pack()
        self.sendButton = tk.Button(self.nframe,relief='raised',text='Send',command=self.sendName).pack()


    def miscFrame(self):
        """Initialize widget for turn, replay, and stat info."""
        # Make frame
        self.mframe = tk.Frame(self.root, width=200, height=200, relief='raised',highlightbackground="grey",highlightthickness=2)
        self.mframe.grid(row=1,column=2,sticky='ns')

        # TKinter variablesz
        self.turn = tk.StringVar()
        self.turnPlayer = tk.StringVar()
        self.turnPlayer.set('P1')
        if self.player:
            self.turn.set(self.board.name)
        else:
            self.turn.set(self.board.name2)

        #Make info labels
        self.turnLabel = tk.Label(self.mframe,width=120,text='Turn:').pack()
        self.turnInfo = tk.Label(self.mframe,textvariable=self.turn).pack()
        self.playerInfo = tk.Label(self.mframe,textvariable=self.turnPlayer).pack()

        # Make P2 wait for move response
        if not(self.player):
            try:
                self.receiveMove()
            except:
                pass

        
#---BOARD GUI FUNCTIONS--------------------------------------------------------------------------------------       
    def boardFrame(self):
        """Initialize widget for tic-tac-toe board"""
        # Receive name and make board object
        if self.player: # If client
            self.board = BoardClass(self.name.get(), receiveInfo(self.socket), True)
        else: # If host
            self.board = BoardClass(self.name.get(), receiveInfo(self.clientSock), False)           
        print(self.board.name)
        print(self.board.name2)
        
        # Make board frame
        self.bframe = tk.Frame(self.root, width=200, height=200, relief='raised',highlightbackground="grey",highlightthickness=2)
        self.bframe.grid(row=2,rowspan=2,column=0,columnspan=2)

        
        # Make buttons for board
        self.nw = tk.Button(self.bframe,relief='raised', text=' ', font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(0))
        self.n = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(1))
        self.ne = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(2))
        self.w = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(3))
        self.center = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(4))
        self.e = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(5))
        self.sw = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(6))
        self.s = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(7))
        self.se = tk.Button(self.bframe,relief='raised', text=' ',font=('Arial'), height=1, width=3,command=lambda:self.placeAndSend(8))
        
        self.nw.grid(row=0,column=0)
        self.n.grid(row=0,column=1)
        self.ne.grid(row=0,column=2)
        self.w.grid(row=1,column=0)
        self.center.grid(row=1,column=1)
        self.e.grid(row=1,column=2)
        self.sw.grid(row=2,column=0)
        self.s.grid(row=2,column=1)
        self.se.grid(row=2,column=2)

        
    def changeBoard(self, pos:int) -> None:
        """Change sign on board GUI"""
        if self.board.getTurn():
            if pos == 0:
                self.nw.configure(text='x')
            elif pos == 1:
                self.n.configure(text='x')
            elif pos == 2:
               self.ne.configure(text='x')
            elif pos == 3:
                self.w.configure(text='x')
            elif pos == 4:
                self.center.configure(text='x')
            elif pos == 5:
                self.e.configure(text='x')
            elif pos == 6:
                self.sw.configure(text='x')
            elif pos == 7:
                self.s.configure(text='x')
            elif pos == 8:
                self.se.configure(text='x')
        else:
            if pos == 0:
                self.nw.configure(text='o')
            elif pos == 1:
                self.n.configure(text='o')
            elif pos == 2:
               self.ne.configure(text='o')
            elif pos == 3:
                self.w.configure(text='o')
            elif pos == 4:
                self.center.configure(text='o')
            elif pos == 5:
                self.e.configure(text='o')
            elif pos == 6:
                self.sw.configure(text='o')
            elif pos == 7:
                self.s.configure(text='o')
            elif pos == 8:
                self.se.configure(text='o')


    def buttonToggle(self, boolean:bool) -> None:
        """Turn board buttons off or on"""
        if boolean:
            self.nw['state'] = tk.NORMAL
            self.n['state'] = tk.NORMAL
            self.ne['state'] = tk.NORMAL
            self.w['state'] = tk.NORMAL
            self.center['state'] = tk.NORMAL
            self.e['state'] = tk.NORMAL
            self.sw['state'] = tk.NORMAL
            self.s['state'] = tk.NORMAL
            self.se['state'] = tk.NORMAL
        else:
            self.nw['state'] = tk.DISABLED
            self.n['state'] = tk.DISABLED
            self.ne['state'] = tk.DISABLED
            self.w['state'] = tk.DISABLED
            self.center['state'] = tk.DISABLED
            self.e['state'] = tk.DISABLED
            self.sw['state'] = tk.DISABLED
            self.s['state'] = tk.DISABLED
            self.se['state'] = tk.DISABLED
        
    
    def buttonUpdate(self):
        """Update all buttons on board to prevent freezing"""
        self.nw.update()
        self.n.update()
        self.ne.update()
        self.w.update()
        self.center.update()
        self.e.update()
        self.sw.update()
        self.s.update()
        self.se.update()

        
    def boardClear(self):
        """Reset GUI"""
        self.nw.configure(text=' ')
        self.n.configure(text=' ')
        self.ne.configure(text=' ')
        self.w.configure(text=' ')
        self.center.configure(text=' ')
        self.e.configure(text=' ')
        self.sw.configure(text=' ')
        self.s.configure(text=' ')
        self.se.configure(text=' ')
        
        self.turnPlayer.set('P1')
        if self.player:
            self.turn.set(self.board.name)
        else:
            self.turn.set(self.board.name2)

        
    def placeAndSend(self, pos: int) -> None:
        """Place x or o on board and send move. Then recieve move after."""
        
        # If turn lines up with correct player
        if (self.board.getTurn() and self.player) or (not(self.board.getTurn()) and not(self.player)):
            # If board isn't full send info/update board + UI
            if self.board._board[pos] == '-':
                self.changeBoard(pos)
                self.board.updateGameBoard(pos)
                self.buttonUpdate()
                self.board.printBoard()
                #Sending move
                # If client
                if self.player:
                    sendInfo(self.socket, str(pos))
                else: # If host
                    sendInfo(self.clientSock, str(pos))
                self.flipTurnGUI()
                #End game/ go to next move
                if self.checkEndAndReset():
                    pass
                else: 
                    self.receiveMove()
                
                
    def receiveMove(self) -> None:
        """Recieve a board from the other player and place it."""
        #Disable buttons while waiting
        self.buttonToggle(False)
        
        if self.player:
            info = receiveInfo(self.socket)
        else: 
            info = receiveInfo(self.clientSock)
        info = int(info)
        self.changeBoard(info)
        self.board.updateGameBoard(info)
        self.board.printBoard()
        self.flipTurnGUI()

        #Reenable buttons after opponent makes turn if no win/tie.
        if self.checkEndAndReset():
            pass
        else:
            self.buttonToggle(True)


    def checkEndAndReset(self) -> bool:
        """Check for end of game + reset GUI. """
        # Check for end of game
        if self.board.boardIsFull() or self.board.isWinner():
            # Reset board object + update games
            self.board.updateGamesPlayed()
            self.board.resetGameBoard()

            #Ask to reset if P1
            if self.player:
                self.replayPrompt()
            else: 
                # Wait for P1 response
                self.root.update()
                response = receiveInfo(self.clientSock)
                if response == "Fun Times":
                    self.endGame()
                elif response == "Play Again":
                    self.continueGame()
            return True
        else:
            return False


    def flipTurnGUI(self) -> None:
        """Change turn in GUI"""
        if self.turnPlayer.get() == 'P1':
            self.turnPlayer.set('P2')
        else:
            self.turnPlayer.set('P1')

        if self.player:
            if self.turn.get() == self.board.name:
                self.turn.set(self.board.name2)
            else:
                self.turn.set(self.board.name)
        else:
            if self.turn.get() == self.board.name:
                self.turn.set(self.board.name2)
            else:
                self.turn.set(self.board.name)
        self.mframe.update()


    def replayPrompt(self):
        """Puts replay screen up and gets reponse"""
        self.buttonToggle(False)
        #Make replay frame
        self.rframe = tk.Frame(self.root, width=200, height=200, relief='raised',highlightbackground="grey",highlightthickness=2)
        self.rframe.grid(row=2,column=2,sticky='e')
        
        self.replayLabel = tk.Label(self.rframe,text='\nReplay?').pack()
        self.replayButton = tk.Button(self.rframe,text='Yes',command=self.continueGame).pack()
        self.endButton = tk.Button(self.rframe,text='No',command=self.endGame).pack()

        
    def endGame(self):
        """End game and print stats"""
        if self.player:
            self.rframe.destroy()
            sendInfo(self.socket, "Fun Times")
        
        # Print out stats
        stats = []
        stats = self.board.computeStats()
        self.statLabel = tk.Label(self.mframe,text=f"Player: {stats[0]}\nOpponent: {stats[1]}\nGames: {stats[2]}\nWins: {stats[3]}\nLosses: {stats[4]}\n Ties: {stats[5]}").pack()
        self.root.quit()


    def continueGame(self):
        """Continue game"""
        if self.player:
            self.rframe.destroy()
            sendInfo(self.socket, "Play Again")
        self.buttonToggle(True)   
        self.boardClear()
        if not(self.player):
            try:
                self.receiveMove()
            except:
                pass


if __name__ == '__main__':
    BoardUIGrid(True)
