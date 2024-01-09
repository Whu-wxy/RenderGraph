from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType
import os
from read_xls_nodes import read_map_xls
from html_to_share import html_to_share
import yaml
from logconfig import log

def render_Graph(xls_path, node_idx, link_idx, comment_idx=None, group_idx=None, seperator=',', row_start_idx=0, graph_cfs=None):
    nodes, links, _, __, grp_set = read_map_xls(xls_path, node_idx, link_idx, comment_idx, group_idx, seperator, row_start_idx)
    categories = [opts.GraphCategory(name=grp) for grp in grp_set]

    # init_opts=opts.InitOpts(width='100%', height='100%')
    G = Graph(init_opts=opts.InitOpts(width=graph_cfs['width'] or '100%',
                                      height=graph_cfs['height'] or '1000px',
                                      renderer='svg',
                                      theme=ThemeType.ESSOS,
                                      animation_opts=opts.AnimationOpts(animation=False)))
    G.add(
        series_name='',
        nodes=nodes,
        symbol_size=graph_cfs['symbol_size'] or 50,
        edge_length=graph_cfs['edge_length'] or 20,
        links=links,
        categories=categories,
        repulsion=graph_cfs['repulsion'] or 2000,  # 斥力
        # edge_label=opts.LabelOpts(is_show=True, position='middle', formatter='{b}的数据{c}'),
        symbol='roundRect',  # arrow pin roundRect
        is_draggable=True,
        friction=0.5,
        is_rotate_label=False,
        is_layout_animation=True,
        edge_symbol=['','arrow'],
        linestyle_opts=opts.LineStyleOpts(is_show=True,
                                          width=2,
                                          curve=0,
                                          color='#000000'),
        label_opts=opts.LabelOpts(is_show=True,
                                  font_size=graph_cfs['font_size'] or '10px')
    )

    G.set_global_opts(title_opts=opts.TitleOpts(title='Entegor调度表Demo'),
                      toolbox_opts=opts.ToolboxOpts(is_show=True,
                                                    pos_top="top",
                                                    pos_left="right",
                                                    feature={"saveAsImage": {},
                                                             "dataZoom": {},
                                                             "restore": {},
                                                             "magicType": {"show": False, "type": ["line", "bar"]},
                                                             "dataView": {},
                                                             "brush": {}
                                                             }
                                                    ),
                      brush_opts=opts.BrushOpts(tool_box=['rect', 'polygon', 'lineX', 'lineY', 'keep', 'clear'],
                                                brush_link='all'),
                      datazoom_opts=opts.DataZoomOpts()
                      )
    G.set_colors(['#6a89cc', '#38ada9', '#f6b93b', '#f8c291', '#c9f29b', '#7bed9f', '#ff6b81', '#70a1ff', '#747d8c', '#574b90',
                  '#c44569', '#3B3B98', '#82589F', '#55E6C1', '#CAD3C8', '#F97F51', '#58B19F', '#191970', '#0ABAB5', '#32CD32'])
    G.render(path='render.html')
    html_to_share('render.html', 'echarts.min.js')
    os.system("render.html")

if __name__ == '__main__':
    print('begin render...')

    yamlPath = 'config.yaml'
    assert os.path.exists(yamlPath), log.logger.warning("config.yaml配置文件不存在")

    cfs = {}
    with open(yamlPath, 'rb') as f:
        cfs = f.read()
        cfs = yaml.load(cfs, Loader=yaml.Loader)
        log.logger.info(cfs)

    data = cfs['data']
    graph = cfs['graph']

    target_xls, \
    node_idx, \
    link_idx, \
    comment_idx, \
    group_idx, \
    seperator, \
    row_start_idx = \
        data['target_xls'], \
        data['node_idx'], \
        data['link_idx'], \
        data['comment_idx'], \
        data['group_idx'], \
        data['seperator'], \
        data['row_start_idx']

    assert os.path.exists(target_xls), log.logger.warning("目标xls文件不存在")
    try:
        render_Graph(target_xls, node_idx, link_idx, comment_idx, group_idx, seperator, row_start_idx, graph)
    except Exception as r:
        log.logger.warning(r)
