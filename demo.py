import zhu


def DNA_2_int(seq):
    DICT = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'a': 0, 't': 1, 'c': 2, 'g': 3}
    res = []
    for i in range(len(seq)-1):
        res.append(DICT[seq[i]]*4+DICT[seq[i+1]])
    return res*1000, seq*1000


# seed = DNA_2_int(''.join("agtttgatcatggctcagattgaacgctggcggcaggcctaacacatgcaagtcgaacggtaacaggaagcagcttgctgctttgctgacgagtggcggacgggtgagtaatgtctggga aactgcctga tggaggggga taactactgg aaacggtagc taataccgca taacgtcgca agcacaaaga gggggacctt agggcctctt gccatcggat gtgcccagat gggattagctagtaggtggg gtaacggctc acctaggcga cgatccctag ctggtctgag aggatgacca gcaacactgg aactgagaca cggtccagac tcctacggga ggcagcagtg gggaatattg cacaatgggc gcaagcctga tgcagccatg cngcgtgtat gaagaaggcc ttcgggttgt aaagtacttt cagcggggag gaagggagta aagttaatac ctttgctcat tgacgttacc cgcagaagaa gcaccggcta actccgtgcc agcagccgcg gtaatacgga gggtgcaagc gttaatcgga attactgggc gtaaagcgca cgcaggcggt ttgttaagtc agatgtgaaa tccccgggct caacctggga actgcatctg atactggcaa gcttgagtct cgtagaggggggtagaattc caggtgtagc ggtgaaatgc gtagagatct ggaggaatac cggtggcgaaggcggccccc tggacgaaga ctgacgctca ggtgcgaaag cgtggggagc aaacaggattagataccctg gtagtccacg ccgtaaacga tgtcgacttg gaggttgtgc ccttgaggcgtggcttccgg anntaacgcg ttaagtcgac cgcctgggga gtacggccgc aaggttaaaactcaaatgaa ttgacggggg ccgcacaagc ggtggagcat gtggtttaat tcgatgcaac gcgaagaacc ttacctggtc ttgacatcca cggaagtttt cagagatgag aatgtgccttcgggaaccgt gagacaggtg ctgcatggct gtcgtcagct cgtgttgtga aatgttgggttaagtcccgc aacgagcgca acccttatcc tttgttgcca gcggtccggc cgggaactcaaaggagactg ccagtgataa actggaggaa ggtggggatg acgtcaagtc atcatggcccttacgaccag ggctacacac gtgctacaat ggcgcataca aagagaagcg acctcgcgagagcaagcgga cctcataaag tgcgtcgtag tccggattgg agtctgcaac tcgactccatgaagtcggaa tcgctagtaa tcgtggatca gaatgccacg gtgaatacgt tcccgggccttgtacacacc gcccgtcaca ccatgggagt gggttgcaaa agaagtaggt agcttaacttcgggagggcg".split()))
seed, seq = DNA_2_int("TCTCCACTCATTGCCTTTACTTTCCTTTAACTAAGACAAAGGCAAACACAAACCCAAAGACGATAACAATAGCAATGACAATTACAATTAATGCCCCGGGCCCAATTAAGACGACAACAACGACGACCACGGAGACAGAGGCAGAGACGGAAGCCGATACTGTAACAGTAACAGTGACCGTGTCAGGAACAGGAGCAGGGACAGGCACAGGTACCGGTGCACAGACACAGACGCAGGCACATACACACTAGCGAACACGGACCCGGTCACCGACACCGGCACCCACACCTACACTAACACTGACGCTTACGTAGACATAGGCATAGACGTATACCTATACTTGAACATGAACATGGACCTGGTCATCAACAGTATCATCGACATCCACATCTACCTCTGCAAAAATCAAAAGGAAGGTCAAGGGGAAGCTCAAGCGGAAGCTTAATGACCCGGAAGAACCTTAACTTCAACTGGAATATGATAATTATAGTGATACTTATGGGGATGGTTATTCTTAGAATGAGGGTCAGGGGGAGCATCAGCAGGAGCATTAGCCTCAGCCGGAGTATCAGTCTCAGTCGGAGTCTTACAATCACAAGGACAATTACAGTCACAGGGGAAATCGAAAGGGAAATTGAGGTCGAGGGGGAGCTCGAGCGGGAGCTTGACATCGATATCGATTTCGATTGGGATTTTGTAATCGTAAGGGTATTCGTATGGGTAGTCGTGATCGTGAGGGTGATTGTGTTCGTGTGGGTGGTCGTGGGGGTGGTTGTGCTCGTGCGGGTCATGGGAATTGGAGTGGGACTTGGGGGGGGGGTTGGCAGGGGCCTCGGCCGGGGTATCGGTAGGGGTATTGGTGTCGGTGGGGGTCTGGGTTTTCAAATTCAGGTTCAGCTGCACATTCATCTGCGAATCCGAAGGCGAGTCCGAGGGCGGATCCGGAG")

import cv2
xuanzhi = zhu.xuan.xuanize(width=618, height=1000)
cv2.imwrite('WANGSHIZHENHAO.jpg', zhu.zhu(xuanzhi, seed, seq=seq)*256)
