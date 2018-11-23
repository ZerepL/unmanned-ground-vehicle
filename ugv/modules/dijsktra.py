'''Modulo responsavel pelos calculos de mapa e rota'''

from collections import deque, namedtuple


INF = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
    '''Cria um edge

    Parametros:
    -- start: Node de inicio (str)
    -- end: Node final (str)
    -- cost: Custo entre nodes (int)

    Retorna um Edge com os valores de parametros ajustados.
    '''
    return Edge(start, end, cost)


def make_edge_reverse(start, end, cost=1):
    '''Cria um Edge reverso, se existe um caminho de A para B
    pode existir uma rota de B para A

    Parametros:
    -- start: Node de inicio (str)
    -- end: Node final (str)
    -- cost: Custo entre nodes (int)

    Retorna um Edge com os valores de parametros ajustados.
    '''
    return Edge(end, start, cost)


class Graph:
    '''Cria uma classe Graph para cada grafo criado'''
    def __init__(self, edges):
        '''Verifica se os dados estao corretos

        Parametros:
        -- edges: Conjunto de dois nodes e uma rota
        '''
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        '''Realiza a soma de custo dos edges
        Retorna a soma entre os custos de todos os edges (int)
        '''
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        '''Retorna os pairs dos nodes'''
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        '''Remove edges do grafo'''
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        '''Adiciona edges ao grafo'''
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        '''Retorna os nodes vizinho a um determinado node'''
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        '''Responsavel por calcular a menor rota entre dois nodes

        Parametros:
        -- source: Ponto de partida (str)
        -- dest: Destino (str)
        '''
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: INF for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == INF:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path
