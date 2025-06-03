import re

def find_cpg_region(sequence, min_cpg=11):
    # Find all CpG sites (CG or TG)
    cpg_sites = [m.start() for m in re.finditer(r'CG|TG', sequence)]
    print(cpg_sites)
    if len(cpg_sites) < min_cpg:
        return "Not enough CpG sites in the sequence."
    
    # Find the smallest region containing at least 'min_cpg' sites
    min_length = len(sequence)
    best_region = ""
    
    for i in range(len(cpg_sites) - min_cpg + 1):
        start = cpg_sites[i]
        end = cpg_sites[i + min_cpg - 1]  # The last required CpG site in this window
        region_length = end - start + 1
        
        if region_length < min_length:
            min_length = region_length
            best_region = sequence[start:end+1]
    print(best_region)
    print(min_length)
    
    return best_region, min_length if best_region else ("No suitable region found.", None)

# Input sequence
seq = "TAAACCCTAAACATATAAACTCTTTATAACTAAAATAAAAAATTAACGTCCACTCATACGTAACCTCACTCCGCATACCTCCTACTCCAACCCAAAAAAAAACTCCCATCTACTCCAACAACTAACCCAAACCCCTTTTATACTATCCTAATAAAAAACAAAAAAAAACCCTACC"

# Find the best region with at least 11 CpG sites
find_cpg_region(seq, min_cpg=11)
