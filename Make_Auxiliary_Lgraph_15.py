import json
import Make_Lgraph_15
import L_class_Lgraph
import L_class_Token

ID = 'ID'



class Make_Auxiliary_Lgraph(Make_Lgraph_15.Make_Lgraph):
    def __init__(self,  sample_solution_filename, start_vertice=0,
                 start_token_number=1):
        super().__init__(sample_solution_filename, start_vertice)
        self.start_token_number = start_token_number

    def make_lgraph(self):
        ''''
        Constructs the L-graph according to the part of the solution
        and returns it.
        Can be applied as an auxiliary procedure for constructing the
        graph of the entire problem.
        '''

        current_lgraph = L_class_Lgraph.Lgraph()
        current_lgraph.add_start_vertice(self.start_vertice)

        for vertice_number in range(len(self.all_tokens)):
            in_vertice = vertice_number + self.start_vertice

            out_vertice = in_vertice + 1
            token = self.all_tokens[vertice_number]

            if token.type == ID:
                new_token_value = token.value + self.start_token_number
                
                new_token = L_class_Token.Token(ID, new_token_value)
                link = {'symbol': new_token,'out_vertice': out_vertice}
            else:
                link = {'symbol': token,'out_vertice': out_vertice}
            current_lgraph.add_link(in_vertice, link)

        return current_lgraph



def main():
    filename = 'task1_second.pas'
    l = Make_Auxiliary_Lgraph( filename, 119)
    print('start_vertice = ', l.start_vertice)
    print('start = ', l.start_token_number)
    
    print(l.get_sample_solution_text())
    print(l.get_all_tokens_from_solution_text())
    l.print_lgraph()
    l.write_lgraph_to_file()



if __name__ == '__main__':
    main()
