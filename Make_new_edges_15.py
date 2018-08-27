import json
import L_class_Lgraph
import Make_Lgraph_15
import Make_Auxiliary_Lgraph_15
import L_class_Token
import lexem_value_tables

ID = 'ID'
INTEGER_CONST = 'INTEGER_CONST'
EOF = 'EOF'


class Make_New_Edges:
    '''
    Reads vertex numbers and a symbol mark for additional edges from
    the txt file, converts the symbol mark to the
    Token (token.type, token.value) and writes the receiving
    representation of edges into the text file.     
    '''
    def __init__(self, additional_edges_filename):
        self.edges_filename = additional_edges_filename

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

    def make_additional_edges(self):
        print(self.edges_filename)
        output_filename = self.edges_filename.split('.')[0] + '_new_edges.txt'
        print('output_filename = ', output_filename)
       
        with open(self.edges_filename) as fh:
            with open(output_filename, 'w') as wr:

                for line in fh:
                    temp = line.strip().split()


                    if len(temp) == 4:
                        in_ver, type_symbol, value, out_ver = temp
                        print(in_ver, type_symbol, value, out_ver)
                        value = int(value)

                        if type_symbol == ID:
                            token = L_class_Token.Token(type_symbol, value)
                        else:
                            token = self.make_token_from_token_name(type_symbol)

                        string = (in_ver + ' ' + token.type + ' ' +
                                  str(token.value) + ' ' + out_ver + '\n')
                        wr.write(string)

                    elif len(temp) == 3:
                        in_ver, type_symbol, out_ver = temp
                        if type_symbol.isdigit():
                            type_symbol = int(type_symbol)
                        if isinstance(type_symbol, int):
                            token = L_class_Token.Token(INTEGER_CONST,
                                                        type_symbol)
                        else:
                            token = self.make_token_from_token_name(type_symbol)

                        string = (in_ver + ' ' + token.type + ' '
                                  + str(token.value)
                                  + ' ' + out_ver + '\n')

                        wr.write(string)


def main():
    additional_edges_filename = 'additional_edges_task1.txt'
    z = Make_New_Edges(additional_edges_filename)
    z.make_additional_edges()

    
if __name__ == '__main__':
    main()









