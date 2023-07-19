import subprocess
import time
import random


def get_mac(interface):
    output = subprocess.check_output(['ifconfig', interface]).decode('utf-8')
    mac_index = output.index('ether') + 6
    return output[mac_index:mac_index + 17]


def get_random_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])


def change_mac(interface, new_mac):
    subprocess.call(['sudo', 'ifconfig', interface, 'down'])
    subprocess.call(['sudo', 'ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['sudo', 'ifconfig', interface, 'up'])


def get_network_interface():
    output = subprocess.check_output(['ifconfig']).decode('utf-8')
    interfaces = []
    lines = output.split('\n')
    for line in lines:
        if 'UP' in line:
            interface = line.split(':')[0]
            interfaces.append(interface)
    return interfaces


if __name__ == "__main__":
    try:
        interfaces = get_network_interface()
        if not interfaces:
            raise Exception("No network interface found.")

        interface = interfaces[0]  # Use the first interface found

        # Store original MAC address
        original_mac = get_mac(interface)
        print(f"Original MAC address: {original_mac}")

        # Change MAC address every 3 minutes
        while True:
            try:
                new_mac = get_random_mac()
                print(f"Changing MAC address to: {new_mac}")
                change_mac(interface, new_mac)
                time.sleep(180)  # Wait for 3 minutes (180 seconds) before changing again (you can set time as you want)
            except KeyboardInterrupt:
                print("Exiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

        # Restore the  original MAC address
        print(f"Restoring original MAC address: {original_mac}")
        change_mac(interface, original_mac)

    except Exception as e:
        print(f"Error: {e}")

