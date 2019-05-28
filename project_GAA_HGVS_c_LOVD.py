#!/usr/bin/env python3

import hgvs.parser
import hgvs.assemblymapper
import hgvs.dataproviders.uta
import csv
import re

hp = hgvs.parser.Parser()
hdp = hgvs.dataproviders.uta.connect()
am = hgvs.assemblymapper.AssemblyMapper(hdp, assembly_name='GRCh37', alt_aln_method='splign', replace_reference=True)
#am38 = hgvs.assemblymapper.AssemblyMapper(hdp, assembly_name='GRCh38', alt_aln_method='splign', replace_reference=True)
'''
#hgvs_g = 'NC_000017.10:g.78078867_78078868delCC'
#transcripts = am.relevant_transcripts(hp.parse_hgvs_variant(hgvs_g))
hgvs_c = 'NM_000152.3:c.1636+460_2672del'
hgvs_g = am.c_to_g(hp.parse_hgvs_variant(hgvs_c))
print hgvs_g
'''

with open ('LOVD_Total_GAA.csv', 'r') as f:
    gaa_db = csv.DictReader(f, delimiter=',')
    for row in gaa_db:
        hgvs = row['VariantOnTranscript/DNA']
        regex=re.compile('([:c.*0-9A-Za-z-?>_]*)')
        transcript_ref= 'NM_000152.3'
        match=regex.search(hgvs)
        #match = re.fullmatch(r'(.+?)(\(GAA\))?:(.+?)( \(.+\))?', hgvs)
        if match is None:
        	print('Couldn\'t match ' + hgvs)
        else:
        	#print transcript_ref + ':' + match.group(1)
        	new_hgvs= transcript_ref + ':' + match.group(1)
        #else:
            #print('Group 1: ' + match.group(1) + ' Group 3: ' + match.group(3))
        try:
            hgvs_g = am.c_to_g(hp.parse_hgvs_variant(new_hgvs))
            hgvs_g = str(hgvs_g)
        except Exception,e:
            hgvs_g = str(e)
        for f in gaa_db.fieldnames:
            if row[f] is None:
                row[f] = ''
        line = [row[f] for f in gaa_db.fieldnames]
        line.insert(2, hgvs_g)
        print '\t'.join(line)
