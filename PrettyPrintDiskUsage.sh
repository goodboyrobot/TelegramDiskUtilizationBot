#!/usr/bin/bash
echo "---Leda---"
if [ "$1" = "full" ]; then
	echo "--Folders--"
	for filename in /media/nas/*; do
  		if [ -d $filename ]
  			then du -sh $filename 2>/dev/null
		fi
	done
fi
echo "--Main Library--"
du -sh "/media/nas/afschuld/TV Shows" 2>/dev/null | sed s:/media/nas/afschuld/::g
du -sh "/media/nas/afschuld/Movies" 2>/dev/null | sed s:/media/nas/afschuld/::g
du -sh "/media/nas/afschuld/4kMovies" 2>/dev/null | sed s:/media/nas/afschuld/::g
du -sh "/media/nas/afschuld/Anime_TV_Shows" 2>/dev/null | sed s:/media/nas/afschuld/::g
du -sh "/media/nas/afschuld/Anime_Movies" 2>/dev/null | sed s:/media/nas/afschuld/::g
du -sh "/media/nas/afschuld/AudioBooks" 2>/dev/null | sed s:/media/nas/afschuld/::g
du -sh "/media/nas/afschuld/Music" 2> /dev/null | sed s:/media/nas/afschuld/::g
echo "--Total--"
du -sh "/media/nas/" 2>/dev/null | sed s:/media/nas/afschuld/::g
