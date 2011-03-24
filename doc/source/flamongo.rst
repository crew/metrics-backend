========
flamongo
========

::

    $ flamongo --help

    USAGE: /scratch/lee/metricsenv/bin/flamongo [flags]

    flags:

    crew.flamongo.main:
      --certificate: The location of the SSL certificate.
        (default: 'test.crt')
      --[no]daemonize: Daemonize.
        (default: 'false')
      -?,--[no]help: show this help
      --[no]helpshort: show usage only for this module
      --[no]helpxml: like --help, but generates XML output
      --logfile: The filename of the log.
      --port: The port number
        (default: '2000')
        (an integer)
      --privatekey: The location of the private key for SSL
        (default: 'test.key')
      --secureport: The secure port number
        (default: '2443')
        (an integer)

    gflags:
      --flagfile: Insert flag definitions from the given file into the command line.
        (default: '')
      --undefok: comma-separated list of flag names that it is okay to specify on
        the command line even if the program does not define a flag with that name.
        IMPORTANT: flags in this list that have arguments MUST use the --flag=value
        format.
        (default: '')
