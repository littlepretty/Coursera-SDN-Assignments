[Host]
h1 - h8

[Switch]
s1 - s8

[Link]
s_i - h_i

[Port Table]
[Switch to switch]
s1.p1 - s8.p1
s1.p2 - s3.p1
s2.p1 - s5.p3
s2.p2 - s4.p3
s2.p3 - s7.p2
s3.p2 - s8.p2
s3.p3 - s6.p2
s3.p4 - s4.p1
s4.p2 - s5.p2
s4.p4 - s7.p3
s5.p1 - s6.p3
s5.p4 - s7.p4
s6.p1 - s8.p3
s7.p1 - s8.p4

[Host to switch]
h1.p1 - s1.p3
h2.p1 - s2.p4
h3.p1 - s3.p5
h4.p1 - s4.p5
h5.p1 - s5.p5
h6.p1 - s6.p4
h7.p1 - s7.p5
h8.p1 - s8.p5


[Flow]
h1 - h6
h2 - h5
h3 - h5
h4 - h7
h5 - h7
h6 - h7
h8 - h6

[Current Rule]
@s1: if Src == h1 && Dst == h6 then Fwd to s8 (s1.p1) 
@s2: if Src == h2 && Dst == h5 then Fwd to s4 (s2.p2)
@s3: if Src == h3 && Dst == h5 then Fwd to s4 (s3.p4)
@s4: if Src == h4 && Dst == h7 then Fwd to s7 (s4.p4)
@s5: if Src == h5 && Dst == h7 then Fwd to s2 (s5.p3)
@s6: if Src == h6 && Dst == h7 then Fwd to s5 (s6.p3)
@s8: if Src == h4 && Dst == h6 then Fwd to s3 (s8.p2)



[Target Rule]
@s1: if Src == h1 && Dst == h6 then Fwd to s3 (s1.p2) 
@s2: if Src == h2 && Dst == h5 then Fwd to s5 (s2.p1)
@s3: if Src == h3 && Dst == h5 then Fwd to s6 (s3.p3)
@s4: if Src == h4 && Dst == h7 then Fwd to s5 (s4.p2)
@s5: if Src == h5 && Dst == h7 then Fwd to s4 (s5.p2)
@s6: if Src == h6 && Dst == h7 then Fwd to s8 (s6.p1)
@s8: if Src == h4 && Dst == h6 then Fwd to s6 (s8.p3)

[Test]
ping h1 - h6, h2 - h5, h3 - h5, h4 - h7, h5 - h7, h6 - h7, h8 - h6
