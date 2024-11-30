from django.contrib.auth.tokens import PasswordResetTokenGenerator
import datetime

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_values(self,user,timestamp):
        return(
            str(user.pk) + str(timestamp) + str(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()