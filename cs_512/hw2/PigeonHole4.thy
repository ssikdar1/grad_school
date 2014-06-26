theory PigeonHole4
imports Main 
begin

(* Pigeon Hole 4 holes: Instead of doing the implication on doing the one with negation and joined wth the or
so the one where there empty holes and two pidgeons in a hole*) 
lemma "(
((\<not>P11 \<and> \<not>P21 \<and> \<not>P31 \<and> \<not>P41 ) 	\<or> (\<not>P12 \<and> \<not>P22 \<and> \<not>P32 \<and> \<not> P42 )\<or>(\<not>P13 \<and> \<not>P23 \<and> \<not>P33 \<and> \<not> P43 ))
 \<or> ((P11 \<and> P21) \<or> (P11 \<and> P31)\<or>(P11 \<and> P41) \<or> (P21 \<and> P31) \<or> (P21 \<and> P41) \<or> (P31 \<and> P41) 
 \<or>(P12 \<and> P22) \<or> (P12 \<and> P32)\<or>(P12 \<and> P42) \<or> (P22 \<and> P32) \<or> (P22 \<and> P42) \<or> (P32 \<and> P42))) "
nitpick

