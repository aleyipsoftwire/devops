docker volume create chimera-volume

docker run -dit \
    -p 8089:80 \
    --mount type=volume,source=chimera-volume,target="/opt/chimera/data",readonly \
    chimera-web-app

docker run -it \
    --mount type=volume,source=chimera-volume,target="/opt/chimera/data" \
    chimera-cli-app
