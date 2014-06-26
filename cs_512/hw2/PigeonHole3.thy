theory PigeonHole3
imports Main
begin

lemma "	((\<not> P00 \<and> \<not> P01) \<or> (\<not> P10 \<and> \<not> P11) \<or> (\<not> P20 \<and> \<not> P21)) \<or>
	(P00 \<and> P10) \<or> (P10 \<and> P20) \<or> (P00 \<and> P20) \<or> 
	(P01 \<and> P11) \<or> (P11 \<and> P21) \<or> (P01 \<and> P21) " by auto

lemma "	((\<not> P00 \<and> \<not> P01) \<or> (\<not> P10 \<and> \<not> P11) \<or> (\<not> P20 \<and> \<not> P21)) \<or>
	(P00 \<and> P10) \<or> (P10 \<and> P20) \<or> (P00 \<and> P20) \<or> 
	(P01 \<and> P11) \<or> (P11 \<and> P21) \<or> (P01 \<and> P21) " by auto
end
