import re

def normalize_spaces(s: str) -> str:
    s = re.sub(r'\s*([/\\\\\/\-~\->()])\s*', r'\1', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

def rem_cl(s: str) -> str:
    while '(' in s:
            clauese_index = s.index('(')
            s = s[:clauese_index] + s[clauese_index + 1:]
    while ')' in s:
        clauese_index = s.index(')')
        s = s[:clauese_index] + s[clauese_index + 1:]
    return s

def del_2neq(s: str) -> str:
    neg_count = s.count('~')
    if neg_count > 1:
        s = s[neg_count:] if neg_count % 2 == 0 else s[neg_count - 1:]
    return s

def to_dnf(parsed_cnf: str) -> str:
        while '->' in parsed_cnf:
            arrow_index = parsed_cnf.index('->')
            left = parsed_cnf[:arrow_index]
            right = parsed_cnf[arrow_index + 2:]
            parsed_cnf = '~' + left + '\\/' + right
        return parsed_cnf

def parse_cnf(s: str) -> list[str]:

    if type(s) != str: raise Exception('Form must be a str')
    parsed_cnf = normalize_spaces(s)
    # print(parsed_cnf)
    parsed_cnf = parsed_cnf.split('/\\')
    for i in range(len(parsed_cnf)):

        parsed_cnf[i] = to_dnf(parsed_cnf[i])
        # print(parsed_cnf)
        parsed_cnf[i] = rem_cl(parsed_cnf[i])
        parsed_cnf[i] = parsed_cnf[i].split('\\/')
        for k in range(len(parsed_cnf[i])):
            parsed_cnf[i][k] = del_2neq(parsed_cnf[i][k])
        
    return parsed_cnf

def dpll(clauses, variables, assignment=None):
    if assignment is None:
        assignment = {}

    if [] in clauses:
        return None

    if not clauses:
        
        for var in variables:
            if var not in assignment:
                assignment[var] = None  
        return assignment

    
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    while unit_clauses:
        unit = unit_clauses.pop()
        if unit not in assignment and f'~{unit}' not in assignment:
            if unit[0] == '~':
                assignment[unit[1]] = False  
            else:
                assignment[unit] = True  
            clauses = simplify(clauses, unit)
            unit_clauses = [c[0] for c in clauses if len(c) == 1]

    for clause in clauses:
        for literal in clause:
            if literal not in assignment and f'~{literal}' not in assignment:
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                new_clauses = simplify(clauses, literal)
                result = dpll(new_clauses, variables, new_assignment)
                if result is not None:
                    return result
                
                new_assignment = assignment.copy()  
                new_assignment[literal] = False
                new_clauses = simplify(clauses, f'~{literal}')
                result = dpll(new_clauses, variables, new_assignment)
                if result is not None:
                    return result

    return None  

def simplify(clauses, literal):
    new_clauses = []
    for clause in clauses:
        if literal in clause:
            continue  
        new_clause = [l for l in clause if l != f'~{literal}']
        new_clauses.append(new_clause)
    return new_clauses



def is_satisfiable(cnf: str) -> bool:
    clauses = parse_cnf(cnf)
    variables = set(var.lstrip('~') for clause in clauses for var in clause)  
    return dpll(clauses, variables) is not None

def sat_assignment(cnf: str) -> dict:
    clauses = parse_cnf(cnf)
    variables = set(var.lstrip('~') for clause in clauses for var in clause)  
    assignment = dpll(clauses, variables)
    
    if assignment is None:
        return None
    

    result = {}
    for var in variables:
        if var in assignment:
            result[var] = assignment[var]
        else:
            result[var] = False  

    return result
