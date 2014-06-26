theory shanPigeonhole4final
imports Main 
begin
(*this again is a different formulation than i had originally. I tried for far too long to get the other formulations to work but for some reason this
one was the only one that worked without giving me a counter example. Again its using demorgans law and the logic that we know that there are 
more pigeons than holes in our formulation of the problem *)
lemma "
(\<not>P00 \<and> \<not>P01 \<and> \<not>P02) \<or> (\<not>P10 \<and> \<not>P11 \<and> \<not>P12) \<or> (\<not>P20 \<and> \<not>P21 \<and> \<not>P22) \<or> (\<not>P30 \<and> \<not>P31 \<and> \<not>P32) \<or>
(P00 \<and> P10) \<or> (P00 \<and> P20) \<or> (P00 \<and> P30) \<or> (P10 \<and> P20) \<or> (P10 \<and> P30) \<or> (P20 \<and> P30) \<or> 
(P01 \<and> P11) \<or> (P01 \<and> P21) \<or> (P01 \<and> P31) \<or> (P11 \<and> P21) \<or> (P11 \<and> P31) \<or> (P21 \<and> P31) \<or>
(P02 \<and> P12) \<or> (P02 \<and> P22) \<or> (P02 \<and> P32) \<or> (P12 \<and> P22) \<or> (P12 \<and> P32) \<or> (P22 \<and> P32) " by auto
end

