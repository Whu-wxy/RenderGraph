import pandas as pd


def read_map_xls(xls_path, node_idx, link_idx, comment_idx=None, seperator=',', row_start_idx=0):
    df = pd.read_excel(xls_path, header=None) # usecols=[node_idx, link_idx],
    # print(df)
    nodes_data = df.iloc[row_start_idx:, node_idx].tolist()
    links_data = df.iloc[row_start_idx:, link_idx].tolist()
    if comment_idx is not None:
        comment_data = df.iloc[:, comment_idx].tolist()

    nodes = []
    links = []
    global_dict = {}
    nodes_set = set()
    for i, nd in enumerate(nodes_data):
        if comment_idx is not None:
            nodes.append({'name': nd, 'value': comment_data[i]})
        else:
            nodes.append({'name': nd})

        nodes_set.add(nd)
        prev_node = links_data[i]
        for prev_nd in str(prev_node).split(seperator):
            links.append({'target': nd, 'source': prev_nd})
            global_dict[prev_nd] = nd
            if prev_nd not in nodes_set:
                nodes.append({'name': prev_nd})

    # print(nodes)
    # print(links)
    # print(global_dict)

    return nodes, links


if __name__ == '__main__':
    read_map_xls('test.xls', 0, 2, 3)
