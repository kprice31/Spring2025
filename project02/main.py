import parser

while True:
    text = input("R@R: ")
    if text.lower() in {"exit", "quit"}:
        break
    try:
        parser.run(text)
    except Exception as e:
        print(f"Error: {e}")