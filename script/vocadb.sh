#!/usr/bin/env bash
set -e

# !! only tested on arch linux !!
# see https://wiki.vocadb.net/docs/development/vocadb-development-environment-linux

# make yourself admin
# /opt/mssql-tools/bin/sqlcmd -C -S localhost -U SA -P "MikuMiku.39" -Q "use VocaloidSite; select Id, Name, UserGroup from Users; update Users set UserGroup = 'Admin' where Id = 1; select Id, Name, UserGroup from Users"

# log is in git/vocadb/VocaDbWeb/bin/Debug/net7.0/App_Data

# https://archlinux.org/packages/extra/x86_64/dbeaver/

DIR_WORKING="${1:?Provide a working directory.}"
shift

pre() {
	mkdir -p "$DIR_WORKING"
	cd "$DIR_WORKING"

	# dotnet
	# currently .dotnet cannot be relocated
	mkdir -p "$DIR_WORKING/dotnet"

	# nuget
	export NUGET_PACKAGES="$DIR_WORKING/nuget"

	# sql
	# not working
	#mkdir -p "$DIR_WORKING/mssql"
	#mkdir -p "$DIR_WORKING/mssql/data"
	#mkdir -p "$DIR_WORKING/mssql/log"

	# npm
	# TODO: npm
}

check_requirements() {
	requirements="git dotnet node npm /opt/mssql/bin/mssql-conf /opt/mssql-tools/bin/sqlcmd"
	#archlinux="git dotnet-runtime nodejs npm AUR/mssql-server AUR/mssql-tools dotnet-sdk-7.0 aspnet-runtime-7.0 AUR/libldap24"

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
	if [ ! -d "$DIR_WORKING/git/vocadb-wiki" ]
	then
		# old wiki: https://github.com/VocaDB/vocadb.wiki.git
		git clone --depth 1 "https://github.com/VocaDB/Wiki.git" "$DIR_WORKING/git/vocadb-wiki"
	else
		git -C "$DIR_WORKING/git/vocadb-wiki" pull
	fi

	if [ ! -d "$DIR_WORKING/git/vocadb" ]
	then
		git clone --depth 1 "https://github.com/VocaDB/vocadb.git" "$DIR_WORKING/git/vocadb"
		git -C "$DIR_WORKING/git/vocadb" submodule update --init
	else
		git -C "$DIR_WORKING/git/vocadb" pull
		git -C "$DIR_WORKING/git/vocadb" submodule update --recursive
	fi
}

prepare_sqlservr() {
	# https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-setup
	# -C https://stackoverflow.com/a/73443215
	if [ ! -d "/var/opt/mssql" ]
	then
		echo "sudo to setup SQL Server"
		sudo systemctl stop mssql-server

		# https://learn.microsoft.com/en-us/sql/linux/sql-server-linux-configure-mssql-conf#change-the-default-data-or-log-directory-location
		# not working
		#sudo chown mssql "$DIR_WORKING/mssql"
		#sudo chgrp mssql "$DIR_WORKING/mssql"
		#sudo /opt/mssql/bin/mssql-conf set filelocation.defaultdatadir "$DIR_WORKING/mssql/data"
		#sudo /opt/mssql/bin/mssql-conf set filelocation.defaultlogdir "$DIR_WORKING/mssql/log"

		sudo MSSQL_PID="Developer" ACCEPT_EULA="Y" MSSQL_SA_PASSWORD="MikuMiku.39" /opt/mssql/bin/mssql-conf -n setup

		/opt/mssql-tools/bin/sqlcmd -C -S localhost -U SA -P "MikuMiku.39" -Q "CREATE DATABASE VocaloidSite"

		wget "https://vocaloid.eu/vocadb/empty-mssql.sql" -O "$DIR_WORKING/empty-mssql.sql"
		/opt/mssql-tools/bin/sqlcmd -C -S localhost -U SA -P "MikuMiku.39" -d "VocaloidSite" -i "$DIR_WORKING/empty-mssql.sql"
	fi

	echo "sudo to start SQL Server"
	# `is-active`, in case it's already started; in which case, don't bother me with a `sudo`
	systemctl is-active --quiet mssql-server || sudo systemctl start mssql-server
}

prepare_dotnet-fm() {
	if [ ! -e "$DIR_WORKING/dotnet/tools/dotnet-fm" ]
	then
		dotnet tool install --tool-path "$DIR_WORKING/dotnet/tools" FluentMigrator.DotNet.Cli
	fi

	# XXX: should run whenever there are new migrations! this is not one-off!
	if [ ! -d "$DIR_WORKING/git/vocadb/VocaDb.Migrations/bin" ]
	then
		dotnet build "$DIR_WORKING/git/vocadb/VocaDb.Migrations"
		# why does the wiki have two different connection strings
		"$DIR_WORKING/dotnet/tools/dotnet-fm" migrate -p sqlserver -c "Data Source=.; Initial Catalog=VocaloidSite; Trusted_Connection=False; User Id=SA; Password=MikuMiku.39; TrustServerCertificate=True;" -a "$DIR_WORKING/git/vocadb/VocaDb.Migrations/bin/Debug/net472/VocaDb.Migrations.dll"
	fi
}

write_default_config() {
	# XXX: ok so it seems like it doesn't like when the config file is a symbolic link on first launch.
	# but after i put the real file there and let it launch correctly,
	# it doesn't seem to care if i put the symbolic links back?
	# or is it just reading the previous config data from somewhere and still ignoring the symbolic link

	if [ ! -e "$DIR_WORKING/appsettings.config" ]
	then
		# ChatGPT wrote the `awk` script BTW
		dos2unix -O "$DIR_WORKING/git/vocadb-wiki/src/content/docs/VocaDB development environment (Windows).mdx" | awk '/^####/ {filename=tolower($2); next}; /^```xml$/ {flag=1; next}; /^```$/ {flag=0; next}; flag {print > filename}'
		ln -s "$DIR_WORKING/"*".config" "$DIR_WORKING/git/vocadb/VocaDbWeb"

		# SqlException: Cannot authenticate using Kerberos. Ensure Kerberos has been initialized on the client with 'kinit' and a Service Principal Name has been registered for the SQL Server to allow Kerberos authentication
		sed --in-place -E '/Trusted_Connection/ s/True/False/' "$DIR_WORKING/connections.config"

		sed --in-place -E '/connectionString=/ s/;(")/; User Id=SA; Password=MikuMiku.39;\1/' "$DIR_WORKING/connections.config"
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
	dotnet run --project "$DIR_WORKING/git/vocadb/VocaDbWeb"
}

stop_server() {
	# there has to be a better way
	killall dotnet

	# probably not a good idea, like when restarting
	# stop the service yourself
	#sudo systemctl stop mssql-server
}

main() {
	pre
	check_requirements

	#prepare_git
	prepare_sqlservr
	prepare_dotnet-fm

	write_default_config
	npm_compile_assets

	start_server
	#stop_server
}

main
