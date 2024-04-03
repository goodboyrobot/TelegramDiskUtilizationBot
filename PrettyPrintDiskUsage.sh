#!/usr/bin/bash
echo "---Leda---"
echo "--Folders--"
for filename in /media/nas/*; do
	if [ -d $filename ]
		then du -sh $filename 2>/dev/null
	fi
done
echo "--Total--"
du -sh "/media/nas/" 2>/dev/null

