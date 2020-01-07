import os
from random import randint
import textwrap

filepath = os.getcwd()


def gen_file(n_props, n_comps):
    file_name = "case_" + str(n_props) + "_" + str(n_comps) + ".py"
    with open(file_name, 'w') as f:
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


if __name__ == '__main__':

    run_file_name = "run_all.py"

    # n_props = [2, 4, 8, 16]
    # n_comps = [4, 8, 16, 32]

    n_props = [2, 6]
    n_comps = [4, 16]

    main_flag = False

    with open(run_file_name, 'w') as rf:

        for n_prop in n_props:
            for n_comp in n_comps:
                gen_file(n_prop, n_comp)
                rf.write("from case_{0}_{1} import *\n".format(n_prop, n_comp))

        for n_prop in n_props:
            for n_comp in n_comps:
                if not main_flag:
                    rf.write("\n\nif __name__ == '__main__':\n\n")
                    main_flag = True

                rf.write("    match_times = run_{0}_{1}()\n".format(n_prop, n_comp))

                rf.write("""\
    print("ciao")
                        """)
                rf.write("\n")
