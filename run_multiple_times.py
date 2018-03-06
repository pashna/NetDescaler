import os

base_path = "/home/pkochetk/images/data/MSU/capture/full_exp_3/"
os.system('mn --topo=tree,depth=4 --test pingall')
#for scale in [1.0, 0.5, 0.2, 0.1]:
for scale in [0.05]:

    scale_path = str(scale).replace(".", "_")
    path = base_path + scale_path + "/"

    for _ in range(5):

        os.system('echo "================" >> {}log'.format(path))
        os.system('echo "================" >> {}log'.format(path))
        os.system('echo "" >> {}log'.format(path))

        os.system('python main.py {} {} >> {}log'.format(scale, path, path))
        os.system('echo "------CLEANING-------" >> {}log'.format(path))
        os.system('mn --topo=tree,depth=4 --test pingpair >> {}log'.format(path))

        """
        print('echo "================" >> {}log'.format(path))
        print('echo "================" >> {}log'.format(path))
        print('echo "" >> {}log'.format(path))

        print('python main.py {} {} >> {}log'.format(scale, path, path))
        print('echo "------CLEANING-------" >> {}log'.format(path))
        print('mn --topo=tree,depth=4 --test pingpair >> {}log'.format(scale, path, path))
        """