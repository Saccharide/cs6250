#!/usr/bin/python
import os
import sys
import time


# netem commands
#netemCommandDelete = "sudo tc qdisc del dev lo root"
#netemCommandShow = "sudo tc qdisc show dev lo"
#netemCommandRoot = "sudo tc qdisc add dev lo root handle 1: netem "
#netemCommandLatencyAddendum = " delay xxxms"
#netemCommandLatencyVarianceAddendum = " xxxms distribution normal"
#netemCommandPacketLossAddendum = " loss xxx%"
#netemCommandBandwidth = "sudo tc qdisc add dev lo parent 1: handle 2: tbf rate xxxmbit burst 256kbit latency 1000ms mtu 1500"
#netemCommandChangeBandwidth = "sudo tc qdisc change dev lo parent 1: handle 2: tbf rate xxxmbit burst 256kbit latency 1000ms mtu 1500"


def main():


    # target websites
    websites = ['google.com', 'twitter.com', 'example.org', 'gatech.edu','localhost4.com/index4.html' ,'localhost32.com/index32.html']

    # Setting up command for tc to run
    losses = [0.5, 1, 2, 5]

    # Delay list
    delays = [100,200,400,1600]
    #losses = [0]

    # Corrupt list
    corrupts = [1,2,5,10]


    # Set bandwidth limit
    #os.system('sudo tc qdisc add dev lo root tbf rate 2mbit')
    os.system('sudo tc qdisc add dev enp0s3 root netem')
    os.system('sudo tc qdisc add dev lo root netem')
    #for loss in losses:
    for delay in delays:
    #for corrupt in corrupts:
        # Deleteing previous stored settings
        #os.system('sudo tc qdisc del dev lo root')
        


        # Set loss rate 
        #os.system('sudo tc qdisc change dev enp0s3 root netem loss {}%'.format(loss))
        #os.system('sudo tc qdisc change dev lo root netem loss {}%'.format(loss))

        #print 'delay 100ms'
        print '===============================================>  DELAY = {} '.format(delay) 
        os.system('sudo tc qdisc change dev enp0s3 root netem delay {}'.format(delay))
        os.system('sudo tc qdisc change dev lo root netem delay {}'.format(delay))

        # Set corrput rate
        #print 'sudo tc qdisc change dev enp0s3 root netem corrupt {}%'.format(corrupt) 
        #os.system('sudo tc qdisc change dev enp0s3 root netem corrupt {}%'.format(corrupt))
        #os.system('sudo tc qdisc change dev lo root netem corrupt {}%'.format(corrupt))


        # TCP
        if "REMOTE" in os.environ:
            print("----------------- Running TCP benchmark on remote server -----------------")
            host_para = "35.184.14.12"
            tcp_command = "http://" + host_para + "/quic-data/www."


        else:
            print("----------------- Running TCP benchmark locally -----------------")
            host_para = "127.0.0.1"
            tcp_command = "https://" + host_para + "/quic-data/www."

        for website in websites:

            # Start measuring time it takes to transfer file
            startTime = time.time()
            os.system('wget --quiet ' + tcp_command + website)

            # With debug
            #os.system('wget ' + tcp_command + website)
            timeElasped = time.time() - startTime
            print("Time to get index.html page from " + website +  ": " + str(timeElasped) + "seconds")
            os.system('ping ' + host_para + "&")
            time.sleep(0.5)
            os.system("kill $(ps -aux | grep -w ping | grep -v grep | awk '{print $2;}')")



        # QUIC
        if "REMOTE" in os.environ:
            print("----------------- Running QUIC benchmark on remote server -----------------")
            host_para = "35.184.14.12"
            local_host = ''


        else:
            print "\n"
            print("----------------- Running QUIC benchmark locally -----------------")
            host_para = "127.0.0.1"
            local_host = 'localhost/'

        # Starting local QUIC server on a background thread
        os.system('/home/saccharide/chromium/src/out/Debug/quic_server --quic_response_cache_dir=/tmp/quic-data/   --certificate_file=net/tools/quic/certs/out/leaf_cert.pem   --key_file=net/tools/quic/certs/out/leaf_cert.pkcs8 &')
        time.sleep(1)

        # target websites
        websites = ['google.com', 'twitter.com', 'example.org', 'gatech.edu','localhost4.com/index4.html' ,'localhost32.com/index32.html']
        for website in websites:

            if 'localhost' in website:
                cmd = '/home/saccharide/chromium/src/out/Debug/quic_client --quiet --host=' + host_para  + ' --disable_certificate_verification --port=6121 https://127.0.0.1/quic-data/www.' + website 
            else:
                cmd = '/home/saccharide/chromium/src/out/Debug/quic_client --quiet --host=' + host_para  + ' --disable_certificate_verification --port=6121 https://www.' + website 

            #print "QUIC client command running = "+ cmd

            startTime = time.time()
            os.system(cmd)
            # With debug
            #os.system(cmd+' -v=1')

            timeElasped = time.time() - startTime
            print "Time to get index.html page from " + website +  ": " + str(timeElasped) + "seconds"

            os.system('ping ' + host_para + "&")
            time.sleep(0.5)
            os.system("kill $(ps -aux | grep -w ping | grep -v grep | awk '{print $2;}')")

        os.system("kill $(ps -aux | grep quic_server | grep -v grep | awk '{print $2;}')")



main()
