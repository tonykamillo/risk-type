from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcXChc-caxgHjym5p4GTBqe3NsDf6fYFJkPsyyPMAH2-3N9_rdS08zGJPXYlzwfzh22O9GTYyZznjS48R65-00ZJP2Ikahs6ieO-8hqCdn4jg0W3k1Z5AXN_C9DsfzmFq52thfQ6Hj3l8LkjyOl_8dDFjANRJ_uJYVR4ikh0rB3XVv064='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
