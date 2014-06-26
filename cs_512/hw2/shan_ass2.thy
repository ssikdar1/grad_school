imports Main 
begin

(*(
Implementation
) Use Isabelle to establish the validity or the non-validity of each of the
WFF’s in Problems 1 and 2 of Assignment 1.:*) 
lemma 1: "((P\<longrightarrow>Q)\<and>(P\<longrightarrow>\<not>Q))\<Longrightarrow>\<not>P" by auto
lemma 2: "(P\<longrightarrow>(Q\<longrightarrow>R))\<and>P\<and>\<not>R\<Longrightarrow>\<not>Q" by auto

lemma 3: "P\<and>\<not>P\<Longrightarrow>\<not>(R\<longrightarrow>Q)\<and>(R\<longrightarrow>Q)" by auto
lemma 4: "(P\<longrightarrow>Q)\<and>(S\<longrightarrow>T)\<Longrightarrow>(P\<or>S)\<longrightarrow>(Q\<and>T)" by auto
lemma 5: "\<not>(\<not>P\<or>Q)\<Longrightarrow>P" by auto

end
