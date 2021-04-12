# DNA-ink-bamboo

This codes converts DNA sequence into ink bamboo - Chinese painting!

## Guide

To do this, first import zhu and cv2:

```python
import zhu, cv2
```

Then, copy the function below, which provides a way to convert a DNA sequence into a random number sequence:

```python
def DNA_2_int(seq):
    DICT = {'A': 0, 'T': 1, 'C': 2, 'G': 3, 'a': 0, 't': 1, 'c': 2, 'g': 3}
    res = []
    for i in range(len(seq)-1):
        res.append(DICT[seq[i]]*4+DICT[seq[i+1]])
    return res*1000, seq*1000
```

Lastly, get a DNA sequence, create a piece of xuanzhi (some traditional Chinese paintings are painted on specially made papers called xuanzhi), and let the codes paint!

```python
seed, seq = DNA_2_int("TCTCCACTCATTGCCTTTACTTTCCTTTAACTAAGACAAAGGCAAACACAAACCCAAAGACGATAACAATAGCAATGACAATTACAATTAATGCCCCGGGCCCAATTAAGACGACAACAACGACGACCACGGAGACAGAGGCAGAGACGGAAGCCGATACTGTAACAGTAACAGTGACCGTGTCAGGAACAGGAGCAGGGACAGGCACAGGTACCGGTGCACAGACACAGACGCAGGCACATACACACTAGCGAACACGGACCCGGTCACCGACACCGGCACCCACACCTACACTAACACTGACGCTTACGTAGACATAGGCATAGACGTATACCTATACTTGAACATGAACATGGACCTGGTCATCAACAGTATCATCGACATCCACATCTACCTCTGCAAAAATCAAAAGGAAGGTCAAGGGGAAGCTCAAGCGGAAGCTTAATGACCCGGAAGAACCTTAACTTCAACTGGAATATGATAATTATAGTGATACTTATGGGGATGGTTATTCTTAGAATGAGGGTCAGGGGGAGCATCAGCAGGAGCATTAGCCTCAGCCGGAGTATCAGTCTCAGTCGGAGTCTTACAATCACAAGGACAATTACAGTCACAGGGGAAATCGAAAGGGAAATTGAGGTCGAGGGGGAGCTCGAGCGGGAGCTTGACATCGATATCGATTTCGATTGGGATTTTGTAATCGTAAGGGTATTCGTATGGGTAGTCGTGATCGTGAGGGTGATTGTGTTCGTGTGGGTGGTCGTGGGGGTGGTTGTGCTCGTGCGGGTCATGGGAATTGGAGTGGGACTTGGGGGGGGGGTTGGCAGGGGCCTCGGCCGGGGTATCGGTAGGGGTATTGGTGTCGGTGGGGGTCTGGGTTTTCAAATTCAGGTTCAGCTGCACATTCATCTGCGAATCCGAAGGCGAGTCCGAGGGCGGATCCGGAG")

xuanzhi = zhu.xuan.xuanize(width=618, height=1000)
cv2.imwrite('demo.jpg', zhu.zhu(xuanzhi, seed, seq=seq)*256)
```

## Demo

### COVID-19

This is an image generated from COVID-19 genome sequence:

![figure 1](https://github.com/Tallopen/DNA-ink-bamboo/blob/main/demo/covid19.jpg)

The bamboo leaves are sparse, which coincide with the pandamic and millions of life lost.

### Firefly fluorescent gene

This example is generated from a gene which makes the firefly glow:

![figure 2](https://github.com/Tallopen/DNA-ink-bamboo/blob/main/demo/firefly.jpg)

The picture is filled with life and hope.
