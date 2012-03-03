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

class SshConfig:
    """
    SSH configuration. An SshConfig consists of multiple SshConfigEntries, with
    at least one general entry applying to all hosts that could not be matched
    to other entries.
    """

    def __init__(self, config, restricted=False):
        """ Create an SshConfig.

        SshConfig(config, restricted=False)
            config:     Must be either a file-like object or a filename or a
                        sequence of file-like objects and/or filenames. When a
                        sequence is given, the first files have precedence over
                        the later files.
            restricted: Whether to only read in the supplied config file. When
                        False, also reads in the system-wide ssh_config.

        """
        pass

    def get(self, host, full=False):
        """ Get the entry for the host.

        get(host, full=False)
            host:   The hostname to look for.
            full:   When set, returns all options with their values. If the
                    option is not set in the entry, the default value is used.
                    When unset, it only returns the values that are different
                    from the default.
        """
        pass

    def set(self, host, *args, **kwargs):
        """ Set the entry for a specific host, replacing any existing entries

        set(host, entry)
            host:   The host to set the entry for.
            entry:  The entry to set. Either a dict-like object with the
                    options as keys or an SshConfigEntry.

        set(host, <option>=<value>, ...)
            host:       The host to set the entry for.
            <option>:   A valid SSH option.
            <value>:    Value for <option>.
        """
        pass

    def update(self, host, *args, **kwargs):
        """ Updates an entry for a specific host, replacing only existing
            options, setting any new options.

        update(host, entry)
            host:   The host to update the entry of.
            entry:  An entry with the options to update. It can either be an
                    SshConfigEntry or a dict-like object with options as keys.

        update(host, <option>=<value>, ...)
            host:       The host to update the entry of.
            <option>:   A valid SSH option.
            <value>:    Value for <option>.
        """
        pass

    def getDefault(self):
        """ Get the default entry.

        getDefault()
        """
        pass


    def contains(self, host):
        """ If we have an entry for the specified host

        contains(host)
            host:   The host to check for.
        """
        pass

    def save(self, dest):
        """ Save the configuration somewhere safe.

        save(dest)
            dest:   A filename or a file-like object. If the file already
                    exists, it will be truncated.
        """
        pass

    def load(self, config, update=False):
        """ Load a configuration.

        load(config, update=False)
            config: A configuration to load. Must be an SshConfig, a file-like
                    object or a filename.
            update: When set, updates existing entries and ignores new entries
                    for existing hosts otherwise.
        """
        pass

class SshConfigEntry:
    """ A collection of SSH options pertaining to a group of hosts
    """
    def __init__(self, *args, **kwargs):
        """ Create an SshConfigEntry.

        SshConfigEntry(entry)
            entry:  The contents of the entry. Can be either another
                    SshConfigEntry or a dict-like object.

        SshConfigEntry(<option>=<value>, ...)
            <option>:   A valid SSH option
            <value>:    Value for <option>
        """
        pass

    def get(self, option):
        """ Get the value for a specific option.

        get(option)
            option: A valid SSH option. If it does not exist, None is returned.
        """
        pass

    def set(self, option, *args, **kwargs):
        """ Set the value for a specific option

        set(name, value)
            name:   A valid SSH option name
            value:  Value for the option

        set(<option>=<value>, ...)
            <option>:   A valid SSH option
            <value>:    Value for <option>

        set(options)
            options:    An SshConfigEntry or a dict-like object with SSH
                        options as keys.
        """
        pass

    def contains(self, option):
        """ Whether the SshConfigEntry contains the specified option

        contains(option)
            option: A valid SSH option
        """
        pass

    def to_dict(self):
        """ Converts the SshConfigEntry to a dict
        """
        pass

def __ssh_config_parser(config):
    """ Parses a ssh_config to an SshConfig

    __ssh_config_parser(config):
        config: A filename or a file-like object.
    """
    pass
