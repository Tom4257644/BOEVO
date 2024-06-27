# below is importing everything i need and will need for future versions (the webscraping which i am not doing here)
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
from tkinter import *

# defining variables, they will all be redefined later but this passes the undefined variable error
game_entry = 'None'
team_a_entry = 'None'
team_b_entry = 'None'
game_id_entry = 'None'
odds_dk_a_entry = 'None'
odds_dk_b_entry = 'None'
odds_tab_a_entry = 'None'
odds_tab_b_entry = 'None'
arb_entry = 'None'
a_value_1_entry = 'None'
a_value_2_entry = 'None'
unchecked_games = []
games = []
number_of_games = 5
error_unfilled_fields = ''
success_message_label = ''
excel_success_message_label = ''

# games class and related functions
class Games:
    """this is a class for games.  """

# initialize Games object
    def __init__(self, game, team_a, team_b, game_id, team_A_odds_draftkings, team_B_odds_draftkings, team_A_odds_tab, team_B_odds_tab, arb, a_value_1, a_value_2):
        self._game = game
        self._team_a = team_a
        self._team_b = team_b
        self._game_id = game_id
        self._team_A_odds_draftkings = team_A_odds_draftkings
        self._team_B_odds_draftkings = team_B_odds_draftkings
        self._team_A_odds_tab = team_A_odds_tab
        self._team_B_odds_tab = team_B_odds_tab
        self._arb = arb
        self._a_value_1 = a_value_1
        self._a_value_2 = a_value_2
        games.append(self)

    # function that changes the value of part of the Games object
    def is_it_an_arb(self, arb):
        self._arb = arb
        
    # function that chnages the value of part of the games object
    def change_A_values(self, a_value_1, a_value_2):
        self._a_value_1 = a_value_1
        self._a_value_2 = a_value_2

    # prints the games information into the termanal, for testing purposes 
    def display_games_info(self):
        print("="*20)
        print(f"game: {self._game}")
        print(f"team_a: {self._team_a}")
        print(f"team_b: {self._team_b}")
        print(f"game_id: {self._game_id}")
        print(f"team A Odds draftkings: {self._team_A_odds_draftkings}")
        print(f"team B Odds draftkings: {self._team_B_odds_draftkings}")
        print(f"team A Odds tab: {self._team_A_odds_tab}")
        print(f"team B Odds tab: {self._team_B_odds_tab}")
        print(f"Checked: {self._arb}")
        if self._arb != 'no' and self._arb != 'unchecked':
            print(f"Working A Value 1: {self._a_value_1}")
            print(f"Working A Value 2: {self._a_value_2}")
        print("="*20)

    # all of the below are requests to the Game to return a part of its object
    def get_game(self):
        return self._game
    
    def get_team_a(self):
        return self._team_a
    
    def get_team_b(self):
        return self._team_b
    
    def get_game_id(self):
        return self._game_id
    
    def get_team_A_odds_draftkings(self):
        return self._team_A_odds_draftkings
    
    def get_team_B_odds_draftkings(self):
        return self._team_B_odds_draftkings
    
    def get_team_A_odds_tab(self):
        return self._team_A_odds_tab
    
    def get_team_B_odds_tab(self):
        return self._team_B_odds_tab
    
    def get_arb(self):
        return self._arb
    
    def a_value_1(self):
        return self._a_value_1
    
    def a_value_2(self):
        return self._a_value_2
    
    # function for deleting games, looks though all the games for ones that match the gamid it was given and removes any it finds, before reloading the page
    def delete_game(game_id):
        for game in games:
            if game._game_id == game_id:
                games.remove(game)
                switch_page(all_games_info_page)

    # creates a list of unchecked Game objects
    def add_list_unchecked(self):
        self.get_arb()
        if self._arb == 'unchecked':
            unchecked_games.append(self)
    
    # checks Game objects for objects - probably best to read information on explaination pages if you want to understand this function
    def check_unchecked_games(self): 
        team_A_odds_draftkings = self._team_A_odds_draftkings
        team_B_odds_draftkings = self._team_B_odds_draftkings
        team_A_odds_tab = self._team_A_odds_tab
        team_B_odds_tab = self._team_B_odds_tab
        moneyline = team_A_odds_draftkings
        team_A_odds_draftkings = moneyline_to_decimal(moneyline)
        moneyline = team_B_odds_draftkings
        team_B_odds_draftkings = moneyline_to_decimal(moneyline)
        moneyline = team_A_odds_tab
        team_A_odds_tab = moneyline_to_decimal(moneyline)
        moneyline = team_B_odds_tab
        team_B_odds_tab = moneyline_to_decimal(moneyline)
        # game = self._game
        # game_id = self._game_id
        option_1_status = 'NO'
        option_2_status = 'NO'

        # "OPTION 1"
        dkta = team_A_odds_draftkings
        # "draft kings team A odds to win, taken from the OO from a game in the games class"
        tabtb = team_B_odds_tab 
        # "TAB team B odds to win, taken from the OO from a game in the games class"

        A_values_that_work_for_option_1 = []
        a = 0.01
        b = 0.99

        for x in range (1,100,1):
            
            payout_a = (a * dkta) 
            payout_b = (b * tabtb)

            if (payout_b - 1) > 0 and (payout_a - 1) > 0:
                A_values_that_work_for_option_1.append(round(a,3))
                option_1_status = 'YES'

            a +=0.01
            b -=0.01

        # "for option 1 dk is team A"


        # "OPTION 2"
        dktb = team_B_odds_draftkings
        # "draft kings team B odds to win, taken from the OO from a game in the games class"
        tabta = team_A_odds_tab 
        # "TAB team A odds to win, taken from the OO from a game in the games class"

        A_values_that_work_for_option_2 = []
        a = 0.01
        b = 0.99

        for x in range (1,100,1):
            
            payout_a = (a * tabta) 
            payout_b = (b * dktb)

            if (payout_b - 1) > 0 and (payout_a - 1) > 0:
                A_values_that_work_for_option_2.append(round(a,3))
                option_2_status = 'YES'

            a+=0.01
            b-=0.01


        # "FOR OPTION 2 TAB IS TEAM A "
    
        if option_1_status == 'YES':
            self.is_it_an_arb('yes') 
            self.change_A_values(A_values_that_work_for_option_1[0],A_values_that_work_for_option_1[-1])

        if option_2_status == 'YES':
            self.is_it_an_arb('yes') 
            self.change_A_values(A_values_that_work_for_option_2[0],A_values_that_work_for_option_2[-1])

        if option_2_status == 'NO' and option_1_status == 'NO':
            self.is_it_an_arb('no')

"=============================================================================================="

"WEBSCRAPING WILL GO HERE IN VERSON 2 (NOT FOR NCEA) AND SHOULD ORGANISE THE DATA INTO THE BELOW FORMAT"

"=============================================================================================="

# some starting code for testing purposes 
game_1 = Games("cardinals vs rays","cardinals","rays",101,+120,-100,+100,-120,"unchecked", "none", "none")
game_2 = Games("rangers vs astros","rangers","astros",102,+200,-150,+280,+100,"unchecked", "none", "none")
game_3 = Games("athletics vs red sox","athletics","red sox",103,+250,-100,+210,+150,"unchecked", "none", "none")
game_4 = Games("cubs vs mariners","cubs","mariners",104,+230,-120,+150,-100,"unchecked", "none", "none")
game_5 = Games("france vs switzerland","france","switzerland",105,-200,600,-183,450,"unchecked", "none", "none")

# this converts odds from moneyline to decimal
def moneyline_to_decimal(moneyline_odds):
    if moneyline_odds >= 0:
        decimal_odds = (moneyline_odds / 100) + 1
    else:
        decimal_odds = (100 / -moneyline_odds) + 1
    return decimal_odds

# this function checks the games for arbs and calls another that prints them in the tkinter gui
def checkgames():
    global unchecked_games
    unchecked_games = []
    for game_instance in games:
        game_instance.add_list_unchecked()
        game_instance.check_unchecked_games()
        print_checked_games()

# this function prints unchecked games in the tkinter interface
def show_unchecked_games():
    global unchecked_games
    unchecked_games = []
    for game_instance in games:
        game_instance.add_list_unchecked()
        print_checked_games()

# this function submits games entered into a form as objects in the games class.
def submit_game(): 
    # globalises variables so they work within the function
    global number_of_games
    global game_entry
    global team_a_entry
    global team_b_entry
    global odds_dk_a_entry
    global odds_dk_b_entry
    global odds_tab_a_entry
    global odds_tab_b_entry
    global error_unfilled_fields

    if game_entry_variable.get() == '' or team_a_entry_variable.get() == '' or team_b_entry_variable.get() == '' or odds_dk_a_entry_variable.get() == '' or odds_dk_b_entry_variable.get() == '' or odds_tab_a_entry_variable.get() == '' or odds_tab_b_entry_variable.get() == '':
        error_unfilled_fields = "Sorry, Please fill in all the fields."

    elif (not odds_dk_a_entry_variable.get().isdigit() or not odds_dk_b_entry_variable.get().isdigit() or not odds_tab_a_entry_variable.get().isdigit() or not odds_tab_b_entry_variable.get().isdigit()):
        error_unfilled_fields = "Odds must be integers."
        
    else:
        number_of_games += 1
        # gets form inputs and asigns them to variables
        game_name = game_entry_variable.get()
        team_a = team_a_entry_variable.get()
        team_b = team_b_entry_variable.get()
        game_id = number_of_games
        odds_dk_a = float(odds_dk_a_entry_variable.get())
        odds_dk_b = float(odds_dk_b_entry_variable.get())
        odds_tab_a = float(odds_tab_a_entry_variable.get())
        odds_tab_b = float(odds_tab_b_entry_variable.get())
        arb = 'unchecked'
        a_value_1 = ''
        a_value_2 = ''
        # creates new objects in the games class
        Games(game_name, team_a, team_b, game_id, odds_dk_a, odds_dk_b, odds_tab_a, odds_tab_b, arb, a_value_1, a_value_2)
        # print in terminal for testing
        print("Game Added") 
        # setting a variable which will go into a label which will allow users to see that a game has been successfully added
        global success_message_label
        success_message_label = "Game Added Successfully"
         
       


    # resets the form
    game_entry.delete(0, 'end')
    team_a_entry.delete(0, 'end')
    team_b_entry.delete(0, 'end')
    odds_dk_a_entry.delete(0, 'end')
    odds_dk_b_entry.delete(0, 'end')
    odds_tab_a_entry.delete(0, 'end')
    odds_tab_b_entry.delete(0, 'end')

    switch_page(enter_games_to_be_checked)

# function for importing games from excel
def import_data_from_excel():
    # globalises variables so they work within the function
    global excel_success_message_label
    global number_of_games
    global excel_file

# error catching, dont want users to be able to input blank inputs
    if import_excel_entry_variable.get() == '':
        excel_success_message_label = "Please enter a file name"

    else:
        try:
            excel_file = import_excel_entry_variable.get()
            number_of_games += 1
            data = pd.read_excel(excel_file)
            # searches the excel doc for data below and puts that data in the games object
            for index, row in data.iterrows():
                Games(row['game'],row['team_a'],row['team_b'],number_of_games,row['team_A_odds_draftkings'],row['team_B_odds_draftkings'],row['team_A_odds_tab'],row['team_B_odds_tab'],'unchecked','','')
                
                excel_success_message_label = "List Added Successfully"
                
        # error catching, need to tell users when results dont show up 
        except FileNotFoundError:
            excel_success_message_label = "File not found"
    switch_page(import_list_from_excel_page)

# GUI 

# HOME PAGE
# the tkinter gui 
root = tk.Tk()
root.title("BOEVO")
root.geometry('1300x800')
font_largest_title = ("Arial-bold", 200)
font_medium_title = ("Arial-bold", 40)
font_small_text = ("Arial-bold", 15)

# labels and buttons that send the user to different pages 
boevo_label = Label(root, text="B.O.E.V.O", font=font_largest_title)
boevo_label.grid(row=0, column=2 )
long_boevo_label = Label(root, text="                                          Betting odds exploiter version one                                           ", font=font_medium_title)
long_boevo_label.grid(row=1, column=2 )
page_checkgames_button = Button(root, text="Check Unchecked Games", command=lambda: switch_page(checkgames))
page_checkgames_button.grid(row=3, column=2)
page_enter_games_to_be_checked_button = Button(root, text="Enter Games to be Checked", command=lambda: switch_page(enter_games_to_be_checked))
page_enter_games_to_be_checked_button.grid(row=4, column=2)
page_show_unchecked_games_page_button = Button(root, text="Show Unchecked Games", command=lambda: switch_page(show_unchecked_games_page))
page_show_unchecked_games_page_button.grid(row=5, column=2)
page_all_games_info_page_button = Button(root, text="Show All Games",command=lambda: switch_page(all_games_info_page))
page_all_games_info_page_button.grid(row=6, column=2)
page_explaination_of_arb_betting_strategy_button = Button(root, text="Explaination of Arb Betting Strategy", command=lambda: switch_page(explaination_of_arb_betting_strategy))
page_explaination_of_arb_betting_strategy_button.grid(row=7, column=2)
page_explaination_of_prolonging_account_access_button = Button(root, text="Explaination of prolonging account access",command=lambda: switch_page(explaination_of_prolonging_account_access))
page_explaination_of_prolonging_account_access_button.grid(row=8, column=2)
page_explaination_of_betting_proportions_button = Button(root, text="Explaination of betting proportions",command=lambda: switch_page(explaination_of_betting_proportions))
page_explaination_of_betting_proportions_button.grid(row=9, column=2)
page_import_list_from_excel_page_button = Button(root, text="Import list from excel",command=lambda: switch_page(import_list_from_excel_page))
page_import_list_from_excel_page_button.grid(row=10, column=2)

# PAGES 

# page for printing out checked games onto the gui, its pretty much just formatting of labels and buttons that link to other pages
def print_checked_games(): #PAGE 1
    frame_print_checked_games = Frame(root)
    frame_print_checked_games.grid(row=0, column=0, sticky="nsew")
    page_title_unchecked_games = Label(frame_print_checked_games, text="Results for check of unchecked games")
    page_title_unchecked_games.grid(row=0, column=0)
    row = 1 
    #  to prevent users getting confused assuming that it isnt working
    if unchecked_games == []:
        no_results_label = Label(frame_print_checked_games, text="SORRY, THERE ARE NO UNCHECKED GAMES")
        no_results_label.grid(row=1, column=0)
    else:
        for game in unchecked_games:
            game.get_arb()
            game.get_game()
            game_message = f"For Game: {game._game}"
            game_message_label = Label(frame_print_checked_games, text=game_message)
            game_message_label.grid(row=row, column=1)
            arb_message_label = Label(frame_print_checked_games, text=f"arbitrage: {game._arb}")
            arb_message_label.grid(row=row, column=2)
            if game._arb == 'yes':
                more_info_button = Button(frame_print_checked_games, text="More info", command=lambda item=game: display_all_games_page(item))
                more_info_button.grid(row=row, column=3)
            row += 1 
    # return button (one of these in every page)
    return_home_button = Button(frame_print_checked_games, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_home_button.grid(row=15, column=0)

# this is the page for entering new games into the object orientation (oo), this is the form for that, its just all labels and entries and formats
def enter_games_to_be_checked(): #PAGE 2
    global error_unfilled_fields
    global success_message_label
    global game_entry
    global team_a_entry
    global team_b_entry
    global odds_dk_a_entry
    global odds_dk_b_entry
    global odds_tab_a_entry
    global odds_tab_b_entry
    frame_enter_games_to_be_checked = Frame(root)
    frame_enter_games_to_be_checked.grid(row=0, column=0, sticky="nsew")
    page_title_tbc_label = Label(frame_enter_games_to_be_checked, text="Enter Games to be Checked")
    page_title_tbc_label.grid(row=0, column=1)
    game_label = Label(frame_enter_games_to_be_checked, text="Game:")
    game_label.grid(row=1, column=1)
    global game_entry_variable
    game_entry_variable = StringVar()
    game_entry = Entry(frame_enter_games_to_be_checked, textvariable=game_entry_variable)
    game_entry.grid(row=1, column=2)
    team_a_label = Label(frame_enter_games_to_be_checked, text="Team A:")
    team_a_label.grid(row=2, column=1)
    global team_a_entry_variable
    team_a_entry_variable = StringVar()
    team_a_entry = Entry(frame_enter_games_to_be_checked, textvariable=team_a_entry_variable)
    team_a_entry.grid(row=2, column=2)
    team_b_label = Label(frame_enter_games_to_be_checked, text="Team B:")
    team_b_label.grid(row=3, column=1)
    global team_b_entry_variable
    team_b_entry_variable = StringVar()
    team_b_entry = Entry(frame_enter_games_to_be_checked, textvariable=team_b_entry_variable)
    team_b_entry.grid(row=3, column=2)
    odds_dk_a_label = tk.Label(frame_enter_games_to_be_checked, text="Team A Odds (DraftKings):")
    odds_dk_a_label.grid(row=5, column=1)
    global odds_dk_a_entry_variable
    odds_dk_a_entry_variable = IntVar()
    odds_dk_a_entry = Entry(frame_enter_games_to_be_checked, textvariable=odds_dk_a_entry_variable)
    odds_dk_a_entry.grid(row=5, column=2)
    odds_dk_b_label = Label(frame_enter_games_to_be_checked, text="Team B Odds (DraftKings):")
    odds_dk_b_label.grid(row=6, column=1)
    global odds_dk_b_entry_variable
    odds_dk_b_entry_variable = IntVar()
    odds_dk_b_entry = Entry(frame_enter_games_to_be_checked, textvariable=odds_dk_b_entry_variable)
    odds_dk_b_entry.grid(row=6, column=2)
    odds_tab_a_label = Label(frame_enter_games_to_be_checked, text="Team A Odds (Tab):")
    odds_tab_a_label.grid(row=7, column=1)
    global odds_tab_a_entry_variable
    odds_tab_a_entry_variable = IntVar()
    odds_tab_a_entry = Entry(frame_enter_games_to_be_checked, textvariable=odds_tab_a_entry_variable)
    odds_tab_a_entry.grid(row=7, column=2)
    odds_tab_b_label = Label(frame_enter_games_to_be_checked, text="Team B Odds (Tab):")
    odds_tab_b_label.grid(row=8, column=1)
    global odds_tab_b_entry_variable
    odds_tab_b_entry_variable = IntVar()
    odds_tab_b_entry = Entry(frame_enter_games_to_be_checked, textvariable=odds_tab_b_entry_variable)
    odds_tab_b_entry.grid(row=8, column=2)
    explaination = Label(frame_enter_games_to_be_checked, text="enter odds in moneyline (eg. +100, -300 ect) \n ")
    explaination.grid(row=9, column=2)
    submit_button = Button(frame_enter_games_to_be_checked, text="Submit", command=submit_game)
    submit_button.grid(row=12, column=1)
    return_button = Button(frame_enter_games_to_be_checked, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=15, column=1)
    # error catching, if there is no input in any of the fields this label will tell the user about the error
    error_label = Label(frame_enter_games_to_be_checked, text=error_unfilled_fields)
    error_label.grid(row=16, column=1)
    error_unfilled_fields = ''
    success_label = Label(frame_enter_games_to_be_checked, text=success_message_label)
    success_label.grid(row=17, column=1)
    success_message_label = ''

# this is the page that displays all the games loaded into the oo, calls functions to return the different parts of the games, sets them as variables, and then displays them in labels
def display_all_games_page(item): #PAGE 3
    frame_display_all_games_page = Frame(root)
    frame_display_all_games_page.grid(row=0, column=0, sticky="nsew")
    first_label3 = Label(frame_display_all_games_page, text="All information concerning specififc game")
    first_label3.grid(row=0, column=0)
    item.display_games_info()
    adittional_data_game = (f"game: {item._game}")
    # ad = adittional data
    ad_team_a = (f"team A: {item._team_a}")
    ad_team_b = (f"team B: {item._team_b}")
    ad_game_id = (f"Game ID: {item._game_id}")
    ad_team_A_odds_draftkings = (f"team A Odds draftkings: {item._team_A_odds_draftkings}")
    ad_team_B_odds_draftkings = (f"team B Odds draftkings: {item._team_B_odds_draftkings}")
    ad_team_A_odds_tab = (f"team A Odds tab: {item._team_A_odds_tab}")
    ad_team_B_odds_tab = (f"team B Odds tab: {item._team_B_odds_tab}")
    ad_arb = (f"Checked: {item._arb}")
    ad_a_value_1 = (f"Working A Value 1: {item._a_value_1}")
    ad_a_value_2 = (f"Working A Value 2: {item._a_value_2}")
    adittional_data_label_1 = Label(frame_display_all_games_page, text=adittional_data_game)
    adittional_data_label_1.grid(row=1, column=1)
    # adl = adittional data label
    adl_team_a = Label(frame_display_all_games_page, text=ad_team_a)
    adl_team_a.grid(row=2, column=1)
    adl_team_b = Label(frame_display_all_games_page, text=ad_team_b)
    adl_team_b.grid(row=3, column=1)
    adl_game_id = Label(frame_display_all_games_page, text=ad_game_id)
    adl_game_id.grid(row=4, column=1)
    adl_team_A_odds_draftkings = Label(frame_display_all_games_page, text=ad_team_A_odds_draftkings)
    adl_team_A_odds_draftkings.grid(row=5, column=1)
    adl_team_B_odds_draftkings = Label(frame_display_all_games_page, text=ad_team_B_odds_draftkings)
    adl_team_B_odds_draftkings.grid(row=6, column=1)
    adl_team_A_odds_tab = Label(frame_display_all_games_page, text=ad_team_A_odds_tab)
    adl_team_A_odds_tab.grid(row=7, column=1)
    adl_team_B_odds_tab = Label(frame_display_all_games_page, text=ad_team_B_odds_tab)
    adl_team_B_odds_tab.grid(row=8, column=1)
    adl_arb = Label(frame_display_all_games_page, text=ad_arb)
    adl_arb.grid(row=9, column=1)
    adl_a_value_1 = Label(frame_display_all_games_page, text=ad_a_value_1)
    adl_a_value_1.grid(row=10, column=1)
    adl_a_value_2 = Label(frame_display_all_games_page, text=ad_a_value_2)
    adl_a_value_2.grid(row=11, column=1)
    return_button = Button(frame_display_all_games_page, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=15, column=0)

# this page is for showing unchecked games on a new page, goes through all the games in the oo and calls the function that returns the information for the unchecked games, just the title data, also displays a button user can click for extra information
def show_unchecked_games_page(): #PAGE 4
    frame_show_unchecked_games_page = Frame(root)
    frame_show_unchecked_games_page.grid(row=0, column=0, sticky="nsew")
    show_unchecked_title_label = Label(frame_show_unchecked_games_page, text="ALL UNCHECKED GAMES",)
    show_unchecked_title_label.grid(row=0, column=0)
    row = 1 
    show_unchecked_games()
    for item in unchecked_games:
        item.get_arb()
        item.get_game()
        game_message = f"For Game: {item._game}"
        game_message_label = Label(frame_show_unchecked_games_page, text=game_message)
        game_message_label.grid(row=row, column=1)
        arbitrage_label = Label(frame_show_unchecked_games_page, text=f"arbitrage: {item._arb}")
        arbitrage_label.grid(row=row, column=2)
        more_info_button = Button(frame_show_unchecked_games_page, text="More info", command=lambda item=item: display_all_games_page(item))
        more_info_button.grid(row=row, column=3)
        row += 1 
    return_button = Button(frame_show_unchecked_games_page, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=15, column=0)

# shows all games reguardless of whether they have been printed or not, with button for more info
def all_games_info_page():
    frame_all_games_info_page = Frame(root)
    frame_all_games_info_page.grid(row=0, column=0, sticky="nsew")
    all_games_title_label = Label(frame_all_games_info_page, text="ALL GAMES", font=font_medium_title)
    all_games_title_label.grid(row=0, column=0)
    row = 1 
    for game_instance in games:
        game_instance.get_arb()
        game_instance.get_game()
        game_instance.get_game_id()
        game_message = f"For Game: {game_instance._game}"
        game_message_label = Label(frame_all_games_info_page, text=game_message)
        game_message_label.grid(row=row, column=0)
        arbitrage_label = Label(frame_all_games_info_page, text=f"arbitrage: {game_instance._arb}")
        arbitrage_label.grid(row=row, column=1)
        more_info_button = Button(frame_all_games_info_page, text="More info", command=lambda item=game_instance: display_all_games_page(item))
        more_info_button.grid(row=row, column=2)
        # button to delete unwanted games
        delete_games_button = Button(frame_all_games_info_page, text="Delete game", command=lambda item=game_instance: Games.delete_game(item._game_id))
        delete_games_button.grid(row=row, column=3)
        row += 1 
    return_button = Button(frame_all_games_info_page, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=15, column=0)

# simple page with information for users to do with arb betting strategy, just simple labels and a back button
def explaination_of_arb_betting_strategy():
    frame_explaination_of_arb_betting_strategy = Frame(root)
    frame_explaination_of_arb_betting_strategy.grid(row=0, column=0, sticky="nsew")
    explaination_title_label = Label(frame_explaination_of_arb_betting_strategy, text="Explaination of Arb Betting Strategy", font=font_medium_title)
    explaination_title_label.grid(row=0, column=0)
    explaination_content_label = Label(frame_explaination_of_arb_betting_strategy, font=font_small_text, text="Arbitrage betting, often referred to as 'arbing,' is a betting strategy used in the world of sports betting or any form of gambling where you can place bets on the outcomes of events. \nThe goal of arbitrage betting is to guarantee a profit by taking advantage of differences in odds offered by different bookmakers or betting platforms for the same event. \n Imagine a scenario where you have the opportunity to bet on the outcome of a sports game, let's say a soccer match.\n Different bookmakers are offering odds on the game's result, and these odds can vary from one bookmaker to another. \n Arbitrage betting involves placing bets on all possible outcomes of an event in a way that guarantees you will make a profit, regardless of the actual outcome of the event. \n This is achieved by carefully calculating the appropriate amount to bet on each outcome so that the total amount wagered is less than the potential winnings.",)
    explaination_content_label.grid(row=1, column=0)
    return_button = Button(frame_explaination_of_arb_betting_strategy, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=15, column=0)

# simple page with information for users to do with prolonging account access, just simple labels and a back button
def explaination_of_prolonging_account_access():
    frame_explaination_of_prolonging_account_access = Frame(root)
    frame_explaination_of_prolonging_account_access.grid(row=0, column=0, sticky="nsew")
    explaination_prolonging_title_label = Label(frame_explaination_of_prolonging_account_access, text="Explaination of prolonging account access", font=font_medium_title)
    explaination_prolonging_title_label.grid(row=0, column=0)
    explaination_prolonging_content_label = Label(frame_explaination_of_prolonging_account_access, text="When an account is first opened sports betting companies begin to monitor the owner to determine whether they should be categorised as a ‘recreational better’ (square/bad) or a ‘sharp better’. \n Therefore, they need to look like recreational better. At first act like a punter.\n Depositing small amounts at first - (eg. If you want 10,000 dollars in a new account slowly add money in small exponentially increasing amounts over the first 2-3 months \n 2-3 months - this is the amount of time you should wait before doing arbs)\n Never deposit more than around 200 to begin with. It makes you look confident. \n Bet immediately after opening account, intentionally losing. \n Betting lots of different ROUNDED amounts on mainstream sports. (End in a 5 or a 0 although there is some debate whether this is actually cared about and how much it is weighted) \n  Mainstream sports because books are more confident in the odds they set for more recognised leagues (eg. Nfl, nba, mlb, prem etc). \n Keep it to mainstream but mix it up, eg. not just football, do all sports. \n Begin by splitting bets about 60 percent bets with more than 2 outcomes and 40 percent with bets that have only 2 outcomes \n Slowly trend this up until the split is completely inverse (60 on only 2 outcomes and 40 on more than 2 outcomes) \n Anything with more than two outcomes you should be aiming to lose those bets, bet small amounts on very long shots, eg. A rookie to win mvp. \n You should never win more than 50 percent of bets \n However obviously you do want to be winning more than you are losing in terms of dollar amounts, so smaller amounts need to be bet on bets you are aiming to lose. \n  Accumulators are perfect, but not too much. \n Bet about half of your intentional losing bets immediately (5-10min) before the match/game begins (makes you look like a punter) \n Live betting is also great. \n Extend the period of loses as long as possible before beginning arb betting \n Never stop losing, never switch how/what your betting on too much. \n Favourite teams is perfect — chose a bad team and just bet constantly on them \n Might help to choose a city, but one with consistently bad teams, \n Eg. Phillies and eagles, both good teams so bad city, braves and falcons, one good one bad so bad city, white sox and bears both bad so great city. \n You will receive bonuses/promotional offers for losing - this is a sign you have been successful in being placed in the recreational better category- only use about 1/10 promotions for are offered \n But do use them EXTREAMLY important to get right \n Never do what people online tell you when they reveal how to take advantage of sign up bonuses to make quick cash - it will make you seem like a ‘sharp better’ \n This should take maybe 3 months, you should aim to lose about $50-100 before starting to find arbs, however the more you lose the longer you will stay open. \n Avoid taking dividends - ideally NEVER take anything out until you’ve been limited \n If you do withdraw take it out after a regular interval and always put more in after a day or two ( eg take 100 out Monday and put 40 in Wednesday) \n NEVER push the max limits. \n Once you have an account categorised as recreational you can start using arbs \n There is an argument that once you have reached recreational betting categorisation you should go hard and fast and aim to make most money in a period of 3-5 days \n Before a human has time to review your account \n However aiming to prolong your account from this point instead of going hard and fast you should do the following:\n Again keep the arbs 40 percent of your account and only bet on arbs with two outcomes, you should win 20 percent. \n Keep losing intentionally as well, always insure more than 50 percent of your bets lose. \n Continue to bet about half of your intentional losing bets immediately (5-10min) before the match/game begins - weekends are also better than weekdays \n If possible minimise the time between placing a arb and the match beginning, as this fits the profile of a punter looked for by betting companies. \n When you are finally identified as a ‘sharp better’ betting firms will keep your account open for a bit longer to learn off you. \n If the value of the information you give them is worth more than what you are winning you will not be limited \n However because your strategy uses arbs this will likely not be true, they won’t be able to learn much from you, so you don’t have much time. \n To lengthen this period, win non arb bets, this is another reason why it is important to only do 40-60 percent arb betting. \n You can’t avoid limiting forever but you can prolong it massively - not doing this can result in accounts limited within weeks. \n")
    explaination_prolonging_content_label.grid(row=1, column=0)
    return_button = Button(frame_explaination_of_prolonging_account_access, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=15, column=0)

# simple page with information for users to do with betting proportions, just simple labels and a back button
def explaination_of_betting_proportions():
    frame_explaination_of_betting_proportions = Frame(root)
    frame_explaination_of_betting_proportions.grid(row=0, column=0, sticky="nsew")
    explaination_proportions_title_label = Label(frame_explaination_of_betting_proportions, text="             Explaination of betting proportions", font=font_medium_title)
    explaination_proportions_title_label.grid(row=0, column=0)
    explaination_proportions_content_label = Label(frame_explaination_of_betting_proportions, text=" If arbitrage is possible for an A value then arbitrage will be possible for all proportions between values of A and 1-A, this means you should bet with bet distribution as follows, a working distribution value \n on Team ONE to win outright on draft kings (betting site ONE) and (1 - the distribution you used for draft kings) on team TWO to win outright on the TAB (Betting site TWO)")
    explaination_proportions_content_label.grid(row=1, column=0)
    return_button = Button(frame_explaination_of_betting_proportions, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=15, column=0)

# page for importing lists from excel, this is just the page that calls that function, it has a form and some labels and a back button
def import_list_from_excel_page():
    frame_import_list_from_excel_page = Frame(root)
    frame_import_list_from_excel_page.grid(row=0, column=0, sticky="nsew")
    import_title_label = Label(frame_import_list_from_excel_page, text="Import list from excel", font=font_medium_title)
    import_title_label.grid(row=0, column=1)
    label_excel_entry = tk.Label(frame_import_list_from_excel_page, text="excel document name (remember .xlsx):")
    label_excel_entry.grid(row=1, column=1)
    global import_excel_entry_variable
    import_excel_entry_variable = StringVar()
    import_excel_entry = tk.Entry(frame_import_list_from_excel_page, textvariable=import_excel_entry_variable)
    import_excel_entry.grid(row=1, column=2)

    import_button = Button(frame_import_list_from_excel_page, text="import list from excel document", command=lambda: import_data_from_excel())
    import_button.grid(row=2, column=1)

    return_button = Button(frame_import_list_from_excel_page, text="Return to Main Menu", command=lambda: switch_page(back_home))
    return_button.grid(row=3, column=1)

    label_excel_info = tk.Label(frame_import_list_from_excel_page, text="\nfor testing purposes there is a excel doc with \ndata already loaded into this file, \n it is called book2.xlsx")
    label_excel_info.grid(row=4, column=1)

    global excel_success_message_label
    excel_success_label = Label(frame_import_list_from_excel_page, text=excel_success_message_label)
    excel_success_label.grid(row=5, column=1)
    excel_success_message_label = ''

# this is the home page/menu used as a link from the home page
def back_home():
    root.title("BOEVO")
    boevo_label = Label(root, text="B.O.E.V.O", font=font_largest_title)
    boevo_label.grid(row=0, column=2 )
    long_boevo_label = Label(root, text="                                          Betting odds exploiter version one                                           ", font=font_medium_title)
    long_boevo_label.grid(row=1, column=2 )
    page_checkgames_button = Button(root, text="Check Unchecked Games", command=lambda: switch_page(checkgames))
    page_checkgames_button.grid(row=3, column=2)
    page_enter_games_to_be_checked_button = Button(root, text="Enter Games to be Checked", command=lambda: switch_page(enter_games_to_be_checked))
    page_enter_games_to_be_checked_button.grid(row=4, column=2)
    page_show_unchecked_games_page_button = Button(root, text="Show Unchecked Games", command=lambda: switch_page(show_unchecked_games_page))
    page_show_unchecked_games_page_button.grid(row=5, column=2)
    page_all_games_info_page_button = Button(root, text="Show All Games",command=lambda: switch_page(all_games_info_page))
    page_all_games_info_page_button.grid(row=6, column=2)
    page_explaination_of_arb_betting_strategy_button = Button(root, text="Explaination of Arb Betting Strategy", command=lambda: switch_page(explaination_of_arb_betting_strategy))
    page_explaination_of_arb_betting_strategy_button.grid(row=7, column=2)
    page_explaination_of_prolonging_account_access_button = Button(root, text="Explaination of prolonging account access",command=lambda: switch_page(explaination_of_prolonging_account_access))
    page_explaination_of_prolonging_account_access_button.grid(row=8, column=2)
    page_explaination_of_betting_proportions_button = Button(root, text="Explaination of betting proportions",command=lambda: switch_page(explaination_of_betting_proportions))
    page_explaination_of_betting_proportions_button.grid(row=9, column=2)
    page_import_list_from_excel_page_button = Button(root, text="Import list from excel",command=lambda: switch_page(import_list_from_excel_page))
    page_import_list_from_excel_page_button.grid(row=10, column=2)

# this is the function that switches the pages when switch_page is called 
def switch_page(page_function):
    for widget in root.winfo_children():
        widget.destroy()
    page_function()

root.mainloop()

