def load_print(text: str) -> None:
    print(f"[*] {text}".ljust(80), end="\r")


def done_print(text: str) -> None:
    print(f"[+] {text}".ljust(80))
