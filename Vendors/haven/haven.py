import requests

def test():
    vendor_url = 'http://havenshop.ca'

    ping_vendor = requests.get(vendor_url)

    print ping_vendor.content

    print ping_vendor.status_code

if __name__ == '__main__':
    test()


