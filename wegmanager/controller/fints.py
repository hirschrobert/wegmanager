"""
Provides classes and functions to work with the Bank FinTS API.
"""
import io
import tkinter as tk
from pprint import pprint

from tkinter import ttk, Label, simpledialog
from datetime import datetime, date, timedelta
from typing import Dict, Optional, List

from fints.client import FinTS3PinTanClient
from fints.models import SEPAAccount
from mt940.models import Transaction as FTT
from PIL import Image, ImageTk


class AccountNotFoundException(Exception):
    """
    Raised if the account could not be found.
    """

    accounts: List[SEPAAccount] = []

    def __init__(self, accounts: List[SEPAAccount]=None) -> None:
        super().__init__()
        self.accounts = accounts

    def __str__(self):
        if self.accounts:
            string = 'not found:\n'
            for a in self.accounts:
                string += f'{a.iban}\n'
            return string
        else:
            message = _('Account not found!')
            return message


class FinTS:
    """
    FinTS provides methods to connect to Bank (i. e. Deutsche Bank) via FinTS.
    Alot taken from https://github.com/bahlo/ing-ynab
    """

    f: FinTS3PinTanClient
    selected_account: SEPAAccount

    def __init__(self, blz: int, username: str, pin: str, finurl: str,
                 fints_product_id: Optional[str] = None):
        self.f = FinTS3PinTanClient(
            blz,  # Your bank's BLZ
            username,  # Your login name
            pin,  # Your banking PIN
            finurl,
            product_id=fints_product_id
        )
        self.parentwindow = None
        self.check_tan()

    def set_parentwindow(self, parentwindow):
        self.parentwindow = parentwindow

    def check_tan(self):
        with self.f:
            # Since PSD2, a TAN might be needed for dialog initialization.
            # Let's check if there is one required
            if self.f.init_tan_response:
                challenge_hhduc = self.f.init_tan_response.challenge_matrix[1]
                print(challenge_hhduc)

                data = self.decode_phototan_image(challenge_hhduc)
                print(data)
                # bytes_io = io.BytesIO(data['image'])
                bytes_io = io.BytesIO(challenge_hhduc)
                img = Image.open(bytes_io)
                img.save("../data/phototan.png")

                img = ImageTk.PhotoImage(Image.open(bytes_io))
                self.open_tan_view(img)
                # root2 = Tk()
                # img = ImageTk.PhotoImage(Image.open(bytes_io))
                # panel = Label(root2, image = img)
                # panel.pack(side = "bottom", fill = "both", expand = "yes")
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
    def open_tan_view(self, img):
        self.w3 = tk.Toplevel(self.parentwindow)
        self.w3.title(_('photo TAN'))
        self.w3.group(self.parentwindow)
        phototan = Label(self.w3, image=img)
        phototan.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        # tan
        tan_label = ttk.Label(self.w3, text=_("TAN") + ":")
        tan_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        tan = ttk.Entry(self.w3)
        tan.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # login button
        # addAccountDataButton = ttk.Button(self.w3, text=_("OK"))
        # addAccountDataButton.grid(column=0, row=2,
        #                             sticky=tk.E, padx=5, pady=5)

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

        end_date = date.today()
        delta = timedelta(days)
        start_date = end_date - delta

        return self.f.get_transactions(
            self.selected_account,
            start_date,
            end_date
        )

    # TODO: actually belongs to model.Transaction
    def transform_transactions(
        self, transactions: List[FTT],
    ) -> List[Dict[str, str]]:
        """
        Transform the FinTS transactions into something easier.
        """
        transformed = []
        for transaction in transactions:
            data = transaction.data

            t = {}
            t['json_original'] = data

            # extract numbers only
            t['json_original']['amount'] = str(
                t['json_original']['amount'].amount)

            # stringify date befor saving as json
            for key, val in t['json_original'].items():
                if isinstance(val, date):
                    t['json_original'][key] = t['json_original'][key].isoformat()

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
