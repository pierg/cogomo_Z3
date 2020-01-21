import argparse
import os
from random import randint
import textwrap
import csv
import random
import string

parser = argparse.ArgumentParser()

parser.add_argument('--cmin', help='# components min', type= int, default= 10)
parser.add_argument('--cmax', help='# components max', type= int, default= 100)
parser.add_argument('--pmin', help='# propositions min', type= int, default= 2)
parser.add_argument('--pmax', help='# propositions max', type= int, default= 20)
parser.add_argument('--cstep', help='step size component', type= int, default= 10)
parser.add_argument('--pstep', help='step size propositions', type= int, default= 2)
parser.add_argument('--cxstep', help='coefficient determing the next step', type= int, default= -1)
parser.add_argument('--pxstep', help='coefficient determing the next step', type= int, default= -1)
parser.add_argument('--ratio', help='ratio of propositions r: # = n_props*n_comps / r', type= int, default= 2)
parser.add_argument('--nexp', help='number of experiments for each configuration', type= int, default= -1)

try:
    args = parser.parse_args()
except Exception:
    print("Using Default Arguments")

filepath = os.getcwd()

idname = ''.join([random.choice(string.ascii_letters
            + string.digits) for n in range(4)])

evaluation_folder = os.path.dirname(os.path.abspath(__file__)) + "/evaluation"



if not os.path.exists(evaluation_folder):
    os.makedirs(evaluation_folder)

result_folder_id = "/results/res_" + str(args.pmin) + "." + \
                    str(args.pmax) + "." + str(args.pstep) + "_" + str(args.cmin) + "." + str(args.cmax) + "." +\
                    str(args.cstep) + "_" + idname

result_folder = evaluation_folder + result_folder_id


def gen_file(n_props, n_comps):
    file_name = "case_" + str(n_props) + "_" + str(n_comps) + ".py"
    with open(evaluation_folder + "/" + file_name, 'w') as f:
        f.write(textwrap.dedent('''\
            from src.operations import *
            import time
            import statistics

            component_library = ComponentsLibrary(name="cogomo")

                '''))
        n_props_total = int(n_props * n_comps / args.ratio)
        for x in range(0, n_props_total + 1):
            f.write(textwrap.dedent('''\
                p{0} = Bool('p{1}')
                ''').format(x, x))

        f.write(textwrap.dedent('''\
        
            component_library.add_components(
                [
                        '''))

        list_of_guarantees = []

        for i in range(0, n_comp):
            f.write('\t\tComponent(id=')
            f.write('"c{0}", assumptions=['.format(i))
            n_ag = int(n_props / 2)
            assumptions_chosen = []
            # writing the assumptions
            for p in range(0, n_ag):
                assumption_chosen = randint(0, n_props_total)
                assumptions_chosen.append(assumption_chosen)
                f.write('p{0}'.format(assumption_chosen))
                f.write(' == True')
                if p != n_ag - 1:
                    f.write(', ')
            f.write('], guarantees=[')
            # writing the guarantees
            for p in range(0, n_ag):
                g_gen = random.choice([i for i in range(0, n_props_total) if i not in assumptions_chosen])
                list_of_guarantees.append(g_gen)
                f.write('p{0}'.format(g_gen))
                f.write(' == True')
                if p != n_ag - 1:
                    f.write(', ')
            f.write('])')
            if i != n_comps - 1:
                f.write(',\n')
        f.write('\n\t])\n\n')

        list_of_guarantees = list(set(list_of_guarantees))

        f.write(textwrap.dedent('''\
                        def run_{0}_{1}():
                                                
                        ''').format(n_props, n_comps))

        f.write("    times = {}\n")
        f.write("    all_times = {}\n")
        f.write("    weighted_all_times = {}\n")

        pool_of_guarantees = list_of_guarantees
        if args.nexp != -1:
            pool_of_guarantees = random.sample(list_of_guarantees, args.nexp)

        for i, g in enumerate(pool_of_guarantees):
            f.write("    print('')\n".format(n_prop, n_comp))
            f.write("    print('')\n".format(n_prop, n_comp))
            f.write("    print('Starting evaluation for {0} propositions and {1} components "
                    "looking for proposition {2}/{3} (p{4})')"
                    "\n".format(n_prop, n_comp, i+1, len(pool_of_guarantees), g))
            f.write("    start_time = time.time()\n")
            f.write("    n = len(mapping(component_library, "
                    "Contract(assumptions=[], guarantees=[p{0} == True])))\n".format(str(g)))
            f.write("""\
    elapsed_time = time.time() - start_time
    all_times["{0}_{1}_p{2}"] = elapsed_time
    weighted_all_times["{0}_{1}_p{2}"] = elapsed_time / n
    
    if n in times:
        times[n].append(elapsed_time)
    else:
        times[n] = [elapsed_time]
                    """.format(n_prop, n_comp, g))
            f.write("\n\n")

        f.write("    return times, all_times, weighted_all_times\n\n")

        f.write(textwrap.dedent('''\

                        if __name__ == '__main__':
                            run_{0}_{1}()
                        ''').format(n_props, n_comps))


def elaborate(folder, mean_match_times, mean_values, weighted_values, all_values):

    with open(folder + '/mean_values.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(mean_values.items())

    with open(folder + '/weighted_values.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(weighted_values.items())

    with open(folder + '/all_values.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(all_values.items())

    with open(folder + '/mean_match_times.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(mean_match_times.items())

    n_match_set = set()
    for combination, results in mean_match_times.items():
        for n_match in results.keys():
            n_match_set.add(n_match)

    n_match_set = list(n_match_set)

    with open(folder + '/match_times.csv', 'w') as f:

        for n_match in range(1, max(n_match_set)+1):
            f.write(str(n_match) + ",")
            for i, (combination, results) in enumerate(mean_match_times.items()):
                if n_match in results.keys():
                    f.write(str(results[n_match]))
                if i < len(mean_match_times) -1:
                    f.write(",")
                else:
                    f.write("\n")
    print("Data Saved")


def logtofile(folder, message):
    pass



if __name__ == '__main__':

    os.makedirs(evaluation_folder + result_folder_id)

    run_file_name = "run_all.py"

    n_props = []
    n_comps = []

    p = args.pmin

    if (args.pxstep != -1):
        i = args.pmin
        while(i <= args.pmax):
            n_props.append(i)
            i = i * args.pxstep
    else:
        for i in range(int((args.pmax-args.pmin)/args.pstep)+1):
            n_props.append(p)
            p += args.pstep

    c = args.cmin

    if (args.cxstep != -1):
        i = args.cmin
        while(i <= args.cmax):
            n_comps.append(i)
            i = i * args.cxstep
    else:
        for i in range(int((args.cmax-args.cmin)/args.cstep)+1):
            n_comps.append(c)
            c += args.cstep

    main_flag = False

    with open(evaluation_folder + "/" + run_file_name, 'w') as rf:

        rf.write("import sys\nsys.path.append('../src')\n")

        for n_prop in n_props:
            for n_comp in n_comps:
                gen_file(n_prop, n_comp)
                rf.write("from case_{0}_{1} import *\n".format(n_prop, n_comp))

        rf.write("\nfrom statistics import mean\nfrom evaluation_generator import *\n\n\n")

        rf.write("""\
if __name__ == '__main__':
    mean_match_times = {}
    mean_values = {}
    weighted_values = {}
    all_values = {}
                 """)
        rf.write("\n\n")


        for n_prop in n_props:
            for n_comp in n_comps:

                rf.write("    logtofile('{0}','starting {1}_{2}...')\n".format(result_folder, n_prop, n_comp))

                rf.write("""\
    match_times_{0}_{1}, all_times_{0}_{1}, weighted_all_times_{0}_{1} = run_{0}_{1}()
    for key, value in match_times_{0}_{1}.items():
        match_times_{0}_{1}[key] = mean(value)
    all_values.update(all_times_{0}_{1})
    mean_match_times["{0}_{1}"] = match_times_{0}_{1}
    mean_values["{0}_{1}"] = mean(list(all_times_{0}_{1}.values()))
    weighted_values["{0}_{1}"] = mean(list(weighted_all_times_{0}_{1}.values()))
                    """.format(n_prop, n_comp))
                rf.write("\n")
                rf.write("    logtofile('{0}','finished {1}_{2}')\n".format(result_folder, n_prop, n_comp))
                rf.write("    elaborate('{}',mean_match_times, mean_values, weighted_values, all_values)\n".format(result_folder))
                rf.write("\n\n")

        rf.write("    print('--------FINISHED--------')")

