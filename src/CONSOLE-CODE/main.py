

# Menu principal
def main():
    print("---------------------- WELCOME TO THE QUIZ APP ----------------------")
    print("1. Connexion")
    print("2. Inscription")
    choice = input("Choisissez une option (1 ou 2): ")

    if choice == '1':
        from user import login
        login()
    elif choice == '2':
        from user import signup
        signup()
    else:
        print("Choix invalide.")

if __name__ == "__main__":
    main()