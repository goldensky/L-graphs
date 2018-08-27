
class Lgraph:
    def __init__(self):
        self.start_vertices = set()
        self.finish_vertices = set()
        self.d_sets = set()     # set of brackets
        self.links = {}         # {in_ver: {'symbol': token, 'out_ver': out_ver}}
        
    # add init vertice
    def add_start_vertice(self, ver):
        self.start_vertices.add(ver)
        
    #add finish vertice
    def add_finish_vertice(self, ver):
        self.finish_vertices.add(ver)
        
    # add bracket_mark
    def add_d_sets(self, d):
        self.d_sets.add(d)

    # add edge
    def add_link(self, in_ver, link):
        '''
        link = {'symbol': token, 'out': out_ver}

        {in_ver: {'symbol': token, 'out_ver': out_ver}}
        '''
        q = self.links.setdefault(in_ver, [])
        q.append(link)

    def print_lgraph(self):
        print('Start vertices: ', self.start_vertices)
        print('Finish vertices: ', self.finish_vertices)
        print('Dsets : ', self.d_sets)
        print('Links: ')
        list_keys = self.links.keys()
        list_keys = list(list_keys)
        list_keys.sort()
        for i in list_keys:
            print(i, ': ', self.links[i])
        


def main1():
    ll = Lgraph()
    ll.print_lgraph()
    in_ver = 0
    out_ver = 1
    br = '[1'
    bracket_mark = (in_ver, out_ver, 'PROGRAM', 23, br)
    ll.add_d_sets(bracket_mark)
    ll.print_lgraph()
    
def main():
    ll = Lgraph()
    ll.print_lgraph()
    
    in_ver = 0
    out_ver1 = 1
    out_ver2 = 2

    l1 = {'symbol': 'readln', 'out': out_ver1}
    l2 = {'symbol': 'read', 'out': out_ver1}
    l3 = {'symbol': 'write', 'out': out_ver2}
    l4 = {'symbol': 'writeln', 'out': out_ver2}
    ll.add_link(in_ver, l1)
    ll.add_link(in_ver, l2)
    ll.add_link(in_ver, l3)
    ll.add_link(in_ver, l4)

    print()
    ll.print_lgraph()
    '''
    Start vertices:  set()
    Finish vertices:  set()
    Dsets :  []
    Links: 
    0 :  [{'out': 1, 'symbol': 'readln'}, {'out': 1, 'symbol': 'read'},
    {'out': 2, 'symbol': 'write'}, {'out': 2, 'symbol': 'writeln'}]
    '''
    in_ver2 = 1
    out_ver2 = 3
    
    vertices_list = ll.links.keys()
    print(vertices_list)
    edge13 = {'symbol': 'LPAREN', 'out': out_ver2}
    w = ll.add_link(in_ver2, edge13)

    print()
    for key, value in ll.links.items():
        print(key, value)
    '''
    0 [{'symbol': 'readln', 'out': 1}, {'symbol': 'read', 'out': 1},
    {'symbol': 'write', 'out': 2}, {'symbol': 'writeln', 'out': 2}]
    
    1 [{'symbol': 'LPAREN', 'out': 3}]

    '''

   

if __name__ == '__main__':
    main1()
