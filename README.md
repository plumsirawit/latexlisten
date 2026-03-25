# latexlisten
Listening to LaTeX updates

## Usage
Just maybe `cp listenlatex.service ~/.config/systemd/user/listenlatex.service`
and maybe `systemctl --user daemon-reload` then `systemctl --user enable --now listenlatex.service`.

`journalctl --user -u mydaemon.service -f` might be handy.
