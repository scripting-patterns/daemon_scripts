#!/usr/bin/perl -w

use IO::Handle;
use IO::Select;

# daemonize

if (! fork()) {
    $0 = "controller";

    $sel = IO::Select->new();
    # spawn five processes
    foreach((1..5)) {
        pipe(${"read$_"}, ${"write$_"});
        my $pid = fork();
        if (! $pid) {
            # close (STDERR);
            # close (STDOUT);

            $0 = "child_$_";

            close(${"read$_"});

            my $count = 0;
            while(1) {
                print(${"write$_"}, "from $_: $count\n");
                sleep(2);
                $count++;
            }
        } else {
            close(${"write$_"});
            $sel->add(${"read$_"}); 
            if ($_ == 5) {
                while(1) {
                    @readable = $sel->can_read(2);
                    foreach (@readable) {
                        print (<$_>);
                    }
                }
            }

        }
    }
} else {
    print ("Daemonizinng...");
    exit(0);
}

