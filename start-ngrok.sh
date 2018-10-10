#!/bin/bash

# Warning: this will close any running instances of the Django server and ngrok
# Otherwise, it can't add the new URL to Django's allowed hosts

site_dir=$(pwd)
ngrok_dir=$HOME
ngrok_api=http://localhost:4040/api/tunnels

if [ ! -z $1 ];
then
	ngrok_dir=$1
fi

if [[ $(uname) == "Darwin" ]];
then
	$(brew install jq)
else
	if [[ ! $(dpkg -s jq) ]]
	then
		$(sudo apt-get install jq)
	fi
fi

finish() {
	cd $site_dir/IceToMeetYou
	if [ -f settingsbak.py ];
	then
		mv settingsbak.py settings.py
		echo "Cleaning up settings.py"
	fi
	
	exit
}

trap finish SIGINT SIGTERM ERR

cd $ngrok_dir
url=.

if pgrep -f "ngrok http" > /dev/null
then 
	pkill -f ngrok
fi


echo "Starting ngrok..."
./ngrok http --log=stdout 8000 > /dev/null &
unset url
sleep 7
stat=$(curl -s $ngrok_api) 

if [[ -z "$stat" ]]
then
	echo "waiting for ngrok tunnel"
	sleep 3
fi

url=$(curl -s $ngrok_api | jq '.tunnels[0].public_url')

if [[ $url == null ]];
then
	echo "ngrok start failed, no URL was generated"
	exit 1
else
	echo "ngrok is now running at $url"
fi

if [[ -z $url ]];
then
	echo "ngrok start failed, no URL was generated"
	exit 1
fi

if [[ ! -z $url ]]
then
	cd $site_dir/IceToMeetYou
	echo $url
	cp settings.py settingsbak.py
	host=${url#*http://}
	host2=${url#*https://}
	if [[ $(echo $host -n | wc -c) -gt $(echo $host2 -n | wc -c) ]]
	then	
		echo "ALLOWED_HOSTS = ["\""$host2]" >> settings.py
	else	
		echo "ALLOWED_HOSTS = ["\""$host]" >> settings.py
	fi
	echo "$url added to ALLOWED_HOSTS"
fi

cd $site_dir
if pgrep -f "python3 manage.py runserver" > /dev/null
then 
	pkill -f "python3 manage.py runserver"
	echo "Django Server already running, terminating..."
else
	python3 manage.py runserver > /dev/null &
fi


while :
do
	sleep 5
done

