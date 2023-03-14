#!/usr/bin/env bash
set -e

# !! only tested on arch linux !!
# see https://github.com/VocaDB/vocadb/wiki/VocaDB-development-environment-(Linux)

# make yourself admin
# /opt/mssql-tools/bin/sqlcmd -C -S localhost -U SA -P "MikuMiku.39" -Q "use VocaloidSite; select Id, Name, UserGroup from Users; update Users set UserGroup = 'Admin' where Id = 1; select Id, Name, UserGroup from Users"

DIR_WORKING="${1:?Provide a working directory.}"
shift
#echo "Provide the SQL password:"
#read SQL_PASSWORD

pre() {
	mkdir -p "$DIR_WORKING"
	cd "$DIR_WORKING"

	# TODO: can i force sqlserver to save data in $DIR_WORKING
}

check_requirements() {
	requirements="git dotnet node npm /opt/mssql/bin/mssql-conf /opt/mssql-tools/bin/sqlcmd"
	#pac="git dotnet-runtime nodejs npm AUR/mssql-server AUR/mssql-tools dotnet-sdk aspnet-runtime"
	#foobar=(
	#https://archive.archlinux.org/packages/l/libldap/libldap-2.4.59-2-x86_64.pkg.tar.zst
	#https://archive.archlinux.org/packages/l/libldap/libldap-2.4.59-2-x86_64.pkg.tar.zst.sig
	#)
	#echo "libldap for mssql-server"
	#sudo pacman -U "libldap-2.4.59-2-x86_64.pkg.tar.zst"
	#echo "Add libldap to /etc/pacman.conf to block automatic upgrades"

	for bin in $requirements
	do
		if ! command -v "$bin"
		then
			echo "Missing! $bin"
			exit
		fi
	done
}

prepare_git() {
	if [ ! -d "$DIR_WORKING/git/vocadb" ]
	then
		git clone --depth 1 "https://github.com/VocaDB/vocadb.git" "$DIR_WORKING/git/vocadb"
		cd "$DIR_WORKING/git/vocadb"
		git submodule update --init
	fi
}

prepare_sqlservr() {
	# https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-setup
	# -C https://stackoverflow.com/a/73443215
	if [ ! -d "/var/opt/mssql" ]
	then
		echo "sudo to setup SQL Server"
		sudo MSSQL_PID="Developer" ACCEPT_EULA="Y" MSSQL_SA_PASSWORD="MikuMiku.39" /opt/mssql/bin/mssql-conf -n setup

		/opt/mssql-tools/bin/sqlcmd -C -S localhost -U SA -P "MikuMiku.39" -Q "CREATE DATABASE VocaloidSite"

		wget "https://vocaloid.eu/vocadb/empty-mssql.sql" -O "$DIR_WORKING/empty-mssql.sql"
		/opt/mssql-tools/bin/sqlcmd -C -S localhost -U SA -P "MikuMiku.39" -d "VocaloidSite" -i "$DIR_WORKING/empty-mssql.sql"
	fi

	echo "sudo to start SQL Server"
	systemctl is-active --quiet mssql-server || sudo systemctl start mssql-server
}

prepare_dotnet-fm() {
	if [ ! -e "$HOME/.dotnet/tools/dotnet-fm" ]
	then
		dotnet tool install -g FluentMigrator.DotNet.Cli
	fi

	if [ ! -d "$DIR_WORKING/git/vocadb/VocaDb.Migrations/bin" ]
	then
		dotnet build "$DIR_WORKING/git/vocadb/VocaDb.Migrations"
		# why does the wiki have two different connection strings
		"$HOME"/.dotnet/tools/dotnet-fm migrate -p sqlserver -c "Data Source=.; Initial Catalog=VocaloidSite; Trusted_Connection=False; User Id=SA; Password=MikuMiku.39;" -a "$DIR_WORKING/git/vocadb/VocaDb.Migrations/bin/Debug/net472/VocaDb.Migrations.dll"
	fi
}

write_default_config() {
	if [ ! -e "$DIR_WORKING/git/vocadb/VocaDbWeb/appsettings.config" ]
	then
		cd "$DIR_WORKING/git/vocadb/VocaDbWeb"
		git clone --depth 1 "https://github.com/VocaDB/vocadb.wiki.git" "$DIR_WORKING/git/vocadb.wiki"
		# ChatGPT wrote the `awk` script BTW
		awk '/^####/ {filename=tolower($2); next}; /^```xml$/ {flag=1; next}; /^```$/ {flag=0; next}; flag {print > filename}' "$DIR_WORKING/git/vocadb.wiki/VocaDB-development-environment-(Windows).md"
		# "C:\VocaDB-data\" is inappropriate for Linux
		# TODO: `sed` won't accept a command that contains `$DIR_WORKING` because `$DIR_WORKING` has `/` in it
		sed --in-place -E '/StaticContentPath/ s/value=".+"/value="\/tmp\/vocadb-data"/g' "$DIR_WORKING/git/vocadb/VocaDbWeb/appsettings.config"
		# SqlException: Cannot authenticate using Kerberos. Ensure Kerberos has been initialized on the client with 'kinit' and a Service Principal Name has been registered for the SQL Server to allow Kerberos authentication
		sed --in-place -E '/Trusted_Connection/ s/True/False/g' "$DIR_WORKING/git/vocadb/VocaDbWeb/connections.config"
		# TODO: add user id and password
		#sed --in-place -E '' "$DIR_WORKING/git/vocadb/VocaDbWeb/connections.config"
		# TODO: recaptcha key https://stackoverflow.com/a/41746466
	fi
}

npm_compile_assets() {
	# XXX: IDK how npm works
	if [ ! -d "$DIR_WORKING/git/vocadb/VocaDbWeb/node_modules" ]
	then
		cd "$DIR_WORKING/git/vocadb/VocaDbWeb"
		npm install
		#npm run dev
		npm run production
		#npm run watch &
	fi
}

start_server() {
	if [ ! -d "$DIR_WORKING/git/vocadb/VocaDbWeb/bin" ]
	then
		dotnet build "$DIR_WORKING/git/vocadb/VocaDbWeb"
	fi
	dotnet run --project "$DIR_WORKING/git/vocadb/VocaDbWeb"
}

stop_server() {
	# there has to be a better way
	killall dotnet
}

main() {
	pre
	check_requirements

	prepare_git
	#prepare_dotnet
	#prepare_node
	#prepare_npm
	prepare_sqlservr
	prepare_dotnet-fm

	write_default_config
	npm_compile_assets

	start_server
	stop_server
}

main
