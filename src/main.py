from user import login, signup

# Menu principal
def main():
    print("1. Connexion")
    print("2. Inscription")
    choice = input("Choisissez une option (1 ou 2): ")

    if choice == '1':
        login()
    elif choice == '2':
        signup()
    else:
        print("Choix invalide.")

if __name__ == "__main__":
    main()