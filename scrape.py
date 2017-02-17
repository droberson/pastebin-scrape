#!/usr/bin/env python

"""
Basic Pastebin scraper
by Daniel Roberson

This is currently very crude, but works.

You must have a lifetime pro membership to pastebin and have your IP
address whitelisted in order for this to function.
"""

import re
import time
import json
import urllib
import urllib2

def is_interesting(data):
    """Determine if data contains any interesting artifacts"""
    # TODO:
    # - phone numbers
    # - email addresses
    # - URLs
    # - IP addresses
    # - various hashes
    # - GPS coordinates
    # - User-specified keywords
    # - Display blurb on WHY the file is interesting in output:
    #   ex: [+] Interesting data found in %s -- saved to %s (exploit)
    if 'exploit' in data.lower():
        return True
    if 'pass' in data.lower():
        return True
    if 'key' in data.lower():
        return True
    if 'database' in data.lower():
        return True
    return False


def main():
    """Scrape all the things"""
    # http://pastebin.com/api_scraping.php
    # http://pastebin.com/api_scrape_item.php?i=UNIQUE_PASTE_KEY
    # http://pastebin.com/api_scrape_item_meta.php?i=UNIQUE_PASTE_KEY
    # api_scraping.php?limit=X (max 500)

    # TODO: KeyboardInterrupt handler

    pastebin_keys = []
    pastebin = ""
    limit = 500  # TODO: CLI setting
    url = "http://pastebin.com/api_scraping.php"
    values = {'limit': limit}
    url_values = urllib.urlencode(values)

    full_url = url + '?' + url_values

    while True:
        # TODO: exit if IP is not whitelisted.
        try:
            pastebin = urllib2.urlopen(full_url)
        except urllib2.HTTPError, e:
            print e

        data = json.load(pastebin)
        pastebin_keys = pastebin_keys[:limit]

        for paste in data:
            if paste['key'] in pastebin_keys:
                continue
            pastebin_keys.insert(0, paste['key'])
            #print paste['key'], paste['date'], paste['scrape_url'], paste['full_url']
            # TODO: add exception handling
            scrape = urllib2.urlopen(paste['scrape_url'])
            scrape_data = scrape.read()
            if is_interesting(scrape_data):
                filename = paste['key'] + ".txt"
                print "[+] Interesting data found in %s -- saving to %s" % \
                    (paste['full_url'], filename)

                # TODO: make sure this succeeds
                filep = open(filename, 'w')
                # TODO: ability to specify write directory, folders by date.
                filep.write(scrape_data)
                filep.close()
                

        time.sleep(60)  # TODO: CLI setting

if __name__ == "__main__":
    main()
