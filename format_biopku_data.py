#!/usr/bin/env python3
# Reformat variant info produced from biopku-scraper.py

from itertools import groupby, chain, izip
from collections import OrderedDict
import csv

biopku_file = open('PAHvdb_variant_details.txt', 'w')

#https://stackoverflow.com/questions/35773600/how-to-split-file-into-chunks-by-string-delimiter-in-python
def get_sections(file):
    with open(file) as f:
        # Split file using PAH Results as separator
        groups = groupby(f, key=lambda x: x.lstrip().startswith("PAH Results"))
        for k, v in groups:
            if k: # if True since k is a bool
                yield chain([next(v)], (next(groups)[1]))
                # yield is like return except code in function block isn't executed when called?
                # chain takes series of iterables (like lists) and flattens them into one iterable
                # if chain isn't used, then this is returned as list(v):
                #[['PAH Results\n'], <itertools._grouper object at 0x10df48090>]
                #[['PAH Results\n'], <itertools._grouper object at 0x10df34fd0>]

records = []
variants = []

biopku_file.write("Gene\tEnsembl\tEntrez_Gene\tHGVS\tPAH_Identifier\tProtein_Variant\tOld_name\tNucleotide_Aberration\tCodon_Wild_Type\tCodon_Mutant\tSequence_Aberration\tVariant_Type\tCoding_Effect\tGene_Region\tProtein_Domain\tCofactor_Binding_Region(CBR)\tEnzyme_Activity(%)\tAssigned_Value(AV)\tAllelic_Phenotype_Value(APV)\tAllele_Freq(%)\tFoldX_Value\tFoldX_Interpretation\tSIFT_value\tSIFT_Interpretation\tPolyphen_2_value\tPolyphen_2_interpretation\tSNPs_3D_interpretation\tAlamut_Visual_Pathogenicity_Report\tMutalyzer_Check/Comments\tPathogenicity\tHGVS_c\tHGVS_g\tHGVS_p\n")

for v in get_sections('biopku-scraper.out'):
    records.append(list(v))

for r in records:
    r.pop(0)
    if r[0] == '! - Still under investigation\n':
        r.pop(0)
    list = [i.rstrip() for i in r]
    d = OrderedDict(zip(list[::2], list[1::2]))
    if '3D Structures' in d:
        del d['3D Structures']
    # None of the variants have values for Splice Taster
    if 'Splice Taster' in d:
        del d['Splice Taster']
    if 'Splice Taster Interpretation' in d:
        del d['Splice Taster Interpretation']
    if 'Experimental_findings' in d:
        del d['Experimental_findings']
    if 'SNPs 3D value\xc2\xa0' in d:
        del d['SNPs 3D value\xc2\xa0']
    # I'm leaving out refs for now since I don't think I need them
    if 'References' in d:
        del d['References']
    # Some of the webpages have blank rows
    # ('\xc2\xa0', '\xc2\xa0')
    if '\xc2\xa0' in d:
        del d['\xc2\xa0']
    variants.append(d)

#count = 0
for var in variants: # var is OrderedDict
    line = []
    '''
    if count == 0:
        header = var.keys()
        new_header = [h.replace("\xc2\xa0","") for h in header]
        biopku_file.write("\t".join(new_header))
        biopku_file.write("\n")
        count += 1
        '''
    for k,v in var.items():
        line.append(v)
    biopku_file.write("\t".join(line))
    biopku_file.write("\n")

# Add in variants that don't have additional data
'''
Keys in reader dictionary:

Nucl No.
Nucleotide Aberration
PAH ID
Still under Investigation
Protein Variant/Alternative Name
In 3D?
'''
vars_no_data = {'PAH0082':1, 'PAH0099':1, 'PAH0214':1, 'PAH0263':1, 'PAH0694':1, 'PAH0777':1, 'PAH0793':1, 'PAH1010':1}
with open ('PAHvdb_variant_list.txt', 'rb') as f:
    reader = csv.DictReader(f, delimiter='\t')
    next(reader)
    for row in reader: #row is a dictionary
        if row['PAH ID'] in vars_no_data:
            add_line = ['PAH', 'ENSG00000171759', '5053', '8582', row['PAH ID'], row['Protein Variant/Alternative Name'], '', row['Nucleotide Aberration']]
            add_line.append("\t"*25)
            biopku_file.write("\t".join(add_line))
            biopku_file.write("\n")

biopku_file.close()
f.close()
