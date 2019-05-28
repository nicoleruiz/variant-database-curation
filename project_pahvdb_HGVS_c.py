#!/usr/bin/env python3

# Project PAHvdb variants back to genomic HGVS GRCh37
# Clinvar uses NM_000277.2 and PAHvdb uses NM_000277.1
# NM_000277.2 is not recognized by Biocommons hgvs or Mutalyzer
# They only have version 1 which is why I'm only converting PAHvdb c. variants
import hgvs.parser
import hgvs.assemblymapper
import hgvs.dataproviders.uta
import csv

hp = hgvs.parser.Parser()
hdp = hgvs.dataproviders.uta.connect()
am = hgvs.assemblymapper.AssemblyMapper(hdp, assembly_name='GRCh37', alt_aln_method='splign', replace_reference=True)
#am38 = hgvs.assemblymapper.AssemblyMapper(hdp, assembly_name='GRCh38', alt_aln_method='splign', replace_reference=True)
# Each individual variant page has NG_008690.1
pahvdb_ref = 'NM_000277.1'

# write header to output output file
print "Gene\tEnsembl\tEntrez_Gene\tHGVS\tPAH_Identifier\tBiocommons_HGVS_g\tProtein_Variant\tOld_name\tNucleotide_Aberration\tCodon_Wild_Type\tCodon_Mutant\tSequence_Aberration\tVariant_Type\tCoding_Effect\tGene_Region\tProtein_Domain\tCofactor_Binding_Region(CBR)\tEnzyme_Activity(%)\tAssigned_Value(AV)\tAllelic_Phenotype_Value(APV)\tAllele_Freq(%)\tFoldX_Value\tFoldX_Interpretation\tSIFT_value\tSIFT_Interpretation\tPolyphen_2_value\tPolyphen_2_interpretation\tSNPs_3D_interpretation\tAlamut_Visual_Pathogenicity_Report\tMutalyzer_Check/Comments\tPathogenicity\tHGVS_c\tHGVS_g\tHGVS_p\n"

with open ('PAHvdb_variant_details.txt', 'rb') as f:
    pahvdb = csv.DictReader(f, delimiter='\t')
    for row in pahvdb:
        hgvs_c = row['Nucleotide_Aberration']
        full_hgvs_c = pahvdb_ref+':'+hgvs_c
        try:
            hgvs_g = am.c_to_g(hp.parse_hgvs_variant(full_hgvs_c))
            hgvs_g = str(hgvs_g)
        except Exception,e:
            hgvs_g = str(e)
        for f in pahvdb.fieldnames:
            if row[f] is None:
                row[f] = ''
        line = [row[f] for f in pahvdb.fieldnames]
        line.insert(5, hgvs_g)
        print '\t'.join(line)
