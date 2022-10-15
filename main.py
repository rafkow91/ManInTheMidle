from time import sleep

from controllers import (
    HackByArp,
    ConfigurationInput,
    ConfigurationReader,
    QuitProgram,
    clear_console,
)


OPTIONS = {
    '1': ConfigurationReader,
    '2': ConfigurationInput,
    'q': QuitProgram
}

if __name__ == '__main__':
    clear_console()
    print('\n\n\tWelcome in the man-in-the-middle attacker!\n\nChoose how you get me attacking objects:\n1 - import from file\n2 - input in console\nq - quit script\n')
    choice = input('\tYour choice:\t')
    while True:
        if choice.lower() not in ['1', '2', 'q']:
            print('Incorect choice!! Choose again.')
            choice = input('\tYour choice:\t')
        else:
            break

    mode = OPTIONS[choice]()
    results = mode.run()
    try:
        i = int(input('\n\nHow many times do you want to send arp response?\t'))
    except ValueError:
        print('Wrong input! Objects are hacking 200 times per object')
        i = 200
    for item in results:
        app = HackByArp(item)
        app.run(i)
        sleep(2)
        print('Done!')
    
    clear_console()
