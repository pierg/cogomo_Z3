import os
from random import randint
import textwrap
import csv

filepath = os.getcwd()

evaluation_folder = os.path.dirname(os.path.abspath(__file__)) + "/evaluation"

if not os.path.exists(evaluation_folder):
    os.makedirs(evaluation_folder)

if not os.path.exists(evaluation_folder + "/results"):
    os.makedirs(evaluation_folder + "/results")

def gen_file(n_props, n_comps):
    file_name = "case_" + str(n_props) + "_" + str(n_comps) + ".py"
    with open(evaluation_folder + "/" + file_name, 'w') as f:
        f.write(textwrap.dedent('''\
            from src.operations import *
            import time
            import statistics

            component_library = ComponentsLibrary(name="cogomo")

                '''))
        n_props_total = int(n_props * n_comps / 2)
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
            # writing the assumptions
            for p in range(0, n_ag):
                f.write('p{0}'.format(randint(0, n_props_total)))
                f.write(' == True')
                if p != n_ag - 1:
                    f.write(', ')
            f.write('], guarantees=[')
            # writing the guarantees
            for p in range(0, n_ag):
                g_gen = randint(0, n_props_total)
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

        for g in list_of_guarantees:
            f.write("    start_time = time.time()\n")
            f.write("    n = len(components_selection(component_library, "
                    "Contract(assumptions=[], guarantees=[p{0} == True])))\n".format(str(g)))
            f.write("""\
    elapsed_time = time.time() - start_time
    if n in times:
        times[n].append(elapsed_time)
    else:
        times[n] = [elapsed_time]
    print(times)
                    """)
            f.write("\n\n")

        f.write("    return times\n\n")

        f.write(textwrap.dedent('''\

                        if __name__ == '__main__':
                            run_{0}_{1}()
                        ''').format(n_props, n_comps))


def elaborate(match_times_dict, comp_props_dict):

    with open(evaluation_folder + '/results/comp_props_dict.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(comp_props_dict.items())

    with open(evaluation_folder + '/results/match_times_dict.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(match_times_dict.items())

    n_match_set = set()
    for combination, results in match_times_dict.items():
        for n_match in results.keys():
            n_match_set.add(n_match)

    n_match_set = list(n_match_set)

    with open(evaluation_folder + '/results/match_times.csv', 'w') as f:

        for n_match in range(1, max(n_match_set)+1):
            f.write(str(n_match) + ",")
            for i, (combination, results) in enumerate(match_times_dict.items()):
                if n_match in results.keys():
                    f.write(str(results[n_match]))
                if i < len(match_times_dict) -1:
                    f.write(",")
                else:
                    f.write("\n")
    print("Data Saved")


if __name__ == '__main__':

    run_file_name = "run_all.py"

    n_props = [2, 4, 8, 16, 32]
    n_comps = [10, 30, 50, 70, 90, 110, 130, 150]

    main_flag = False

    with open(evaluation_folder + "/" + run_file_name, 'w') as rf:

        rf.write("import sys\nsys.path.append('../src')\n")

        for n_prop in n_props:
            for n_comp in n_comps:
                gen_file(n_prop, n_comp)
                rf.write("from case_{0}_{1} import *\n".format(n_prop, n_comp))

        rf.write("\nfrom statistics import mean\nfrom evaluation_generator import elaborate\n\n\n")

        rf.write("""\
if __name__ == '__main__':
    match_times_dict = {}
    comp_props_dict = {}
                 """)
        rf.write("\n\n")


        for n_prop in n_props:
            for n_comp in n_comps:

                rf.write("""\
    match_times_{0}_{1} = run_{0}_{1}()
    for key, value in match_times_{0}_{1}.items():
        match_times_{0}_{1}[key] = mean(value)
    match_times_dict[({0}, {1})] = match_times_{0}_{1}
    comp_props_dict[({0}, {1})] = mean(match_times_{0}_{1}[k] for k in match_times_{0}_{1})
                """.format(n_prop, n_comp))
                rf.write("\n")
                rf.write("    elaborate(match_times_dict, comp_props_dict)\n")
                rf.write("\n\n")

