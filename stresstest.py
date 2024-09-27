import subprocess
import threading
import re
import os


def get_swarm_status():
    # Run the 'swarm status' command and capture its output
    result = subprocess.run(['swarm', 'status'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return output


def parse_swarm_status(output):
    # Regular expression to match node names
    node_pattern = r'([a-zA-Z0-9\-]+\.swarm)'

    # Find all node names using the regular expression
    nodes = re.findall(node_pattern, output)

    # Print the filtered node names
    print(nodes)

    nodes.pop(0)

    nodes.remove('macbookanton.swarm')
    nodes.remove('macbook-philippe.swarm')
    nodes.remove('vm-ansible.swarm')

    print(nodes)

    return nodes


def ping_node(node):
    # Exclude the first node
    response = subprocess.run(['ping', '-c', '10', '-s', '65000', node], stdout=subprocess.PIPE)

if __name__ == "__main__":
    # Step 1: Get the swarm status
    swarm_output = get_swarm_status()

    devices = parse_swarm_status(swarm_output)

    threads = []

    while True:
        for node in devices:
            thread = threading.Thread(target=ping_node, args=(node,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
