#!/usr/bin/bash

ACCOUNT="student";

function setpass {
  VNC_DIR="/home/$ACCOUNT/.vnc"

  echo -e "$1\n$1" | passwd "$ACCOUNT";

  rm "$VNC_DIR/passwd";
  echo "$1" | vncpasswd -f > "$VNC_DIR/passwd";
  chown "$ACCOUNT:$ACCOUNT" "$VNC_DIR/passwd";
  chmod 0600 "$VNC_DIR/passwd";
}

if [ $1 == "-set" ]; then
  setpass $2
fi

if [ $1 == "-create" ]; then
  GENERATED_PASSWORD=$(date +%s | sha256sum | base64 | head -c 12);
  setpass "$GENERATED_PASSWORD";
  echo "generated: $GENERATED_PASSWORD";
fi
