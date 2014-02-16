my($correct) = 0;
my($total) = 0;
while(<STDIN>) {
    chomp;
    $total++;
    my(@fields) = split(/,/, $_);
    if ($fields[$#fields-1] eq $fields[$#fields]) {
	$correct++;
    }
}
print "$correct / $total = " . $correct/$total . "\n";
