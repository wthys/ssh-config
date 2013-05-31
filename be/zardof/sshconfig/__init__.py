# package be.zardof.sshconfig
#
#   Copyright (c) 2012, Wim Thys <wim.thys@zardof.be>
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.
#
from os.path import expanduser

import copy
import logging

class SshConfig:
    """
    SSH configuration. An SshConfig consists of multiple SshConfigEntries, with
    at least one general entry applying to all hosts that could not be matched
    to other entries.
    """

    def __init__(self, default=None, **kwargs):
        """ Create an SshConfig.

        SshConfig(default=<options>, <host>=<options>)
            default:	The default values that must be used. <options>
                        defaults to None here.
            <host>:	The hostname for the host entry.
            <options>:	A SshConfigEntry object describing the options of the
                        entry. If None will be ignored.
        """
        self.__entries = {}
        if not default is None:
            self.set(None, default)
        for h, e in kwargs.items():
            if not e is None:
                self.set(h, e)

    def get(self, host, option=None):
        """ Get the entry for the host. If the host does not have an entry,
            None is returned. To get the default entry, use None as a value.
            If the option is supplied, this is equivalent to
            get(host).get(option)

        get(host)
            host:   The hostname to look for.
        
        get(host, option)
            host:   The hostname to look for.
            option: The option to look for.
        """
        host_name = "ssh_%s" % host
        if host is None:
            logging.debug("SC.get: host is None in get")
	    host_name = "default"

        if host_name not in self.__entries:
            logging.debug("SC.get: host = %s, host_name = %s" % (host,
                host_name))
	    return None
	
        if option is None:
            return self.__entries[host_name]
        else:
            return self.__entries[host_name].get(option)

    def set(self, host, *args, **kwargs):
        """ Set the entry options for a specific host and create an entry if
        there is none yet. If this is a new host, it will have a priority equal
        to the number of entries. This can be changed with the set_priority()
        method of SshConfigEntry.

        set(host, entry)
            host:   The host to set the entry for.
            entry:  The entry to set. Either a dict-like object with the
                    options as keys or an SshConfigEntry.

        set(host, <option>=<value>, ...)
            host:       The host to set the entry for.
            <option>:   A valid SSH option.
            <value>:    Value for <option>.
        """
        logging.debug("SC.set: Set a host entry for host %s using %s and %s" % (host,
            args, kwargs))
        host_name = "ssh_%s" % host
        if host is None:
	    host_name = "default"

        if (
                # No args or kwargs
                (len(args) == 0 and len(kwargs) == 0)
                # Entry is None or not specified and all supplied hostnames
                # have None values or no options
                or ((len(args) == 0 or (len(args) == 1 and args[0] is None))
                        and len([1 for k in kwargs if not kwargs[k] is None or
                            len(kwargs[k]) == 0]) == 0)
           ):
            # Nothing to do, just exit
            return 

        entry = SshConfigEntry(len(self.__entries))

	if len(args) == 1:
            logging.debug("SC.set: Entry, before: %s" % repr(args[0]))
	    entry.set(args[0])
            logging.debug("SC.set: Entry, after: %s" % repr(entry))
	elif len(args) > 1:
	    raise TypeError("set() only takes up to 2 positional arguments (%d given)" % len(args))
	
        if len(kwargs) > 0:
            entry.set(**kwargs)

        # Guarantee that an entry will have entries
        if len(entry) > 0:
            if host not in self or (host is None and "default" not in
                    self.__entries):
                logging.debug("SC.set: host not present or None")
                self.__entries[host_name] = entry
                logging.debug("SC.set: entry for %s is %s" % (host_name, repr(entry)))
            else:
                self.get(host).set(entry)

    def __delitem__(self, host):
        """ Remove an entire host entry """
        if host in self:
            del self.__entries["ssh_%s" % host]
        elif host is None:
            del self.__entries["default"]
        else:
            raise KeyError(host)

    def remove(self, host, *options):
        """ Remove a host entry or specific options in a host entry.
        
        remove(host)
            host:	the host for which to remove the entire entry
            
        remove(host, <option>...)
            host:	the host for which to remove specified options
            <option>:	the name of the option to be removed so that it does
                        not exist afterwards. It need not exist beforehand.
        """
        if len(options) == 0:
            del self[host]
        else:
            entry = self.get(host)
            entry.remove(*options)

    def __contains__(self, host):
        """ If we have an entry for the specified host

        contains(host)
            host:   The host to check for.
        """
        if host is None:
            return False
        host_name = "ssh_%s" % host
        return host_name in self.__entries

    def hosts(self):
        """ Return all the hostnames
        """
        return [x.partition("ssh_")[2] for x in self.__entries.keys() if
                x.find("ssh_",0,4) >= 0]

    def save(self, dest):
        """ Save the configuration somewhere safe.

        save(dest)
            dest:   A filename or a file-like object. If the file already
                    exists, it will be overwritten.
        """
        if (isinstance(dest, file)):
            dest.write(str(self))
        elif isinstance(dest,str):
            f = open(dest, "w")
            f.writelines(str(self).split("\n"))
            f.close()
        else:
            raise TypeError("Argument is not a file or str")

    def load(self, config):
        """ Load a configuration.

        load(config)
            config: A configuration to load. Must be an SshConfig, a file-like
                    object or a filename.
        """
        cfg = load_sshconfig(config)
        hosts = [None]
        hosts.extend(cfg.hosts())
        for h in hosts:
            self.set(h, cfg.get(h))

    def __repr__(self):
        rep = "SshConfig("
        entries = []
        for k,v in self.__entries.items():
            if v is None:
                continue
            if k == "default":
                entries.append(repr(v))
            else:
                entries.append("%s = %s" % (k.partition('ssh_')[2], repr(v)))
        rep += ", ".join(entries)
        rep += ")"
        return rep

    def __str__(self):
        lines = []
        for h, e in sorted(self.__entries.items(), key=lambda t: t[1].priority()):
            opts = str(e)
            if not h == "default":
                lines.append("Host %s" % h.partition("ssh_")[2])
                opts = "\n".join(["    %s" % s for s in opts.split("\n")])
            lines.append(opts)
        return "\n".join(lines)


class SshConfigEntry:
    """ A collection of SSH options pertaining to a group of hosts
    """

    def __add_to_opts(self, ddict=None, llist=None, ttuple=None):
#        logging.debug("SCE.__add_to_opts: %s" % ("%s %s %s" % (ddict, llist,
#            ttuple)))
        
        try:
            k = self.__options
            del k
        except AttributeError, ae:
            self.__options = {}
	
        if llist is not None and len(llist) > 0:
            for t in llist:
                if not (t[1] is None or t[0] is None):
                    self.__options[str(t[0])] = t[1]
        if ddict is not None and len(ddict) > 0:
            for o, v in ddict.items():
                if not (o is None or v is None):
                    self.__options[o] = v
        if ttuple is not None and len(ttuple) >= 2:
            if not (ttuple[0] is None or ttuple[1] is None):
                self.__options[ttuple[0]] = ttuple[1]
	
    def __init__(self, priority, *args, **kwargs):
        """ Create an SshConfigEntry.

        SshConfigEntry(priority, entry)
            priority:   The priority for this entry.
            entry:      The contents of the entry. Can be either another
                        SshConfigEntry or a dict-like object.

        SshConfigEntry(priority, <option>=<value>, ...)
            priority:   The priority for this entry.
            <option>:   A valid SSH option
            <value>:    Value for <option>
        """
	self.__options = {}
        self.__priority = priority
	
        if len(args) == 1:
	    entry = args[0]
	    if isinstance(entry, SshConfigEntry):
                opts = entry.options()
                #logging.debug("SCE.__init__: loading existing SshConfigEntry: %s" % opts)
		self.__add_to_opts(ddict=opts)
	    elif isinstance(entry, dict):
                #logging.debug("SCE.__init__: loading dict: %s" % entry)
		self.__add_to_opts(ddict=entry)
	    else:
		raise TypeError("SshConfigEntry(entry): entry is not of type SshConfigEntry or dict")
	elif len(args) > 1:
	    raise TypeError("SshConfigEntry() takes up to 1 positional argument (%d given)" % len(args))

        if len(kwargs) > 0:
            #logging.debug("SCE.__init__: loading keyword arguments")
            self.__add_to_opts(ddict=kwargs)

    def priority(self):
        """ Get the priority of this host entry. This is used for ordering in
        the eventual ssh_config.
        """
        return self.__priority

    def set_priority(self, priority):
        """ Set the priority of the entry. If None is supplied, nothing
        happens.
        set_priority(priority)
            priority:	The new priority. A value of None will have no effect
        """
        if priority is None:
            return
        else:
            self.__priority = int(priority)

    def get(self, option):
        """ Get the value for a specific option.

        get(option)
            option: A valid SSH option. If it does not exist, None is returned.
        """
        try:
	    return self.__options[option]
	except KeyError, e:
	    return None

    def set(self, *args, **kwargs):
        """ Set the value for a specific option. Options with a name or value
        of None will be ignored.

        set(options)
            options:    An SshConfigEntry or a dict-like object with SSH
                        options as keys.

        set(name, value)
            name:   A valid SSH option name
            value:  Value for the option

        set(<option>=<value>, ...)
            <option>:   A valid SSH option
            <value>:    Value for <option>
        """
        #logging.debug("SCE.set: Setting options for entry: %s %s" % (args, kwargs))
        if len(args) == 1:
	    options = args[0]
	    if isinstance(options, SshConfigEntry):
                logging.debug("SCE.set: We have a SshConfigEntry")
                self.__add_to_opts(ddict=options.__options)
                self.set_priority(options.priority())
	    elif isinstance(options, dict):
                logging.debug("SCE.set: We have a dict")
                self.__add_to_opts(ddict=options)
	    else:
                logging.debug("SCE.set: We have something else: %s" % options)
		pass
	elif len(args) == 2:
            #logging.debug("SCE.set: regular two-valued call")
	    name = args[0]
	    value = args[1]

            self.__add_to_opts(ttuple=(name, value))
	elif len(args) > 2:
	    raise TypeError("set() takes up to 2 positional parameters (%d given)" % len(args))
	
        if len(kwargs) > 0:
            self.__add_to_opts(ddict=kwargs)
        #logging.debug("SCE.__options = %s" % self.__options)
    
    def remove(self, *options):
        """ Remove the specified entries.

        remove(<option>, ...)
            <option>:	The option to remove. It will not exist afterwards. It
                        need not exist beforehand.
        """
        if len(options) < 1:
            raise TypeError("remove() takes at least one paramter (none given)")
        else:
            for opt in options:
                try:
                    del self[opt]
                except KeyError,e :
                    pass

    def __delitem__(self, option):
        """ Remove the specified option."""
        if option in self:
            del self.__options[option]
        else:
            raise KeyError(option)

    def __contains__(self, option):
        """ Whether the SshConfigEntry contains the specified option

        __contains__(option)
            option: A valid SSH option
        """
        return option in self.__options

    def __len__(self):
        """ Return the number of defined options """
        return len(self.__options)

    def to_dict(self):
        """ Converts the SshConfigEntry to a dict
        """
        l = {}
        l.update(self.__options)
        return l
    
    def items(self):
        return [x for x in self.__options.items() if not x[1] is None]

    def options(self):
        return copy.copy(self.__options)

    def __repr__(self):
        rep = "SshConfigEntry(%d" % self.priority()
        entries = []
        for k, v in self.__options.items():
            if v is None:
                continue
            entries.append("%s = \"%s\"" % (k, v))
        if len(entries) > 0:
            rep += ", "
        rep += ", ".join(entries)
        rep += ")"
        return rep

    def __str__(self):
        lines = []
        for k, v in self.__options.items():
            if v is None:
                continue
            lines.append("%s %s" % (k, v))
        return "\n".join(lines)

def load_sshconfig(config):
    """ Parses a ssh_config to an SshConfig

    load_sshconfig(config):
        config: A filename or a file-like object.
    """
    logging.debug("Opening `%s'" % config)
    cfgfile = []
    if isinstance(config, str):
	k = open(config,'r')
	cfgfile = k.readlines()
	k.close()
    elif isinstance(config, file):
	cfgfile = config.readlines()
    else:
	raise TypeError("config is not a string or file")

    logging.debug("contents of configfile: %s" % "".join(cfgfile))

    ssh_cfg = SshConfig()
    host_name = None
    host_entry = SshConfigEntry(0)
    ignoring = False
    priority = 0
    for line in cfgfile:
	line = line.strip().split('#')[0]
	option = line.split(' ')[0]
	value = " ".join(line.strip().split(' ')[1:])
        #logging.debug("option = %s , value = %s" % (option, value))

	if len(option) == 0:
	    # we have a comment!
            continue
	elif option == "Host":
	    ssh_cfg.set(host_name, host_entry)
            priority += 1

	    host_name = value
	    host_entry = SshConfigEntry(priority)
	else:
	    host_entry.set(option, value)
    ssh_cfg.set(host_name, host_entry)

    return ssh_cfg
