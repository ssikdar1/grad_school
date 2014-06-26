theory shanPigeonhole3final
imports Main 
begin

(* Pigeon Hole 3 holes: A slightly different formulation, the others were giving me strange counter examples I couldn't explian. This is equivelent though to what
I wrote in part a, just using DeMorgan's laws*) 
lemma "((\<not> P11 \<and> \<not> P12) \<or> (\<not> P21 \<and> \<not> P21) \<or> (\<not> P31 \<and> \<not> P32))\<or>
(P11 \<and> P11) \<or> (P21 \<and> P31) \<or> (P11 \<and> P31) \<or> (P12 \<and> P22) \<or> (P22 \<and> P32) \<or> (P12 \<and> P32) "
nitpick




