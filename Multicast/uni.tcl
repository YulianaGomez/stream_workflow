#Create a simulator object
set ns [new Simulator]

#Define different colors for data flows (for NAM)
$ns color 1 Blue
$ns color 2 Red

#Open the NAM trace file
set nf [open uni.nam w]
$ns namtrace-all $nf

#Open the Trace file
set tf [open uni.tr w]
$ns trace-all $tf

#set xg1 [open xg1.xg w]

#Define a 'finish' procedure
proc finish {} {
        global ns nf tf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Close the Trace file
        close $tf
        #Execute NAM on the trace file
        exec nam uni.nam &

        exec gawk -f throughput.awk uni.tr > uni.xg
        exit 0
}

#Create six nodes
set n(1) [$ns node]
set n(2) [$ns node]
set n(3) [$ns node]
set n(4) [$ns node]
set n(5) [$ns node]
set n(6) [$ns node]
set n(7) [$ns node]
set n(8) [$ns node]
set nswitch [$ns node]

$n(1) label APS
$n(2) label 75
$n(3) label 60
$n(4) label 50
$n(5) label 40
$n(6) label 35
$n(7) label 25
$n(8) label 80
$nswitch label switch
# set n8 [$ns node]


#Create links between the nodes
$ns duplex-link $n(1) $nswitch 20Mb 2ms DropTail
$ns duplex-link $n(2) $nswitch 10Mb 1ms DropTail
$ns duplex-link $n(3) $nswitch 10Mb 1ms DropTail
$ns duplex-link $n(4) $nswitch 10Mb 1ms DropTail
$ns duplex-link $n(5) $nswitch 10Mb 1ms DropTail
$ns duplex-link $n(6) $nswitch 10Mb 1ms DropTail
$ns duplex-link $n(7) $nswitch 10Mb 1ms DropTail
$ns duplex-link $n(8) $nswitch 10Mb 1ms DropTail

proc create_tcp_connection {i j k} {
    global ns n tcp ftp
    #Setup a TCP connection
    set tcp($k) [new Agent/TCP/Newreno]
    #$tcp1 set class_ 2
    $tcp($k) set window_ 200
    $ns attach-agent $n($i) $tcp($k)
    set sink($k) [new Agent/TCPSink]
    $ns attach-agent $n($j) $sink($k)
    $ns connect $tcp($k) $sink($k)
    $tcp($k) set fid_ ($k)

    #Setup a FTP over TCP connection
    set ftp($k) [new Application/FTP]
    $ftp($k) attach-agent $tcp($k)
    $ftp($k) set type_ FTP
}

create_tcp_connection 1 2 1 
create_tcp_connection 1 3 2 
create_tcp_connection 1 4 3 
create_tcp_connection 1 5 4 
create_tcp_connection 1 6 5 
create_tcp_connection 1 7 6
create_tcp_connection 1 8 7


for {set i 1} {$i <= 6} {incr i} {
   $ns at 0.0 "$ftp($i) start"                      
}


$ns at 5.0 "$ftp(7) start"

$ns at 10.0 "$ftp(1) stop"

for {set i 1} {$i <= 7} {incr i} {
   $ns at 15.0 "$ftp($i) stop"                      
}

$ns at 16.0 "finish"

#Run the simulation
$ns run

