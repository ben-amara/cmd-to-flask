#coding : utf8
import re
import requests

cms = ""
cms_version = ""
cms_plugin = []

# "cms": "$type", "cms-version" : "$version", "cms-plugin" : "[ ]"

###########
#
#   WORDPRESS 
#  
###########

def is_wordpress(url):
    try:
        result = callApi(url+"/wp-content/uploads/")
        print (result[1])
        if result[1] != 404:
            print ("c'est un wordpress")

            cms = "WordPress"
            # detection de la version
            wp_version = which_wordpress_version(url)
	    #print (wp_version[0])
            if wp_version:
                cms_version = wp_version[0]
                print ("version detected "+str(cms_version))
                
                # detection des plugins
            wordpress_plugin_detection(url)

            return True
        if result[1] == 404:
            return False
    except Exception as e:
        print (e)        
        return False


def which_wordpress_version(url):
    print ("WordPress version "+str(url))
    if url[-1] != "/":
        url = url+"/"

    version = callApi(url+"feed/")
    #print type(version[1])
    if version[1] != 200:
        print ("feed non disponible")

    else:
        for line in version[0].splitlines(True):
            print ("FEED")
            print (line)
            WP = re.findall(r"wordpress\.org\/\?v=(\d\.\d\.\d)",line)
            if WP:
                return WP
    return ""


def wordpress_plugin_detection(url):
    if url[-1] != "/":
        url = url+"/"

    # page/wp-content/plugins/
    # WP-SUPER-CACHE - wp-content/plugins/wp-super-cache/ 
    result = callApi(url+"wp-content/plugins/wp-super-cache/")
    #print result[1]
    if result[1] == 403:
        cms_plugin.append("WP-SUPER-CACHE")    
        print ("WP-SUPER-CACHE"  )  

    result = callApi(url+"wp-content/plugins/leadin/")
    if result[1] == 403:        
        cms_plugin.append("HUBSPOT")    
        print ("HUBSPOT" )   

    # WORDFENCE - /wp-content/plugins/wordfence/ 
    result = callApi(url+"wp-content/plugins/wordfence/")
    print( result[1])
    if result[1] == 200:
        cms_plugin.append("WORDFENCE")    
        print ("WORDFENCE")

    # YOAST -  
    #result = callApi(url+"wp-content/plugins/wp-cache/"
    return ""

###############
#
#  OTHERS
#
###############


def is_shopify(url):
    page = callApi(url)
    if not page:
        return False

    for line in page[0].splitlines(True):
        #print line
        shopify = re.findall(r"cdn.shopify.com",line)
        if shopify:
            #print "C'est un site Shopify"
            cms = ("Shopify")
            print (url+";shopify")
            return True
 
        shopifycloud = re.findall(r"cdn.shopifycloud.com",line)
        if shopifycloud:
            #print "C'est un site Shopify"
            print (url+";shopify")
            cms = "Shopify"
            return True
    return False

def is_prestashop(url):
    page = callApi(url)
    if not page:
        return False

    for line in page[0].splitlines(True):
        print (line)
        pshop = re.findall(r"cdn.shopify.com",line)
        if pshop:
            print ("C'est un site Prestashop")
            cms = "Prestashop"
            return True
    return False

def is_drupal(url):
    page = callApi(url)
    if not page:
        return False

    for line in page[0].splitlines(True):
        print (line)
        drupal = re.findall(r"cdn.shopify.com",line)
        if drupal:
            print ("C'est un site Drupal")
            cms = "Drupal"
            return True
    return False

def is_wix(url):
    page = callApi(url)
    if not page:
        return False

    for line in page[0].splitlines(True):
        wix = re.findall(r"cdn.shopify.com",line)
        if wix:
            print ("C'est un site WIX")
            cms = "Wix"
            return True
    return False

def is_hubspot(url):
    print ("Dans la fonction Hubspot "+str(url))
    page = callApi(url)
    if not page:
        return False

    for line in page[0].splitlines(True):
        hubspot = re.findall(r"HubSpot Template Builder",line)
        if hubspot:
            print ("C'est un site hubspot")
            cms = "Hubspot"
            return True

        hubspot2 = re.findall(r"content=\"HubSpot\"",line)
        if hubspot2:
            print ("C'est un site hubspot")
            cms = "Hubspot"
            return True

        hubspot3 = re.findall(r"js.hs-analytics.net",line)
        if hubspot3:
            print ("C'est un site hubspot")
            cms = "Hubspot"
            return True





def is_phpbb(url):
    if url[-1] != "/":
        url = url+"/"

    page = callApi(url+"ucp.php?mode=login")
    if not page:
        return False

    if page[1] == 200:
        print ("C'est un site phpbb")
        cms = "phpbb"
        return True

def callApi(name):
    try:
        print (name)
        user_agent = {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'}
        r    = requests.get(name, headers = user_agent, verify=True, timeout=10, allow_redirects=True)
        #print ("#############-------> CALLING "+name+" <-----------------\n")

        #for h in r.history:
        #     print h.url
        #print r.url

        prompt  = [r.text, r.status_code] 
        return prompt 

    except Exception as e:
        print(name+"  "+str(e))
        #print ""
        return False

def write_in_a_file(content, filename):
    files = open(filename,"a")
    files.write(content+"\n")
    cms_version = ""
    del cms_plugin[:]
    files.close()

