# k8s-pov

I just wanted to view how pods are laid out in a cluster without any fancy junk. This fits the bill.

Note: the node names (headers) have the common prefix stripped away. I hate sifting through the node names trying to find the one portion that's actually different. This can be disabled with `-n` or `--no-strip`.

If you're looking for something without tables, you can achieve something similar with kubectl using:

```
$ kubectl -n elasticsearch get pods -o wide --sort-by ".spec.nodeName"
NAME                         READY     STATUS    RESTARTS   AGE       IP           NODE
es-data-5                    1/1       Running   0          3h        10.28.0.12   gke-fiddle-default-pool-af11f6b5-blp4
es-data-1                    1/1       Running   0          3h        10.28.1.10   gke-fiddle-default-pool-af11f6b5-f1k2
kibana-599d9468df-44826      1/1       Running   0          4d        10.28.1.6    gke-fiddle-default-pool-af11f6b5-f1k2
es-data-4                    1/1       Running   0          3h        10.28.5.3    gke-fiddle-default-pool-af11f6b5-mc2h
es-data-2                    1/1       Running   0          3h        10.28.2.12   gke-fiddle-default-pool-af11f6b5-nvg9
es-master-57f76b6658-bz46g   1/1       Running   0          1d        10.28.2.10   gke-fiddle-default-pool-af11f6b5-nvg9
es-data-0                    1/1       Running   0          3h        10.28.3.14   gke-fiddle-default-pool-af11f6b5-qgkv
es-master-57f76b6658-bphmm   1/1       Running   0          1d        10.28.3.13   gke-fiddle-default-pool-af11f6b5-qgkv
es-master-57f76b6658-m8swk   1/1       Running   0          1d        10.28.3.12   gke-fiddle-default-pool-af11f6b5-qgkv
es-data-3                    1/1       Running   0          3h        10.28.4.3    gke-fiddle-default-pool-af11f6b5-xb8p
```

It's not "table-y", but good enough if you don't want to use this.

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
