from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='


# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcSGkUFC_G_NKyv1q88vUT5NNCAnRavqUtwZpptyunpgW1-r0gCINmLCQiMVLIWBFRan9XWwzYWiaXMe-8IHeJbDTzySQvhusR2MlWF6hOb5bZ4Uio-LvFu8Iig8MXJfrktvyP8x1ZgE_yFq1-DbBxKD57Fivc49_a4PcPiheMi9Os_P0='


def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
