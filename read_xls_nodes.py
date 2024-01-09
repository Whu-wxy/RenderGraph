import pandas as pd
from logconfig import log

def read_map_xls(xls_path, node_idx, link_idx, comment_idx=None, group_idx=None, seperator=',', row_start_idx=0):
    df = pd.read_excel(xls_path, header=None) # usecols=[node_idx, link_idx],
    nodes_data = df.iloc[row_start_idx:, node_idx].tolist()
    links_data = df.iloc[row_start_idx:, link_idx].tolist()
    if comment_idx is not None:
        comment_data = df.iloc[row_start_idx:, comment_idx].tolist()
    if group_idx is not None:
        group_data = df.iloc[row_start_idx:, group_idx].tolist()

    nodes = []
    links = []
    global_link_dict = {}
    nodes_set = set()
    if group_idx is not None:
        grp_set = set(group_data)
        for nd in group_data:
            if nd not in nodes_set:
                nodes.append({'name': nd, 'category': nd})
            nodes_set.add(nd)
    else:
        grp_set = set()

    for i, nd in enumerate(nodes_data):
        assert nd not in nodes_set, log.logger.error('节点定义重复:{}, 行数:{}'.format(nd, i))
        assert nd != 'nan', log.logger.error('节点名字未定义:{}, 行数:{}'.format(nd, i))

        nodes_set.add(nd)
        prop = {}
        prop['name'] = nd
        if comment_idx is not None:
            prop['value'] = comment_data[i]
        if group_idx is not None:
            prop['category'] = group_data[i]

        nodes.append(prop)

    for i, prev_nodes in enumerate(links_data):
        target_nd = nodes_data[i]
        target_grp = group_data[i]

        is_head = True
        for prev_nd in str(prev_nodes).split(seperator):
            if prev_nd != 'nan':
                assert prev_nd in nodes_set, log.logger.error('前置节点未定义: {}, 行数:{}'.format(prev_nd, i))
                prev_grp = group_data[nodes_data.index(prev_nd)]
                if group_idx is not None and target_grp == prev_grp:
                    is_head = False
            else:
                if group_idx is not None:
                    links.append({'target': target_nd, 'source': target_grp})
                    continue

            if is_head:
                links.append({'target': target_nd, 'source': target_grp})

            links.append({'target': target_nd, 'source': prev_nd})
            global_link_dict[prev_nd] = target_nd

    return nodes, links, global_link_dict, nodes_set, grp_set


if __name__ == '__main__':
    nodes, links = read_map_xls('entegor.xls', 0, 2, 3, row_start_idx=1)
    print(nodes)
    print(links)
