ssh-config
==========

SSH config file query and modification commandline tool.

Less manually editing or viewing the config file for that one setting you need.

Also makes it easier for other tools to read the same ssh_config.

Possible uses
=============

- List the options for a specific host

        ssh-config -l -H yourhost

- List a specific option for a specific host

        ssh-config -l -H myserver -o IdentityFile

- List all hosts that have a specific option with a specific value
        
        ssh-config -l -o Port=1337

- Change or set the value of a specific option for a specific host
        
        ssh-config -s -H myserver -o Port=1337

- Add an entirely new host entry with all its options
        
        ssh-config -s -H newhost -o Hostname=newhost.example.net -o Port=1337

- Remove host entry
        
        ssh-config -d -H newhost

- Remove specific options from a host entry
        
        ssh-config -d -H somehost -o someoption

- Use a different file as a source
        
        ssh-config -f somefile -l
