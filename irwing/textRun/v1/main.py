from GUI import GUI

gui = GUI()

gui.ShowStartScreen()

while True:
    gui.ShowMainMenu()
    option = gui.GetMainMenuInput()

    if option in gui.MenuOptions:
        if option == 1:
            gui.ShowGameScreen()
        elif option == 2:
            gui.ShowRankingScreen()
        elif option == 3:
            gui.ShowHowToPlayScreen()
        elif option == 4:
            break;
