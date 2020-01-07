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

            component_library = ComponentsLibrary(name="cogomo")

                '''))
        n_props_total = n_props * n_comps - n_comps + 1
        for x in range(0, n_props_total):
            f.write(textwrap.dedent('''\
                p{0} = Bool('p{1}')
                ''').format(x, x))

        f.write(textwrap.dedent('''\

            component_library.add_components(
                [
                        '''))

        pcount = 0
        for i in range(0, int(n_comps/2)):
            f.write('\t\tComponent(id=')
            f.write('"c{0}", assumptions=['.format(i))
            n_ag = int(n_props / 2)
            if i > 1:
                pcount -= n_ag
            # writing the assumptions
            for p in range(0, n_ag):
                f.write('p{0}'.format(pcount))
                f.write(' == True')
                if p != n_ag - 1:
                    f.write(', ')
                pcount += 1
            f.write('], guarantees=[')
            # writing the guarantees
            for p in range(0, n_ag):
                f.write('p{0}'.format(randint(0, n_props_total)))
                f.write(' == True')
                if p != n_ag - 1:
                    f.write(', ')
                pcount += 1
            f.write('])')
            f.write(',\n')

        for i in range(int(n_comps / 2), n_comp):
            f.write('\t\tComponent(id=')
            f.write('"c{0}", assumptions=['.format(i))
            n_ag = int(n_props / 2)
            if i > 1:
                pcount -= n_ag
            # writing the assumptions
            for p in range(0, n_ag):
                f.write('p{0}'.format(pcount))
                f.write(' == True')
                if p != n_ag - 1:
                    f.write(', ')
                pcount += 1
            f.write('], guarantees=[')
            # writing the guarantees
            for p in range(0, n_ag):
                f.write('p{0}'.format(pcount))
                f.write(' == True')
                if p != n_ag - 1:
                    f.write(', ')
                pcount += 1
            f.write('])')

            if i != n_comps - 1:
                f.write(',\n')
        f.write('\n\t])\n\n')

        f.write(textwrap.dedent('''\
                    spec_a = []
                    spec_g = [p{0} == True]

                    specification = Contract(assumptions=spec_a, guarantees=spec_g)\n

                        ''').format(pcount - 1))

        f.write(textwrap.dedent('''\
                        def run_{0}_{1}():
                            start_time = time.time()
                            components_selection(component_library, specification)
                            elapsed_time = time.time() - start_time
                            return elapsed_time
                            
                        
                        if __name__ == '__main__':
                            run_{0}_{1}()
                        ''').format(n_props, n_comps))


if __name__ == '__main__':

    run_file_name = "run_all.py"

    # n_props = [2, 4, 8, 16]
    # n_comps = [4, 8, 16, 32]

    n_props = [6]
    n_comps = [16]


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

                rf.write("\tsys.stdout = open(os.devnull, 'w')\n")
                rf.write("\ttime = run_{0}_{1}()\n".format(n_prop, n_comp))
                rf.write("\tsys.stdout = sys.__stdout__\n")
                rf.write("\tprint('\t{0}_{1}\t\t' + str(time))\n".format(n_prop, n_comp))


"""
Results

	2_4		0.688688993454
	2_8		2.25693678856
	2_16		8.30225801468
	2_32		30.1880400181
	4_4		1.71299004555
	4_8		6.05677604675
	4_16		22.7483189106
	4_32		87.1651818752
	8_4		5.4546751976
	8_8		19.6110460758
	8_16		74.1302411556
	8_32		288.108966827
	16_4		19.4766969681
	16_8		70.1793510914
	16_16		266.141678095

"""
