import ivy_transrel
import ivy_logic as il
import ivy_logic_utils as ilu
import logic as lg
from ivy_solver import get_small_model
import ivy_module as im
from ivy_interp import State,EvalContext,reverse,decompose_action_app
from proof import ProofGoal
from ivy_logic_utils import Clauses, and_clauses, dual_clauses
from random import randrange
from ivy_art import AnalysisGraph, render_rg
import ivy_web_utils

# TODO: refactor to remove
class Thing(object):
    def __init__(self,value):
        self.value = value

compile_kwargs = {'ext':'ext'}

# TODO: check about relations_to_minimize
def check_inductiveness(art, conjectures):

    
    ag = AnalysisGraph()

    pre = State()
    pre.clauses = and_clauses(*conjectures)

    action = im.module.actions['ext']
    with EvalContext(check=False): # don't check safety
        post = ag.execute(action, pre, None, 'ext')
    post.clauses = ilu.true_clauses()

    to_test =  [None] + list(conjectures)  # None = check safety

    while len(to_test) > 0:
        # choose randomly, so the user can get another result by
        # clicking again
#                conj = to_test.pop(randrange(len(to_test)))
        conj = to_test.pop(0)
        assert conj == None or conj.is_universal_first_order()
        used_names = frozenset(x.name for x in il.sig.symbols.values())
        def witness(v):
            c = lg.Const('@' + v.name, v.sort)
            assert c.name not in used_names
            return c
        
        relations_to_minimize = Thing('relations to minimize')
        transitive_relations = []

        # TODO: this is still a bit hacky, and without nice error reporting
        if relations_to_minimize.value == 'relations to minimize':
            relations_to_minimize.value = ' '.join(sorted(
                k for k, v in il.sig.symbols.iteritems()
                if (type(v.sort) is lg.FunctionSort and
                    v.sort.range == lg.Boolean and
                    v.name not in transitive_relations 
#                            and '.' not in v.name
                )
            ))

        if conj == None: # check safety
            clauses = ilu.true_clauses()
            rels_to_min = [il.sig.symbols[x] for x in relations_to_minimize.value.split()]
        else:
            clauses = dual_clauses(conj, witness)
            history = ag.get_history(post)
            rels_to_min = []
            for x in relations_to_minimize.value.split():
                relation = il.sig.symbols[x]
                relation = history.maps[0].get(relation, relation)
                rels_to_min.append(relation)
                
        _get_model_clauses = lambda clauses, final_cond=False: get_small_model(
            clauses,
            sorted(il.sig.sorts.values()),
            rels_to_min,
            final_cond = final_cond
        )

        if conj == None:
            res = ag.check_bounded_safety(post, _get_model_clauses)
        else:
            res = ag.bmc(post, clauses, None, None, _get_model_clauses)

        if res is not None:
            current_conjecture = conj
            assert len(res.states) == 2

            return (res, ag)

def serve(art):
    if not hasattr(art, 'state_graphs'):
        art.state_graphs = []

    conjectures = im.module.conjs
    # print render_rg(art).elements

    ag = check_inductiveness(art, conjectures)[0]

    # print ag
    print ivy_web_utils.cy_elements_to_json(render_rg(ag).elements)