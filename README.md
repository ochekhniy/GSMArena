# **cite:** https://www.webshare.io/

## Load proxy list in file named ***proxies.txt*** in project directory

# **cite:** http://free-proxy.cz/ru/

In PxRequest (singleton) class there are two static methods which return prepared list of proxies to use.
default_get_proxy_func static parameter include pointer to that function.

---

get_proxy_list_from_file() read ***proxies.txt*** file

structure like

ip:port:user:password

___

get_proxy_list_from_simple_file() read ***proxies_list.txt*** file

structure like

ip:port 
