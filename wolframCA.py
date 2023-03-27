import numpy as np
import os
import matplotlib.pyplot as plt

def rule_create():
    rule = []
    coi = 3 # cells to check (cells of interest)

    for i in range(0,2**coi):
        rule.append(np.binary_repr(i,3))
        
    # results = np.array([0, 1, 1, 1, 1, 0, 0, 0]).astype('int') # rule 30    
    return rule, coi
    

def one_iter(grid0, grid1, rule, results):
    for i in range(1,len(grid0)-2):
        cell = grid0[i-1:i+2]
        # print(cell)
        for j in range(len(rule)):
            rulet = [int(k) for k in rule[j]]
            if (sum(cell==rulet) == 3):
                grid1[i] = results[j]

def wolf_CA(rule_num, n, iter, each_iter=0,grid_choice=0, highres=300):
    script_dir = os.path.dirname(__file__)
    [rule, coi] = rule_create()

    results_dir = os.path.join(script_dir, f'rule{rule_num}_{n}_{iter}/')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    
    results = np.flip(np.array([int(i) for i in np.binary_repr(rule_num,2**coi)]).astype('int'))
    
    whole = np.zeros([iter,n]).astype('int')
    
    if (grid_choice == 0):
        grid0 = np.random.randint(2,size=n) # random starting values
    elif (grid_choice == 1):
        grid0 = np.insert(np.zeros(n-1),n//2,1).astype('int') # all 0s except for 1 in  middleg
        
    grid1 = np.zeros(n).astype('int')
    print(f"\nrule{rule_num}")
    for i in range(iter):
        # print(grid0)
        whole[i,:] = grid0
        if each_iter:
            create_plot(whole, rule_num, f"{i}", results_dir, highres)
        one_iter(grid0, grid1, rule, results)
        grid0 = grid1
        grid1 = np.zeros(n).astype('int')
        if (i % 100 == 0):
            print(f"{i/iter * 100:0.2f}")
    
    plt.clf()
    create_plot(whole, rule_num, f"{n}_{iter}",results_dir, highres)
    # plt.show()

def create_plot(whole, rule_num, id, path, highres):
        plt.clf()
        plt.imshow(whole, cmap="gray")
        plt.tight_layout()
        plt.title(f"rule{rule_num}_{n}_{iter}")
        plt.savefig(path+f"rule{rule_num}_{id}.png", dpi=highres)

n = 500 # x size
iter = 500 # y size
wolf_CA(184, n, iter, each_iter=0, grid_choice=0, highres=500)