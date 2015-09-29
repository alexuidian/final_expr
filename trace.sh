
sudo xm tmem-list -al > tmem-stats
mkdir old
mv stats_* old

sudo ./parse_tmem_stats.py "tmem-stats" &

a=1

while [ $a ]
do
    sleep 0.5
    sudo xm tmem-list -al > tmem-stats
done  
