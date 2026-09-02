from backend.auth.google_auth import get_google_credentials


print("===================================")
print("       LARVI GOOGLE AUTH TEST")
print("===================================")
print()

try:
    credentials = get_google_credentials()

    print("SUCCESS!")
    print("Google authentication completed.")
    print()

    if credentials.valid:
        print("Credential status: VALID")
    else:
        print("Credential status: INVALID")

except Exception as error:
    print()
    print("AUTHENTICATION FAILED")
    print()
    print(error)
