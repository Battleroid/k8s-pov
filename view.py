import click
import json
from itertools import chain
from os.path import commonprefix
from tabulate import tabulate
from subprocess import Popen, PIPE


@click.command()
@click.option(
    '-c', '--chunk-size',
    default=3,
    type=int,
    help='Chunk size (nodes per row).',
    show_default=True
)
@click.option(
    '-n', '--no-strip',
    default=False,
    is_flag=True,
    help='Do not strip common prefix.'
)
@click.argument('namespace', default='all')
def main(namespace, chunk_size, no_strip):
    """
    Dump a table of the pods attached to each node.
    """

    # set namespace appropriately
    if namespace == 'all':
        namespace = ['--all-namespaces']
    else:
        namespace = ['-n', namespace]

    # get pod junk
    data = Popen(
        ['kubectl', 'get', 'pods', *namespace, '-o', 'json'],
        stdout=PIPE
    ).stdout.read().strip().decode('utf-8')
    data = json.loads(data)

    if not data['items']:
        raise SystemExit('No pods/nodes found.')

    # get pods per node
    nodes = {}
    for item in data['items']:
        node = item['spec']['nodeName']
        name = item['metadata']['name']
        nodes.setdefault(node, [])
        nodes[node].append(name)

    # truncate name to unique part
    if not no_strip:
        prefix = commonprefix(list(nodes.keys()))
        for node in list(nodes.keys()):
            pods = nodes.pop(node)
            node = node.replace(prefix, '')
            nodes[node] = pods

    # ensure constant width
    max_width = max(map(len, chain.from_iterable([nodes.keys(), *nodes.values()])))
    for node in list(nodes.keys()):
        pods = nodes.pop(node)
        node = node.ljust(max_width)
        nodes[node] = pods

    # chunk nodes to keep horizontal size down
    chunks = [dict(list(nodes.items())[x:x + chunk_size]) for x in range(0, len(nodes), chunk_size)]

    # present
    for chunk in chunks:
        print(tabulate(chunk, headers='keys', tablefmt='psql'))


if __name__ == '__main__':
    main()
