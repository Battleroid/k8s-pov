import click
import json
from itertools import chain
from os.path import commonprefix
from tabulate import tabulate, _table_formats
from subprocess import Popen, PIPE


@click.command()
@click.option(
    '-t', '--tablefmt',
    type=str,
    default='psql',
    envvar='TABLEFMT',
    help='Tabulate table format.'
)
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
def main(namespace, chunk_size, no_strip, tablefmt):
    """
    Dump a table of the pods attached to each node.
    """

    # set tablefmt
    if tablefmt not in _table_formats:
        tablefmt = 'psql'

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

    # little map of status to color
    status_map = {
        'Running': 'green',
        'Succeeded': 'green',
        'Pending': 'yellow',
        'Init': 'yellow',
        'Failed': 'red',
        'Terminating': 'red',
        'Terminated': 'red',
        'Unknown': 'red'
    }

    # get pods per node
    nodes = {}
    for item in data['items']:
        node = item['spec']['nodeName']
        name = item['metadata']['name']
        status = status_map.get(item['status']['phase'], 'white')
        nodes.setdefault(node, {})
        nodes[node][name] = status

    # truncate name to unique part
    if not no_strip:
        prefix = commonprefix(list(nodes.keys()))
        for node in list(nodes.keys()):
            pods = nodes.pop(node)
            node = node.replace(prefix, '')
            nodes[node] = pods

    # ensure constant width, color pods according status
    max_width = max(map(len, chain.from_iterable([nodes.keys(), *[p.keys() for p in nodes.values()]])))
    for node in list(nodes.keys()):
        pods = nodes.pop(node)
        node = node.ljust(max_width)
        pretty_pods = []
        for pod, color in pods.items():
            pretty_pods.append(click.style(pod, fg=color))
        nodes[node] = pretty_pods

    # chunk nodes to keep horizontal size down
    chunks = [dict(list(nodes.items())[x:x + chunk_size]) for x in range(0, len(nodes), chunk_size)]

    # present
    for chunk in chunks:
        click.secho(tabulate(chunk, headers='keys', tablefmt=tablefmt))


if __name__ == '__main__':
    main()
