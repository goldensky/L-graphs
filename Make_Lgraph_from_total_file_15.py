import lexem_value_tables
import L_class_Token
import L_class_Lgraph
import Lexer_5


DEBUG = 0
EOF = 'EOF'
ID = 'ID'


class Make_Lgraph_From_File:
    def __init__(self, lgraph_representation_filename):
        self.filename = lgraph_representation_filename
        self.lgraph = self.make_lgraph()
                
    def print_lgraph(self):
        '''
        Outputs the initial and final vertices,
        bracketed marks and edges.
        
        '''
        self.lgraph.print_lgraph()

    def make_lgraph(self):
        lgraph = L_class_Lgraph.Lgraph()
        with open(self.filename) as fh:
            line = fh.readline().strip()
            if len(line) >= 3 and line[0] == '{' and line[-1] == '}':
                line = line.lstrip('{').rstrip('}')
                set_start_vertice = int(line)

                lgraph.start_vertices.add(set_start_vertice)

            line = fh.readline().strip()
            if len(line) >= 3 and line[0] == '{' and line[-1] == '}':
                line = line.lstrip('{').rstrip('}')
                set_finish_vertices = set()
                lst = [int(i) for i in line.split()]
                for vertice in lst:
                    lgraph.finish_vertices.add(vertice)

            #
            while line != '#':
                
                line = fh.readline().strip()
                temp = line.split()
                if len(temp) == 6:
                    in_vertice, out_vertice, token_type, token_value, closing_bracket, open_bracket = temp
                    if DEBUG:
                        print()
                        print(line)
                        print('temp = ', temp)
                        print('in = {0}, out = {1}'.format( in_vertice, out_vertice))
                        print('type =  {0}, value = {1}'.format( token_type, token_value))
                        print('close = {0}, open = {1}'.format(closing_bracket, open_bracket))
                        print()

                    in_vertice = int(in_vertice)
                    out_vertice = int(out_vertice)
                    token_value = int(token_value)
                    token = L_class_Token.Token(token_type, token_value)
                    if DEBUG:
                        print(token)
                        print()

                    bracket_mark = (in_vertice, out_vertice, token, closing_bracket, open_bracket)
                    lgraph.add_d_sets(bracket_mark)

                    
                elif len(temp) == 5:
                    in_vertice, out_vertice, token_type, token_value, one_bracket = temp                   
                    in_vertice = int(in_vertice)
                    out_vertice = int(out_vertice)
                    token_value = int(token_value)
                    token = L_class_Token.Token(token_type, token_value)

                    bracket_mark = (in_vertice, out_vertice, token, one_bracket)
                    lgraph.add_d_sets(bracket_mark)
                
            #
            if DEBUG:
                print('line = ', line)

            for line in fh:
                temp = line.split()
                in_vertice, token_type, token_value, out_vertice = temp
                in_vertice = int(in_vertice)
                out_vertice = int(out_vertice)
                token_value = int(token_value)
                token = L_class_Token.Token(token_type, token_value)
                edge =  {'symbol': token, 'out_vertice': out_vertice}
                lgraph.add_link(in_vertice, edge)
        return lgraph

    @property
    def links(self):
        '''
        Representation the edges in the form
        0: [
            {'symbol': 'readln', 'out': 1},
            {'symbol': 'read', 'out': 1},
            {'symbol': 'write', 'out': 2},
            {'symbol': 'writeln', 'out': 2}
            ]
        
        in_ver [{symbol,                       out_ver         }]
             0 [{'symbol': Token(PROGRAM, 23), 'out_vertice': 1}]
        '''
        links = self.lgraph.links
        return links

    def print_bracket_marks(self):
        marks = self.lgraph.d_sets
        marks_lst = list(marks)
        for item in marks:
            print(item)
    
    def print_links(self):
        links = self.lgraph.links
        for key, value in links.items():
            print(key, value)



def main():
    lgraph_representation_filename = 'total_task1_total_lgraph_.txt'
    lgraph = Make_Lgraph_From_File(lgraph_representation_filename)
    lgraph.print_lgraph()
    lgraph.print_bracket_marks()
    lgraph.print_links()

if __name__ == '__main__':
    main()
