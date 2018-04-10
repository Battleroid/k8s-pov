# k8s-pov

I just wanted to view how pods are laid out in a cluster without any fancy junk. This fits the bill.

Note: the node names (headers) have the common prefix stripped away. I hate sifting through the node names trying to find the one portion that's actually different. This can be disabled with `-n` or `--no-strip`.

## Usage

```
Usage: k8s-pov [OPTIONS] [NAMESPACE]

  Dump a table of the pods attached to each node.

Options:
  -t, --tablefmt TEXT       Tabulate table format.
  -c, --chunk-size INTEGER  Chunk size (nodes per row).  [default: 3]
  -n, --no-strip            Do not strip common prefix.
  --help                    Show this message and exit.
```

## Example

```
$ k8s-pov elasticsearch
+------------------------------+------------------------------+------------------------------+
| qgkv                         | f1k2                         | nvg9                         |
|------------------------------+------------------------------+------------------------------|
| es-data-0                    | es-data-1                    | es-data-2                    |
| es-master-57f76b6658-bphmm   | kibana-599d9468df-44826      | es-master-57f76b6658-bz46g   |
| es-master-57f76b6658-m8swk   |                              |                              |
+------------------------------+------------------------------+------------------------------+
+------------------------------+------------------------------+------------------------------+
| xb8p                         | mc2h                         | blp4                         |
|------------------------------+------------------------------+------------------------------|
| es-data-3                    | es-data-4                    | es-data-5                    |
+------------------------------+------------------------------+------------------------------+
```
