FROM alpine:latest as server_files

ENV TERRARIA_VERSION=1436
ENV TMOD_VERSION=2022.07.58.8

ENV TMOD_SHUTDOWN_MSG="Shutting down!"
ENV TMOD_AUTOSAVE_INTERVAL="*/10 * * * *"

RUN apk update && apk add --no-cache curl unzip

WORKDIR /terraria-server

# Extract Terraria Server
RUN curl -SLO "https://terraria.org/api/download/pc-dedicated-server/terraria-server-${TERRARIA_VERSION}.zip" &&\
    unzip terraria-server-${TERRARIA_VERSION}.zip &&\
    rm terraria-server-${TERRARIA_VERSION}.zip &&\
    cp --verbose -a "${TERRARIA_VERSION}/Linux/." . &&\
    rm -rf "${TERRARIA_VERSION}" &&\
    rm TerrariaServer.exe &&\
    chmod u+x TerrariaServer.bin.x86_64
# TerrariaServer.bin.x86_64, TerrariaServer, lib64/*, etc.

# Extract tModLoader Server
RUN curl -SLO "https://github.com/tModLoader/tModLoader/releases/download/v${TMOD_VERSION}/tModLoader.zip" &&\
    unzip tModLoader.zip &&\
    rm -rf tModLoader.zip &&\
    chmod u+x DedicatedServerUtils/Setup_tModLoaderServer.sh &&\
    chmod u+x start-tModLoaderServer.sh
# start-tModLoaderServer.sh, serverconfig.txt, DedicatedServerUtils\Setup_tModLoaderServer.sh, etc.

#FROM mono:6.10.0.104-slim
#FROM steamcmd/steamcmd:alpine
FROM steamcmd/steamcmd:ubuntu

# Handle SteamCMD Linkage
RUN mkdir -p ${HOME}/.steam/sdk64 &&\
    ln -s ${HOME}/.steam/steamcmd/linux64/steamclient.so ${HOME}/.steam/sdk64/steamclient.so

#RUN apk update && apk add --no-cache procps tmux
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install libicu-dev

COPY --from=server_files /terraria-server/ ./

# Install tMod
RUN steamcmd +force_install_dir /opt/tmod +login anonymous +app_update 1281930 +quit
RUN sed -i '1d' DedicatedServerUtils/Setup_tModLoaderServer.sh

WORKDIR /opt/terraria

RUN ln -s ${HOME}/.local/share/Terraria/ /opt/terraria-home
COPY tmod-send-cmd.sh /usr/local/bin/tmod-send-cmd
COPY serverconfig.txt entrypoint.sh ./
RUN chmod +x entrypoint.sh /usr/local/bin/tmod-send-cmd

EXPOSE 7777

VOLUME /opt/terraria
VOLUME /opt/terraria-home

ENTRYPOINT [ "/opt/terraria/entrypoint.sh" ]