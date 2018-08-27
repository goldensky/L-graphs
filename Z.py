import json
import Make_Lgraph_15
import Make_Auxiliary_Lgraph_15
import Make_total_Lgraph_15
import L_class_Token
import lexem_value_tables
import Lexer_5
import Make_Lgraph_from_total_file_15



DEBUG_DEBUG = 0
DEBUG = 1
DEBUG_VAR = 1

EOF = 'EOF'
ID = 'ID'
VAR = 'VAR'
SEMI = 'SEMI'

       
class IncompatibilityLgraphStructure(Exception):
    '''
    Exception raises when a discrepancy between the structure
    of the problem solution to the structure of the graph
    is detected.   
    '''
    def __init__(self, message):
        self.message = message
        self.finish()
        
    def finish(self):
        raise StopRunProgram('The end! Structure of your program is not right!')


class FindForbiddenLexem(Exception):
    '''
    An exception raises  when the forbidden lexemes is detected 
    in the solution of a problem.
    '''
    def __init__(self, message):
        self.message = message
        self.finish()
        
    def finish(self):
        raise StopRunProgram('The end! Forbidden lexem was found!')

           
class FindUnexpectedLexem(Exception):
    '''
    An exception raises when the lexemes that do not provided by
    the standard Pascal is detected in the problem solution.     
    Lexer_5.flag_Unexpected_Lexem
    '''
    def __init__(self, message):
        self.message = message
        self.finish()
        
    def finish(self):
        raise StopRunProgram('!The end! Unexpected lexem was found!' )


        
class StopRunProgram(Exception):
    '''
    Raises when an exception of IncompatibilityLgraphStructure,
    FindForbiddenLexem, FindUnexpectedLexem is detected.
    '''
    def __init__(self, message):
        self.message = message
        self.finish()

    def finish(self):
        raise SystemExit(1)

class Analyser:
    def __init__(self, sample_lgraph, student_solution_filename,
                 task_restriction_file=None):
        self.lgraph = sample_lgraph
        self.student_solution_filename = student_solution_filename
        self.task_restriction_file = task_restriction_file
        self.solution_text = self.get_student_solution_text()
        self.forbidden_lexems = self.get_forbidden_lexems_list()

        self.flag_var_declare_section = False
        self.flag_FindForbiddenLexem = False
        self.flag_IncompatibilityLgraphStructure = False

        self.flag_return = False

        self.content_table = []
        self.lexer = Lexer_5.Lexer(self.solution_text)
        self.current_token = self.lexer.get_next_token()
        self.all_tokens = self.get_all_tokens()

    def get_student_solution_text(self):
        '''
        Returns the text of the solution to the problem
        written by the student.
        '''
        with open(self.student_solution_filename) as fh:
            text = fh.read()           
        return text

    def get_forbidden_lexems_list(self):
        '''
        Returns the list of the forbidden tokens or an empty list.
        '''
        if self.task_restriction_file != None:
            with open(self.task_restriction_file) as fh:
                json_forbidden_lexems = fh.read()
            forbidden_dict = json.loads(json_forbidden_lexems)
            forbidden_lexems_list = forbidden_dict["forbidden"]
        else:
            forbidden_lexems_list = []
        return forbidden_lexems_list

    def get_all_tokens(self):
        all_tokens = []
        try:
            if self.current_token.type.lower()  in self.forbidden_lexems:
                self.flag_FindForbiddenLexem = True
                print('Forbidden Lexem {0} was found in {1} string'.format(
                        self.current_token, self.lexer.line_number))
                raise FindForbiddenLexem('Forbidden Lexem {0} was found in {1} '
                    'string'.format(self.current_token, self.lexer.line_number))
            
            elif Lexer_5.flag_Unexpected_Lexem:
                raise FindUnexpectedLexem(
                    '_Find Unexpected Lexem {0} in {1} string'.format(
                        self.lexer.current_char, self.lexer.line_number))
            else:
                all_tokens.append(self.current_token)  # first token

            while self.current_token.type != EOF:
                self.current_token = self.lexer.get_next_token()               
                #
                if self.flag_var_declare_section  == True:
                    if self.current_token.type == 'SEMI':                       
                        self.flag_var_declare_section = False
                    else:
                        if self.current_token.type == ID:
                            if DEBUG_VAR:
                                print('Declare ', self.current_token)
                            self.content_table.append(self.current_token)
                            
                else:   #  self.flag_var_declare_section == False
                    
                    if self.current_token.type == VAR:
                        self.flag_var_declare_section = True               
                if self.current_token.type.lower()  in self.forbidden_lexems:
                    self.flag_FindForbiddenLexem = True
                    
                    print('Forbidden Lexem {0} was found in {1} string'.format(
                        self.current_token, self.lexer.line_number))                   
                    raise FindForbiddenLexem('Forbidden Lexem {0} was found in '
                        '{1} string'.format(self.current_token,
                                            self.lexer.line_number))
                
                # Unexpected_Lexem
                elif Lexer_5.flag_Unexpected_Lexem:
                    raise FindUnexpectedLexem(
                        '_Find Unexpected Lexem {0} in {1} string'.format(
                            self.lexer.current_char, self.lexer.line_number))
                else:
                    all_tokens.append(self.current_token)

        except FindUnexpectedLexem as err1:
            print(err1)
            print('!!!   flag_Unexpected_Lexem = ',
                  Lexer_5.flag_Unexpected_Lexem)

            raise StopRunProgram

        except FindForbiddenLexem as err2:
            print('Forbidden Lexem {0} was found in {1} string'.format(
                self.current_token, self.lexer.line_number))
            raise StopRunProgram

        if all_tokens[-1].type == EOF:
            all_tokens.pop()
        return all_tokens       

    def func(self):
        links = self.lgraph.lgraph.links

        
        in_trace = []  # пройденный путь (содержит пройденные вершины in_vertice)

        # список возможных путей для возврата (содержит список дуг)
        stack_edges = []   # main stack of resources

        # в стек lexem_numbers записываются номера лексем из списка лексем из
        # программы студента - они соответствуют возможным путям возврата из stack_edges
        lexem_numbers = []   # номера лексем студента для возможных путей из стека возможностей

        
        # B - список скобочных пометок, соответствующих возможным путям из  stack_edges
        B = []

        # стек скобочных пометок (содержит одну скобочную пометку (вида [1 или [2 ),
        # показывающую по какой дуге из помеченных возможных ищется путь решения
        # путь по индексам скобочных пометок
        stack_brackets = []
        
        # 1
        current_in_vertice = start_in_vertice = 0
        current_out_vertice = 0
        student_token_number = 0

        last_path = None            #  последняя дуга , по которой только что прошли
        last_bracket_mark = None    #  скобочная пометка последней пройденной только что дуги
        BM = []                     #   для записи скобочных пометок дуг, по которым уже прошли
        stack_return = []           #   стек пройденных неуспешных дуг

        EF = []                     #  стек дуг с соответствием по лексеме, по которым не ходили
                                    #  (возможные пути)


        d_sets_list = list(self.lgraph.lgraph.d_sets)
        d_sets_list.sort(key = lambda e: e[0])

        in_vertice_with_brackets_list = []

        for item in d_sets_list:
            in_vertice_with_brackets_list.append(item[0])           

        try:
            while current_out_vertice  not in self.lgraph.lgraph.finish_vertices:
                #  2  список всех исходящих дуг
                edges = links[current_in_vertice]
                
                # 3  лексема студента 
                student_token = self.all_tokens[student_token_number]
                if DEBUG:
                    print()
                    print('--' * 30)
                    print('in = {0}'.format(current_in_vertice))
                    print('Лексема студента     student_token = {0}'.format(student_token))

                    
                #  заглядываем вперед на одну лексему
                #student_token_advance = self.all_tokens[student_token_number+1]

                # 4                  
                # локальный стек дуг, исходящих из этой вершины
                # (если символьная пометка дуги совпадает с лексемой из программы студента)
                stack_local = []
                if DEBUG:
                    print('\nВсе дуги в текущей вершине')
                for edge in edges:
                    if DEBUG:
                        print(edge)
                                              
                    symbol = edge['symbol']
                    out_vertice = edge['out_vertice']
                    if str(symbol) == str(student_token):
                        stack_local.append(edge)
                        
                # 5
                # скобочные пометки в данной вершине
                local_brackets_list = []

                for number in range(len(in_vertice_with_brackets_list)):
                    if in_vertice_with_brackets_list[number] == current_in_vertice:
                        local_brackets_list.append(d_sets_list[number])
                        if DEBUG:
                            print('We have brackets in this in_vertice! ', d_sets_list[number])
                if DEBUG:
                    print('\nлокальный стек дуг, исходящих из этой вершины, при совпадении с лексемой  из анализируемой программы студента')
                    print('stack_local = {0}\n'.format(stack_local))

                if DEBUG:
                    if len(local_brackets_list) == 0:
                        print('\n\nСкобочных пометок на текущей дуге   нет ')
                        print('local_brackets_list = {0}'.format(local_brackets_list))

                    elif len(local_brackets_list) > 0:
                        print('\nЕсть скобочные пометки  на текущих дугах ')
                        print('local_brackets_list = ')
                        for item in local_brackets_list:
                            print(item)

                # 6 есть путь по дугам
                if len(stack_local) > 0:
                    if DEBUG:
                        print('')
                        print('stack_local = ', stack_local)
                        print('******************')
                    
                    # 6.1   скобочных пометок нет
                    if len(local_brackets_list) == 0:
                        if DEBUG:
                            print('\n\nСкобок нет\n\n')
                        current_edge = stack_local.pop()
                        symbol = current_edge['symbol']
                        out_vertice = current_edge['out_vertice']
                        in_trace.append(current_in_vertice)
                        current_out_vertice = out_vertice
                        last_path = current_edge
                        if DEBUG:
                            print('!!!     out = ', current_out_vertice)
                      
                    # 6.2   скобочные пометки    есть 
                    elif len(local_brackets_list) > 0:
                        if DEBUG:
                            print('------------    in = ', current_in_vertice)
                            print('stack_brackets  = ', stack_brackets )
                        
                        # 6.2.1  стек скобок пуст --     начало пути по индексам скобок
                        if len(stack_brackets) == 0:
                            if DEBUG:
                                print('\n\n     начало пути по индексам скобок\n\n\n')                           
                            #6.2.1.1
                            # взять дугу  из стека
                            current_edge = stack_local.pop()
                            edge_symbol = current_edge['symbol']
                            edge_out_vertice = current_edge['out_vertice']
                            print('взяли дугу      current_edge = ', current_edge)
                            #6.2.1.2   сохранить оставшиеся дуги в стек возможностей
                            if len(stack_local) > 0:   #  
                                while len(stack_local) > 0:
                                    temp = stack_local.pop()
                                    stack_edges.append(temp)
                                    
                            if DEBUG:
                                print('В стеке дуг для вoзможного возврата   stack_edges = ', stack_edges)
                                print('Номера лексем для возврата           lexem_numbers = ', lexem_numbers)
                                print('\n\n  ищем индекс на этой дуге')
                                print('current_edge = ', current_edge)
                                print('local_brackets_list = ', local_brackets_list)                               
                            #6.2.1.3   
                            for bracket_mark in local_brackets_list:
                                if DEBUG:
                                    print('------------ bracket_mark = ', bracket_mark)
                                #  установить соответствие между дугой и ее скобочной пометкой
                                if len(bracket_mark) == 4:
                                    br_in_vertice, br_out_vertice, br_token, br_one_bracket = bracket_mark
                                    if DEBUG:
                                        print('\n 4  bracket_mark = ', bracket_mark)
                                    if str(br_token) == str(edge_symbol):
                                        if edge_out_vertice == br_out_vertice:
                                            if DEBUG:
                                                print('current_edge, bracket_mark = ', current_edge, bracket_mark)
                                            if br_one_bracket[0] == '[':
                                                if DEBUG:
                                                    print('[', current_in_vertice , current_out_vertice)
                                                stack_brackets.append(br_one_bracket)  # 6.2.1.3 индекс маршрута
                                                
                                                current_out_vertice = out_vertice        # 6.2.1.4.
                                                in_trace.append(current_in_vertice)       # 6.2.1.5.
                                                last_path = current_edge    # last   6.2.1.6.
                                                break                                               
                            #   6.2.1.7.
                            if DEBUG:
                                print('Маршрут по скобкам     stack_brackets = ', stack_brackets)
                            position = local_brackets_list.index(bracket_mark)
                            local_brackets_list.pop(position)
                                                       
                            #6.2.1.8                          
                            if len(local_brackets_list) > 0:
                                while len(local_brackets_list) > 0:
                                    temp = local_brackets_list.pop()
                                    B.append(temp)
                                    lexem_numbers.append(student_token_number)   # 6.2.1.9.
                                                  
                        # 6.2.2    стек скобок  не  пуст --   уже  есть номер маршрута                         
                        elif len(stack_brackets) > 0:
                            if DEBUG:
                                #if student_token_number < len(self.all_tokens) - 1:
                                    #print('student_token_advance = ', student_token_advance)
                                print('\n\nself_flag_return = ', self.flag_return)
                                print('\n\n в стеке  скобок   уже  есть номер маршрута \n\n')
                                print('stack_brackets = ', stack_brackets)
                                print('stack_local = ', stack_local)
                            #
                            #  6.2.2.1
                            #   Установить соответствие между дугами и их скобочными пометками  
                            for temp_edge in stack_local:
                                temp_edge_symbol = temp_edge['symbol']
                                temp_edge_out_vertice = temp_edge['out_vertice']
                                for temp_bracket in local_brackets_list:

                                    # 6.2.2.1.1
                                    if len(temp_bracket) == 4:
                                        if DEBUG:
                                            print('\n\n\n\n4   ]',   temp_bracket)
                                        br_in_vertice, br_out_vertice, br_token, br_one_bracket = temp_bracket
                                        q = stack_brackets[-1]
                                        q_number = q[1:]
                                        br_one_bracket_number = br_one_bracket[1:]
                                        if q_number == br_one_bracket_number:
                                            if str(temp_edge_symbol) == str(br_token):
                                                if temp_edge_out_vertice == br_out_vertice:
                                                    current_out_vertice = br_out_vertice
                                                    last_path = temp_edge   # last
                                                    last_bracket_mark = temp_bracket   # last
                                                    break
                                    # 6.2.2.1.2                                       
                                    elif len(temp_bracket) == 5:                                       
                                        if self.flag_return == True:
                                            if DEBUG:
                                                print('\n\n\n   stack_local = ', stack_local)
                                                print('\n\n\n\n\n   5   self.flag_return =  ', True)
                                                print('stack_return = ', stack_return)
                                                print('BM = ', BM)
                                                print('local_brackets_list = ', local_brackets_list)
                                        
                                        br_in_vertice, br_out_vertice, br_token, br_closing_bracket, br_open_bracket = temp_bracket
                                        if DEBUG:
                                            print('=======       temp_bracket = ', temp_bracket)
                                        if str(temp_edge_symbol) == str(br_token):
                                            if br_open_bracket == stack_brackets[-1]:
                                                if br_out_vertice == temp_edge_out_vertice:
                                                    if DEBUG:
                                                        print('temp_edge,  temp_bracket = ', temp_edge, temp_bracket)
                                                    current_out_vertice = br_out_vertice
                                                    in_trace.append(current_in_vertice)
                                                    stack_brackets.pop()
                                                    stack_brackets.append(br_open_bracket)
                                                    
                                                    last_path = temp_edge   #  last
                                                    last_bracket_mark = temp_bracket   # last
                                                    break
                                                      
                            #
                            #  6.2.2.2
                            position = local_brackets_list.index(temp_bracket)
                            
                            #  6.2.2.3
                            local_brackets_list.pop(position)
                            
                            #  6.2.2.4
                            for i in stack_return:
                                if i in stack_local:
                                    stack_local.pop(stack_local.index(i))

                            if len(stack_local) > 0:
                                while len(stack_local) > 0:
                                    temp = stack_local.pop()
                                    EF.append(temp)
                                    
                                    
                            if DEBUG:
                                print('\n\n    position = ', position)
                                print('local_brackets_list = ', local_brackets_list)
                                print('\n   stack_return = ', stack_return)
                                print('\nBM = ')
                                for item in BM:
                                    print(item)
                                    
                            #  6.2.2.5
                            for item in BM:   # BM  -- список скобочных пометок  пройденных дуг (при возврате)
                                if item in local_brackets_list:
                                    index = local_brackets_list.index(item)
                                    local_brackets_list.pop(index)
                            if DEBUG:
                                print('local_brackets_list = ', local_brackets_list)

                            #  6.2.2.6                           
                            if len(local_brackets_list) > 0:   #  
                                #if len(B) == 0:
                                while len(local_brackets_list) > 0:
                                    temp = local_brackets_list.pop()
                                    B.append(temp)

                                                             

                # 7 нет пути по дугам                   
                elif len(stack_local) == 0:
                    # 7.1
                    self.flag_return = True
                    # 7.2
                    stack_return.append(last_path)
                    # 7.3
                    BM.append(last_bracket_mark)
                    
                    if DEBUG:
                        print('Нет совпадения символьной пометки на дуге с лексемой студента')
                        print('\nСтек скобочных пометок   stack_brackets = ')
                        print(stack_brackets)
                        print('\nCтек возможностей - список дуг для возможного возврата по графу')
                        print('stack_edges = ', stack_edges)
                    # 7.4                        
                    # в стеке возможностей есть дуги для возврата
                    if len(stack_edges) > 0:
                        # 7.4.1
                        possible_way = stack_edges.pop()
                        symbol = possible_way['symbol']
                        out_vertice = possible_way['out_vertice']
                        if DEBUG:
                            print('possible_way = ', possible_way)
                            print('lexem_numbers = ', lexem_numbers)
                        # 7.4.2
                        current_out_vertice = out_vertice
                        # 7.4.3
                        student_token_number = lexem_numbers.pop()

                        if DEBUG:
                            print( 'out =    ', current_out_vertice)
                            print('student_token_number = ', student_token_number)
                            
                        # 7.4.4   найти новый индекс маршрута
                        for item in B:
                            #
                            if len(item) == 4:
                                    br_in_vertice, br_out_vertice, br_token, br_one_bracket = item
                                    if DEBUG:
                                        print('4    item = ', item)
                                    if str(symbol) == str(br_token):
                                        if out_vertice == br_out_vertice:
                                            path = item
                                            stack_brackets.pop()
                                            stack_brackets.append(br_one_bracket)
                                            if DEBUG:
                                                print('new bracket mark = ', br_one_bracket)
                                                print('NEW   NEW   stack_brackets  ', stack_brackets)
                                            break
                            # 7.4.5                                          
                            position = B.index(item)  # B - список скобочных пометок, соответствующих возможным путям из  stack_edges
                            B.pop(position)
                    # 7.5 
                    # в стеке возможностей нет  дуг для возврата
                    elif len(stack_edges) == 0:
                        print('Несоответствие структуры графа структуре задачи')
                        self.flag_IncompatibilityLgraphStructure = True
                        print('in_trace = ', in_trace)
                        break
                    
                # 8
                student_token_number += 1
                # 9
                current_in_vertice = current_out_vertice
                
                if DEBUG:
                    print()
                    print('--- ++++++ --------'* 5)
                    print('lexem_numbers = ', lexem_numbers)
                    print('stack_brackets = ', stack_brackets)                   
                    print('\nсписок скобочных пометок для  stack_edges')
                    print('B = ')
                    for item in B:
                        print(item)
                    print()
                    print('stack_edges = ', stack_edges)
                    print('------')
                    print('last_path = ', last_path)
                    print('last_bracket_mark = ', last_bracket_mark)
                    print('BM = ')
                    for item in BM:
                        print(item)

                    print('\nEF = ')
                    for item in EF:
                        print(item)

                    print('stack_return = ', stack_return)

                    print('*********' * 5)
                    print()
                    print('self.flag_return = ', self.flag_return)
                    print()
                    print('in_trace = ', in_trace)
                    #if student_token_number < len(self.all_tokens) - 1:
                        #print('student_token_advance = ', student_token_advance)

        except IncompatibilityLgraphStructure as err3:
            self.flag_IncompatibilityLgraphStructure = True
            if DEBUG:
                print('err3 = ', err3)
            
            if DEBUG:
                print('flag_IncompatibilityLgraphStructure = ',
                      self.flag_IncompatibilityLgraphStructure)
            raise StopRunProgram

        finally:
            flags = [self.flag_IncompatibilityLgraphStructure,
                 self.flag_FindForbiddenLexem,
                 Lexer_5.flag_Unexpected_Lexem]
            if DEBUG:
                print('--' * 25)
                print('flags = ', flags)
                print('\nstudent_solution_filename = {0}'.format(self.student_solution_filename))
                print('\nsolution_text: ')
                print(self.solution_text)
                
            # 10
            return (not any(flags))


# task1.pas  task1w.pas  task1_2.pas  task1_3.pas   task1_4.pas  task1_s.pas   --- True
# task.pas   task_not_1.pas   task1_struct.pas   task11.pas  task1f.pas   --- False


       
def main1():
    lgraph_representation_filename = 'combine_two_files_total_lgraph_.txt'

    lgraph = Make_Lgraph_from_total_file_15.Make_Lgraph_From_File(
        lgraph_representation_filename)
    
    forbidden1 = 't_frbd1.json'
    forbidden2 = 't_frbd2.json'
    lgraph.print_lgraph()
    print('-------\n\n')
    # t1.pas    task_041_2.pas  t2.pas   task_041_1.pas     t3.pas   t9   t8
    student_solution_filename = 'task_041_1.pas'
    a = Analyser(lgraph, student_solution_filename)    
    print('\nforbidden_lexems = ', a.forbidden_lexems)
    result = a.func()
    print('\n-------')
    print('result = ', result)



if __name__ == '__main__':
    main1()



                            
