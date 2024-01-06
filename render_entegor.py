from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType
import os
from read_xls_nodes import read_map_xls
from html_to_share import html_to_share

# nodes = [
#     {'name': '结点1'},
#     {'name': '结点2'},
#     {'name': '结点3'},
#     {'name': '结点4'},
#     {'name': '结点5'},
#     {'name': '结点6'},
# ]
#
# links = [
#     {'source': '结点1', 'target': '结点2', 'value': 2},
#     {'source': '结点2', 'target': '结点3', 'value': 3},
#     {'source': '结点3', 'target': '结点4', 'value': 4},
#     # {'source': '结点4', 'target': '结点5', 'value': 5},
#     # {'source': '结点5', 'target': '结点6', 'value': 6},
#     # {'source': '结点6', 'target': '结点1', 'value': 7},
# ]

def render_entegor(xls_path, node_idx, link_idx, comment_idx=None, seperator=',', row_start_idx=0):
    nodes, links = read_map_xls(xls_path, node_idx, link_idx, comment_idx, seperator, row_start_idx)

    # init_opts=opts.InitOpts(width='100%', height='100%')
    G = Graph(init_opts=opts.InitOpts(width='100%', height='1000px', renderer='svg', theme=ThemeType.ESSOS, animation_opts=opts.AnimationOpts(animation=False)))
    G.add(
        series_name='',
        nodes=nodes,
        symbol_size=50,
        links=links,
        repulsion=1000,  # 斥力
        # edge_label=opts.LabelOpts(is_show=True, position='middle', formatter='{b}的数据{c}'),
        symbol='rect',
        is_draggable=True,
        friction=0.4,
        is_rotate_label=False,
        is_layout_animation=True,
        edge_symbol=['','arrow']
    )
    G.set_global_opts(title_opts=opts.TitleOpts(title='Entegor调度表Demo'))
    G.render(path='render.html')
    html_to_share('render.html', 'echarts.min.js')
    os.system("render.html")

if __name__ == '__main__':
    target_xls = 'entegor.xlsx'
    # if os.path.exists(target_xls):
    #     render_xls(target_xls, 0, 2, 3)
    # else:

    assert os.path.exists(target_xls), "目标xls文件不存在"
    render_entegor(target_xls, 0, 2, 3)

