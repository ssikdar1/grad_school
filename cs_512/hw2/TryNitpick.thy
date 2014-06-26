theory TryNitpick
imports Main 
begin

(* Prove the following or else disprove it with a counter-example:*) 
lemma "(\<not>P1 \<or> R1) \<and> (\<not>P7 \<or> \<not> R6) 
       \<and> ((\<not>P2 \<or> R2) \<and> (\<not>R1 \<or> R2) \<and> (\<not>P2 \<or> \<not>R1))
       \<and> ((\<not>P3 \<or> R3) \<and> (\<not>R2 \<or> R3) \<and> (\<not>P3 \<or> \<not>R2))
       \<and> ((\<not>P4 \<or> R4) \<and> (\<not>R3 \<or> R4) \<and> (\<not>P4 \<or> \<not>R3))
       \<and> ((\<not>P5 \<or> R5) \<and> (\<not>R4 \<or> R5) \<and> (\<not>P5 \<or> \<not>R4))
       \<and> ((\<not>P6 \<or> R6) \<and> (\<not>R5 \<or> R6) \<and> (\<not>P6 \<or> \<not>R5))"
nitpick


