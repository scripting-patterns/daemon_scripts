#!/usr/bin/perl -w

my $file = "/var/log/httpd/access_log";


sub mail_out {
    my ($missing_link, $referrer) = @_;

    print "
    Write your code to send out the mail alerts
    $missing_link is missing refered from $referrer
    ";

}


if (! fork()) {
    $0 = "log_reader";

    print ("open file\n");
    open(LOG, "<$file") or die("Unable to open ");

    print ("Seek to the end of file\n");
    seek(LOG, 0, 2); #seek to the end of the file.... listen to only new entries

    print ("loop\n");
    while(1) {
        while(<LOG>) {
            if (/GET\s{1,}(\S{1,})\s{1,}\S{1,}\s{1,}404\s{1,}\d{1,}\s{1,}(\S{1,})/) {
                mail_out($1, $2)
            }
        }
        sleep(10);        
    }

} else {
    print ("Daemonizinng...\n");
    exit(0);
}

