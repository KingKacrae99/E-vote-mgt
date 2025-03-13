import secrets
from django.core.cache import cache

def send_otp(phone):
    otp = secrets.randbelow(900000) + 100000
    cache.set(f'otp_{phone}', otp, timeout=300)
    cache.set(f'otp_attempts_{phone}', 0 , timeout=300)
    print(f'otp for {phone}: {otp}')

def verify_otp(phone, entered_otp):
    attempts = cache.get(f'otp_attempts_{phone}',0)
    if attempts >= 5:
        return False
    
    stored_otp = cache.get(f'otp_{phone}')
    print('checking in Processing')
    if str(stored_otp) == str(entered_otp):
        print('Verification Successful!')
        cache.delete(f'otp_{phone}')
        cache.delete(f'otp_attempts_{phone}')
        return True
    
    cache.set(f'otp_attempts_{phone}', attempts + 1, timeout=300 )
    return False