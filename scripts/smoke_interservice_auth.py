import os, time, argparse, jwt

os.environ["INTERNAL_AUTH_SECRET"] = "your_secret_value"

def make_token(secret: str) -> str:
    now = int(time.time())
    payload = {"sub": "interservice", "iat": now, "exp": now + 300}  # 5 min
    return jwt.encode(payload, secret, algorithm="HS256")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--secret", default=os.getenv("INTERNAL_AUTH_SECRET"), help="HS256 shared secret")
    p.add_argument("--url", default=None, help="Optional: show a curl command to this URL")
    a = p.parse_args()

    if not a.secret:
        raise SystemExit("Set INTERNAL_AUTH_SECRET or pass --secret")

    token = make_token(a.secret)
    header = f"Authorization: Bearer {token}"
    print(header)
    if a.url:
        print(f'\ncurl -H "{header}" "{a.url}"')
