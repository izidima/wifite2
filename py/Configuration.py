#!/usr/bin/python

import os

class Configuration(object):
    ''' Stores configuration variables and functions for Wifite. '''

    initialized = False # Flag indicating config has been initialized
    temp_dir = None     # Temporary directory

    @staticmethod
    def initialize():
        '''
            Sets up default initial configuration values.
            Also sets config values based on command-line arguments.
        '''

        # Only initialize this class once
        if Configuration.initialized:
            return
        Configuration.initialized = True

        Configuration.version = 2.00 # Program version
        Configuration.tx_power = 0 # Wifi transmit power (0 is default)
        Configuration.interface = None
        Configuration.target_channel = None # User-defined channel to scan
        Configuration.target_essid = None # User-defined AP name
        Configuration.target_bssid = None # User-defined AP BSSID
        Configuration.pillage = False # "All" mode to attack everything

        Configuration.encryption_filter = ['WEP', 'WPA', 'WPS']

        # WEP variables
        Configuration.wep_filter = False # Only attack WEP networks
        Configuration.wep_pps = 600 # Packets per second
        Configuration.wep_timeout = 600 # Seconds to wait before failing
        Configuration.wep_crack_at_ivs = 10000 # Minimum IVs to start cracking
        Configuration.require_fakeauth = False
        Configuration.wep_restart_stale_ivs = 11 # Seconds to wait before restarting
                                                 # Aireplay if IVs don't increaes.
                                                 # "0" means never restart.
        Configuration.wep_restart_aircrack = 30  # Seconds to give aircrack to crack
                                                 # before restarting the process.
        # WEP-specific attacks
        Configuration.wep_fragment = True 
        Configuration.wep_caffelatte = True 
        Configuration.wep_p0841 = True
        Configuration.wep_hirte = True
        Configuration.wep_crack_at_ivs = 10000 # Number of IVS to start cracking

        # WPA variables
        Configuration.wpa_filter = False # Only attack WPA networks
        Configuration.wpa_deauth_timeout = 10 # Wait time between deauths
        Configuration.wpa_attack_timeout = 500 # Wait time before failing
        Configuration.wpa_handshake_dir = "hs" # Dir to store handshakes

        # Default dictionary for cracking
        Configuration.wordlist = None
        wordlists = [
            '/usr/share/wfuzz/wordlist/fuzzdb/wordlists-user-passwd/passwds/phpbb.txt',
            '/usr/share/fuzzdb/wordlists-user-passwd/passwds/phpbb.txt'
        ]
        for wlist in wordlists:
            if os.path.exists(wlist):
                Configuration.wordlist = wlist
                break

        # WPS variables
        Configuration.wps_filter  = False  # Only attack WPS networks
        Configuration.no_reaver   = False  # Do not use Reaver on WPS networks
        Configuration.reaver      = False  # ONLY use Reaver on WPS networks
        Configuration.pixie_only  = False  # ONLY use Pixie-Dust attack on WPS
        Configuration.wps_pin_timeout = 600   # Seconds to wait before reaver fails
        Configuration.wps_pixie_timeout = 600 # Seconds to wait before pixie fails
        Configuration.wps_max_retries = 20 # Retries before failing
        Configuration.wps_fail_threshold = 30  # Max number of failures
        Configuration.wps_timeout_threshold = 30  # Max number of timeouts
        Configuration.wps_skip_rate_limit = True # Skip rate-limited WPS APs

        # Commands
        Configuration.cracked = False
        Configuration.check_handshake = None
        Configuration.crack_wpa = None
        Configuration.crack_wep = None
        Configuration.update = False

        # Overwrite config values with arguments (if defined)
        Configuration.load_from_arguments()


    @staticmethod
    def load_from_arguments():
        ''' Sets configuration values based on Argument.args object '''
        from Arguments import Arguments

        args = Arguments(Configuration).args
        if args.channel:      Configuration.target_channel = args.channel
        if args.interface:    Configuration.interface    = args.interface
        if args.target_bssid: Configuration.target_bssid = args.target_bssid
        if args.target_essid: Configuration.target_essid = args.target_essid

        # WEP
        if args.wep_filter:  Configuration.wep_filter  = args.wep_filter
        if args.wep_pps:     Configuration.wep_pps     = args.wep_pps
        if args.wep_timeout: Configuration.wep_timeout = args.wep_timeout
        if args.require_fakeauth: Configuration.require_fakeauth = False
        if args.wep_crack_at_ivs:
            Configuration.wep_crack_at_ivs = args.wep_crack_at_ivs
        if args.wep_restart_stale_ivs:
            Configuration.wep_restart_stale_ivs = args.wep_restart_stale_ivs
        if args.wep_restart_aircrack:
            Configuration.wep_restart_aircrack = args.wep_restart_aircrack

        # WPA
        if args.wpa_filter:  Configuration.wpa_filter  = args.wpa_filter
        if args.wordlist:    Configuration.wordlist    = args.wordlist
        if args.wpa_deauth_timeout:
            Configuration.wpa_deauth_timeout = args.wpa_deauth_timeout
        if args.wpa_attack_timeout:
            Configuration.wpa_attack_timeout = args.wpa_attack_timeout
        if args.wpa_handshake_dir:
            Configuration.wpa_handshake_dir = args.wpa_handshake_dir

        # WPS
        if args.wps_filter:  Configuration.wps_filter  = args.wps_filter
        if args.reaver_only: Configuration.reaver_only = args.reaver_only
        if args.no_reaver:   Configuration.no_reaver   = args.no_reaver
        if args.pixie_only:  Configuration.pixie_only  = args.pixie_only
        if args.wps_pixie_timeout:
            Configuration.wps_pixie_timeout = args.wps_pixie_timeout
        if args.wps_pin_timeout:
            Configuration.wps_pin_timeout = args.wps_pin_timeout
        if args.wps_max_retries:
            Configuration.wps_max_retries = args.wps_max_retries
        if args.wps_fail_threshold:
            Configuration.wps_fail_threshold = args.wps_fail_threshold
        if args.wps_timeout_threshold:
            Configuration.wps_timeout_threshold = args.wps_timeout_threshold
        if args.wps_ignore_rate_limit:
            Configuration.wps_skip_rate_limit = not args.wps_ignore_rate_limit

        # Adjust encryption filter
        if Configuration.wep_filter or \
           Configuration.wpa_filter or \
           Configuration.wps_filter:
            # Reset filter
            Configuration.encryption_filter = []
        if Configuration.wep_filter: Configuration.encryption_filter.append('WEP')
        if Configuration.wpa_filter: Configuration.encryption_filter.append('WPA')
        if Configuration.wps_filter: Configuration.encryption_filter.append('WPS')

        # Commands
        if args.cracked:   Configuration.show_cracked = True
        if args.crack_wpa: Configuration.crack_wpa = args.crack_wpa
        if args.crack_wep: Configuration.crack_wep = args.crack_wep
        if args.update:    Configuration.update = True
        if args.check_handshake: Configuration.check_handshake = args.check_handshake

        if Configuration.interface == None:
            # Interface wasn't defined, select it!
            from Airmon import Airmon
            Configuration.interface = Airmon.ask()
        

    @staticmethod
    def temp(subfile=''):
        ''' Creates and/or returns the temporary directory '''
        if Configuration.temp_dir == None:
            Configuration.temp_dir = Configuration.create_temp()
        return Configuration.temp_dir + subfile

    @staticmethod
    def create_temp():
        ''' Creates and returns a temporary directory '''
        from tempfile import mkdtemp
        tmp = mkdtemp(prefix='wifite')
        if not tmp.endswith(os.sep):
            tmp += os.sep
        return tmp

    @staticmethod
    def delete_temp():
        ''' Remove temp files and folder '''
        if Configuration.temp_dir == None: return
        if os.path.exists(Configuration.temp_dir):
            for f in os.listdir(Configuration.temp_dir):
                os.remove(Configuration.temp_dir + f)
            os.rmdir(Configuration.temp_dir)


    @staticmethod
    def exit_gracefully(code=0):
        ''' Deletes temp and exist with the given code '''
        Configuration.delete_temp()
        exit(code)

    @staticmethod
    def dump():
        ''' (Colorful) string representation of the configuration '''
        from Color import Color

        max_len = 20
        for key in Configuration.__dict__.keys():
            max_len = max(max_len, len(key))

        result  = Color.s('{W}%s  Value{W}\n' % 'Configuration Key'.ljust(max_len))
        result += Color.s('{W}%s------------------{W}\n' % ('-' * max_len))

        for (key,val) in sorted(Configuration.__dict__.iteritems()):
            if key.startswith('__'): continue
            if type(val) == staticmethod: continue
            if val == None: continue
            result += Color.s("{G}%s {W} {C}%s{W}\n" % (key.ljust(max_len),val))
        return result

if __name__ == '__main__':
    Configuration.initialize()
    print Configuration.dump()

