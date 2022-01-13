"""
Provides classes and functions to work with the Bank FinTS API.
"""
from fints.client import FinTS3PinTanClient
from fints.models import SEPAAccount
from mt940.models import Transaction as FTT
from datetime import datetime, date
from tkinter import ttk, Label, simpledialog
from PIL import Image
import io
import tkinter as tk
import arrow
from typing import Dict, Optional, List
import hashlib
from pprint import pprint


class AccountNotFoundException(Exception):
    """
    Raised if the account could not be found.
    """

    accounts: List[SEPAAccount] = []

    def __init__(self, accounts: List[SEPAAccount]):
        Exception.__init__()
        self.accounts = accounts


class FinTS:
    """
    FinTS provides methods to connect to Bank (i. e. Deutsche Bank) via FinTS.
    Alot taken from https://github.com/bahlo/ing-ynab
    """

    f: FinTS3PinTanClient
    selected_account: SEPAAccount

    def __init__(self, blz: int, username: str, pin: str, finurl: str, fints_product_id: Optional[str] = None):
        self.f = FinTS3PinTanClient(
            blz,  # Your bank's BLZ
            username,  # Your login name
            pin,  # Your banking PIN
            finurl,  # Deutsche Bank: https://fints.deutsche-bank.de
            product_id=fints_product_id
        )
        self.check_tan()

    def check_tan(self):
        with self.f:
            # Since PSD2, a TAN might be needed for dialog initialization.
            # Let's check if there is one required
            if self.f.init_tan_response:
                challenge_hhduc = self.f.init_tan_response.challenge_matrix[1]
                print(challenge_hhduc)

                data = self.decode_phototan_image(challenge_hhduc)
                print(data)
                #bytes_io = io.BytesIO(data['image'])
                bytes_io = io.BytesIO(challenge_hhduc)
                img = Image.open(bytes_io)
                img.save("../data/phototan.png")

                #img = ImageTk.PhotoImage(Image.open(bytes_io))
                self.open_tan_view(img)
                #root2 = Tk()
                #img = ImageTk.PhotoImage(Image.open(bytes_io))
                #panel = Label(root2, image = img)
                #panel.pack(side = "bottom", fill = "both", expand = "yes")
                # root2.mainloop()
                tan = simpledialog.askstring(
                    _("TAN Input"), _("A TAN is required:"))
                response = self.f.send_tan(self.f.init_tan_response, tan)

                # TODO: error handling
                # Dialog response: 3076 - Keine starke Authentifizierung erforderlich.
                # Dialog response: 3060 - Teilweise liegen Warnungen/Hinweise vor.
                # 3000ish seems ok ==> return true; 9000ish should be an error
                # ==> return false
                print(response.status)
                print(response.responses)

    # TODO: move to view
    def open_tan_view(self, parentwindow, img):
        self.w3 = tk.Toplevel(parentwindow)
        self.w3.title(_('photo TAN'))
        self.w3.group(parentwindow)
        phototan = Label(self.w3, image=img)
        phototan.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # tan
        tan_label = ttk.Label(self.w3, text=_("TAN") + ":")
        tan_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        tan = ttk.Entry(self.w3)
        tan.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # login button
        #addAccountDataButton = ttk.Button(self.w3, text=_("OK"))
        #addAccountDataButton.grid(column=0, row=2, sticky=tk.E, padx=5, pady=5)

        # cancel button
        cancel_button = ttk.Button(self.w3, text=_(
            "Close"), command=self.w3.destroy)
        cancel_button.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

    def select_account(self, iban: str) -> None:
        """
        Select the account with the given IBAN.
        """
        accounts = self.f.get_sepa_accounts()

        self.selected_account = None
        for account in accounts:
            if account.iban == iban:
                self.selected_account = account
                break

        if self.selected_account is None:
            raise AccountNotFoundException(accounts)

    def get_transactions(
            self, days: Optional[int] = None) -> List[FTT]:
        """
        Get transactions for the selected account.

        :param int days: retreive transactions of last n days 
        """
        return self.f.get_transactions(
            self.selected_account, start_date=arrow.now().shift(days=-1*days).datetime,
            end_date=arrow.now().datetime
        )

    def transform_transactions(
        self, transactions: List[FTT],
    ) -> List[Dict[str, str]]:
        """
        Transform the FinTS transactions into something easier.
        """
        transformed = []
        for transaction in transactions:
            data = transaction.data

            # should not happen, because end date today is given to FinTS
            # request
            transaction_date = data["date"]
            if transaction_date > date.today():
                # This is a future transaction, skip it. We'll import it at the
                # day it actually occurs.
                continue

            float_amount = float(data["amount"].amount)
            # similar_transactions = [
            #    x
            #    for x in transformed
            #    if date.fromisoformat(x["date"]) == transaction_date
            #    and x["amount"] == milliunits_amount
            #]
            #occurence = len(similar_transactions) + 1
            # import_id = (
            #    f"YNAB:{milliunits_amount}:{transaction_date.isoformat()}:{occurence}"
            #)

            # If this is a PayPal transaction, try to get the Payee from the memo
            # if PAYPAL_PAYEE_REGEX.match(data["applicant_name"]):
            #    payee = PAYPAL_MEMO_REGEX.match(data["purpose"])
            #    if payee is not None:
            #        payee = payee.group(2)
            #        if payee.endswith(PAYPAL_SUFFIX):
            #            payee = payee[: -len(PAYPAL_SUFFIX)]
            #        data["applicant_name"] = "PAYPAL " + payee

            orig = {}
            for k, v in data.items():
                orig[k] = v

            orig["amount"] = str(float_amount)
            orig['date'] = orig['date'].isoformat()
            t = {}
            t['json_original'] = orig

            t['account_iban'] = self.selected_account.iban
            t['date_retreived'] = datetime.now().replace(microsecond=0)

            t['date'] = data['date']
            t['applicant_name'] = data['applicant_name']
            t['applicant_iban'] = data['applicant_iban']
            t['applicant_bin'] = data['applicant_bin']
            if 'applicant_creditor_id' in data:
                t['applicant_creditor_id'] = data['applicant_creditor_id']
            t['purpose'] = data['purpose']
            t['amount'] = float_amount
            t['currency'] = data['currency']
            t['customer_reference'] = data['customer_reference']
            if 'end_to_end_reference' in data:
                t['end_to_end_reference'] = data['end_to_end_reference']

            print(t["amount"])
            print(t["date"])
            print(t['json_original']["transaction_code"])
            hash_str = datetime.now().isoformat()
            # protection against empty date fields
            # hash_str = str(t["date"]) + str(t["amount"]) + t['json_original']["transaction_code"] + \
            # t["applicant_bin"] + t["applicant_iban"] + \
            #t["applicant_name"] + t["purpose"] + t['json_original']["id"]
            hashvalue = hashlib.sha256(hash_str.encode('UTF-8')).hexdigest()
            t["hash"] = hashvalue

            transformed.append(t)
        return transformed

    def decode_phototan_image(self, data):
        """
        This decodes photoTAN data sent as challenge_hhduc into its mime type and the actual image data.
        :returns: a dictionary with two values, 'mime_type' and 'image'
        :rtype: dict
        The markup of the data is taken from https://github.com/hbci4j/hbci4java/blob/c8eabe6809e8d0271f944ea28a59ed6b736af56e/src/main/java/org/kapott/hbci/manager/MatrixCode.java#L61-L97
        The encoding is taken from https://github.com/hbci4j/hbci4java/blob/c8eabe6809e8d0271f944ea28a59ed6b736af56e/src/main/java/org/kapott/hbci/comm/Comm.java#L46
        """
        # Mime type length is the first two bytes of data
        mime_type_length = int.from_bytes(data[:2], byteorder='big')

        # The mime type follows from byte three to (mime_type_length - 1)
        mime_type = data[2:2 + mime_type_length].decode("iso-8859-1")

        # The image length is coded in the next two bytes
        image_length_start = 2 + mime_type_length
        image_length = int.from_bytes(
            data[image_length_start:2 + image_length_start], byteorder='big')

        # The actual image data is everything that follows.
        # To be compatible with possible future extensions, we still slice the
        # data
        image = data[2 + image_length_start: 2 +
                     image_length_start + image_length]

        return {
            "mime_type": mime_type,
            "image": image
        }
