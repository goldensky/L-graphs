import json
import Lexer_5
import L_class_Lgraph
import L_class_Token
import lexem_value_tables


DEBUG = 0

INTEGER_CONST = 'INTEGER_CONST'
EOF = 'EOF'
ID = 'ID'


class Make_Lgraph:
    '''
    Constructs an L-graph according to the main solution of the problem
    and returns it.

    sample_solution_file_name is the name of the sample solution file.
    The text of the sample solution is written to the variable
    self.sample_text.
    The class creates an object of the L-graph self.lgraph.
    '''
    
    def __init__(self, sample_solution_filename, start_vertice=0):
        self.sample_solution_filename = sample_solution_filename
        self.start_vertice = start_vertice
        self.sample_text = self.get_sample_solution_text()
        self.all_tokens = self.get_all_tokens_from_solution_text()
       
    def get_sample_solution_text(self):
        '''
        Returns the text of the sample solution for constructing the
        L-graph.
        '''
        with open(self.sample_solution_filename) as fh:
            sample_text = fh.read()
        return sample_text

    def get_all_tokens_from_solution_text(self):
        ''''
        Returns a list of all tokens from the sample text of the
        solution of the problem.
        '''
        lexer = Lexer_5.Lexer(self.sample_text)
        all_tokens = []
        current_token = lexer.get_next_token()
        all_tokens.append(current_token)
        while current_token.type != EOF:
            current_token = lexer.get_next_token()
            all_tokens.append(current_token)
        
        if all_tokens[-1].type == EOF:
            all_tokens.pop()
        return all_tokens

    @property
    def links(self):
        '''
        Representation of edges in the form
        0: [
            {'symbol': 'readln', 'out': 1},
            {'symbol': 'read', 'out': 1},
            {'symbol': 'write', 'out': 2},
            {'symbol': 'writeln', 'out': 2}
            ]
        
        in_ver [{symbol,                       out_ver         }]
             0 [{'symbol': Token(PROGRAM, 23), 'out_vertice': 1}]
        '''
        links = self.make_lgraph().links
        return links

    def print_links(self):
        links = self.links
        for key, value in links.items():
            print(key, value)
            
        '''
        value_dict = links.values()
        for item in value_dict:
            print(item)
            #print(item['symbol'])
        '''
        
    def make_lgraph(self):
        ''''
        Constructs an L-graph by the main solution of the problem
        and returns it.

        The vertex with the outgoing edge containing the point as mark,   
        is final.
        Thus, we determine the number of the final vertex.
        '''
        current_lgraph = L_class_Lgraph.Lgraph()
        current_lgraph.add_start_vertice(self.start_vertice)

        for vertice_number in range(len(self.all_tokens)):
            in_vertice = vertice_number
            out_vertice = vertice_number + 1
            token = self.all_tokens[vertice_number]
            link = {'symbol': token,'out_vertice': out_vertice}
            current_lgraph.add_link(in_vertice, link)

            if DEBUG:
                print(in_vertice, token, out_vertice)
                print(link)
                
        links_dict = current_lgraph.links
        value_dict = links_dict.values()
        for item in value_dict:
            if item[0]['symbol'].type == 'DOT':
                finish_vertice = item[0]['out_vertice']
                
        current_lgraph.add_finish_vertice(finish_vertice)

        return current_lgraph

    def make_token_from_token_name(self, token_name):
        try:
            j = lexem_value_tables.TW.index(token_name.lower())
            token = L_class_Token.Token(lexem_value_tables.words(j).name, j)
        except ValueError as err:
            try:
                j = lexem_value_tables.ST_ID.index(token_name.lower())
                token = L_class_Token.Token(lexem_value_tables.st_id_lex(j).name, j)
            except ValueError as err2:
                j = lexem_value_tables.TD.index(token_name)
                token = L_class_Token.Token(lexem_value_tables.dlms(j).name, j)
        return token

    def print_lgraph(self):
        '''
        Output of the initial and final vertices, bracketed
        marks, and edges.
        '''
        self.make_lgraph().print_lgraph()

    def write_lgraph_to_file(self):
        '''
        The method displays the name of the .txt file,
        where the representation of the L-graph is written.       
        '''
        ll = self.links
        start_vertices = self.make_lgraph().start_vertices
        finish_vertices = self.make_lgraph().finish_vertices

        file_name_to_write_lgraph = (self.sample_solution_filename.split('.')[0]
                                     + '_lgraph_' + '.txt')

        try:
            with open(file_name_to_write_lgraph, 'w') as fh:
                fh.write(str(start_vertices) + '\n')  
                fh.write(str(finish_vertices) + '\n')

                keys_list = list(ll.keys())
                keys_list.sort()
                for key in keys_list:
                    value = ll[key]
                    for j in range(len(value)):
                        j_symbol = value[j]['symbol']
                        j_out = value[j]['out_vertice']
                        s = (str(key) + ' ' + str(j_symbol.type)
                             + ' ' + str(j_symbol.value) + ' '
                             + str(j_out) + '\n')
                        fh.write(s)
        except IOError as er_cannot_open_file_to_write_in:
            print("Can't open file to write  in current directory")
        else:
            print("L-graph representatin was written to file {0}".format(
            file_name_to_write_lgraph))


def main():
    filename = 'task1.pas'
    lgraph_object = Make_Lgraph(filename)
    print(lgraph_object.get_sample_solution_text())
    print(lgraph_object.get_all_tokens_from_solution_text())
    lgraph_object.print_lgraph()
    lgraph_object.write_lgraph_to_file()
    ll = lgraph_object.links
    print(ll)
    lgraph_object.print_links()
    a = lgraph_object.make_lgraph()
    print(a)


if __name__ == '__main__':
    main()



    













                    


        
