import json
import L_class_Lgraph
import Make_Lgraph_15
import Make_Auxiliary_Lgraph_15
import L_class_Token
import lexem_value_tables




DEBUG = 0

ID = 'ID'
INTEGER_CONST = 'INTEGER_CONST'
EOF = 'EOF'

class Make_Total_Lgraph:
    '''
    Reads a graph representation from the txt file and adds the
    bracketed marks.
    Writes the receiving L-graph to the file.

    '''
    
    def __init__(self,  lgraph_representation_filename,
                 bracket_marks_filename = None):
        self.filename = lgraph_representation_filename
        self.bracket_marks_filename = bracket_marks_filename
        self.lgraph = self.make_lgraph()
        self.add_bracket_marks()
                   
    def print_lgraph(self):
        '''
        Outputs the initial and final vertices, bracketed marks,
        and edges.

        '''
        self.lgraph.print_lgraph()

    @property
    def links(self):
        '''
        Representation of the edges in the form
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

            for line in fh:             # 18 ID 2 119
                temp = line.split()     # temp = ['18', 'ID', '2', '119']   
                in_vertice, token_type, token_value, out_vertice = temp
                token = L_class_Token.Token(token_type, int(token_value))
                in_vertice = int(in_vertice)
                out_vertice = int(out_vertice)
                edge = {'symbol': token, 'out_vertice': out_vertice}
                lgraph.add_link(in_vertice, edge)
                    
        return lgraph

    def add_bracket_marks(self):
        if self.bracket_marks_filename != None:
            with open(self.bracket_marks_filename) as fh:
                for line in fh:
                    temp = line.strip().split()
                    if len(temp) == 5:
                        if temp[2] == ID:                           
                            in_vertice, out_vertice, token_type, token_value, one_bracket = temp
                            in_vertice = int(in_vertice)
                            out_vertice = int(out_vertice)
                            token = L_class_Token.Token(token_type, int(token_value))
                            bracket_mark = (in_vertice, out_vertice, token, one_bracket)
                            if DEBUG:
                                print('1--------- bracket_mark =  ', bracket_mark)
                            self.lgraph.add_d_sets(bracket_mark)
                           
                        else :      # temp[2] != ID:
                            in_vertice, out_vertice, token_symbol, closing_bracket, open_bracket = temp
                            
                            if DEBUG:
                                print('temp = ', temp)
                            
                            if token_symbol.isdigit():
                                token_symbol = int(token_symbol)
                                if DEBUG:
                                    print(isinstance(token_symbol, int))                              
                            if isinstance(token_symbol, int):                               
                                token = L_class_Token.Token(INTEGER_CONST, token_symbol)
                                if DEBUG:
                                    print('token = ', token)
                                    print('in_ver = {0}, out_ver = {1}, clos = {2}, open = {3}'.
                                         format(in_vertice, out_vertice,
                                                closing_bracket, open_bracket))                               
                              
                            else:
                                token = self.make_token_from_token_name(token_symbol)
                                print()
                                
                            bracket_mark = (in_vertice, out_vertice, token,
                                            closing_bracket, open_bracket)
                            if DEBUG:
                                print('bracket_mark = ', bracket_mark)


                            self.lgraph.add_d_sets(bracket_mark)
                            
                    elif len(temp) == 6:
                        if temp[2] == ID:
                            in_ver, out_ver, token_type, token_value, closing_bracket, open_bracket = temp
                            in_vertice = int(in_ver)
                            out_vertice = int(out_ver)
                            token = L_class_Token.Token(token_type, int(token_value))
                            bracket_mark = (in_vertice, out_vertice, token,
                                            closing_bracket, open_bracket)
                            self.lgraph.add_d_sets(bracket_mark)
                    
                        
    def print_bracket_marks(self):
        marks = self.lgraph.d_sets
        marks_lst = list(marks)
        for item in marks:
            print(item)

    def write_lgraph_to_file(self):
        '''
        The method displays the name of the .txt file,
        where the representation of the L-graph is written.

        '''      
        ll = self.links
        start_vertices = self.lgraph.start_vertices
        finish_vertices = self.lgraph.finish_vertices
        filename_to_write_lgraph = (self.filename.split('.')[0]
                                     + '_total_lgraph_' + '.txt')

        try:
            with open(filename_to_write_lgraph, 'w') as fh:
                fh.write(str(start_vertices) + '\n')
                str_finish_vertices = ' '.join(str(v) for v in finish_vertices)
                fh.write('{' + str_finish_vertices + '}' +'\n')

                print()

                bracket_set = self.lgraph.d_sets
                for item in bracket_set:
                    if DEBUG:
                        print('---', item)
                    if len(item) == 4:
                        in_vertice, out_vertice, token, one_bracket = item
                        s = (str(in_vertice) + ' ' + str(out_vertice) + ' '
                             + token.type + ' ' + str(token.value) + ' '
                             + one_bracket)
                        fh.write(s + '\n')

                    elif len(item) == 5:
                        in_vertice, out_vertice, token, closing_bracket, open_bracket = item
                        s = (str(in_vertice) + ' ' + str(out_vertice) + ' '
                             + token.type + ' ' + str(token.value) + ' '
                             + closing_bracket + ' ' + open_bracket)
                        fh.write(s + '\n')
                        
                fh.write('#\n')
                                
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
            filename_to_write_lgraph))


def main1():
    brackets_filename = 'brackets2.txt'
    lgraph_representation_filename = 'combine_two_files.txt'
    lgraph_obj = Make_Total_Lgraph(lgraph_representation_filename,
                                   brackets_filename)
    lgraph = lgraph_obj.lgraph
    lgraph.print_lgraph()
    lgraph_obj.print_bracket_marks()
    lgraph_obj.write_lgraph_to_file()


def main2():
    brackets_filename = 'brackets2.txt'
    lgraph_representation_filename = 'combine_two_files.txt'
    lgraph_object  = Make_Total_Lgraph(lgraph_representation_filename,
                                       brackets_filename)
    lgraph = lgraph_object.make_lgraph()
    lgraph_object.print_lgraph()
    ll = lgraph_object.links
    lgraph_object.print_links()
    lgraph_object.add_bracket_marks()
    lgraph_object.print_bracket_marks()
    lgraph_object.write_lgraph_to_file()

def main():

    brackets_filename = 'brackets2.txt'
    lgraph_representation_filename = 'combine_two_files.txt'
    lgraph_object  = Make_Total_Lgraph(lgraph_representation_filename,
                                       brackets_filename)
    ll = lgraph_object.lgraph

    lgraph_object.print_lgraph()
    print()
    ll = lgraph_object.links

    for key, value in ll.items():
        print(key, value)


    
if __name__ == '__main__':
    main()
























