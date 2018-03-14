# From http://ns2awk.blogspot.com/p/calculate-throughput-of-throughput.html
# Edited by Zhi Hong
#============================= throughput.awk ========================

BEGIN {
recv=0;
gotime = 0;
time = 0;
#packet_size = 1000;
time_interval = 0.2;
}
#body
{
    event = $1
    time = $2
    node_id = $4
    pktType = $5
    pktSize = $6

 if(time>gotime) {
  #packet size * ... gives results in Mbps
  print gotime, (recv / time_interval * 8.0)/1024/1024;
  gotime+= time_interval;
  recv=0;
  }

#============= CALCULATE throughput=================

if (( event == "r") && ( node_id != 8 ) )
{
 recv += pktSize;
}

} #body


END {
;
}
#============================= Ends ============================