#!/usr/bin/env python3

import hgvs.parser
import hgvs.assemblymapper
import hgvs.dataproviders.uta
import csv

hp = hgvs.parser.Parser()
hdp = hgvs.dataproviders.uta.connect()
am = hgvs.assemblymapper.AssemblyMapper(hdp, assembly_name='GRCh37', alt_aln_method='splign', replace_reference=True)
vr = hgvs.validator.Validator(hdp=hdp)
norm = hgvs.normalizer.Normalizer(hdp)

# write header to output output file
#print "Gene\tEnsembl\tEntrez_Gene\tHGVS\tPAH_Identifier\tBiocommons_HGVS_g\tProtein_Variant\tOld_name\tNucleotide_Aberration\tCodon_Wild_Type\tCodon_Mutant\tSequence_Aberration\tVariant_Type\tCoding_Effect\tGene_Region\tProtein_Domain\tCofactor_Binding_Region(CBR)\tEnzyme_Activity(%)\tAssigned_Value(AV)\tAllelic_Phenotype_Value(APV)\tAllele_Freq(%)\tFoldX_Value\tFoldX_Interpretation\tSIFT_value\tSIFT_Interpretation\tPolyphen_2_value\tPolyphen_2_interpretation\tSNPs_3D_interpretation\tAlamut_Visual_Pathogenicity_Report\tMutalyzer_Check/Comments\tPathogenicity\tHGVS_c\tHGVS_g\tHGVS_p\n"

with open ('clinvar_pah_clinical_testing_variants_hgvs_separated.txt', 'rb') as f:
    clinvar_pah = csv.DictReader(f, delimiter='\t')
    for row in clinvar_pah:
        hgvs_g = row['hgvs_g']
        hgvs_c = row['hgvs_c']
        try:
            tool_hgvs_g = am.c_to_g(hp.parse_hgvs_variant(hgvs_c))
            tool_hgvs_g = str(tool_hgvs_g)
        except Exception,e:
            hgvs_g = str(e)
