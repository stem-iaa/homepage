#!/usr/bin/bash

ACCOUNT="student";
VNC_DIR="/home/$ACCOUNT/.vnc";
GENERATED_PASSWORD=$(date +%s | sha256sum | base64 | head -c 8);

rm "$VNC_DIR/passwd";
echo "$GENERATED_PASSWORD" | vncpasswd -f >"$VNC_DIR/passwd";
chown "$ACCOUNT:$ACCOUNT" "$VNC_DIR/passwd";
chmod 0600 "$VNC_DIR/passwd";

echo "generated vnc pass:";
echo "$GENERATED_PASSWORD";
