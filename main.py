from dotenv import load_dotenv
from folders import options
from reports import generate


load_dotenv()


if __name__ == "__main__":
    # Ask for which option to run and execute per module
    option = input(
        "Which option do you want to run?\n"
        "1: Options\n"
        "2: Generate PDF\n"
    )

    # Add modules here
    if option == "1":
        options.run()
    elif option == "2":
        generate.run()
    else:
        print("Invalid option. Exiting...")
