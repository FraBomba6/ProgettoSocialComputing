from pyvis.network import Network
import networkx.readwrite.gpickle as pkl

twitter = pkl.read_gpickle("graph/graph_networkx.pkl")

nt = Network(height="100%", width="100%", bgcolor="#111111", font_color="white",
             heading="Twitter Graph - Broken Edition")

node = list(twitter.nodes)[:2000]
twitter = twitter.subgraph(node)

nt.barnes_hut()  # (gravity=-5000, central_gravity=0, spring_length=200, spring_strength=0.009, damping=0.025, overlap=0) #me li mette un po vicini il damping verso 1 credo #gravity ti mostra subito i nodi per bene
nt.from_nx(twitter)
neighbor_map = nt.get_adj_list()


for node in nt.nodes:
    # node["id"] += " Neighbors:<br>" + "<br>".join(neighbor_map[node["id"]])
    info = "nome utente: " + node['screen_name'] + "<br>" + "id: " + node['id_str']
    node["value"] = len(neighbor_map[node["id"]])
    node['title'] = info
    node['label'] = node['name']
    # node['shape'] = 'circularImage'
    # node['image'] = node['profile_image_url']
    if node['screen_name'] == 'damiano10':
        node['color'] = 'red'
        node['mass'] = 50
        node['x'] = 500
        node['y'] = 50
    elif node['screen_name'] == 'eglu81':
        node['color'] = 'yellow'
        node['mass'] = 50
    elif node['screen_name'] == 'mizzaro':
        node['color'] = 'blue'
        node['mass'] = 50
    elif node['screen_name'] == 'Miccighel_':
        node['color'] = '#0fefff'
        node['mass'] = 50
    elif node['screen_name'] == 'KevinRoitero':
        node['color'] = '#ff0fd3'
        node['mass'] = 50

for edge in nt.edges:
    if edge['to'] == 132646210:
        edge['color'] = 'red'
    elif edge['to'] == 19659370:
        edge['color'] = 'yellow'
    elif edge['to'] == 18932422:
        edge['color'] = 'blue'
    elif edge['to'] == 15750573:
        edge['color'] = '#0fefff'
    elif edge['to'] == 3036907250:
        edge['color'] = '#ff0fd3'
    else:
        edge['color'] = 'white'

nt.show("twitShape2.html")
