from tkinter import *
from tkinter import messagebox
from Game_Logic import GLogic


#Refactoring code to
# fit  UI requiements  

class SoS_GUI: 
    def __init__(self):
        self.root =Tk()
        self.root.title("Ready...")
        #getting rid of the boring default color 
        self.root.configure(bg='black') 
       
        self.game_choice = StringVar(value="Simple")
        self.r_letter_choice = StringVar(value="S")
        self.b_letter_choice = StringVar(value="S")
        self.create()
        
        self.sos_logic= GLogic()
        self.turn_label = None
    
    def mainloop(self):
        self.root.mainloop() 
    
    def display_board(self, gsize):
        for widget in self.root.winfo_children():
            if isinstance(widget, Frame):
             widget.destroy()
        # need to make sure that the grid aligned 
        # within the given area
        self.grid_frame = Frame(self.root,bg='black')
        self.grid_frame.grid(row=5,column=0,columnspan=3,rowspan=4,pady=10)
        for i in range(gsize):
            for j in range(gsize):
                cell = Button(self.grid_frame, text=" ", width=4, height=2, relief="solid",
                              command=lambda row=i,col=j:self.move_letter(row,col))
                cell.grid(row=i, column=j, padx=2, pady=2)
    def move_letter(self,row,col): 
        if self.sos_logic.turn =='Red':
            letter_choice= self.r_letter_choice.get()
        else:
            letter_choice=self.b_letter_choice.get()
            
        self.sos_logic.players[self.sos_logic.turn]=letter_choice
        
        if self.sos_logic.letter_placement(row,col,letter_choice):
            self.update_b()
            self.update_turn()
        else:
            messagebox.showerror("Error, invalid move, cell is ocupied")    
            
    def update_b(self): 
        for i in range(len(self.sos_logic.grid)):
            for j in range(len(self.sos_logic.grid[i])):
                self.grid_frame.grid_slaves(row=i,column=j)[0].config(text=self.sos_logic.grid[i][j])
    def update_turn(self):
        if not self.turn_label:
            self.turn_label = Label(self.root, text=f"{self.sos_logic.turn}'s Turn", bg='black', fg='white', font=("Times New Roman", 14))
            self.turn_label.grid(row=15, column=1, pady=5)
        else:
            self.turn_label.config(text=f"{self.sos_logic.turn}'s Turn")
   
    def create(self):
        
        # title for the game 
        self.game_title =Label(self.root, text="SOS Game!",font=("Times New Roman",20,"bold"),bg='black', fg='white')
        self.game_title.grid(row=0,column=0,columnspan=3, pady=10)
        
        #grid size   
        self.gsize_lable = Label(self.root, text="Grid Size:", bg='black', fg='white')
        self.gsize_lable.grid(row=3,column=1, pady=5)

        self.gsize_input = Entry(self.root, bg='black', fg='white',width=10) 
        self.gsize_input.grid(row=4,column=1,pady=5)
        
        
        
        #game mode choice 
        self.Simple =Radiobutton(self.root,text='Simple Game',variable=self.game_choice,value="Simple", bg='black', fg='white', selectcolor='black')
        self.Simple.grid(row=1,column=0,pady=5)
        
        self.General=Radiobutton(self.root,text='General Game',variable=self.game_choice,value="General", bg='black', fg='white', selectcolor='black')
        self.General.grid(row=1,column=2,pady=5,)
        
        #choice of Letter for Red player
        self.r_label=Label(self.root,text="Red Player",bg='black', fg='white')
        self.r_label.grid(row=10,column=0,pady=5,sticky='e')                        
         
        self.rS =Radiobutton(self.root,text='S', variable=self.r_letter_choice,value="S",bg='black', fg='white',selectcolor='black')
        self.rS.grid(row=11,column=0,pady=10,sticky='e')
        
        self.rO =Radiobutton(self.root,text='O',variable=self.r_letter_choice,value="O",bg='black', fg='white',selectcolor='black')
        self.rO.grid(row=12,column=0, pady=10,sticky='e')
        
        #choice of Letter for Blue player
        self.b_label=Label(self.root,text="Blue Player",bg='black', fg='white')
        self.b_label.grid(row=10,column=2,pady=5,sticky='w')   
        
        self.bS =Radiobutton(self.root,text='S', variable=self.b_letter_choice,value="S",bg='black', fg='white',selectcolor='black')
        self.bS.grid(row=11,column=2, pady=10, sticky='w')
        
        self.bO =Radiobutton(self.root,text='O', variable=self.b_letter_choice,value="O",bg='black', fg='white',selectcolor='black')
        self.bO.grid(row=12,column=2, pady=10,sticky='w')
        
        #start button 
        self.start = Button(self.root,text="Start Game!", bg='black', fg='white', command=self.starting) 
        self.start.grid(row=14,column=1,pady=5)
        
    def starting(self): 
        g_size = self.gsize_input.get()
        print(f"Grid Size entered: {g_size}")
        num=self.sos_logic.g_verify(g_size)
        
        if isinstance(num,str): 
            messagebox.showerror("Error",num)
        else:
            print(f"Grid Size entered: {g_size}")
            self.sos_logic.players['Red']=self.r_letter_choice.get()
            self.sos_logic.players['Blue']=self.b_letter_choice.get()
            self.sos_logic.mode=self.game_choice.get()
            self.display_board(num)
    
if __name__ == "__main__":
    gui = SoS_GUI()
    gui.mainloop()
        