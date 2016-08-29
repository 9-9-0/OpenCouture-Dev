import json
import os

#Add in customized profile name input from GUI
#Review OOP principles for this implementation

class UserProfile():
    def __init__(self):
        self.template = {
                "email_address": "",
                "first_name"   : "",
                "last_name"    : "",
                "phone_num"    : "",     
                "bill_first_name"   : "",
                "bill_last_name"    : "",
                "bill_address_ln1"  : "",
                "bill_address_ln2"  : "",
                "bill_city"         : "",
                "bill_zip_code"     : "",
                "bill_state"        : "",
                "bill_state_short"  : "",
                "bill_country"      : "",
                "bill_country_short": "",
                "card_name"     : "",
                "card_num"      : "",
                "card_type"     : "",
                "card_ccv"      : "",
                "card_exp_month": "",
                "card_exp_day"  : "",
                "ship_first_name"   : "",
                "ship_last_name"    : "",
                "ship_address_ln1"  : "",
                "ship_address_ln2"  : "",
                "ship_city"         : "",
                "ship_zip_code"     : "",
                "ship_state"        : "",
                "ship_state_short"  : "",
                "ship_country"      : "",
                "ship_country_short": ""
                }
        #print self.template

    def SaveProfile(self):
        fileDest = os.path.join(os.path.expanduser('~'), 'test.json')
        print fileDest
        #Change fileDest to where file configs are located by default
        with open(fileDest, 'w') as profileFile:
            json.dump(self.template, profileFile, indent=4)

# USE BELOW TO TEST #
def main():
    x = UserProfile()
    x.SaveProfile()

if __name__ == '__main__':
    main()
